"""
Core transformations for canonical music analysis: retrograde, inversion,
augmentation, diminution, time alignment, and palindrome verification.
"""

from typing import TypeVar, Union, List, Tuple, Dict, Optional
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


def spectral_analysis(score_or_stream: Union[stream.Score, stream.Stream]) -> Dict[str, any]:
    """
    Perform spectral/frequency analysis on a score or stream.

    Analyzes the frequency distribution of pitches, including:
    - Pitch class histogram (C, C#, D, etc.)
    - Octave distribution
    - Most/least common pitches
    - Pitch range and tessitura

    Args:
        score_or_stream: A Score or Stream to analyze

    Returns:
        Dictionary with spectral statistics

    Examples:
        >>> from cancrizans import load_bach_crab_canon, spectral_analysis
        >>> score = load_bach_crab_canon()
        >>> analysis = spectral_analysis(score)
        >>> print(f"Most common pitch class: {analysis['most_common_pitch_class']}")
    """
    if isinstance(score_or_stream, stream.Score):
        parts = list(score_or_stream.parts)
    else:
        parts = [score_or_stream]

    all_pitches = []
    pitch_class_histogram = {i: 0 for i in range(12)}  # 0=C, 1=C#, etc.
    octave_histogram = {}
    pitch_histogram = {}

    for part in parts:
        for el in part.flatten().notes:
            if isinstance(el, note.Note):
                midi = el.pitch.midi
                pc = midi % 12
                octave = midi // 12

                all_pitches.append(midi)
                pitch_class_histogram[pc] += 1
                octave_histogram[octave] = octave_histogram.get(octave, 0) + 1
                pitch_histogram[midi] = pitch_histogram.get(midi, 0) + 1
            elif isinstance(el, chord.Chord):
                for p in el.pitches:
                    midi = p.midi
                    pc = midi % 12
                    octave = midi // 12

                    all_pitches.append(midi)
                    pitch_class_histogram[pc] += 1
                    octave_histogram[octave] = octave_histogram.get(octave, 0) + 1
                    pitch_histogram[midi] = pitch_histogram.get(midi, 0) + 1

    if not all_pitches:
        return {
            'total_pitches': 0,
            'pitch_class_histogram': pitch_class_histogram,
            'octave_histogram': {},
            'pitch_range': 0,
            'lowest_pitch': None,
            'highest_pitch': None
        }

    # Pitch class names
    pc_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    # Find most common pitch class
    most_common_pc = max(pitch_class_histogram.items(), key=lambda x: x[1])
    most_common_pc_name = pc_names[most_common_pc[0]]

    # Calculate tessitura (average pitch)
    tessitura = sum(all_pitches) / len(all_pitches)

    return {
        'total_pitches': len(all_pitches),
        'pitch_class_histogram': pitch_class_histogram,
        'pitch_class_histogram_named': {pc_names[i]: count for i, count in pitch_class_histogram.items()},
        'octave_histogram': octave_histogram,
        'most_common_pitch_class': most_common_pc_name,
        'most_common_pitch_class_count': most_common_pc[1],
        'pitch_range': max(all_pitches) - min(all_pitches),
        'lowest_pitch': min(all_pitches),
        'highest_pitch': max(all_pitches),
        'tessitura': tessitura,
        'unique_pitches': len(set(all_pitches)),
        'pitch_diversity': len(set(all_pitches)) / len(all_pitches) if all_pitches else 0
    }


def symmetry_metrics(score: stream.Score) -> Dict[str, any]:
    """
    Calculate advanced symmetry metrics for a two-voice canon.

    Analyzes multiple dimensions of symmetry including:
    - Pitch symmetry (retrograde matching)
    - Rhythmic symmetry
    - Interval symmetry
    - Temporal symmetry

    Args:
        score: A Score with two voices

    Returns:
        Dictionary with detailed symmetry measurements

    Examples:
        >>> from cancrizans import load_bach_crab_canon, symmetry_metrics
        >>> score = load_bach_crab_canon()
        >>> metrics = symmetry_metrics(score)
        >>> print(f"Overall symmetry: {metrics['overall_symmetry']:.2%}")
    """
    parts = list(score.parts)

    if len(parts) != 2:
        return {
            'error': 'Symmetry metrics require exactly 2 voices',
            'num_voices': len(parts)
        }

    # Extract note sequences from both parts
    voice1_notes = [(float(n.offset), n) for n in parts[0].flatten().notes]
    voice2_notes = [(float(n.offset), n) for n in parts[1].flatten().notes]

    # Sort by offset
    voice1_notes.sort(key=lambda x: x[0])
    voice2_notes.sort(key=lambda x: x[0])

    if len(voice1_notes) != len(voice2_notes):
        return {
            'error': 'Voices have different numbers of notes',
            'voice1_notes': len(voice1_notes),
            'voice2_notes': len(voice2_notes)
        }

    if len(voice1_notes) == 0:
        return {
            'overall_symmetry': 1.0,
            'pitch_symmetry': 1.0,
            'rhythmic_symmetry': 1.0,
            'interval_symmetry': 1.0,
            'temporal_symmetry': 1.0,
            'note_count': 0
        }

    n = len(voice1_notes)

    # Calculate pitch symmetry (retrograde)
    pitch_matches = 0
    for i in range(n):
        note1 = voice1_notes[i][1]
        note2 = voice2_notes[n - 1 - i][1]

        if isinstance(note1, note.Note) and isinstance(note2, note.Note):
            if note1.pitch.midi == note2.pitch.midi:
                pitch_matches += 1

    pitch_symmetry = pitch_matches / n if n > 0 else 0

    # Calculate rhythmic symmetry
    rhythm_matches = 0
    for i in range(n):
        dur1 = voice1_notes[i][1].quarterLength
        dur2 = voice2_notes[n - 1 - i][1].quarterLength

        if abs(dur1 - dur2) < 0.01:  # Small tolerance for floating point
            rhythm_matches += 1

    rhythmic_symmetry = rhythm_matches / n if n > 0 else 0

    # Calculate interval symmetry
    if n > 1:
        interval_matches = 0
        for i in range(n - 1):
            # Forward intervals in voice 1
            if isinstance(voice1_notes[i][1], note.Note) and isinstance(voice1_notes[i + 1][1], note.Note):
                interval1 = voice1_notes[i + 1][1].pitch.midi - voice1_notes[i][1].pitch.midi

                # Backward intervals in voice 2 (should match for retrograde)
                rev_i = n - 2 - i
                if rev_i >= 0 and isinstance(voice2_notes[rev_i][1], note.Note) and isinstance(voice2_notes[rev_i + 1][1], note.Note):
                    interval2 = voice2_notes[rev_i][1].pitch.midi - voice2_notes[rev_i + 1][1].pitch.midi

                    if interval1 == interval2:
                        interval_matches += 1

        interval_symmetry = interval_matches / (n - 1) if n > 1 else 0
    else:
        interval_symmetry = 1.0

    # Calculate temporal symmetry (timing alignment)
    total_duration_v1 = max(off + n.quarterLength for off, n in voice1_notes)
    total_duration_v2 = max(off + n.quarterLength for off, n in voice2_notes)

    temporal_symmetry = 1.0 - abs(total_duration_v1 - total_duration_v2) / max(total_duration_v1, total_duration_v2)

    # Overall symmetry (weighted average)
    overall_symmetry = (
        pitch_symmetry * 0.4 +
        rhythmic_symmetry * 0.3 +
        interval_symmetry * 0.2 +
        temporal_symmetry * 0.1
    )

    return {
        'overall_symmetry': overall_symmetry,
        'pitch_symmetry': pitch_symmetry,
        'rhythmic_symmetry': rhythmic_symmetry,
        'interval_symmetry': interval_symmetry,
        'temporal_symmetry': temporal_symmetry,
        'note_count': n,
        'pitch_matches': pitch_matches,
        'rhythm_matches': rhythm_matches,
        'is_perfect_palindrome': overall_symmetry >= 0.99
    }


def chord_progression_analysis(score: stream.Score) -> Dict[str, any]:
    """
    Analyze chord progressions in a multi-voice score.

    Identifies vertical sonorities and analyzes harmonic progressions.

    Args:
        score: A Score with multiple voices

    Returns:
        Dictionary with chord progression information

    Examples:
        >>> analysis = chord_progression_analysis(two_voice_score)
        >>> print(f"Unique chords: {analysis['unique_chords']}")
    """
    parts = list(score.parts)

    if len(parts) < 2:
        return {
            'error': 'Chord analysis requires at least 2 voices',
            'num_voices': len(parts)
        }

    # Get all unique time points where notes sound
    time_points = set()
    for part in parts:
        for el in part.flatten().notes:
            time_points.add(float(el.offset))

    chords_at_time = []
    chord_types = {}

    for time_point in sorted(time_points):
        # Find all pitches sounding at this time
        sounding_pitches = []
        for part in parts:
            for el in part.flatten().notes:
                if float(el.offset) <= time_point < float(el.offset + el.quarterLength):
                    if isinstance(el, note.Note):
                        sounding_pitches.append(el.pitch.midi)
                    elif isinstance(el, chord.Chord):
                        sounding_pitches.extend([p.midi for p in el.pitches])

        if len(sounding_pitches) >= 2:
            # Sort and create chord signature
            sounding_pitches.sort()
            chord_sig = tuple(p % 12 for p in sounding_pitches)  # Pitch classes

            # Classify chord type (simplified)
            chord_type = _classify_chord(chord_sig)
            chord_types[chord_type] = chord_types.get(chord_type, 0) + 1

            chords_at_time.append({
                'time': time_point,
                'pitches': sounding_pitches,
                'pitch_classes': chord_sig,
                'type': chord_type
            })

    return {
        'total_chords': len(chords_at_time),
        'unique_chords': len(set(c['pitch_classes'] for c in chords_at_time)),
        'chord_types': chord_types,
        'progression': chords_at_time[:20],  # First 20 chords
        'most_common_chord_type': max(chord_types.items(), key=lambda x: x[1])[0] if chord_types else None
    }


def _classify_chord(pitch_classes: Tuple[int, ...]) -> str:
    """
    Classify a chord by its interval structure (simplified).

    Args:
        pitch_classes: Tuple of pitch classes (0-11)

    Returns:
        String describing chord type
    """
    if len(pitch_classes) < 2:
        return 'single_note'

    # Calculate intervals from root
    intervals = [(pc - pitch_classes[0]) % 12 for pc in pitch_classes]
    intervals_set = set(intervals)

    # Common chord types (simplified)
    if intervals_set == {0, 4, 7}:
        return 'major_triad'
    elif intervals_set == {0, 3, 7}:
        return 'minor_triad'
    elif intervals_set == {0, 3, 6}:
        return 'diminished_triad'
    elif intervals_set == {0, 4, 8}:
        return 'augmented_triad'
    elif 7 in intervals_set or 5 in intervals_set:
        return 'contains_fifth'
    elif 3 in intervals_set or 4 in intervals_set:
        return 'contains_third'
    else:
        return 'other'


def compare_canons(canon1: stream.Score, canon2: stream.Score) -> Dict[str, any]:
    """
    Compare two canons across multiple dimensions.

    Analyzes similarities and differences between two canonical works.

    Args:
        canon1: First canon to compare
        canon2: Second canon to compare

    Returns:
        Dictionary with comparison metrics

    Examples:
        >>> from cancrizans import load_bach_crab_canon
        >>> bach_canon = load_bach_crab_canon()
        >>> my_canon = assemble_crab_from_theme(my_theme)
        >>> comparison = compare_canons(bach_canon, my_canon)
        >>> print(f"Similarity: {comparison['overall_similarity']:.2%}")
    """
    # Get analyses for both canons
    interval1 = interval_analysis(canon1)
    interval2 = interval_analysis(canon2)

    rhythm1 = rhythm_analysis(canon1)
    rhythm2 = rhythm_analysis(canon2)

    spectral1 = spectral_analysis(canon1)
    spectral2 = spectral_analysis(canon2)

    # Compare interval distributions
    interval_similarity = _compare_distributions(
        interval1.get('histogram', {}),
        interval2.get('histogram', {})
    )

    # Compare rhythmic distributions
    rhythm_similarity = _compare_distributions(
        rhythm1.get('histogram', {}),
        rhythm2.get('histogram', {})
    )

    # Compare pitch class distributions
    pc_similarity = _compare_distributions(
        spectral1.get('pitch_class_histogram', {}),
        spectral2.get('pitch_class_histogram', {})
    )

    # Overall similarity (weighted average)
    overall_similarity = (
        interval_similarity * 0.4 +
        rhythm_similarity * 0.3 +
        pc_similarity * 0.3
    )

    return {
        'overall_similarity': overall_similarity,
        'interval_similarity': interval_similarity,
        'rhythm_similarity': rhythm_similarity,
        'pitch_class_similarity': pc_similarity,
        'canon1_length': interval1.get('total_intervals', 0),
        'canon2_length': interval2.get('total_intervals', 0),
        'length_ratio': interval2.get('total_intervals', 1) / max(interval1.get('total_intervals', 1), 1),
        'comparison_summary': _generate_comparison_summary(overall_similarity)
    }


def _compare_distributions(dist1: Dict, dist2: Dict) -> float:
    """
    Calculate similarity between two distributions using cosine similarity.

    Args:
        dist1: First distribution dictionary
        dist2: Second distribution dictionary

    Returns:
        Similarity score between 0 and 1
    """
    if not dist1 or not dist2:
        return 0.0

    # Get all keys from both distributions
    all_keys = set(dist1.keys()) | set(dist2.keys())

    if not all_keys:
        return 0.0

    # Create vectors
    vec1 = np.array([dist1.get(k, 0) for k in all_keys])
    vec2 = np.array([dist2.get(k, 0) for k in all_keys])

    # Cosine similarity
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    similarity = dot_product / (norm1 * norm2)
    return float(similarity)


def _generate_comparison_summary(similarity: float) -> str:
    """Generate a text summary of canon similarity."""
    if similarity >= 0.9:
        return "Very similar - nearly identical structure"
    elif similarity >= 0.7:
        return "Similar - shares many characteristics"
    elif similarity >= 0.5:
        return "Moderately similar - some common features"
    elif similarity >= 0.3:
        return "Somewhat different - few shared characteristics"
    else:
        return "Very different - distinct structures"


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


def voice_leading_analysis(score: stream.Score) -> Dict[str, any]:
    """
    Comprehensive voice leading analysis for two-voice counterpoint.

    Analyzes motion types, leap resolutions, approach to perfect intervals,
    and overall voice independence.

    Args:
        score: A Score with two voices to analyze

    Returns:
        Dictionary with detailed voice leading metrics

    Examples:
        >>> results = voice_leading_analysis(two_voice_score)
        >>> print(f"Contrary motion: {results['motion_types']['contrary']}")
        >>> print(f"Leap resolutions: {results['leap_resolution_rate']}")
    """
    parts = list(score.parts)

    if len(parts) != 2:
        return {
            'error': 'Voice leading analysis requires exactly 2 voices',
            'num_voices': len(parts)
        }

    # Extract notes with offsets
    voice1_notes = [(float(n.offset), n) for n in parts[0].flatten().notes]
    voice2_notes = [(float(n.offset), n) for n in parts[1].flatten().notes]

    voice1_notes.sort(key=lambda x: x[0])
    voice2_notes.sort(key=lambda x: x[0])

    # Motion type counters
    motion_types = {
        'parallel': 0,
        'similar': 0,
        'contrary': 0,
        'oblique': 0
    }

    # Voice range tracking
    voice1_range = {'min': 127, 'max': 0}
    voice2_range = {'min': 127, 'max': 0}

    # Leap tracking
    voice1_leaps = []
    voice2_leaps = []
    resolved_leaps = 0
    total_leaps = 0

    # Approach to perfect intervals
    perfect_approaches = {
        'contrary': 0,
        'similar': 0,
        'direct': 0
    }

    # Track ranges for ALL notes in both voices
    for offset, n in voice1_notes:
        if isinstance(n, note.Note):
            voice1_range['min'] = min(voice1_range['min'], n.pitch.midi)
            voice1_range['max'] = max(voice1_range['max'], n.pitch.midi)

    for offset, n in voice2_notes:
        if isinstance(n, note.Note):
            voice2_range['min'] = min(voice2_range['min'], n.pitch.midi)
            voice2_range['max'] = max(voice2_range['max'], n.pitch.midi)

    # Analyze motion between consecutive simultaneities
    for i in range(min(len(voice1_notes), len(voice2_notes)) - 1):
        offset1, note1 = voice1_notes[i]
        offset2, note2 = voice2_notes[i]

        if i + 1 < min(len(voice1_notes), len(voice2_notes)):
            next_note1 = voice1_notes[i + 1][1]
            next_note2 = voice2_notes[i + 1][1]

            if all(isinstance(n, note.Note) for n in [note1, note2, next_note1, next_note2]):
                # Calculate motion
                v1_motion = next_note1.pitch.midi - note1.pitch.midi
                v2_motion = next_note2.pitch.midi - note2.pitch.midi

                # Classify motion type
                if v1_motion == 0 and v2_motion == 0:
                    pass  # No motion
                elif v1_motion == 0 or v2_motion == 0:
                    motion_types['oblique'] += 1
                elif (v1_motion > 0 and v2_motion > 0) or (v1_motion < 0 and v2_motion < 0):
                    if abs(v1_motion) == abs(v2_motion):
                        motion_types['parallel'] += 1
                    else:
                        motion_types['similar'] += 1
                else:
                    motion_types['contrary'] += 1

                # Check approach to perfect intervals
                next_interval = abs(next_note1.pitch.midi - next_note2.pitch.midi) % 12
                if next_interval in [0, 7]:  # Unison or perfect fifth
                    if (v1_motion > 0 and v2_motion < 0) or (v1_motion < 0 and v2_motion > 0):
                        perfect_approaches['contrary'] += 1
                    elif (v1_motion > 0 and v2_motion > 0) or (v1_motion < 0 and v2_motion < 0):
                        if abs(v1_motion) == abs(v2_motion):
                            perfect_approaches['direct'] += 1
                        else:
                            perfect_approaches['similar'] += 1

    # Analyze leaps and resolutions in each voice
    for voice_notes, voice_leaps in [(voice1_notes, voice1_leaps), (voice2_notes, voice2_leaps)]:
        for i in range(len(voice_notes) - 1):
            _, note_a = voice_notes[i]
            _, note_b = voice_notes[i + 1]

            if isinstance(note_a, note.Note) and isinstance(note_b, note.Note):
                leap = note_b.pitch.midi - note_a.pitch.midi
                if abs(leap) > 4:  # Larger than a major third
                    voice_leaps.append(i)
                    total_leaps += 1

                    # Check if leap is resolved by step in opposite direction
                    if i + 2 < len(voice_notes):
                        _, note_c = voice_notes[i + 2]
                        if isinstance(note_c, note.Note):
                            resolution = note_c.pitch.midi - note_b.pitch.midi
                            if abs(resolution) <= 2 and (leap * resolution < 0):  # Step in opposite direction
                                resolved_leaps += 1

    # Calculate metrics
    total_motion = sum(motion_types.values())
    leap_resolution_rate = resolved_leaps / total_leaps if total_leaps > 0 else 1.0

    # Voice independence score (prefer contrary motion, avoid parallel)
    if total_motion > 0:
        independence_score = (
            motion_types['contrary'] * 1.0 +
            motion_types['oblique'] * 0.8 +
            motion_types['similar'] * 0.3 -
            motion_types['parallel'] * 0.5
        ) / total_motion
        independence_score = max(0.0, min(1.0, independence_score))
    else:
        independence_score = 0.5

    # Perfect interval approach score (prefer contrary motion)
    total_perfect = sum(perfect_approaches.values())
    if total_perfect > 0:
        perfect_approach_score = (
            perfect_approaches['contrary'] * 1.0 +
            perfect_approaches['similar'] * 0.3 -
            perfect_approaches['direct'] * 1.0
        ) / total_perfect
        perfect_approach_score = max(0.0, min(1.0, perfect_approach_score))
    else:
        perfect_approach_score = 1.0

    # Overall voice leading quality
    overall_quality = (
        independence_score * 0.4 +
        leap_resolution_rate * 0.3 +
        perfect_approach_score * 0.3
    )

    return {
        'motion_types': motion_types,
        'motion_percentages': {
            k: (v / total_motion * 100) if total_motion > 0 else 0
            for k, v in motion_types.items()
        },
        'voice_ranges': {
            'voice1': {
                'min_midi': voice1_range['min'] if voice1_range['min'] != 127 else 0,
                'max_midi': voice1_range['max'],
                'span': voice1_range['max'] - voice1_range['min'] if voice1_range['min'] != 127 else 0
            },
            'voice2': {
                'min_midi': voice2_range['min'] if voice2_range['min'] != 127 else 0,
                'max_midi': voice2_range['max'],
                'span': voice2_range['max'] - voice2_range['min'] if voice2_range['min'] != 127 else 0
            }
        },
        'leap_statistics': {
            'total_leaps': total_leaps,
            'resolved_leaps': resolved_leaps,
            'resolution_rate': leap_resolution_rate
        },
        'perfect_interval_approaches': perfect_approaches,
        'independence_score': independence_score,
        'perfect_approach_score': perfect_approach_score,
        'overall_quality': overall_quality,
        'grade': _get_quality_grade(overall_quality)
    }


def cadence_detection(score: stream.Score) -> Dict[str, any]:
    """
    Detect cadences in a two-voice score.

    Identifies authentic, half, plagal, and deceptive cadences based on
    intervallic motion and melodic patterns.

    Args:
        score: A Score to analyze for cadences

    Returns:
        Dictionary with detected cadences and their locations

    Examples:
        >>> results = cadence_detection(two_voice_score)
        >>> print(f"Authentic cadences: {results['cadence_counts']['authentic']}")
        >>> for loc, cad_type in results['cadences']:
        ...     print(f"Cadence at {loc}: {cad_type}")
    """
    parts = list(score.parts)

    if len(parts) < 2:
        return {
            'error': 'Cadence detection requires at least 2 voices',
            'num_voices': len(parts)
        }

    # Use first two parts
    voice1_notes = [(float(n.offset), n) for n in parts[0].flatten().notes]
    voice2_notes = [(float(n.offset), n) for n in parts[1].flatten().notes]

    voice1_notes.sort(key=lambda x: x[0])
    voice2_notes.sort(key=lambda x: x[0])

    cadences = []
    cadence_counts = {
        'authentic': 0,
        'half': 0,
        'plagal': 0,
        'deceptive': 0,
        'other': 0
    }

    # Analyze final few notes of phrases (looking for cadential patterns)
    # Simple heuristic: check last 3-4 simultaneities
    min_len = min(len(voice1_notes), len(voice2_notes))

    if min_len >= 3:
        # Check final cadence
        final_idx = min_len - 1

        # Get last 3 notes from each voice
        v1_notes = [voice1_notes[final_idx - 2][1], voice1_notes[final_idx - 1][1], voice1_notes[final_idx][1]]
        v2_notes = [voice2_notes[final_idx - 2][1], voice2_notes[final_idx - 1][1], voice2_notes[final_idx][1]]

        if all(isinstance(n, note.Note) for n in v1_notes + v2_notes):
            # Calculate intervals
            final_interval = abs(v1_notes[2].pitch.midi - v2_notes[2].pitch.midi) % 12
            penult_interval = abs(v1_notes[1].pitch.midi - v2_notes[1].pitch.midi) % 12

            # Calculate bass motion (assuming voice2 is bass)
            bass_motion = v2_notes[2].pitch.midi - v2_notes[1].pitch.midi

            # Calculate upper voice motion
            upper_motion = v1_notes[2].pitch.midi - v1_notes[1].pitch.midi

            # Authentic cadence: V-I motion, ending on unison/octave
            # Heuristic: bass rises by 4th or falls by 5th, upper voice resolves stepwise
            if final_interval == 0 and abs(upper_motion) <= 2:
                if abs(bass_motion) == 5 or abs(bass_motion) == 7:
                    cadences.append((float(voice1_notes[final_idx][0]), 'authentic'))
                    cadence_counts['authentic'] += 1
                # Plagal cadence: IV-I motion (bass rises by step or falls by third)
                elif abs(bass_motion) <= 4:
                    cadences.append((float(voice1_notes[final_idx][0]), 'plagal'))
                    cadence_counts['plagal'] += 1
                else:
                    cadences.append((float(voice1_notes[final_idx][0]), 'other'))
                    cadence_counts['other'] += 1
            # Half cadence: ending on fifth
            elif final_interval == 7:
                cadences.append((float(voice1_notes[final_idx][0]), 'half'))
                cadence_counts['half'] += 1
            # Deceptive cadence: expected resolution avoided
            elif penult_interval == 7 and final_interval != 0:
                cadences.append((float(voice1_notes[final_idx][0]), 'deceptive'))
                cadence_counts['deceptive'] += 1
            else:
                cadences.append((float(voice1_notes[final_idx][0]), 'other'))
                cadence_counts['other'] += 1

    return {
        'cadences': cadences,
        'cadence_counts': cadence_counts,
        'total_cadences': len(cadences),
        'has_final_cadence': len(cadences) > 0,
        'final_cadence_type': cadences[0][1] if cadences else None
    }


def modulation_detection(score: stream.Score, window_size: int = 8) -> Dict[str, any]:
    """
    Detect potential modulations (key changes) in a score.

    Uses a sliding window analysis of pitch content to identify
    shifts in tonal center.

    Args:
        score: A Score to analyze for modulations
        window_size: Number of notes in analysis window (default: 8)

    Returns:
        Dictionary with detected modulations and key analysis

    Examples:
        >>> results = modulation_detection(score)
        >>> print(f"Key changes detected: {results['num_modulations']}")
        >>> print(f"Starting key: {results['starting_key']}")
    """
    # Get all notes from all parts
    all_notes = []
    for part in score.parts:
        for n in part.flatten().notes:
            if isinstance(n, note.Note):
                all_notes.append((float(n.offset), n.pitch.midi % 12))
            elif isinstance(n, chord.Chord):
                for p in n.pitches:
                    all_notes.append((float(n.offset), p.midi % 12))

    all_notes.sort(key=lambda x: x[0])

    if len(all_notes) < window_size * 2:
        return {
            'num_modulations': 0,
            'modulations': [],
            'starting_key': None,
            'ending_key': None,
            'error': 'Insufficient notes for modulation detection'
        }

    # Analyze pitch class distribution in sliding windows
    windows = []
    for i in range(0, len(all_notes) - window_size + 1, window_size // 2):
        window_notes = all_notes[i:i + window_size]
        pitch_classes = [pc for _, pc in window_notes]

        # Count pitch class distribution
        pc_counts = {pc: pitch_classes.count(pc) for pc in set(pitch_classes)}

        # Simple key estimation: most common pitch class might be tonic
        dominant_pc = max(pc_counts.items(), key=lambda x: x[1])[0]

        windows.append({
            'start_offset': window_notes[0][0],
            'end_offset': window_notes[-1][0],
            'dominant_pitch_class': dominant_pc,
            'distribution': pc_counts
        })

    # Detect changes in dominant pitch class
    modulations = []
    for i in range(len(windows) - 1):
        if windows[i]['dominant_pitch_class'] != windows[i + 1]['dominant_pitch_class']:
            modulations.append({
                'offset': windows[i + 1]['start_offset'],
                'from_tonic': windows[i]['dominant_pitch_class'],
                'to_tonic': windows[i + 1]['dominant_pitch_class']
            })

    return {
        'num_modulations': len(modulations),
        'modulations': modulations,
        'starting_key': windows[0]['dominant_pitch_class'] if windows else None,
        'ending_key': windows[-1]['dominant_pitch_class'] if windows else None,
        'windows_analyzed': len(windows),
        'window_size': window_size
    }


def species_counterpoint_check(score: stream.Score, species: int = 1) -> Dict[str, any]:
    """
    Check compliance with species counterpoint rules.

    Validates two-voice counterpoint according to Fux's species rules:
    - First species: note-against-note
    - Second species: two-against-one
    - Third species: four-against-one

    Args:
        score: A Score with two voices to check
        species: Species number (1, 2, or 3) - default: 1

    Returns:
        Dictionary with compliance results and rule violations

    Examples:
        >>> results = species_counterpoint_check(score, species=1)
        >>> print(f"Rule violations: {results['total_violations']}")
        >>> print(f"Compliance: {results['compliance_rate']:.1%}")
    """
    parts = list(score.parts)

    if len(parts) != 2:
        return {
            'error': 'Species counterpoint requires exactly 2 voices',
            'num_voices': len(parts)
        }

    if species not in [1, 2, 3]:
        return {'error': f'Invalid species: {species}. Must be 1, 2, or 3'}

    # Extract notes
    cantus_notes = [(float(n.offset), n, n.quarterLength) for n in parts[1].flatten().notes]
    counterpoint_notes = [(float(n.offset), n, n.quarterLength) for n in parts[0].flatten().notes]

    cantus_notes.sort(key=lambda x: x[0])
    counterpoint_notes.sort(key=lambda x: x[0])

    violations = {
        'parallel_perfect': [],
        'bad_intervals': [],
        'bad_opening': [],
        'bad_closing': [],
        'large_leaps': [],
        'unresolved_leaps': [],
        'rhythm_violations': []
    }

    # First species rules
    if species == 1:
        # Check note-against-note rhythm
        if len(cantus_notes) != len(counterpoint_notes):
            violations['rhythm_violations'].append({
                'rule': 'First species requires equal number of notes',
                'cantus_count': len(cantus_notes),
                'counterpoint_count': len(counterpoint_notes)
            })

        # Check opening (should be perfect consonance: unison, fifth, or octave)
        if cantus_notes and counterpoint_notes:
            if all(isinstance(n[1], note.Note) for n in [cantus_notes[0], counterpoint_notes[0]]):
                opening_interval = abs(cantus_notes[0][1].pitch.midi - counterpoint_notes[0][1].pitch.midi) % 12
                if opening_interval not in [0, 7]:
                    violations['bad_opening'].append({
                        'rule': 'Must begin with perfect consonance',
                        'interval': opening_interval
                    })

            # Check closing (should be octave or unison)
            if all(isinstance(n[1], note.Note) for n in [cantus_notes[-1], counterpoint_notes[-1]]):
                closing_interval = abs(cantus_notes[-1][1].pitch.midi - counterpoint_notes[-1][1].pitch.midi) % 12
                if closing_interval != 0:
                    violations['bad_closing'].append({
                        'rule': 'Must end with unison or octave',
                        'interval': closing_interval
                    })

    # Check intervals (all species)
    for i in range(min(len(cantus_notes), len(counterpoint_notes))):
        cantus_note = cantus_notes[i][1]
        cp_note = counterpoint_notes[i][1]

        if isinstance(cantus_note, note.Note) and isinstance(cp_note, note.Note):
            interval = abs(cantus_note.pitch.midi - cp_note.pitch.midi) % 12

            # Dissonances (2nds, 7ths, tritones) are generally forbidden (except passing tones in higher species)
            if species == 1 and interval in [1, 2, 6, 10, 11]:
                violations['bad_intervals'].append({
                    'location': i,
                    'offset': cantus_notes[i][0],
                    'interval': interval,
                    'rule': 'Dissonance in first species'
                })

    # Check parallel perfect intervals (all species)
    for i in range(min(len(cantus_notes), len(counterpoint_notes)) - 1):
        if all(isinstance(cantus_notes[j][1], note.Note) and isinstance(counterpoint_notes[j][1], note.Note)
               for j in [i, i + 1]):
            interval1 = abs(cantus_notes[i][1].pitch.midi - counterpoint_notes[i][1].pitch.midi) % 12
            interval2 = abs(cantus_notes[i + 1][1].pitch.midi - counterpoint_notes[i + 1][1].pitch.midi) % 12

            # Parallel fifths or octaves
            if interval1 in [0, 7] and interval1 == interval2:
                violations['parallel_perfect'].append({
                    'location': i,
                    'offset': cantus_notes[i][0],
                    'interval': interval1
                })

    # Check melodic intervals in counterpoint (all species)
    for i in range(len(counterpoint_notes) - 1):
        if all(isinstance(counterpoint_notes[j][1], note.Note) for j in [i, i + 1]):
            leap = abs(counterpoint_notes[i + 1][1].pitch.midi - counterpoint_notes[i][1].pitch.midi)

            # Leaps larger than octave forbidden
            if leap > 12:
                violations['large_leaps'].append({
                    'location': i,
                    'offset': counterpoint_notes[i][0],
                    'leap': leap
                })
            # Leaps larger than third should be followed by stepwise motion in opposite direction
            elif leap > 4:
                if i + 2 < len(counterpoint_notes) and isinstance(counterpoint_notes[i + 2][1], note.Note):
                    motion1 = counterpoint_notes[i + 1][1].pitch.midi - counterpoint_notes[i][1].pitch.midi
                    motion2 = counterpoint_notes[i + 2][1].pitch.midi - counterpoint_notes[i + 1][1].pitch.midi

                    # Check if resolved by step in opposite direction
                    if not (abs(motion2) <= 2 and motion1 * motion2 < 0):
                        violations['unresolved_leaps'].append({
                            'location': i,
                            'offset': counterpoint_notes[i][0],
                            'leap': leap
                        })

    # Calculate compliance
    total_violations = sum(len(v) for v in violations.values())
    total_checks = (len(cantus_notes) + len(counterpoint_notes) +
                   min(len(cantus_notes), len(counterpoint_notes)))

    compliance_rate = 1.0 - (total_violations / total_checks) if total_checks > 0 else 0.0
    compliance_rate = max(0.0, compliance_rate)

    return {
        'species': species,
        'violations': violations,
        'total_violations': total_violations,
        'compliance_rate': compliance_rate,
        'passed': compliance_rate > 0.8,
        'grade': _get_quality_grade(compliance_rate),
        'cantus_notes': len(cantus_notes),
        'counterpoint_notes': len(counterpoint_notes)
    }


def _get_quality_grade(score: float) -> str:
    """Convert quality score (0-1) to letter grade."""
    if score >= 0.97:
        return 'A+'
    elif score >= 0.93:
        return 'A'
    elif score >= 0.90:
        return 'A-'
    elif score >= 0.87:
        return 'B+'
    elif score >= 0.83:
        return 'B'
    elif score >= 0.80:
        return 'B-'
    elif score >= 0.77:
        return 'C+'
    elif score >= 0.73:
        return 'C'
    elif score >= 0.70:
        return 'C-'
    elif score >= 0.67:
        return 'D+'
    elif score >= 0.63:
        return 'D'
    elif score >= 0.60:
        return 'D-'
    else:
        return 'F'


# ============================================================================
# Phase 9: Advanced Canon Types
# ============================================================================


def table_canon(
    theme: stream.Stream,
    num_voices: int = 4,
    axis_pitch: Union[str, m21.pitch.Pitch] = 'C4'
) -> stream.Score:
    """
    Create a table canon where each voice reads the same music rotated/transformed.

    A table canon (also called "canon per tonos" or "crab canon on a table") allows
    multiple performers to read the same notation from different orientations:
    - Voice 1: Normal (0°)
    - Voice 2: Inverted (pitch inversion)
    - Voice 3: Retrograde (180° rotation)
    - Voice 4: Retrograde inversion (180° + pitch inversion)

    This creates a four-way symmetry where all voices can be read from a single
    page placed on a table.

    Args:
        theme: The base musical theme
        num_voices: Number of voices (2 or 4, default 4)
        axis_pitch: Pitch axis for inversion (default C4)

    Returns:
        A Score with 2 or 4 voices in table canon arrangement

    Example:
        >>> from cancrizans import table_canon
        >>> from music21 import stream, note
        >>> theme = stream.Stream()
        >>> theme.append(note.Note('C4', quarterLength=1.0))
        >>> theme.append(note.Note('E4', quarterLength=1.0))
        >>> theme.append(note.Note('G4', quarterLength=1.0))
        >>> canon = table_canon(theme, num_voices=4)
        >>> len(canon.parts)
        4
    """
    if num_voices not in [2, 4]:
        raise ValueError("num_voices must be 2 or 4")

    score = stream.Score()

    # Voice 1: Normal (original theme)
    voice1 = stream.Part()
    voice1.id = 'voice1_normal'
    for el in theme.flatten().notesAndRests:
        voice1.insert(el.offset, el)
    score.append(voice1)

    if num_voices >= 2:
        # Voice 2: Inversion
        voice2 = stream.Part()
        voice2.id = 'voice2_inversion'
        inverted = invert(theme, axis_pitch)
        for el in inverted.flatten().notesAndRests:
            voice2.insert(el.offset, el)
        score.append(voice2)

    if num_voices >= 4:
        # Voice 3: Retrograde
        voice3 = stream.Part()
        voice3.id = 'voice3_retrograde'
        retro = retrograde(theme)
        for el in retro.flatten().notesAndRests:
            voice3.insert(el.offset, el)
        score.append(voice3)

        # Voice 4: Retrograde + Inversion
        voice4 = stream.Part()
        voice4.id = 'voice4_retro_inversion'
        retro_inv = invert(retrograde(theme), axis_pitch)
        for el in retro_inv.flatten().notesAndRests:
            voice4.insert(el.offset, el)
        score.append(voice4)

    return score


def mensuration_canon(
    theme: stream.Stream,
    ratios: List[float] = [1.0, 2.0],
    offset_quarters: float = 0.0
) -> stream.Score:
    """
    Create a mensuration canon where voices play the same melody at different speeds.

    A mensuration canon (also called "prolation canon") has multiple voices singing
    the same melody simultaneously but at different tempi. This was common in
    Renaissance music, where different mensuration signs indicated different speeds.

    Args:
        theme: The base musical theme
        ratios: List of speed ratios (1.0 = original speed, 2.0 = twice as slow, etc.)
        offset_quarters: Temporal offset between voice entrances in quarter notes

    Returns:
        A Score with voices at different speeds

    Example:
        >>> from cancrizans import mensuration_canon
        >>> from music21 import stream, note
        >>> theme = stream.Stream()
        >>> for pitch in ['C4', 'D4', 'E4', 'F4']:
        ...     theme.append(note.Note(pitch, quarterLength=1.0))
        >>> canon = mensuration_canon(theme, ratios=[1.0, 2.0, 4.0])
        >>> len(canon.parts)
        3
    """
    score = stream.Score()

    for i, ratio in enumerate(ratios):
        part = stream.Part()
        part.id = f'voice{i+1}_ratio_{ratio}'

        # Apply augmentation (ratio > 1.0 makes it slower)
        if ratio != 1.0:
            transformed = augmentation(theme, ratio)
        else:
            # Create a copy even if ratio is 1.0 to avoid sharing note objects
            transformed = stream.Stream()
            for el in theme.flatten().notesAndRests:
                new_el = el.__class__()
                new_el.quarterLength = el.quarterLength
                if isinstance(el, note.Note):
                    new_el.pitch = el.pitch
                elif isinstance(el, chord.Chord):
                    new_el.pitches = el.pitches
                transformed.insert(el.offset, new_el)

        # Add with offset
        # Voice 0 at 0, voice 1 at offset_quarters, voice 2 at 2*offset_quarters, etc.
        current_offset = i * offset_quarters
        for el in transformed.flatten().notesAndRests:
            part.insert(el.offset + current_offset, el)

        score.append(part)

    return score


def spiral_canon(
    theme: stream.Stream,
    num_iterations: int = 4,
    transposition_interval: int = 2,
    mode: str = 'ascending'
) -> stream.Score:
    """
    Create a spiral (modulating) canon that transposes with each iteration.

    A spiral canon repeatedly transposes the theme, creating a modulating effect
    that "spirals" upward or downward through different keys. This was used by
    Bach in some of the canons from The Musical Offering.

    Args:
        theme: The base musical theme
        num_iterations: Number of times to repeat and transpose
        transposition_interval: Semitones to transpose each iteration (default 2 = whole step)
        mode: 'ascending' or 'descending' (direction of transposition)

    Returns:
        A Score with the spiraling canon

    Example:
        >>> from cancrizans import spiral_canon
        >>> from music21 import stream, note
        >>> theme = stream.Stream()
        >>> theme.append(note.Note('C4', quarterLength=1.0))
        >>> theme.append(note.Note('E4', quarterLength=1.0))
        >>> canon = spiral_canon(theme, num_iterations=3, transposition_interval=2)
        >>> len(canon.parts[0].flatten().notes)
        6
    """
    if mode not in ['ascending', 'descending']:
        raise ValueError("mode must be 'ascending' or 'descending'")

    score = stream.Score()
    part = stream.Part()
    part.id = 'spiral_canon'

    theme_duration = theme.duration.quarterLength

    for i in range(num_iterations):
        # Calculate transposition for this iteration
        if mode == 'ascending':
            semitones = i * transposition_interval
        else:
            semitones = -i * transposition_interval

        # Transpose the theme using music21's built-in method
        if semitones != 0:
            # Use music21's transpose method
            transposed = stream.Stream()
            for el in theme.flatten().notesAndRests:
                new_el = el.__class__()
                new_el.quarterLength = el.quarterLength

                if isinstance(el, note.Note):
                    new_el.pitch = el.pitch.transpose(semitones)
                elif isinstance(el, chord.Chord):
                    new_el.pitches = [p.transpose(semitones) for p in el.pitches]
                # Rests don't need pitch transposition

                transposed.insert(el.offset, new_el)
        else:
            transposed = theme

        # Add to the part at the appropriate offset
        offset = i * theme_duration
        for el in transposed.flatten().notesAndRests:
            part.insert(el.offset + offset, el)

    score.append(part)
    return score


def solve_puzzle_canon(
    given_voice: stream.Stream,
    canon_type: str = 'retrograde',
    axis_pitch: Union[str, m21.pitch.Pitch] = 'C4',
    offset_quarters: float = 0.0
) -> stream.Score:
    """
    Solve a puzzle canon by deriving the missing voice(s) from a given voice.

    Given one voice of a canon, this function generates the complementary voice(s)
    based on the specified canon type. This is useful for "puzzle canons" where
    performers must deduce how to read the notation.

    Args:
        given_voice: The known voice
        canon_type: Type of canon to solve:
            - 'retrograde': Crab canon (time reversal)
            - 'inversion': Mirror canon (pitch inversion)
            - 'retro_inversion': Combined retrograde + inversion
            - 'augmentation': Mensuration canon at 2:1 ratio
        axis_pitch: Pitch axis for inversion types (default C4)
        offset_quarters: Temporal offset for the derived voice

    Returns:
        A Score with both the given voice and the solved voice

    Example:
        >>> from cancrizans import solve_puzzle_canon
        >>> from music21 import stream, note
        >>> voice = stream.Stream()
        >>> voice.append(note.Note('C4', quarterLength=1.0))
        >>> voice.append(note.Note('D4', quarterLength=1.0))
        >>> canon = solve_puzzle_canon(voice, canon_type='retrograde')
        >>> len(canon.parts)
        2
    """
    valid_types = ['retrograde', 'inversion', 'retro_inversion', 'augmentation']
    if canon_type not in valid_types:
        raise ValueError(f"canon_type must be one of {valid_types}")

    score = stream.Score()

    # Add the given voice
    voice1 = stream.Part()
    voice1.id = 'given_voice'
    for el in given_voice.flatten().notesAndRests:
        voice1.insert(el.offset, el)
    score.append(voice1)

    # Solve for the complementary voice
    voice2 = stream.Part()
    voice2.id = f'solved_{canon_type}'

    if canon_type == 'retrograde':
        solved = retrograde(given_voice)
    elif canon_type == 'inversion':
        solved = invert(given_voice, axis_pitch)
    elif canon_type == 'retro_inversion':
        solved = invert(retrograde(given_voice), axis_pitch)
    elif canon_type == 'augmentation':
        solved = augmentation(given_voice, 2.0)

    # Add with offset
    for el in solved.flatten().notesAndRests:
        voice2.insert(el.offset + offset_quarters, el)

    score.append(voice2)
    return score


# ============================================================================
# Phase 11: Harmonic Enhancement
# ============================================================================


def analyze_chord_progressions(
    score: stream.Score,
    key_sig: Optional[Union[str, m21.key.Key]] = None
) -> Dict[str, any]:
    """
    Analyze chord progressions in a score.

    Identifies chords at each time point and analyzes the progression.
    Uses music21's chord detection and analysis capabilities.

    Args:
        score: The score to analyze
        key_sig: The key signature (detected automatically if not provided)

    Returns:
        Dictionary containing:
        - 'chords': List of detected chords with offsets
        - 'progressions': Common progression patterns detected
        - 'key': Detected or specified key
        - 'num_chords': Total number of chords
        - 'unique_chords': Number of unique chord types

    Example:
        >>> from cancrizans import analyze_chord_progressions
        >>> from music21 import stream, note
        >>> score = stream.Score()
        >>> # Add C major triad
        >>> part1, part2, part3 = stream.Part(), stream.Part(), stream.Part()
        >>> part1.append(note.Note('C4', quarterLength=1.0))
        >>> part2.append(note.Note('E4', quarterLength=1.0))
        >>> part3.append(note.Note('G4', quarterLength=1.0))
        >>> score.append(part1)
        >>> score.append(part2)
        >>> score.append(part3)
        >>> result = analyze_chord_progressions(score)
        >>> result['num_chords'] >= 1
        True
    """
    # Detect key if not provided
    if key_sig is None:
        try:
            key_sig = score.analyze('key')
        except:
            # Default to C major if key detection fails
            key_sig = m21.key.Key('C')
    elif isinstance(key_sig, str):
        key_sig = m21.key.Key(key_sig)

    # Use music21's chordify to get vertical slices
    try:
        chordified = score.chordify()
    except:
        return {
            'error': 'Could not chordify score',
            'chords': [],
            'progressions': [],
            'key': str(key_sig),
            'num_chords': 0,
            'unique_chords': 0
        }

    # Extract chords
    chords_list = []
    for element in chordified.flatten():
        if isinstance(element, chord.Chord):
            chord_data = {
                'offset': float(element.offset),
                'duration': float(element.quarterLength),
                'pitches': [p.nameWithOctave for p in element.pitches],
                'root': element.root().name if element.root() else None,
                'bass': element.bass().name if element.bass() else None,
                'quality': element.quality if hasattr(element, 'quality') else 'unknown'
            }

            # Try to get Roman numeral in the key
            try:
                rn = m21.roman.romanNumeralFromChord(element, key_sig)
                chord_data['roman_numeral'] = str(rn.figure)
            except:
                chord_data['roman_numeral'] = None

            chords_list.append(chord_data)

    # Identify common progressions
    progressions = []
    roman_numerals = [c.get('roman_numeral') for c in chords_list if c.get('roman_numeral')]

    # Check for common patterns
    common_patterns = {
        'authentic_cadence': ['V', 'I'],
        'plagal_cadence': ['IV', 'I'],
        'half_cadence': ['I', 'V'],
        'deceptive_cadence': ['V', 'vi'],
        'circle_of_fifths': ['ii', 'V', 'I'],
        'extended_circle': ['vi', 'ii', 'V', 'I'],
        'four_five_one': ['IV', 'V', 'I'],
    }

    for pattern_name, pattern in common_patterns.items():
        # Look for pattern in the progression
        pattern_len = len(pattern)
        for i in range(len(roman_numerals) - pattern_len + 1):
            segment = roman_numerals[i:i + pattern_len]
            # Normalize for comparison (remove inversions)
            normalized_segment = [rn.split('/')[0] for rn in segment if rn]
            normalized_pattern = [p.split('/')[0] for p in pattern]

            if normalized_segment == normalized_pattern:
                progressions.append({
                    'type': pattern_name,
                    'location': i,
                    'chords': segment
                })

    # Count unique chords
    unique_chord_types = set()
    for c in chords_list:
        if c.get('roman_numeral'):
            unique_chord_types.add(c['roman_numeral'].split('/')[0])

    return {
        'chords': chords_list,
        'progressions': progressions,
        'key': str(key_sig),
        'num_chords': len(chords_list),
        'unique_chords': len(unique_chord_types),
        'roman_numerals': roman_numerals
    }


def functional_harmony_analysis(
    score: stream.Score,
    key_sig: Optional[Union[str, m21.key.Key]] = None
) -> Dict[str, any]:
    """
    Analyze functional harmony (tonic, dominant, subdominant relationships).

    Classifies chords by their function in the key and analyzes harmonic rhythm.

    Args:
        score: The score to analyze
        key_sig: The key signature (detected automatically if not provided)

    Returns:
        Dictionary containing:
        - 'functions': List of harmonic functions for each chord
        - 'harmonic_rhythm': Analysis of how often harmonies change
        - 'tonic_percentage': Percentage of time spent on tonic
        - 'dominant_percentage': Percentage on dominant
        - 'subdominant_percentage': Percentage on subdominant
        - 'key': The key being analyzed

    Example:
        >>> from cancrizans import functional_harmony_analysis
        >>> from music21 import stream, note, key
        >>> score = stream.Score()
        >>> part = stream.Part()
        >>> part.append(note.Note('C4', quarterLength=1.0))
        >>> score.append(part)
        >>> result = functional_harmony_analysis(score, 'C')
        >>> 'functions' in result
        True
    """
    # First get chord progressions
    chord_analysis = analyze_chord_progressions(score, key_sig)

    if 'error' in chord_analysis:
        return chord_analysis

    key_str = chord_analysis['key']
    chords_list = chord_analysis['chords']

    # Classify functions
    functions = []
    tonic_duration = 0.0
    dominant_duration = 0.0
    subdominant_duration = 0.0
    other_duration = 0.0

    for chord_data in chords_list:
        rn = chord_data.get('roman_numeral', '')
        duration = chord_data.get('duration', 0.0)

        # Remove inversion notation
        base_rn = rn.split('/')[0] if rn else ''

        # Classify function
        function = 'other'
        if base_rn in ['I', 'i', 'vi', 'VI']:
            function = 'tonic'
            tonic_duration += duration
        elif base_rn in ['V', 'v', 'VII', 'vii', 'viio']:
            function = 'dominant'
            dominant_duration += duration
        elif base_rn in ['IV', 'iv', 'ii', 'II']:
            function = 'subdominant'
            subdominant_duration += duration
        else:
            other_duration += duration

        functions.append({
            'offset': chord_data['offset'],
            'roman_numeral': rn,
            'function': function,
            'duration': duration
        })

    # Calculate percentages
    total_duration = tonic_duration + dominant_duration + subdominant_duration + other_duration

    tonic_pct = (tonic_duration / total_duration * 100) if total_duration > 0 else 0
    dominant_pct = (dominant_duration / total_duration * 100) if total_duration > 0 else 0
    subdominant_pct = (subdominant_duration / total_duration * 100) if total_duration > 0 else 0

    # Analyze harmonic rhythm (how often chords change)
    if len(chords_list) > 1:
        changes = []
        for i in range(1, len(chords_list)):
            time_diff = chords_list[i]['offset'] - chords_list[i-1]['offset']
            changes.append(time_diff)

        avg_harmonic_rhythm = sum(changes) / len(changes) if changes else 0
        min_change = min(changes) if changes else 0
        max_change = max(changes) if changes else 0
    else:
        avg_harmonic_rhythm = 0
        min_change = 0
        max_change = 0

    return {
        'functions': functions,
        'harmonic_rhythm': {
            'average': avg_harmonic_rhythm,
            'min': min_change,
            'max': max_change
        },
        'tonic_percentage': tonic_pct,
        'dominant_percentage': dominant_pct,
        'subdominant_percentage': subdominant_pct,
        'other_percentage': (other_duration / total_duration * 100) if total_duration > 0 else 0,
        'key': key_str,
        'num_functions': len(functions)
    }


def analyze_nonchord_tones(
    score: stream.Score,
    key_sig: Optional[Union[str, m21.key.Key]] = None
) -> Dict[str, any]:
    """
    Analyze non-chord tones (passing tones, neighbor tones, suspensions, etc.).

    Identifies notes that are not part of the prevailing harmony and classifies
    their type based on melodic motion and metric position.

    Args:
        score: The score to analyze
        key_sig: The key signature (detected automatically if not provided)

    Returns:
        Dictionary containing:
        - 'nonchord_tones': List of identified non-chord tones with types
        - 'summary': Count of each type
        - 'total_notes': Total number of notes analyzed
        - 'nonchord_percentage': Percentage of notes that are non-chord tones

    Types identified:
    - 'passing': Passing tone (stepwise approach and departure)
    - 'neighbor': Neighbor tone (stepwise approach and return)
    - 'suspension': Suspension (prepared, held over, resolved down)
    - 'anticipation': Anticipation (jumps to next chord tone early)
    - 'escape': Escape tone (stepwise approach, leap away)
    - 'appoggiatura': Appoggiatura (leap to, stepwise resolution)
    - 'other': Cannot classify

    Example:
        >>> from cancrizans import analyze_nonchord_tones
        >>> from music21 import stream, note
        >>> score = stream.Score()
        >>> part = stream.Part()
        >>> part.append(note.Note('C4', quarterLength=1.0))
        >>> part.append(note.Note('D4', quarterLength=1.0))
        >>> part.append(note.Note('E4', quarterLength=1.0))
        >>> score.append(part)
        >>> result = analyze_nonchord_tones(score)
        >>> 'nonchord_tones' in result
        True
    """
    # Get chord analysis
    chord_analysis = analyze_chord_progressions(score, key_sig)

    if 'error' in chord_analysis:
        return chord_analysis

    chords_list = chord_analysis['chords']

    # Get all notes from all parts
    all_notes = []
    for part in score.parts:
        for n in part.flatten().notes:
            if isinstance(n, note.Note):
                all_notes.append({
                    'offset': float(n.offset),
                    'pitch': n.pitch.midi,
                    'pitch_name': n.pitch.name,
                    'duration': float(n.quarterLength)
                })

    # Sort notes by offset
    all_notes.sort(key=lambda x: x['offset'])

    nonchord_tones = []
    summary = {
        'passing': 0,
        'neighbor': 0,
        'suspension': 0,
        'anticipation': 0,
        'escape': 0,
        'appoggiatura': 0,
        'other': 0
    }

    # For each note, check if it's in the current chord
    for i, note_data in enumerate(all_notes):
        note_offset = note_data['offset']
        note_name = note_data['pitch_name']

        # Find the chord active at this offset
        current_chord = None
        for chord_data in chords_list:
            if chord_data['offset'] <= note_offset < chord_data['offset'] + chord_data['duration']:
                current_chord = chord_data
                break

        if current_chord is None:
            continue

        # Check if note is in the chord
        chord_pitch_names = [p.rstrip('0123456789') for p in current_chord['pitches']]  # Remove octave

        if note_name not in chord_pitch_names:
            # This is a non-chord tone - classify it
            nct_type = 'other'

            # Get previous and next notes if they exist
            prev_note = all_notes[i-1] if i > 0 else None
            next_note = all_notes[i+1] if i < len(all_notes) - 1 else None

            if prev_note and next_note:
                # Calculate intervals
                prev_interval = note_data['pitch'] - prev_note['pitch']
                next_interval = next_note['pitch'] - note_data['pitch']

                # Passing tone: stepwise in same direction
                if abs(prev_interval) <= 2 and abs(next_interval) <= 2:
                    if (prev_interval > 0 and next_interval > 0) or (prev_interval < 0 and next_interval < 0):
                        nct_type = 'passing'
                    # Neighbor tone: stepwise approach and return
                    elif prev_interval * next_interval < 0 and abs(prev_interval) == abs(next_interval):
                        nct_type = 'neighbor'

                # Escape tone: stepwise approach, leap away
                if abs(prev_interval) <= 2 and abs(next_interval) > 2:
                    nct_type = 'escape'

                # Appoggiatura: leap to, stepwise away
                if abs(prev_interval) > 2 and abs(next_interval) <= 2:
                    nct_type = 'appoggiatura'

                # Suspension: prepared (same pitch before), resolved down by step
                if prev_interval == 0 and next_interval == -1:
                    nct_type = 'suspension'

                # Anticipation: resolved by staying on same pitch
                if next_interval == 0:
                    nct_type = 'anticipation'

            nonchord_tones.append({
                'offset': note_offset,
                'pitch': note_data['pitch'],
                'pitch_name': note_name,
                'type': nct_type,
                'chord': current_chord.get('roman_numeral', 'unknown')
            })

            summary[nct_type] += 1

    total_notes = len(all_notes)
    num_nonchord = len(nonchord_tones)
    nonchord_pct = (num_nonchord / total_notes * 100) if total_notes > 0 else 0

    return {
        'nonchord_tones': nonchord_tones,
        'summary': summary,
        'total_notes': total_notes,
        'total_nonchord_tones': num_nonchord,
        'nonchord_percentage': nonchord_pct
    }


def generate_figured_bass(
    score: stream.Score,
    key_sig: Optional[Union[str, m21.key.Key]] = None
) -> Dict[str, any]:
    """
    Generate figured bass notation from a score.

    Analyzes the harmonic structure and generates figured bass symbols
    that would be written below the bass line in baroque notation.

    Args:
        score: The score to analyze
        key_sig: The key signature (detected automatically if not provided)

    Returns:
        Dictionary containing:
        - 'figures': List of figured bass symbols with offsets
        - 'bass_line': The bass line notes
        - 'key': The key being analyzed

    Figured bass symbols:
    - '': Root position triad (assumed, often not notated)
    - '6': First inversion triad
    - '6/4' or '64': Second inversion triad
    - '7': Root position seventh chord
    - '6/5' or '65': First inversion seventh
    - '4/3' or '43': Second inversion seventh
    - '4/2' or '42' or '2': Third inversion seventh
    - '#', 'b', natural sign: Chromatic alterations

    Example:
        >>> from cancrizans import generate_figured_bass
        >>> from music21 import stream, note
        >>> score = stream.Score()
        >>> bass = stream.Part()
        >>> bass.append(note.Note('C3', quarterLength=1.0))
        >>> upper = stream.Part()
        >>> upper.append(note.Note('E4', quarterLength=1.0))
        >>> score.append(bass)
        >>> score.append(upper)
        >>> result = generate_figured_bass(score)
        >>> 'figures' in result
        True
    """
    # Get chord analysis
    chord_analysis = analyze_chord_progressions(score, key_sig)

    if 'error' in chord_analysis:
        return chord_analysis

    chords_list = chord_analysis['chords']

    # Extract bass line (lowest part)
    if len(score.parts) == 0:
        return {
            'error': 'No parts in score',
            'figures': [],
            'bass_line': [],
            'key': str(key_sig) if key_sig else 'C'
        }

    bass_part = score.parts[-1]  # Assume lowest part is bass
    bass_notes = []
    for n in bass_part.flatten().notes:
        if isinstance(n, note.Note):
            bass_notes.append({
                'offset': float(n.offset),
                'pitch': n.pitch.nameWithOctave,
                'duration': float(n.quarterLength)
            })

    # Generate figured bass symbols
    figures = []

    for chord_data in chords_list:
        bass_note = chord_data.get('bass')
        root_note = chord_data.get('root')

        if not bass_note or not root_note:
            continue

        # Determine inversion
        figure = ''

        # Count chord members
        num_pitches = len(chord_data['pitches'])

        # Simple logic for triads and seventh chords
        if bass_note == root_note:
            # Root position
            if num_pitches >= 4:
                figure = '7'  # Seventh chord
            else:
                figure = ''  # Root position triad (often omitted)
        else:
            # Inverted
            try:
                # Find which chord member is in bass
                pitch_classes = [m21.pitch.Pitch(p).pitchClass for p in chord_data['pitches']]
                bass_pc = m21.pitch.Pitch(bass_note).pitchClass
                root_pc = m21.pitch.Pitch(root_note).pitchClass

                # Calculate position
                if num_pitches >= 4:
                    # Seventh chord inversions
                    if bass_pc == root_pc:
                        figure = '7'
                    else:
                        # Count up from bass to determine inversion
                        sorted_pcs = sorted(set(pitch_classes))
                        bass_pos = sorted_pcs.index(bass_pc)

                        if bass_pos == 1:
                            figure = '6/5'
                        elif bass_pos == 2:
                            figure = '4/3'
                        elif bass_pos == 3:
                            figure = '4/2'
                else:
                    # Triad inversions
                    sorted_pcs = sorted(set(pitch_classes))
                    bass_pos = sorted_pcs.index(bass_pc)

                    if bass_pos == 1:
                        figure = '6'
                    elif bass_pos == 2:
                        figure = '6/4'
            except:
                figure = '?'

        figures.append({
            'offset': chord_data['offset'],
            'figure': figure,
            'bass_note': bass_note,
            'roman_numeral': chord_data.get('roman_numeral'),
            'duration': chord_data['duration']
        })

    return {
        'figures': figures,
        'bass_line': bass_notes,
        'key': chord_analysis['key'],
        'num_figures': len(figures)
    }

