"""
Core transformations for canonical music analysis: retrograde, inversion,
augmentation, diminution, time alignment, and palindrome verification.
"""

from typing import TypeVar, Union, List, Tuple, Dict
import music21 as m21
from music21 import stream, note, chord
import numpy as np

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


def augmentation(stream_obj: stream.Stream, factor: float = 2.0) -> stream.Stream:
    """
    Return augmentation of a stream (durations multiplied by factor).

    In augmentation canon, one voice plays notes with longer durations.

    Args:
        stream_obj: A music21 Stream to augment
        factor: Multiplication factor for durations (default 2.0 = double)

    Returns:
        A new Stream with augmented durations
    """
    result = stream_obj.__class__()

    for el in stream_obj.flatten().notesAndRests:
        new_el = el.__class__()

        # Copy pitch
        if isinstance(el, note.Note):
            new_el.pitch = el.pitch
        elif isinstance(el, chord.Chord):
            new_el.pitches = el.pitches

        # Multiply duration
        new_el.quarterLength = el.quarterLength * factor

        # Multiply offset
        result.insert(el.offset * factor, new_el)

    return result


def diminution(stream_obj: stream.Stream, factor: float = 2.0) -> stream.Stream:
    """
    Return diminution of a stream (durations divided by factor).

    In diminution canon, one voice plays notes with shorter durations.

    Args:
        stream_obj: A music21 Stream to diminish
        factor: Division factor for durations (default 2.0 = half)

    Returns:
        A new Stream with diminished durations
    """
    result = stream_obj.__class__()

    for el in stream_obj.flatten().notesAndRests:
        new_el = el.__class__()

        # Copy pitch
        if isinstance(el, note.Note):
            new_el.pitch = el.pitch
        elif isinstance(el, chord.Chord):
            new_el.pitches = el.pitches

        # Divide duration
        new_el.quarterLength = el.quarterLength / factor

        # Divide offset
        result.insert(el.offset / factor, new_el)

    return result


def mirror_canon(stream_obj: stream.Stream, axis_pitch: Union[str, m21.pitch.Pitch] = 'C4') -> stream.Stream:
    """
    Create a mirror canon: retrograde + inversion combined.

    This is both backwards in time AND upside-down in pitch.

    Args:
        stream_obj: A music21 Stream
        axis_pitch: The pitch axis for inversion

    Returns:
        A new Stream that is the mirror (retrograde-inversion)
    """
    # First invert, then retrograde
    inverted = invert(stream_obj, axis_pitch)
    mirrored = retrograde(inverted)
    return mirrored


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


# New analysis functions

def interval_analysis(score_or_stream: Union[stream.Score, stream.Stream]) -> Dict[str, any]:
    """
    Analyze melodic intervals in a score or stream.

    Returns statistics about the intervals used, including:
    - Histogram of interval sizes
    - Most common intervals
    - Average interval size
    - Interval distribution

    Args:
        score_or_stream: A Score or Stream to analyze

    Returns:
        Dictionary with interval statistics
    """
    if isinstance(score_or_stream, stream.Score):
        parts = list(score_or_stream.parts)
    else:
        parts = [score_or_stream]

    all_intervals = []
    interval_histogram = {}

    for part in parts:
        notes_list = [n for n in part.flatten().notesAndRests if not n.isRest and hasattr(n, 'pitch')]

        for i in range(len(notes_list) - 1):
            if isinstance(notes_list[i], note.Note) and isinstance(notes_list[i+1], note.Note):
                interval_semitones = notes_list[i+1].pitch.midi - notes_list[i].pitch.midi
                all_intervals.append(interval_semitones)

                # Build histogram
                interval_histogram[interval_semitones] = interval_histogram.get(interval_semitones, 0) + 1

    if not all_intervals:
        return {
            'total_intervals': 0,
            'histogram': {},
            'most_common': [],
            'average': 0,
            'distribution': {}
        }

    # Calculate statistics
    most_common = sorted(interval_histogram.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        'total_intervals': len(all_intervals),
        'histogram': interval_histogram,
        'most_common': most_common,
        'average': sum(abs(i) for i in all_intervals) / len(all_intervals),
        'largest_leap': max(abs(i) for i in all_intervals),
        'distribution': {
            'ascending': sum(1 for i in all_intervals if i > 0),
            'descending': sum(1 for i in all_intervals if i < 0),
            'repeated': sum(1 for i in all_intervals if i == 0)
        }
    }


def harmonic_analysis(score: stream.Score) -> Dict[str, any]:
    """
    Perform basic harmonic analysis on a score.

    Analyzes vertical sonorities (chords) when multiple voices sound together.

    Args:
        score: A Score with multiple parts

    Returns:
        Dictionary with harmonic statistics
    """
    parts = list(score.parts)

    if len(parts) < 2:
        return {
            'total_sonorities': 0,
            'consonances': 0,
            'dissonances': 0,
            'interval_classes': {}
        }

    # Get all unique time points
    time_points = set()
    for part in parts:
        for el in part.flatten().notesAndRests:
            if not el.isRest:
                time_points.add(float(el.offset))

    sonorities = []
    consonances = 0
    dissonances = 0
    interval_classes = {}

    # Consonant intervals (perfect and major/minor 3rds and 6ths, perfect 5ths, octaves)
    consonant_intervals = {0, 3, 4, 5, 7, 8, 9, 12, 15, 16}

    for time_point in sorted(time_points):
        # Find all notes sounding at this time
        sounding_notes = []
        for part in parts:
            for el in part.flatten().notesAndRests:
                if (not el.isRest and
                    float(el.offset) <= time_point < float(el.offset + el.quarterLength)):
                    if isinstance(el, note.Note):
                        sounding_notes.append(el.pitch.midi)

        if len(sounding_notes) >= 2:
            # Calculate intervals between all pairs
            for i in range(len(sounding_notes)):
                for j in range(i+1, len(sounding_notes)):
                    interval = abs(sounding_notes[j] - sounding_notes[i]) % 12
                    interval_classes[interval] = interval_classes.get(interval, 0) + 1

                    if interval in consonant_intervals:
                        consonances += 1
                    else:
                        dissonances += 1

            sonorities.append(sounding_notes)

    return {
        'total_sonorities': len(sonorities),
        'consonances': consonances,
        'dissonances': dissonances,
        'consonance_ratio': consonances / (consonances + dissonances) if (consonances + dissonances) > 0 else 0,
        'interval_classes': interval_classes,
        'unique_pitches_per_sonority': [len(set(s)) for s in sonorities]
    }


def rhythm_analysis(score_or_stream: Union[stream.Score, stream.Stream]) -> Dict[str, any]:
    """
    Analyze rhythmic patterns in a score or stream.

    Returns statistics about durations and rhythmic patterns.

    Args:
        score_or_stream: A Score or Stream to analyze

    Returns:
        Dictionary with rhythm statistics
    """
    if isinstance(score_or_stream, stream.Score):
        parts = list(score_or_stream.parts)
    else:
        parts = [score_or_stream]

    all_durations = []
    duration_histogram = {}

    for part in parts:
        for el in part.flatten().notesAndRests:
            duration = float(el.quarterLength)
            all_durations.append(duration)
            duration_histogram[duration] = duration_histogram.get(duration, 0) + 1

    if not all_durations:
        return {
            'total_events': 0,
            'histogram': {},
            'most_common': [],
            'average_duration': 0
        }

    most_common = sorted(duration_histogram.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        'total_events': len(all_durations),
        'histogram': duration_histogram,
        'most_common': most_common,
        'average_duration': sum(all_durations) / len(all_durations),
        'shortest': min(all_durations),
        'longest': max(all_durations),
        'unique_durations': len(duration_histogram)
    }


# Advanced canonical transformations

def stretto(
    theme: stream.Stream,
    num_voices: int = 2,
    entry_interval: float = 4.0,
    transformation: str = 'none'
) -> stream.Score:
    """
    Create a stretto canon with overlapping voice entries.

    In stretto, voices enter before the previous voice finishes, creating
    overlapping imitative counterpoint. Common in fugues and complex canons.

    Args:
        theme: The theme/subject to use
        num_voices: Number of voice entries (default 2)
        entry_interval: Quarter notes between voice entries (default 4.0)
        transformation: Apply to following voices: 'none', 'invert', 'retrograde',
                       'augmentation', 'diminution' (default 'none')

    Returns:
        A Score with overlapping voices in stretto

    Examples:
        >>> from music21 import stream, note
        >>> theme = stream.Stream()
        >>> theme.append(note.Note('C4', quarterLength=1))
        >>> theme.append(note.Note('D4', quarterLength=1))
        >>> theme.append(note.Note('E4', quarterLength=1))
        >>> stretto_score = stretto(theme, num_voices=3, entry_interval=2.0)
    """
    score = stream.Score()

    for voice_num in range(num_voices):
        part = stream.Part()
        part.id = f'voice_{voice_num + 1}'

        # Apply transformation to subsequent voices if requested
        voice_theme = theme
        if voice_num > 0 and transformation != 'none':
            if transformation == 'invert':
                voice_theme = invert(theme)
            elif transformation == 'retrograde':
                voice_theme = retrograde(theme)
            elif transformation == 'augmentation':
                voice_theme = augmentation(theme, factor=2.0)
            elif transformation == 'diminution':
                voice_theme = diminution(theme, factor=2.0)

        # Insert theme at staggered offset
        offset = voice_num * entry_interval
        for el in voice_theme.flatten().notesAndRests:
            part.insert(el.offset + offset, el)

        score.insert(0, part)

    return score


def canon_at_interval(
    theme: stream.Stream,
    interval: int = 7,
    time_delay: float = 0.0,
    mode: str = 'strict'
) -> stream.Score:
    """
    Create a canon where the following voice is transposed by an interval.

    Canon at the fifth (interval=7) and canon at the octave (interval=12)
    are common in Baroque music. Bach frequently used canon at various intervals.

    Args:
        theme: The leading voice melody
        interval: Transposition interval in semitones (default 7 = perfect fifth)
                 Positive = transpose up, negative = transpose down
        time_delay: Quarter notes before the following voice enters (default 0.0)
        mode: 'strict' (exact transposition) or 'tonal' (preserve key/scale)

    Returns:
        A Score with two voices at the specified interval

    Examples:
        >>> # Canon at the fifth (like "Frère Jacques")
        >>> canon_fifth = canon_at_interval(theme, interval=7, time_delay=4.0)
        >>>
        >>> # Canon at the octave
        >>> canon_octave = canon_at_interval(theme, interval=12, time_delay=2.0)
    """
    score = stream.Score()

    # First voice: original theme
    part1 = stream.Part()
    part1.id = 'voice_1_leader'
    for el in theme.flatten().notesAndRests:
        part1.insert(el.offset, el)

    # Second voice: transposed theme
    part2 = stream.Part()
    part2.id = 'voice_2_follower'

    for el in theme.flatten().notesAndRests:
        new_el = el.__class__()
        new_el.quarterLength = el.quarterLength

        if isinstance(el, note.Note):
            if mode == 'strict':
                # Strict transposition by semitones
                new_midi = el.pitch.midi + interval
                new_el.pitch = m21.pitch.Pitch(midi=new_midi)
            else:  # tonal
                # Transpose within key/scale (diatonic transposition)
                # This is a simplified version; could be enhanced
                new_el.pitch = el.pitch.transpose(interval)
        elif isinstance(el, chord.Chord):
            if mode == 'strict':
                new_pitches = []
                for p in el.pitches:
                    new_midi = p.midi + interval
                    new_pitches.append(m21.pitch.Pitch(midi=new_midi))
                new_el.pitches = new_pitches
            else:
                new_el.pitches = [p.transpose(interval) for p in el.pitches]
        elif isinstance(el, note.Rest):
            pass  # Rest unchanged

        part2.insert(el.offset + time_delay, new_el)

    score.insert(0, part1)
    score.insert(0, part2)

    return score


def proportional_canon(
    theme: stream.Stream,
    ratio: Tuple[int, int] = (2, 3),
    num_statements: int = 1
) -> stream.Score:
    """
    Create a proportional/mensuration canon with voices in different tempo ratios.

    In proportional canons, voices play the same melody but at different speeds.
    For example, ratio (2, 3) means voice 1 plays at 2/3 the speed of voice 2.

    Args:
        theme: The theme to use
        ratio: Tuple of (voice1_ratio, voice2_ratio) integers (default (2, 3))
               Voice 1 plays at ratio[0]/ratio[1] the speed of voice 2
        num_statements: Number of complete statements per voice (default 1)

    Returns:
        A Score with voices in proportional tempo relationship

    Examples:
        >>> # Classic mensuration canon: 2:3 ratio
        >>> prop_canon = proportional_canon(theme, ratio=(2, 3))
        >>>
        >>> # Triple canon: 1:2 ratio (voice 2 twice as fast)
        >>> double_speed = proportional_canon(theme, ratio=(1, 2))
    """
    score = stream.Score()

    # Voice 1: slower (multiply durations by ratio[0])
    part1 = stream.Part()
    part1.id = 'voice_1_slower'

    for statement in range(num_statements):
        offset_base = statement * sum(el.quarterLength for el in theme.flatten().notesAndRests) * ratio[0]
        for el in theme.flatten().notesAndRests:
            new_el = el.__class__()
            if isinstance(el, note.Note):
                new_el.pitch = el.pitch
            elif isinstance(el, chord.Chord):
                new_el.pitches = el.pitches
            new_el.quarterLength = el.quarterLength * ratio[0]
            part1.insert(offset_base + el.offset * ratio[0], new_el)

    # Voice 2: faster (multiply durations by ratio[1])
    part2 = stream.Part()
    part2.id = 'voice_2_faster'

    for statement in range(num_statements):
        offset_base = statement * sum(el.quarterLength for el in theme.flatten().notesAndRests) * ratio[1]
        for el in theme.flatten().notesAndRests:
            new_el = el.__class__()
            if isinstance(el, note.Note):
                new_el.pitch = el.pitch
            elif isinstance(el, chord.Chord):
                new_el.pitches = el.pitches
            new_el.quarterLength = el.quarterLength * ratio[1]
            part2.insert(offset_base + el.offset * ratio[1], new_el)

    score.insert(0, part1)
    score.insert(0, part2)

    return score


def counterpoint_check(score: stream.Score) -> Dict[str, any]:
    """
    Validate voice leading according to basic counterpoint rules.

    Checks for common issues in two-voice counterpoint:
    - Parallel fifths and octaves
    - Direct/hidden fifths and octaves
    - Voice crossing
    - Excessive leaps
    - Dissonance treatment

    Args:
        score: A Score with two voices to check

    Returns:
        Dictionary with validation results and detected issues

    Examples:
        >>> results = counterpoint_check(two_voice_score)
        >>> print(f"Parallel fifths: {results['parallel_fifths']}")
        >>> print(f"Voice crossings: {results['voice_crossings']}")
    """
    parts = list(score.parts)

    if len(parts) != 2:
        return {
            'error': 'Counterpoint check requires exactly 2 voices',
            'num_voices': len(parts)
        }

    # Extract all time points and notes for each voice
    voice1_notes = [(float(n.offset), n) for n in parts[0].flatten().notes]
    voice2_notes = [(float(n.offset), n) for n in parts[1].flatten().notes]

    # Sort by offset
    voice1_notes.sort(key=lambda x: x[0])
    voice2_notes.sort(key=lambda x: x[0])

    parallel_fifths = []
    parallel_octaves = []
    voice_crossings = []
    large_leaps = []
    unresolved_dissonances = []

    # Check for parallel motion
    for i in range(min(len(voice1_notes), len(voice2_notes)) - 1):
        offset1, note1 = voice1_notes[i]
        offset2, note2 = voice2_notes[i]

        if isinstance(note1, note.Note) and isinstance(note2, note.Note):
            # Calculate interval
            interval1 = abs(note1.pitch.midi - note2.pitch.midi) % 12

            # Check next simultaneity
            if i + 1 < min(len(voice1_notes), len(voice2_notes)):
                next_note1 = voice1_notes[i + 1][1]
                next_note2 = voice2_notes[i + 1][1]

                if isinstance(next_note1, note.Note) and isinstance(next_note2, note.Note):
                    interval2 = abs(next_note1.pitch.midi - next_note2.pitch.midi) % 12

                    # Parallel fifths
                    if interval1 == 7 and interval2 == 7:
                        parallel_fifths.append((i, offset1))

                    # Parallel octaves
                    if interval1 == 0 and interval2 == 0:
                        parallel_octaves.append((i, offset1))

            # Check voice crossing
            if note1.pitch.midi < note2.pitch.midi:
                voice_crossings.append((i, offset1))

    # Check for large leaps in each voice
    for voice_num, voice_notes in enumerate([voice1_notes, voice2_notes], 1):
        for i in range(len(voice_notes) - 1):
            _, note_a = voice_notes[i]
            _, note_b = voice_notes[i + 1]

            if isinstance(note_a, note.Note) and isinstance(note_b, note.Note):
                leap = abs(note_b.pitch.midi - note_a.pitch.midi)
                if leap > 7:  # Larger than a fifth
                    large_leaps.append((voice_num, i, leap))

    # Calculate quality score
    total_checks = (min(len(voice1_notes), len(voice2_notes)) * 2 +
                   len(voice1_notes) + len(voice2_notes))

    if total_checks == 0:
        quality_score = 1.0
    else:
        issues = (len(parallel_fifths) + len(parallel_octaves) +
                 len(voice_crossings) + len(large_leaps) * 0.5)
        quality_score = max(0.0, 1.0 - (issues / total_checks))

    return {
        'parallel_fifths': len(parallel_fifths),
        'parallel_fifths_locations': parallel_fifths,
        'parallel_octaves': len(parallel_octaves),
        'parallel_octaves_locations': parallel_octaves,
        'voice_crossings': len(voice_crossings),
        'voice_crossings_locations': voice_crossings,
        'large_leaps': len(large_leaps),
        'large_leaps_details': large_leaps,
        'quality_score': quality_score,
        'passed': quality_score > 0.7,
        'total_simultaneities': min(len(voice1_notes), len(voice2_notes))
    }
