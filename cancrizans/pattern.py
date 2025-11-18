"""
Advanced pattern analysis for musical sequences and canons.

This module provides sophisticated pattern detection, motif tracking,
and thematic development analysis capabilities.
"""

from dataclasses import dataclass
from typing import Any

import numpy as np
from music21 import note, stream


@dataclass
class Motif:
    """Represents a musical motif with its properties."""
    pitches: list[int]  # MIDI pitch numbers
    rhythms: list[float]  # Durations in quarter notes
    intervals: list[int]  # Intervallic content in semitones
    offset: float  # Position in the score
    length: float  # Total duration
    occurrences: list[float]  # List of offsets where this motif appears

    def __hash__(self):
        return hash((tuple(self.intervals), tuple(self.rhythms)))

    def __eq__(self, other):
        if not isinstance(other, Motif):
            return False
        return (self.intervals == other.intervals and
                self.rhythms == other.rhythms)


@dataclass
class PatternMatch:
    """Represents a pattern match in the score."""
    pattern_id: int
    offset: float
    transposition: int  # Semitones of transposition
    similarity: float  # 0.0-1.0 similarity score
    match_type: str  # 'exact', 'transposed', 'rhythmic', 'contour'


def detect_motifs(
    score_or_stream: stream.Stream,
    min_length: int = 3,
    max_length: int = 8,
    min_occurrences: int = 2,
    fuzzy_match: bool = True
) -> list[Motif]:
    """
    Detect recurring melodic and rhythmic motifs in a musical stream.

    Uses sliding window analysis to find patterns that repeat throughout
    the piece, with optional fuzzy matching for transposed or slightly
    varied repetitions.

    Args:
        score_or_stream: Musical score or stream to analyze
        min_length: Minimum number of notes in a motif (default: 3)
        max_length: Maximum number of notes in a motif (default: 8)
        min_occurrences: Minimum times a pattern must appear (default: 2)
        fuzzy_match: Allow transposed/varied matches (default: True)

    Returns:
        List of Motif objects found in the score

    Example:
        >>> from cancrizans.pattern import detect_motifs
        >>> motifs = detect_motifs(my_score, min_length=4, min_occurrences=3)
        >>> print(f"Found {len(motifs)} recurring motifs")
    """
    # Extract notes from the stream
    notes_list = []
    if isinstance(score_or_stream, stream.Score):
        for part in score_or_stream.parts:
            notes_list.extend([(n.offset, n) for n in part.flatten().notes])
    else:
        notes_list = [(n.offset, n) for n in score_or_stream.flatten().notes]

    notes_list.sort(key=lambda x: x[0])

    if len(notes_list) < min_length:
        return []

    # Extract pitch and rhythm sequences
    pitches = []
    rhythms = []
    offsets = []

    for offset, n in notes_list:
        if isinstance(n, note.Note):
            pitches.append(n.pitch.midi)
            rhythms.append(n.quarterLength)
            offsets.append(offset)
        elif isinstance(n, note.Rest):
            pitches.append(-1)  # Use -1 for rests
            rhythms.append(n.quarterLength)
            offsets.append(offset)

    # Find patterns using sliding window
    pattern_candidates: dict[tuple, list[float]] = {}

    for length in range(min_length, min(max_length + 1, len(pitches))):
        for i in range(len(pitches) - length + 1):
            # Extract intervallic pattern (transposition-independent)
            interval_pattern = []
            for j in range(i, i + length - 1):
                if pitches[j] != -1 and pitches[j + 1] != -1:
                    interval_pattern.append(pitches[j + 1] - pitches[j])
                else:
                    interval_pattern.append(0)  # Rest or continuation

            rhythm_pattern = tuple(rhythms[i:i + length])
            pattern_key = (tuple(interval_pattern), rhythm_pattern)

            if pattern_key not in pattern_candidates:
                pattern_candidates[pattern_key] = []
            pattern_candidates[pattern_key].append(offsets[i])

    # Filter patterns by minimum occurrences
    motifs = []
    for (intervals, rhythm_pattern), occurrence_list in pattern_candidates.items():
        if len(occurrence_list) >= min_occurrences:
            # Reconstruct a representative pitch sequence
            # (we'll use the first occurrence)
            first_offset = occurrence_list[0]
            idx = offsets.index(first_offset)
            pattern_length = len(rhythm_pattern)

            pattern_pitches = pitches[idx:idx + pattern_length]
            pattern_rhythms = list(rhythm_pattern)
            total_duration = sum(pattern_rhythms)

            motif = Motif(
                pitches=pattern_pitches,
                rhythms=pattern_rhythms,
                intervals=list(intervals),
                offset=first_offset,
                length=total_duration,
                occurrences=occurrence_list
            )
            motifs.append(motif)

    # Sort by number of occurrences (most frequent first)
    motifs.sort(key=lambda m: len(m.occurrences), reverse=True)

    return motifs


def identify_melodic_sequences(
    score_or_stream: stream.Stream,
    min_repetitions: int = 2,
    max_transposition: int = 12
) -> list[dict[str, Any]]:
    """
    Identify melodic sequences (repeated patterns at different pitch levels).

    Detects sequential patterns like rising or falling sequences commonly
    found in Baroque and Classical music.

    Args:
        score_or_stream: Musical score or stream to analyze
        min_repetitions: Minimum number of sequential repetitions (default: 2)
        max_transposition: Maximum transposition interval in semitones (default: 12)

    Returns:
        List of dictionaries containing sequence information:
        - 'pattern': The intervallic pattern
        - 'transpositions': List of transposition amounts
        - 'offsets': Starting positions of each repetition
        - 'type': 'ascending', 'descending', or 'mixed'

    Example:
        >>> sequences = identify_melodic_sequences(my_score, min_repetitions=3)
        >>> for seq in sequences:
        ...     print(f"{seq['type']} sequence: {seq['transpositions']}")
    """
    notes_list = []
    if isinstance(score_or_stream, stream.Score):
        for part in score_or_stream.parts:
            notes_list.extend([(n.offset, n) for n in part.flatten().notes])
    else:
        notes_list = [(n.offset, n) for n in score_or_stream.flatten().notes]

    notes_list.sort(key=lambda x: x[0])

    # Extract pitch sequence
    pitches = []
    offsets = []
    for offset, n in notes_list:
        if isinstance(n, note.Note):
            pitches.append(n.pitch.midi)
            offsets.append(offset)

    if len(pitches) < min_repetitions * 2:
        return []

    sequences = []

    # Try different pattern lengths
    for pattern_length in range(2, 8):
        for i in range(len(pitches) - pattern_length * min_repetitions):
            # Extract base pattern
            base_pattern = [pitches[i + j + 1] - pitches[i + j]
                           for j in range(pattern_length - 1)]

            # Look for sequential repetitions
            transpositions = []
            seq_offsets = [offsets[i]]

            current_pos = i
            for rep in range(1, min_repetitions + 3):  # Look ahead
                next_pos = current_pos + pattern_length
                if next_pos + pattern_length - 1 >= len(pitches):
                    break

                # Check if next segment matches the pattern (intervals)
                next_pattern = [pitches[next_pos + j + 1] - pitches[next_pos + j]
                               for j in range(pattern_length - 1)]

                if next_pattern == base_pattern:
                    # Calculate transposition
                    trans = pitches[next_pos] - pitches[current_pos]
                    if abs(trans) <= max_transposition and trans != 0:
                        transpositions.append(trans)
                        seq_offsets.append(offsets[next_pos])
                        current_pos = next_pos
                    else:
                        break
                else:
                    break

            # Check if we found a sequence
            if len(transpositions) >= min_repetitions - 1:
                # Determine sequence type
                if all(t > 0 for t in transpositions):
                    seq_type = 'ascending'
                elif all(t < 0 for t in transpositions):
                    seq_type = 'descending'
                else:
                    seq_type = 'mixed'

                # Check if this sequence is already detected
                is_duplicate = False
                for existing in sequences:
                    if (existing['pattern'] == base_pattern and
                        existing['offsets'][0] == seq_offsets[0]):
                        is_duplicate = True
                        break

                if not is_duplicate:
                    sequences.append({
                        'pattern': base_pattern,
                        'transpositions': transpositions,
                        'offsets': seq_offsets,
                        'type': seq_type,
                        'pattern_length': pattern_length,
                        'repetitions': len(transpositions) + 1
                    })

    # Sort by number of repetitions
    sequences.sort(key=lambda s: s['repetitions'], reverse=True)

    return sequences


def detect_imitation_points(
    score: stream.Score,
    time_window: float = 4.0,
    similarity_threshold: float = 0.7
) -> list[dict[str, Any]]:
    """
    Find points where voices imitate each other in counterpoint.

    Analyzes multi-voice music to detect imitative entries, measuring
    the delay and similarity between voices.

    Args:
        score: Musical score with multiple parts
        time_window: Maximum time difference to consider (quarter notes)
        similarity_threshold: Minimum similarity score (0.0-1.0)

    Returns:
        List of imitation points with details:
        - 'leader_voice': Index of the leading voice
        - 'follower_voice': Index of the following voice
        - 'delay': Time delay in quarter notes
        - 'similarity': Similarity score (0.0-1.0)
        - 'type': 'exact', 'tonal', 'rhythmic', or 'contour'
        - 'offset': Position in the score

    Example:
        >>> imitations = detect_imitation_points(fugue, time_window=2.0)
        >>> for im in imitations:
        ...     print(f"Voice {im['leader_voice']} → {im['follower_voice']}, "
        ...           f"delay: {im['delay']}q")
    """
    if not isinstance(score, stream.Score):
        return []

    if len(score.parts) < 2:
        return []

    imitation_points = []

    # Extract notes from each voice
    voices = []
    for part in score.parts:
        voice_notes = []
        for n in part.flatten().notes:
            if isinstance(n, note.Note):
                voice_notes.append({
                    'offset': n.offset,
                    'pitch': n.pitch.midi,
                    'duration': n.quarterLength
                })
        voices.append(voice_notes)

    # Compare each pair of voices
    for i in range(len(voices)):
        for j in range(i + 1, len(voices)):
            voice1 = voices[i]
            voice2 = voices[j]

            # Look for imitation at different time delays
            for delay_quarters in np.arange(0.5, time_window + 0.5, 0.5):
                for start_idx1, note1 in enumerate(voice1):
                    offset1 = note1['offset']

                    # Find corresponding note in voice2
                    target_offset = offset1 + delay_quarters

                    # Find notes in voice2 around this time
                    for start_idx2, note2 in enumerate(voice2):
                        if abs(note2['offset'] - target_offset) < 0.25:
                            # Found a potential imitation point
                            # Compare the following notes
                            pattern_length = min(8,
                                               len(voice1) - start_idx1,
                                               len(voice2) - start_idx2)

                            if pattern_length < 3:
                                continue

                            # Extract patterns
                            pattern1_intervals = []
                            pattern2_intervals = []
                            pattern1_rhythms = []
                            pattern2_rhythms = []

                            for k in range(pattern_length - 1):
                                if start_idx1 + k + 1 < len(voice1):
                                    p1 = voice1[start_idx1 + k]['pitch']
                                    p2 = voice1[start_idx1 + k + 1]['pitch']
                                    pattern1_intervals.append(p2 - p1)
                                    pattern1_rhythms.append(voice1[start_idx1 + k]['duration'])

                                if start_idx2 + k + 1 < len(voice2):
                                    p1 = voice2[start_idx2 + k]['pitch']
                                    p2 = voice2[start_idx2 + k + 1]['pitch']
                                    pattern2_intervals.append(p2 - p1)
                                    pattern2_rhythms.append(voice2[start_idx2 + k]['duration'])

                            # Calculate similarity
                            interval_sim = _calculate_similarity(
                                pattern1_intervals, pattern2_intervals
                            )
                            rhythm_sim = _calculate_similarity(
                                pattern1_rhythms, pattern2_rhythms
                            )

                            overall_sim = (interval_sim + rhythm_sim) / 2

                            if overall_sim >= similarity_threshold:
                                # Classify imitation type
                                if interval_sim > 0.95 and rhythm_sim > 0.95:
                                    im_type = 'exact'
                                elif interval_sim > 0.85:
                                    im_type = 'tonal'
                                elif rhythm_sim > 0.85:
                                    im_type = 'rhythmic'
                                else:
                                    im_type = 'contour'

                                imitation_points.append({
                                    'leader_voice': i,
                                    'follower_voice': j,
                                    'delay': delay_quarters,
                                    'similarity': overall_sim,
                                    'type': im_type,
                                    'offset': offset1,
                                    'pattern_length': pattern_length
                                })

    # Remove duplicates and sort by similarity
    imitation_points.sort(key=lambda x: x['similarity'], reverse=True)

    return imitation_points


def analyze_thematic_development(
    score_or_stream: stream.Stream,
    theme_length: int = 8
) -> dict[str, Any]:
    """
    Analyze how themes evolve and develop throughout a piece.

    Tracks transformations like fragmentation, augmentation, diminution,
    and recombination of thematic material.

    Args:
        score_or_stream: Musical score or stream to analyze
        theme_length: Length of themes to track (default: 8 notes)

    Returns:
        Dictionary containing:
        - 'themes': List of identified themes
        - 'transformations': List of theme transformations
        - 'development_sections': Identified development areas
        - 'recapitulations': Theme returns/recapitulations

    Example:
        >>> analysis = analyze_thematic_development(sonata_movement)
        >>> print(f"Found {len(analysis['themes'])} themes")
        >>> print(f"Transformations: {len(analysis['transformations'])}")
    """
    # Detect motifs as potential themes
    motifs = detect_motifs(
        score_or_stream,
        min_length=theme_length // 2,
        max_length=theme_length,
        min_occurrences=2
    )

    # Identify most prominent themes (top occurrences)
    themes = motifs[:5] if len(motifs) >= 5 else motifs

    # Analyze transformations
    transformations = []

    for i, theme in enumerate(themes):
        for occurrence_offset in theme.occurrences[1:]:  # Skip first occurrence
            # Check for augmentation/diminution
            # This would compare rhythmic values
            transformation = {
                'theme_id': i,
                'offset': occurrence_offset,
                'type': 'repetition',  # Default
                'original_offset': theme.offset
            }
            transformations.append(transformation)

    # Identify development sections (areas with high transformation density)
    development_sections = []

    # Simple heuristic: look for clusters of transformations
    if transformations:
        offsets = [t['offset'] for t in transformations]
        offsets.sort()

        current_section_start = offsets[0]
        current_section_transformations = 1

        for i in range(1, len(offsets)):
            if offsets[i] - offsets[i-1] < 8.0:  # Within 8 quarter notes
                current_section_transformations += 1
            else:
                if current_section_transformations >= 3:
                    development_sections.append({
                        'start_offset': current_section_start,
                        'end_offset': offsets[i-1],
                        'transformation_count': current_section_transformations
                    })
                current_section_start = offsets[i]
                current_section_transformations = 1

    # Identify recapitulations (theme returns after absence)
    recapitulations = []

    for i, theme in enumerate(themes):
        if len(theme.occurrences) >= 2:
            # Check if there's a significant gap before the last occurrence
            last_occurrence = theme.occurrences[-1]
            previous_occurrence = theme.occurrences[-2]

            if last_occurrence - previous_occurrence > 16.0:  # More than 16 quarter notes
                recapitulations.append({
                    'theme_id': i,
                    'offset': last_occurrence,
                    'gap_duration': last_occurrence - previous_occurrence
                })

    return {
        'themes': [
            {
                'id': i,
                'intervals': theme.intervals,
                'rhythms': theme.rhythms,
                'occurrences': theme.occurrences,
                'first_appearance': theme.offset
            }
            for i, theme in enumerate(themes)
        ],
        'transformations': transformations,
        'development_sections': development_sections,
        'recapitulations': recapitulations,
        'theme_count': len(themes)
    }


def _calculate_similarity(seq1: list, seq2: list) -> float:
    """Calculate similarity between two sequences (0.0-1.0)."""
    if not seq1 or not seq2:
        return 0.0

    min_len = min(len(seq1), len(seq2))
    if min_len == 0:
        return 0.0

    matches = sum(1 for i in range(min_len) if
                  abs(float(seq1[i]) - float(seq2[i])) < 0.1)

    return matches / min_len


def find_contour_similarities(
    score_or_stream: stream.Stream,
    min_length: int = 4
) -> list[dict[str, Any]]:
    """
    Find melodic contours that share similar shapes regardless of exact intervals.

    Useful for identifying thematic relationships that may not be obvious
    from pitch or interval analysis alone.

    Args:
        score_or_stream: Musical score or stream to analyze
        min_length: Minimum contour length to consider

    Returns:
        List of contour matches with similarity scores

    Example:
        >>> contours = find_contour_similarities(my_score, min_length=5)
        >>> for c in contours[:3]:
        ...     print(f"Contour at offset {c['offset']}, "
        ...           f"similarity: {c['similarity']:.2f}")
    """
    notes_list = []
    if isinstance(score_or_stream, stream.Score):
        for part in score_or_stream.parts:
            notes_list.extend([(n.offset, n) for n in part.flatten().notes])
    else:
        notes_list = [(n.offset, n) for n in score_or_stream.flatten().notes]

    notes_list.sort(key=lambda x: x[0])

    # Extract pitches
    pitches = []
    offsets = []
    for offset, n in notes_list:
        if isinstance(n, note.Note):
            pitches.append(n.pitch.midi)
            offsets.append(offset)

    if len(pitches) < min_length:
        return []

    # Convert to contours (up, down, same)
    def to_contour(pitch_seq):
        contour = []
        for i in range(len(pitch_seq) - 1):
            if pitch_seq[i + 1] > pitch_seq[i]:
                contour.append(1)  # Up
            elif pitch_seq[i + 1] < pitch_seq[i]:
                contour.append(-1)  # Down
            else:
                contour.append(0)  # Same
        return tuple(contour)

    # Find matching contours
    contour_matches: dict[tuple, list[float]] = {}

    for length in range(min_length, min(12, len(pitches))):
        for i in range(len(pitches) - length + 1):
            segment = pitches[i:i + length]
            contour = to_contour(segment)

            if contour not in contour_matches:
                contour_matches[contour] = []
            contour_matches[contour].append(offsets[i])

    # Build results
    results = []
    for contour, occurrence_offsets in contour_matches.items():
        if len(occurrence_offsets) >= 2:  # At least 2 occurrences
            results.append({
                'contour': contour,
                'length': len(contour) + 1,
                'offsets': occurrence_offsets,
                'occurrences': len(occurrence_offsets),
                'similarity': 1.0  # Exact contour match
            })

    # Sort by number of occurrences
    results.sort(key=lambda x: x['occurrences'], reverse=True)

    return results


def analyze_fugue_structure(
    score: stream.Score,
    subject_length: int = 8
) -> dict[str, Any]:
    """
    Analyze fugue structure: subject, answer, episodes, stretto sections.

    Detects the main subject, its answers (real or tonal), counter-subjects,
    episodes, and stretto passages.

    Args:
        score: Musical score (typically a fugue)
        subject_length: Expected length of the subject in notes

    Returns:
        Dictionary containing:
        - 'subject': Main subject motif
        - 'answers': List of answer entries (with voice and offset)
        - 'counter_subjects': Counter-subject motifs
        - 'episodes': Episode sections (non-imitative development)
        - 'stretto_sections': Stretto passages (overlapping entries)
        - 'exposition_end': Estimated offset where exposition ends

    Example:
        >>> analysis = analyze_fugue_structure(fugue_score, subject_length=6)
        >>> print(f"Found {len(analysis['answers'])} fugue answers")
        >>> print(f"Stretto sections: {len(analysis['stretto_sections'])}")
    """
    if not isinstance(score, stream.Score) or len(score.parts) < 2:
        return {
            'subject': None,
            'answers': [],
            'counter_subjects': [],
            'episodes': [],
            'stretto_sections': [],
            'exposition_end': 0.0
        }

    # Extract the presumed subject (first melodic statement in first voice)
    first_voice = score.parts[0]
    subject_notes = []
    for n in first_voice.flatten().notes:
        if isinstance(n, note.Note):
            subject_notes.append({
                'pitch': n.pitch.midi,
                'offset': n.offset,
                'duration': n.quarterLength
            })
        if len(subject_notes) >= subject_length:
            break

    if len(subject_notes) < subject_length:
        subject_length = len(subject_notes)

    # Extract subject intervals
    subject_intervals = [
        subject_notes[i+1]['pitch'] - subject_notes[i]['pitch']
        for i in range(len(subject_notes) - 1)
    ]

    # Find answers in other voices
    answers = []
    imitations = detect_imitation_points(score, time_window=8.0, similarity_threshold=0.6)

    for im in imitations:
        if im['similarity'] >= 0.7 and im['offset'] < 20.0:  # Within exposition
            answer_type = 'real' if abs(im.get('transposition', 0) - 7) > 2 else 'tonal'
            answers.append({
                'voice': im['follower_voice'],
                'offset': im['offset'],
                'type': answer_type,
                'similarity': im['similarity']
            })

    # Detect counter-subjects (material accompanying subject/answer)
    counter_subjects = []
    motifs = detect_motifs(score, min_length=4, max_length=8, min_occurrences=2)

    # Counter-subjects typically appear when subject appears
    for motif in motifs[:3]:  # Check top 3 motifs
        if len(motif.occurrences) >= 2:
            # Check if this motif appears during subject/answer entries
            appears_with_subject = any(
                abs(motif.offset - ans['offset']) < 2.0
                for ans in answers
            )
            if appears_with_subject:
                counter_subjects.append(motif)

    # Estimate exposition end (when all voices have entered)
    exposition_end = 0.0
    if answers:
        exposition_end = max(ans['offset'] for ans in answers) + subject_length

    # Detect episodes (sections without clear subject/answer)
    episodes = []
    if exposition_end > 0:
        # Look for gaps in subject appearances after exposition
        all_subject_offsets = [0.0] + [ans['offset'] for ans in answers]
        all_subject_offsets.sort()

        for i in range(len(all_subject_offsets) - 1):
            gap = all_subject_offsets[i+1] - all_subject_offsets[i]
            if gap > subject_length * 2:  # Significant gap
                episodes.append({
                    'start': all_subject_offsets[i] + subject_length,
                    'end': all_subject_offsets[i+1],
                    'duration': gap - subject_length
                })

    # Detect stretto (overlapping subject entries)
    stretto_sections = []
    for i, im in enumerate(imitations):
        if im['delay'] < subject_length * 0.75:  # Entries overlap
            stretto_sections.append({
                'offset': im['offset'],
                'voices': [im['leader_voice'], im['follower_voice']],
                'overlap': subject_length - im['delay']
            })

    return {
        'subject': {
            'intervals': subject_intervals,
            'length': subject_length,
            'first_occurrence': subject_notes[0]['offset'] if subject_notes else 0.0
        },
        'answers': answers,
        'counter_subjects': counter_subjects,
        'episodes': episodes,
        'stretto_sections': stretto_sections,
        'exposition_end': exposition_end
    }


def calculate_voice_independence(
    score: stream.Score,
    time_window: float = 4.0
) -> dict[str, Any]:
    """
    Calculate voice independence metrics for polyphonic music.

    Analyzes rhythmic independence, melodic independence, and harmonic
    interdependence between voices.

    Args:
        score: Musical score with multiple parts
        time_window: Size of analysis window in quarter notes

    Returns:
        Dictionary containing:
        - 'rhythmic_independence': Score 0.0-1.0 (1.0 = completely independent)
        - 'melodic_independence': Score 0.0-1.0
        - 'contour_independence': Score 0.0-1.0
        - 'harmonic_density': Average number of simultaneous notes
        - 'voice_crossing_count': Number of times voices cross
        - 'per_voice_activity': Activity level for each voice

    Example:
        >>> metrics = calculate_voice_independence(fugue)
        >>> print(f"Rhythmic independence: {metrics['rhythmic_independence']:.2f}")
        >>> print(f"Voice crossings: {metrics['voice_crossing_count']}")
    """
    if not isinstance(score, stream.Score) or len(score.parts) < 2:
        return {
            'rhythmic_independence': 0.0,
            'melodic_independence': 0.0,
            'contour_independence': 0.0,
            'harmonic_density': 0.0,
            'voice_crossing_count': 0,
            'per_voice_activity': []
        }

    num_voices = len(score.parts)

    # Extract note events from each voice
    voices_data = []
    for part in score.parts:
        voice_notes = []
        for n in part.flatten().notes:
            if isinstance(n, note.Note):
                voice_notes.append({
                    'offset': n.offset,
                    'pitch': n.pitch.midi,
                    'duration': n.quarterLength,
                    'end': n.offset + n.quarterLength
                })
        voices_data.append(voice_notes)

    # Calculate rhythmic independence
    # (measure how often voices attack at different times)
    rhythmic_coincidences = 0
    total_attacks = sum(len(v) for v in voices_data)

    for i in range(len(voices_data)):
        for j in range(i + 1, len(voices_data)):
            for note1 in voices_data[i]:
                for note2 in voices_data[j]:
                    if abs(note1['offset'] - note2['offset']) < 0.25:
                        rhythmic_coincidences += 1

    rhythmic_independence = 1.0 - (rhythmic_coincidences / max(total_attacks, 1))
    rhythmic_independence = max(0.0, min(1.0, rhythmic_independence))

    # Calculate melodic independence
    # (measure correlation of melodic motion)
    melodic_independence = 0.0
    comparisons = 0

    for i in range(len(voices_data)):
        for j in range(i + 1, len(voices_data)):
            # Compare melodic contours
            contour1 = _extract_contour_from_notes(voices_data[i])
            contour2 = _extract_contour_from_notes(voices_data[j])

            if contour1 and contour2:
                # Measure dissimilarity
                sim = _calculate_similarity(contour1, contour2)
                melodic_independence += (1.0 - sim)
                comparisons += 1

    if comparisons > 0:
        melodic_independence /= comparisons

    # Calculate contour independence (similar to melodic but focuses on shape)
    contour_independence = melodic_independence  # Simplified for now

    # Calculate harmonic density
    # (average number of simultaneous notes)
    score_duration = max(
        max((n['end'] for n in voice), default=0.0)
        for voice in voices_data
        if voice
    )

    if score_duration > 0:
        time_points = np.arange(0, score_duration, 0.5)
        density_samples = []

        for t in time_points:
            active_count = 0
            for voice in voices_data:
                for n in voice:
                    if n['offset'] <= t < n['end']:
                        active_count += 1
                        break
            density_samples.append(active_count)

        harmonic_density = np.mean(density_samples) if density_samples else 0.0
    else:
        harmonic_density = 0.0

    # Count voice crossings
    voice_crossing_count = 0
    for i in range(len(voices_data)):
        for j in range(i + 1, len(voices_data)):
            # Sample at regular intervals
            for offset in np.arange(0, score_duration, 1.0):
                # Get pitches at this time
                pitch_i = _get_pitch_at_time(voices_data[i], offset)
                pitch_j = _get_pitch_at_time(voices_data[j], offset)

                if pitch_i is not None and pitch_j is not None:
                    # Check if relative order changed from previous
                    prev_offset = offset - 1.0
                    if prev_offset >= 0:
                        prev_pitch_i = _get_pitch_at_time(voices_data[i], prev_offset)
                        prev_pitch_j = _get_pitch_at_time(voices_data[j], prev_offset)

                        if (prev_pitch_i is not None and prev_pitch_j is not None and
                                (pitch_i > pitch_j) != (prev_pitch_i > prev_pitch_j)):
                            voice_crossing_count += 1

    # Calculate per-voice activity
    per_voice_activity = []
    for voice in voices_data:
        if voice:
            total_duration = sum(n['duration'] for n in voice)
            activity = total_duration / score_duration if score_duration > 0 else 0.0
        else:
            activity = 0.0
        per_voice_activity.append(activity)

    return {
        'rhythmic_independence': float(rhythmic_independence),
        'melodic_independence': float(melodic_independence),
        'contour_independence': float(contour_independence),
        'harmonic_density': float(harmonic_density),
        'voice_crossing_count': int(voice_crossing_count),
        'per_voice_activity': per_voice_activity,
        'num_voices': num_voices
    }


def _extract_contour_from_notes(notes: list[dict]) -> list[int]:
    """Extract melodic contour from list of note dictionaries."""
    if len(notes) < 2:
        return []

    contour = []
    for i in range(len(notes) - 1):
        if notes[i+1]['pitch'] > notes[i]['pitch']:
            contour.append(1)
        elif notes[i+1]['pitch'] < notes[i]['pitch']:
            contour.append(-1)
        else:
            contour.append(0)

    return contour


def _get_pitch_at_time(notes: list[dict], offset: float) -> int | None:
    """Get the pitch of the note sounding at a given offset."""
    for n in notes:
        if n['offset'] <= offset < n['end']:
            return n['pitch']
    return None


def calculate_pattern_complexity(
    score_or_stream: stream.Stream
) -> dict[str, float]:
    """
    Calculate complexity metrics for musical patterns.

    Measures various aspects of pattern complexity including interval variety,
    rhythmic complexity, and melodic range.

    Args:
        score_or_stream: Musical score or stream to analyze

    Returns:
        Dictionary with complexity metrics:
        - 'interval_complexity': Variety of intervals used (0.0-1.0)
        - 'rhythmic_complexity': Variety of rhythmic values (0.0-1.0)
        - 'range_complexity': Melodic range utilization (0.0-1.0)
        - 'direction_changes': Number of melodic direction changes
        - 'overall_complexity': Weighted average (0.0-1.0)

    Example:
        >>> complexity = calculate_pattern_complexity(melody)
        >>> print(f"Overall complexity: {complexity['overall_complexity']:.2f}")
    """
    # Extract notes
    notes_list = []
    if isinstance(score_or_stream, stream.Score):
        for part in score_or_stream.parts:
            notes_list.extend(part.flatten().notes)
    else:
        notes_list = list(score_or_stream.flatten().notes)

    if len(notes_list) < 2:
        return {
            'interval_complexity': 0.0,
            'rhythmic_complexity': 0.0,
            'range_complexity': 0.0,
            'direction_changes': 0,
            'overall_complexity': 0.0
        }

    # Extract pitches and durations
    pitches = []
    durations = []
    for n in notes_list:
        if isinstance(n, note.Note):
            pitches.append(n.pitch.midi)
            durations.append(n.quarterLength)

    # Calculate interval complexity (variety of intervals)
    intervals = [abs(pitches[i+1] - pitches[i]) for i in range(len(pitches) - 1)]
    unique_intervals = len(set(intervals))
    max_possible_intervals = 12  # Within an octave
    interval_complexity = min(1.0, unique_intervals / max_possible_intervals)

    # Calculate rhythmic complexity (variety of durations)
    unique_durations = len(set(durations))
    max_expected_durations = 8  # Common rhythmic values
    rhythmic_complexity = min(1.0, unique_durations / max_expected_durations)

    # Calculate range complexity (how much of the range is used)
    if pitches:
        pitch_range = max(pitches) - min(pitches)
        expected_range = 24  # Two octaves
        range_complexity = min(1.0, pitch_range / expected_range)
    else:
        range_complexity = 0.0

    # Count direction changes
    direction_changes = 0
    for i in range(1, len(pitches) - 1):
        prev_direction = pitches[i] - pitches[i-1]
        next_direction = pitches[i+1] - pitches[i]
        if prev_direction * next_direction < 0:  # Sign change
            direction_changes += 1

    # Calculate overall complexity (weighted average)
    overall_complexity = (
        interval_complexity * 0.3 +
        rhythmic_complexity * 0.3 +
        range_complexity * 0.2 +
        min(1.0, direction_changes / len(pitches)) * 0.2
    )

    return {
        'interval_complexity': float(interval_complexity),
        'rhythmic_complexity': float(rhythmic_complexity),
        'range_complexity': float(range_complexity),
        'direction_changes': int(direction_changes),
        'overall_complexity': float(overall_complexity)
    }
