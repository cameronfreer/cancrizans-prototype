"""
Machine learning and intelligent analysis for Cancrizans.

Provides pattern recognition, style classification, canon detection,
and generative assistance using statistical and heuristic methods.
"""

from pathlib import Path
from typing import Union, Dict, List, Optional, Tuple
import random
from collections import Counter
import numpy as np
from music21 import stream, note, chord, interval, key
import music21 as m21


# ============================================================================
# Phase 16: Machine Learning for Canon Analysis
# ============================================================================


def analyze_patterns(
    score: stream.Score,
    min_pattern_length: int = 3,
    max_pattern_length: int = 8,
    confidence_threshold: float = 0.6
) -> Dict[str, any]:
    """
    Analyze and learn musical patterns from a score using statistical methods.

    Identifies recurring melodic and rhythmic patterns, calculates their
    frequency and confidence scores.

    Args:
        score: The Score to analyze
        min_pattern_length: Minimum pattern length in notes (default 3)
        max_pattern_length: Maximum pattern length in notes (default 8)
        confidence_threshold: Minimum confidence for pattern inclusion (0.0-1.0)

    Returns:
        Dict containing:
            - patterns: List of identified patterns with metadata
            - num_patterns: Total number of patterns found
            - most_common: Most frequently occurring pattern
            - confidence_scores: Confidence score for each pattern
            - pattern_transitions: Common transitions between patterns

    Example:
        >>> canon = mirror_canon(theme)
        >>> analysis = analyze_patterns(canon, min_pattern_length=4)
        >>> print(f"Found {analysis['num_patterns']} patterns")
    """
    patterns = []
    pattern_occurrences = {}

    # Extract all notes from the score
    all_notes = []
    for part in score.parts:
        for el in part.flatten().notes:
            if isinstance(el, note.Note):
                all_notes.append({
                    'pitch': el.pitch.midi,
                    'duration': float(el.quarterLength),
                    'offset': float(el.offset)
                })

    if len(all_notes) < min_pattern_length:
        return {
            'patterns': [],
            'num_patterns': 0,
            'most_common': None,
            'confidence_scores': {},
            'pattern_transitions': {}
        }

    # Find patterns of different lengths
    for length in range(min_pattern_length, min(max_pattern_length + 1, len(all_notes))):
        for i in range(len(all_notes) - length + 1):
            # Create pattern signature (intervals + rhythms)
            pattern_notes = all_notes[i:i+length]

            # Melodic contour (intervals)
            intervals = []
            for j in range(len(pattern_notes) - 1):
                intervals.append(pattern_notes[j+1]['pitch'] - pattern_notes[j]['pitch'])

            # Rhythmic pattern
            durations = [n['duration'] for n in pattern_notes]

            # Create pattern signature
            pattern_sig = (tuple(intervals), tuple(durations))

            if pattern_sig in pattern_occurrences:
                pattern_occurrences[pattern_sig] += 1
            else:
                pattern_occurrences[pattern_sig] = 1

    # Calculate confidence scores and filter patterns
    total_possible_patterns = sum(pattern_occurrences.values())

    for pattern_sig, count in pattern_occurrences.items():
        if count >= 2:  # Pattern appears at least twice
            intervals_tuple, durations_tuple = pattern_sig

            # Confidence based on frequency and consistency
            frequency = count / total_possible_patterns
            consistency = min(1.0, count / 5.0)  # More occurrences = higher consistency
            confidence = (frequency + consistency) / 2.0

            if confidence >= confidence_threshold:
                patterns.append({
                    'intervals': list(intervals_tuple),
                    'durations': list(durations_tuple),
                    'occurrences': count,
                    'confidence': confidence,
                    'length': len(intervals_tuple) + 1
                })

    # Sort by confidence
    patterns.sort(key=lambda p: p['confidence'], reverse=True)

    # Find most common pattern
    most_common = patterns[0] if patterns else None

    # Analyze pattern transitions (simplified)
    transitions = {}
    if len(patterns) >= 2:
        for i in range(min(5, len(patterns) - 1)):
            for j in range(i + 1, min(5, len(patterns))):
                trans_key = f"pattern_{i}_to_{j}"
                transitions[trans_key] = 0.5  # Placeholder probability

    return {
        'patterns': patterns[:10],  # Top 10 patterns
        'num_patterns': len(patterns),
        'most_common': most_common,
        'confidence_scores': {i: p['confidence'] for i, p in enumerate(patterns[:10])},
        'pattern_transitions': transitions
    }


def classify_style(
    score: stream.Score,
    return_probabilities: bool = False
) -> Dict[str, any]:
    """
    Classify musical style using feature-based analysis.

    Analyzes musical features (intervals, rhythm complexity, harmonic content)
    to classify the style as baroque, classical, or romantic.

    Args:
        score: The Score to classify
        return_probabilities: Whether to return probability scores for all styles

    Returns:
        Dict containing:
            - style: Predicted style ('baroque', 'classical', 'romantic')
            - confidence: Confidence score (0.0-1.0)
            - probabilities: Probability for each style (if requested)
            - features: Extracted musical features used for classification

    Example:
        >>> analysis = classify_style(bach_canon, return_probabilities=True)
        >>> print(f"Style: {analysis['style']} ({analysis['confidence']:.2f})")
    """
    features = {}

    # Extract musical features
    all_notes = list(score.flatten().notes)
    if not all_notes:
        return {
            'style': 'unknown',
            'confidence': 0.0,
            'probabilities': {'baroque': 0.33, 'classical': 0.33, 'romantic': 0.34},
            'features': {}
        }

    # Feature 1: Interval complexity
    intervals_list = []
    for i in range(len(all_notes) - 1):
        if isinstance(all_notes[i], note.Note) and isinstance(all_notes[i+1], note.Note):
            intv = interval.Interval(all_notes[i].pitch, all_notes[i+1].pitch)
            intervals_list.append(abs(intv.semitones))

    if intervals_list:
        avg_interval = np.mean(intervals_list)
        interval_variance = np.var(intervals_list)
        large_leaps = sum(1 for i in intervals_list if i > 7) / len(intervals_list)
    else:
        avg_interval = 0
        interval_variance = 0
        large_leaps = 0

    features['avg_interval'] = avg_interval
    features['interval_variance'] = interval_variance
    features['large_leaps'] = large_leaps

    # Feature 2: Rhythmic complexity
    durations = [float(n.quarterLength) for n in all_notes]
    unique_durations = len(set(durations))
    duration_variance = np.var(durations) if durations else 0

    features['unique_durations'] = unique_durations
    features['rhythmic_complexity'] = duration_variance

    # Feature 3: Chromatic content
    pitches = [n.pitch.midi for n in all_notes if isinstance(n, note.Note)]
    if len(pitches) > 1:
        chromatic_steps = sum(1 for i in range(len(pitches)-1)
                             if abs(pitches[i+1] - pitches[i]) == 1)
        chromatic_ratio = chromatic_steps / (len(pitches) - 1)
    else:
        chromatic_ratio = 0

    features['chromatic_ratio'] = chromatic_ratio

    # Feature 4: Range
    if pitches:
        pitch_range = max(pitches) - min(pitches)
    else:
        pitch_range = 0

    features['pitch_range'] = pitch_range

    # Simple heuristic classification based on features
    baroque_score = 0.0
    classical_score = 0.0
    romantic_score = 0.0

    # Baroque: smaller intervals, less chromatic, moderate range
    if avg_interval < 3.5:
        baroque_score += 0.3
    if chromatic_ratio < 0.15:
        baroque_score += 0.3
    if pitch_range < 20:
        baroque_score += 0.2
    if unique_durations <= 4:
        baroque_score += 0.2

    # Classical: balanced intervals, clear rhythm, moderate chromatic
    if 3.0 <= avg_interval <= 4.5:
        classical_score += 0.3
    if 0.1 <= chromatic_ratio <= 0.25:
        classical_score += 0.3
    if 15 <= pitch_range <= 25:
        classical_score += 0.2
    if 3 <= unique_durations <= 6:
        classical_score += 0.2

    # Romantic: larger intervals, more chromatic, wider range
    if avg_interval > 4.0:
        romantic_score += 0.3
    if chromatic_ratio > 0.2:
        romantic_score += 0.3
    if pitch_range > 20:
        romantic_score += 0.2
    if unique_durations > 5:
        romantic_score += 0.2

    # Normalize scores
    total = baroque_score + classical_score + romantic_score
    if total > 0:
        baroque_prob = baroque_score / total
        classical_prob = classical_score / total
        romantic_prob = romantic_score / total
    else:
        baroque_prob = classical_prob = romantic_prob = 1/3

    # Determine predicted style
    probabilities = {
        'baroque': baroque_prob,
        'classical': classical_prob,
        'romantic': romantic_prob
    }

    predicted_style = max(probabilities, key=probabilities.get)
    confidence = probabilities[predicted_style]

    result = {
        'style': predicted_style,
        'confidence': confidence,
        'features': features
    }

    if return_probabilities:
        result['probabilities'] = probabilities

    return result


def detect_canon_type(
    score: stream.Score,
    analysis_depth: str = 'medium'
) -> Dict[str, any]:
    """
    Automatically detect canon type using intelligent analysis.

    Analyzes voice relationships, transformations, and structural patterns
    to identify the type of canon (retrograde, mirror, crab, etc.).

    Args:
        score: The Score to analyze
        analysis_depth: Depth of analysis ('quick', 'medium', 'thorough')

    Returns:
        Dict containing:
            - canon_type: Detected canon type
            - confidence: Detection confidence (0.0-1.0)
            - evidence: Evidence supporting the detection
            - voice_relationships: Relationships between voices
            - transformations: Detected transformations

    Example:
        >>> detection = detect_canon_type(mysterious_canon)
        >>> print(f"Detected: {detection['canon_type']}")
    """
    parts = list(score.parts)

    if len(parts) < 2:
        return {
            'canon_type': 'monophonic',
            'confidence': 1.0,
            'evidence': ['Only one voice present'],
            'voice_relationships': {},
            'transformations': []
        }

    evidence = []
    transformations = []
    voice_relationships = {}

    # Extract notes from each voice
    voices = []
    for part in parts:
        voice_notes = []
        for el in part.flatten().notes:
            if isinstance(el, note.Note):
                voice_notes.append({
                    'pitch': el.pitch.midi,
                    'offset': float(el.offset)
                })
        voices.append(voice_notes)

    # Analyze pairwise voice relationships
    for i in range(len(voices)):
        for j in range(i + 1, len(voices)):
            relationship = _analyze_voice_pair(voices[i], voices[j])
            voice_relationships[f'voice_{i+1}_to_{j+1}'] = relationship

            if relationship['type'] != 'independent':
                evidence.append(f"Voice {i+1} and {j+1}: {relationship['type']}")
                transformations.append(relationship['type'])

    # Determine canon type based on evidence
    canon_type = 'unknown'
    confidence = 0.0

    if 'retrograde' in transformations and 'inversion' in transformations:
        canon_type = 'crab_canon'
        confidence = 0.9
        evidence.append('Detected both retrograde and inversion')
    elif 'retrograde' in transformations:
        canon_type = 'retrograde_canon'
        confidence = 0.85
        evidence.append('Detected retrograde relationship')
    elif 'inversion' in transformations:
        canon_type = 'mirror_canon'
        confidence = 0.85
        evidence.append('Detected inversion relationship')
    elif 'strict_imitation' in transformations:
        canon_type = 'strict_canon'
        confidence = 0.8
        evidence.append('Detected strict imitation')
    elif 'free_imitation' in transformations:
        canon_type = 'free_canon'
        confidence = 0.6
        evidence.append('Detected free imitation')
    else:
        canon_type = 'polyphonic'
        confidence = 0.5
        evidence.append('Multiple independent voices')

    return {
        'canon_type': canon_type,
        'confidence': confidence,
        'evidence': evidence,
        'voice_relationships': voice_relationships,
        'transformations': list(set(transformations))
    }


def suggest_continuation(
    theme: stream.Stream,
    num_measures: int = 4,
    style: str = 'baroque',
    variation_level: float = 0.3
) -> stream.Stream:
    """
    Suggest musical continuation based on learned patterns.

    Analyzes the input theme and generates a plausible continuation
    using pattern-based generation and style constraints.

    Args:
        theme: The theme to continue
        num_measures: Number of measures to generate (approximate)
        style: Style to emulate ('baroque', 'classical', 'romantic')
        variation_level: Amount of variation (0.0=strict, 1.0=free)

    Returns:
        Stream containing the suggested continuation

    Example:
        >>> continuation = suggest_continuation(
        ...     theme, num_measures=8, style='baroque'
        ... )
    """
    # Extract pattern from theme
    theme_notes = []
    for el in theme.flatten().notes:
        if isinstance(el, note.Note):
            theme_notes.append({
                'pitch': el.pitch.midi,
                'duration': float(el.quarterLength)
            })

    if not theme_notes:
        # Return empty stream if no notes
        return stream.Stream()

    # Calculate intervals and durations from theme
    intervals = []
    durations = []

    for i in range(len(theme_notes) - 1):
        intervals.append(theme_notes[i+1]['pitch'] - theme_notes[i]['pitch'])
        durations.append(theme_notes[i]['duration'])
    if theme_notes:
        durations.append(theme_notes[-1]['duration'])

    # Style-specific parameters
    style_params = {
        'baroque': {
            'preferred_intervals': [-2, -1, 1, 2, 3, -3],
            'preferred_durations': [0.5, 1.0, 2.0],
            'step_probability': 0.7
        },
        'classical': {
            'preferred_intervals': [-2, -1, 1, 2, 4, -4],
            'preferred_durations': [0.25, 0.5, 1.0, 1.5, 2.0],
            'step_probability': 0.6
        },
        'romantic': {
            'preferred_intervals': [-3, -2, -1, 1, 2, 3, 5, -5],
            'preferred_durations': [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0],
            'step_probability': 0.5
        }
    }

    params = style_params.get(style, style_params['baroque'])

    # Generate continuation
    continuation = stream.Part()
    current_pitch = theme_notes[-1]['pitch']
    target_length = num_measures * 4.0  # Approximate quarter notes
    current_length = 0.0

    while current_length < target_length:
        # Choose next interval
        if random.random() < (1 - variation_level):
            # Use pattern from theme
            if intervals:
                next_interval = random.choice(intervals)
            else:
                next_interval = random.choice(params['preferred_intervals'])
        else:
            # Use style-appropriate interval
            next_interval = random.choice(params['preferred_intervals'])

        # Apply step motion preference
        if random.random() < params['step_probability']:
            next_interval = random.choice([-2, -1, 1, 2])

        # Choose duration
        if random.random() < (1 - variation_level) and durations:
            next_duration = random.choice(durations)
        else:
            next_duration = random.choice(params['preferred_durations'])

        # Create next note
        current_pitch = max(48, min(84, current_pitch + next_interval))  # Stay in range
        new_note = note.Note(current_pitch, quarterLength=next_duration)
        continuation.append(new_note)

        current_length += next_duration

    return continuation


def _analyze_voice_pair(voice1: List[Dict], voice2: List[Dict]) -> Dict[str, any]:
    """
    Analyze relationship between two voices (helper function).

    Args:
        voice1: List of note dicts from first voice
        voice2: List of note dicts from second voice

    Returns:
        Dict with relationship type and similarity score
    """
    if not voice1 or not voice2:
        return {'type': 'independent', 'similarity': 0.0}

    # Extract pitches
    pitches1 = [n['pitch'] for n in voice1]
    pitches2 = [n['pitch'] for n in voice2]

    # Check for retrograde (reversed pitches)
    if len(pitches1) == len(pitches2):
        retrograde_similarity = sum(
            1 for i in range(min(10, len(pitches1)))
            if pitches1[i] == pitches2[-(i+1)]
        ) / min(10, len(pitches1))

        if retrograde_similarity > 0.7:
            return {'type': 'retrograde', 'similarity': retrograde_similarity}

    # Check for inversion
    if len(pitches1) >= 3 and len(pitches2) >= 3:
        # Calculate intervals
        intervals1 = [pitches1[i+1] - pitches1[i] for i in range(min(10, len(pitches1)-1))]
        intervals2 = [pitches2[i+1] - pitches2[i] for i in range(min(10, len(pitches2)-1))]

        # Check if intervals are inverted
        inversion_matches = sum(
            1 for i in range(min(len(intervals1), len(intervals2)))
            if intervals1[i] == -intervals2[i]
        )

        if inversion_matches > 0:
            inversion_similarity = inversion_matches / min(len(intervals1), len(intervals2))
            if inversion_similarity > 0.6:
                return {'type': 'inversion', 'similarity': inversion_similarity}

    # Check for strict imitation
    matching_pitches = sum(
        1 for i in range(min(10, len(pitches1), len(pitches2)))
        if pitches1[i] == pitches2[i]
    )

    if matching_pitches > 0:
        strict_similarity = matching_pitches / min(10, len(pitches1), len(pitches2))
        if strict_similarity > 0.8:
            return {'type': 'strict_imitation', 'similarity': strict_similarity}
        elif strict_similarity > 0.5:
            return {'type': 'free_imitation', 'similarity': strict_similarity}

    return {'type': 'independent', 'similarity': 0.0}
