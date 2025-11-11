"""
Core transformations for canonical music analysis: retrograde, inversion,
time alignment, and palindrome verification.
"""

from typing import TypeVar, Union, List, Tuple
import music21 as m21
from music21 import stream, note, chord

StreamType = TypeVar('StreamType', bound=stream.Stream)


def retrograde(stream_or_sequence: StreamType) -> StreamType:
    """
    Return the retrograde (time reversal) of a musical stream or sequence.

    For a Stream, notes are reversed in time but keep their original pitches and durations.
    The retrograde of a sequence [A, B, C] is [C, B, A].

    Args:
        stream_or_sequence: A music21 Stream or sequence to reverse

    Returns:
        The retrograde of the input, same type as input
    """
    if isinstance(stream_or_sequence, stream.Stream):
        # Get all notes and chords with their offsets
        elements = []
        for el in stream_or_sequence.flatten().notesAndRests:
            elements.append((el.offset, el.quarterLength, el))

        if not elements:
            return stream_or_sequence.__class__()

        # Calculate total duration
        max_end = max(offset + duration for offset, duration, _ in elements)

        # Create retrograde stream
        result = stream_or_sequence.__class__()
        for offset, duration, el in elements:
            # New offset: mirror around the total duration
            new_offset = max_end - offset - duration
            new_el = el.__class__()

            # Copy pitch information
            if isinstance(el, note.Note):
                new_el.pitch = el.pitch
            elif isinstance(el, chord.Chord):
                new_el.pitches = el.pitches
            elif isinstance(el, note.Rest):
                pass  # Rest has no pitch

            new_el.quarterLength = el.quarterLength
            result.insert(new_offset, new_el)

        return result
    else:
        # Assume it's a sequence
        return list(reversed(stream_or_sequence))


def invert(
    stream_or_sequence: StreamType,
    axis_pitch: Union[str, m21.pitch.Pitch] = 'C4'
) -> StreamType:
    """
    Return the pitch inversion of a musical stream around an axis pitch.

    Each pitch is reflected around the axis: if the original is N semitones above
    the axis, the inverted pitch is N semitones below the axis.

    Args:
        stream_or_sequence: A music21 Stream or sequence to invert
        axis_pitch: The pitch to use as the axis of inversion (default C4)

    Returns:
        The inverted stream, same type as input
    """
    if isinstance(axis_pitch, str):
        axis_pitch = m21.pitch.Pitch(axis_pitch)
    axis_midi = axis_pitch.midi

    if isinstance(stream_or_sequence, stream.Stream):
        result = stream_or_sequence.__class__()

        for el in stream_or_sequence.flatten().notesAndRests:
            new_el = el.__class__()
            new_el.quarterLength = el.quarterLength

            if isinstance(el, note.Note):
                # Invert the pitch around the axis
                interval = el.pitch.midi - axis_midi
                new_midi = axis_midi - interval
                new_el.pitch = m21.pitch.Pitch(midi=new_midi)
            elif isinstance(el, chord.Chord):
                # Invert each pitch in the chord
                new_pitches = []
                for p in el.pitches:
                    interval = p.midi - axis_midi
                    new_midi = axis_midi - interval
                    new_pitches.append(m21.pitch.Pitch(midi=new_midi))
                new_el.pitches = new_pitches
            elif isinstance(el, note.Rest):
                pass  # Rest unchanged

            result.insert(el.offset, new_el)

        return result
    else:
        # For sequences, invert each pitch
        result = []
        for item in stream_or_sequence:
            if hasattr(item, 'midi'):
                interval = item.midi - axis_midi
                new_midi = axis_midi - interval
                result.append(m21.pitch.Pitch(midi=new_midi))
            else:
                result.append(item)
        return result


def time_align(
    voice_a: stream.Stream,
    voice_b: stream.Stream,
    offset_quarters: float
) -> stream.Score:
    """
    Align two voices with a specified offset in quarter notes.

    Creates a Score with two parts, where voice_b starts offset_quarters
    after voice_a begins.

    Args:
        voice_a: First voice (Stream)
        voice_b: Second voice (Stream)
        offset_quarters: Quarter note offset for voice_b (positive = later start)

    Returns:
        A Score containing both voices aligned with the specified offset
    """
    score = stream.Score()

    # Create parts
    part_a = stream.Part()
    part_a.id = 'voice_a'
    for el in voice_a.flatten().notesAndRests:
        part_a.insert(el.offset, el)

    part_b = stream.Part()
    part_b.id = 'voice_b'
    for el in voice_b.flatten().notesAndRests:
        part_b.insert(el.offset + offset_quarters, el)

    score.insert(0, part_a)
    score.insert(0, part_b)

    return score


def is_time_palindrome(score: stream.Score) -> bool:
    """
    Verify if a score represents a time palindrome (crab canon).

    A true crab canon has two voices where one is the exact retrograde of the other,
    possibly with an offset. This function checks if the score exhibits this property.

    Args:
        score: A Score with two voices to check

    Returns:
        True if the score is a time palindrome, False otherwise
    """
    parts = list(score.parts)
    if len(parts) != 2:
        return False

    # Extract note events from both parts
    events_a = _extract_events(parts[0])
    events_b = _extract_events(parts[1])

    if len(events_a) != len(events_b):
        return False

    if len(events_a) == 0:
        return True

    # Get time bounds for each part
    max_time_a = max(e[0] + e[1] for e in events_a)  # offset + duration
    max_time_b = max(e[0] + e[1] for e in events_b)

    # Check if events in B are the retrograde of events in A
    # Sort both by their positions
    events_a_sorted = sorted(events_a, key=lambda x: x[0])
    events_b_sorted = sorted(events_b, key=lambda x: x[0])

    # For each event in A, check if there's a corresponding retrograde event in B
    tolerance = 0.01  # Small tolerance for floating point comparison

    for i, (offset_a, dur_a, pitch_a, is_rest_a) in enumerate(events_a_sorted):
        # Calculate expected position in B (retrograde)
        # If A has event at time t with duration d, ending at t+d,
        # B should have a corresponding event ending at max_time_b - t
        expected_end_b = max_time_b - offset_a
        expected_start_b = expected_end_b - dur_a

        # Find matching event in B
        found = False
        for offset_b, dur_b, pitch_b, is_rest_b in events_b_sorted:
            if (abs(offset_b - expected_start_b) < tolerance and
                abs(dur_b - dur_a) < tolerance and
                pitch_a == pitch_b and
                is_rest_a == is_rest_b):
                found = True
                break

        if not found:
            return False

    return True


def _extract_events(part: stream.Part) -> List[Tuple[float, float, int, bool]]:
    """
    Extract events from a part as (offset, duration, midi_pitch, is_rest) tuples.

    Args:
        part: A Part to extract events from

    Returns:
        List of event tuples: (offset, duration, midi_pitch or 0, is_rest)
    """
    events = []
    for el in part.flatten().notesAndRests:
        offset = float(el.offset)
        duration = float(el.quarterLength)

        if isinstance(el, note.Rest):
            events.append((offset, duration, 0, True))
        elif isinstance(el, note.Note):
            events.append((offset, duration, el.pitch.midi, False))
        elif isinstance(el, chord.Chord):
            # For chords, use the lowest pitch
            midi = min(p.midi for p in el.pitches)
            events.append((offset, duration, midi, False))

    return events


def pairwise_symmetry_map(voice: stream.Stream) -> List[Tuple[int, int]]:
    """
    Generate a mapping of symmetric pairs in a voice for palindrome visualization.

    For a voice with N events, returns pairs (i, N-1-i) showing which events
    correspond in a retrograde transformation.

    Args:
        voice: A Stream representing a single voice

    Returns:
        List of (forward_index, backward_index) pairs
    """
    events = list(voice.flatten().notesAndRests)
    n = len(events)

    pairs = []
    for i in range(n):
        j = n - 1 - i
        if i <= j:  # Only include each pair once
            pairs.append((i, j))

    return pairs
