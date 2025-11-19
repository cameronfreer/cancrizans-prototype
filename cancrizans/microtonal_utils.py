"""
Microtonal Utility Functions & Helpers

Additional utility functions for working with microtonal music,
including scale transformation, comparison, and visualization helpers.

Phase 18.5 - v0.35.1
"""

from typing import List, Dict, Tuple, Optional, Set, Union
from dataclasses import dataclass
from pathlib import Path
import math
from .microtonal import (
    MicrotonalScale, MicrotonalPitch, TuningSystem, ScaleType,
    create_tuning_system_scale, create_world_music_scale,
    compare_scales, find_common_pitches
)


@dataclass
class ScaleRecommendation:
    """Recommendation for a microtonal scale based on musical context"""
    scale_type: str
    tuning_system: Optional[TuningSystem]
    world_scale_type: Optional[ScaleType]
    confidence: float
    reason: str
    example_use_cases: List[str]


def recommend_scale_for_style(
    style: str,
    key_characteristics: Optional[List[str]] = None
) -> List[ScaleRecommendation]:
    """
    Recommend microtonal scales based on musical style

    Args:
        style: Musical style (e.g., "baroque", "jazz", "world", "experimental")
        key_characteristics: Optional list of desired characteristics

    Returns:
        List of scale recommendations sorted by relevance
    """
    recommendations = []

    style_lower = style.lower()

    # Baroque/Classical recommendations
    if any(s in style_lower for s in ["baroque", "classical", "renaissance", "bach"]):
        recommendations.append(ScaleRecommendation(
            scale_type="Historical Temperament",
            tuning_system=TuningSystem.WERCKMEISTER_III,
            world_scale_type=None,
            confidence=0.95,
            reason="Werckmeister III was commonly used in Bach's era",
            example_use_cases=["Bach fugues", "Well-Tempered Clavier", "18th century keyboard music"]
        ))
        recommendations.append(ScaleRecommendation(
            scale_type="Historical Temperament",
            tuning_system=TuningSystem.KIRNBERGER_III,
            world_scale_type=None,
            confidence=0.90,
            reason="Popular 18th century German temperament",
            example_use_cases=["Classical keyboard works", "Chamber music"]
        ))
        recommendations.append(ScaleRecommendation(
            scale_type="Historical Temperament",
            tuning_system=TuningSystem.MEANTONE,
            world_scale_type=None,
            confidence=0.85,
            reason="Standard Renaissance tuning",
            example_use_cases=["Renaissance vocal music", "Early keyboard works"]
        ))

    # World music recommendations
    elif any(s in style_lower for s in ["arabic", "middle eastern", "maqam"]):
        recommendations.append(ScaleRecommendation(
            scale_type="Arabic Maqam",
            tuning_system=None,
            world_scale_type=ScaleType.MAQAM_RAST,
            confidence=0.90,
            reason="Fundamental Arabic maqam with quarter tones",
            example_use_cases=["Arabic classical music", "Middle Eastern improvisation"]
        ))
        recommendations.append(ScaleRecommendation(
            scale_type="Arabic Maqam",
            tuning_system=None,
            world_scale_type=ScaleType.MAQAM_HIJAZ,
            confidence=0.85,
            reason="Distinctive maqam with characteristic intervals",
            example_use_cases=["Arabic folk music", "Eastern Mediterranean music"]
        ))

    elif any(s in style_lower for s in ["indian", "raga", "hindustani"]):
        recommendations.append(ScaleRecommendation(
            scale_type="Indian Raga",
            tuning_system=None,
            world_scale_type=ScaleType.RAGA_BHAIRAV,
            confidence=0.90,
            reason="Important morning raga with distinctive intervals",
            example_use_cases=["Hindustani classical", "Morning ragas"]
        ))
        recommendations.append(ScaleRecommendation(
            scale_type="Indian Raga",
            tuning_system=None,
            world_scale_type=ScaleType.RAGA_YAMAN,
            confidence=0.85,
            reason="Evening raga, one of the most fundamental",
            example_use_cases=["Evening performances", "Classical Indian music"]
        ))

    elif any(s in style_lower for s in ["gamelan", "indonesian", "javanese"]):
        recommendations.append(ScaleRecommendation(
            scale_type="Gamelan Scale",
            tuning_system=None,
            world_scale_type=ScaleType.PELOG,
            confidence=0.90,
            reason="Traditional Javanese 5-note scale",
            example_use_cases=["Gamelan orchestra", "Indonesian classical music"]
        ))
        recommendations.append(ScaleRecommendation(
            scale_type="Gamelan Scale",
            tuning_system=None,
            world_scale_type=ScaleType.SLENDRO,
            confidence=0.85,
            reason="Pentatonic Javanese scale with equal divisions",
            example_use_cases=["Shadow puppet theater", "Gamelan music"]
        ))

    # Experimental/Modern recommendations
    elif any(s in style_lower for s in ["experimental", "contemporary", "avant-garde"]):
        recommendations.append(ScaleRecommendation(
            scale_type="Xenharmonic",
            tuning_system=TuningSystem.BOHLEN_PIERCE,
            world_scale_type=None,
            confidence=0.85,
            reason="Non-octave scale based on 3:1 tritave",
            example_use_cases=["Experimental composition", "Electronic music", "Sound art"]
        ))
        recommendations.append(ScaleRecommendation(
            scale_type="Equal Temperament",
            tuning_system=TuningSystem.EQUAL_19,
            world_scale_type=None,
            confidence=0.80,
            reason="19-TET provides excellent approximations of just intervals",
            example_use_cases=["Microtonal composition", "Neo-medieval music"]
        ))
        recommendations.append(ScaleRecommendation(
            scale_type="Wendy Carlos",
            tuning_system=TuningSystem.ALPHA,
            world_scale_type=None,
            confidence=0.75,
            reason="9-EDO with near-just thirds",
            example_use_cases=["Electronic music", "Film scores"]
        ))

    # Jazz/Just Intonation
    elif any(s in style_lower for s in ["jazz", "blues", "folk"]):
        recommendations.append(ScaleRecommendation(
            scale_type="Just Intonation",
            tuning_system=TuningSystem.JUST_INTONATION_7,
            world_scale_type=None,
            confidence=0.80,
            reason="7-limit JI includes blues-like intervals",
            example_use_cases=["Jazz harmony", "Vocal music", "A cappella"]
        ))

    # Default to 12-TET if no specific style matched
    if not recommendations:
        recommendations.append(ScaleRecommendation(
            scale_type="Equal Temperament",
            tuning_system=TuningSystem.EQUAL_12,
            world_scale_type=None,
            confidence=0.70,
            reason="Standard Western tuning",
            example_use_cases=["General purpose", "Western classical", "Popular music"]
        ))

    # Sort by confidence
    recommendations.sort(key=lambda x: x.confidence, reverse=True)

    return recommendations


def blend_scales(
    scale1: MicrotonalScale,
    scale2: MicrotonalScale,
    weight: float = 0.5
) -> MicrotonalScale:
    """
    Create a hybrid scale by blending two scales

    Args:
        scale1: First scale
        scale2: Second scale
        weight: Blend weight (0.0 = all scale1, 1.0 = all scale2)

    Returns:
        New blended scale
    """
    # Find union of all intervals from both scales
    all_intervals = sorted(set(scale1.intervals_cents + scale2.intervals_cents))

    # For intervals that appear in both, blend them
    blended_intervals = []
    tolerance = 5.0  # cents

    used_from_scale2 = set()

    for interval1 in scale1.intervals_cents:
        # Find matching interval in scale2
        match_found = False
        for i, interval2 in enumerate(scale2.intervals_cents):
            if i not in used_from_scale2 and abs(interval1 - interval2) < tolerance:
                # Blend the two intervals
                blended = interval1 * (1 - weight) + interval2 * weight
                blended_intervals.append(blended)
                used_from_scale2.add(i)
                match_found = True
                break

        if not match_found:
            # No match, use original with weight applied towards 0
            blended_intervals.append(interval1 * (1 - weight * 0.5))

    # Add remaining intervals from scale2
    for i, interval2 in enumerate(scale2.intervals_cents):
        if i not in used_from_scale2:
            blended_intervals.append(interval2 * weight)

    # Sort and remove duplicates
    blended_intervals = sorted(set(round(x, 2) for x in blended_intervals))

    return MicrotonalScale(
        name=f"{scale1.name} ⊕ {scale2.name} ({weight:.0%})",
        intervals_cents=blended_intervals,
        tonic_midi=scale1.tonic_midi
    )


def find_modulation_path(
    source_scale: MicrotonalScale,
    target_scale: MicrotonalScale,
    max_steps: int = 5
) -> List[MicrotonalScale]:
    """
    Find a smooth modulation path between two scales

    Args:
        source_scale: Starting scale
        target_scale: Target scale
        max_steps: Maximum number of intermediate steps

    Returns:
        List of scales forming a modulation path
    """
    path = [source_scale]

    for i in range(1, max_steps):
        weight = i / max_steps
        intermediate = blend_scales(source_scale, target_scale, weight)
        path.append(intermediate)

    path.append(target_scale)

    return path


def calculate_scale_tension(scale: MicrotonalScale) -> float:
    """
    Calculate harmonic tension/dissonance level of a scale

    Higher values indicate more dissonant/tense scales.

    Args:
        scale: Scale to analyze

    Returns:
        Tension score (0.0 = consonant, 1.0+ = dissonant)
    """
    if len(scale.intervals_cents) < 2:
        return 0.0

    # Check interval sizes
    intervals_between = []
    for i in range(len(scale.intervals_cents) - 1):
        diff = scale.intervals_cents[i + 1] - scale.intervals_cents[i]
        intervals_between.append(diff)

    # Small intervals increase tension
    small_interval_count = sum(1 for i in intervals_between if i < 100)
    small_interval_factor = small_interval_count / len(intervals_between)

    # Check deviation from 12-TET (unfamiliar = tense)
    tet12_intervals = [i * 100 for i in range(12)]
    deviations = []
    for interval in scale.intervals_cents:
        min_dev = min(abs(interval - tet12) for tet12 in tet12_intervals)
        deviations.append(min_dev)

    avg_deviation = sum(deviations) / len(deviations)
    deviation_factor = min(1.0, avg_deviation / 50.0)

    # Combine factors
    tension = (small_interval_factor * 0.6) + (deviation_factor * 0.4)

    return tension


def quantize_to_scale(
    pitch_cents: float,
    scale: MicrotonalScale,
    allow_octave_shift: bool = True
) -> MicrotonalPitch:
    """
    Quantize a pitch to the nearest scale degree

    Args:
        pitch_cents: Pitch in cents from C0
        scale: Target scale
        allow_octave_shift: Allow finding pitch in different octave

    Returns:
        Quantized microtonal pitch
    """
    if allow_octave_shift:
        # Find the scale degree in any octave
        pitch_within_octave = pitch_cents % 1200.0

        # Find nearest scale degree
        min_distance = float('inf')
        nearest_interval = 0.0

        for interval in scale.intervals_cents:
            distance = abs(pitch_within_octave - interval)
            if distance < min_distance:
                min_distance = distance
                nearest_interval = interval

        # Calculate final pitch with octave
        octave = int(pitch_cents / 1200.0)
        final_cents = octave * 1200.0 + nearest_interval
    else:
        # Find nearest scale degree considering absolute pitch
        min_distance = float('inf')
        final_cents = 0.0

        # Check all octaves around the target pitch
        target_octave = int(pitch_cents / 1200.0)
        for octave in range(target_octave - 1, target_octave + 2):
            for interval in scale.intervals_cents:
                test_cents = octave * 1200.0 + interval
                distance = abs(pitch_cents - test_cents)
                if distance < min_distance:
                    min_distance = distance
                    final_cents = test_cents

    # Convert to MIDI note and cent deviation
    midi_note = int(final_cents / 100.0)
    cent_deviation = final_cents % 100.0

    return MicrotonalPitch(
        midi_note=midi_note,
        cent_deviation=cent_deviation
    )


def generate_scale_variants(
    base_scale: MicrotonalScale,
    num_variants: int = 5
) -> List[MicrotonalScale]:
    """
    Generate variations of a scale for exploration

    Creates variants by:
    - Transposing
    - Rotating (modal)
    - Stretching/compressing intervals
    - Removing/adding degrees

    Args:
        base_scale: Scale to create variants from
        num_variants: Number of variants to generate

    Returns:
        List of scale variants
    """
    from .microtonal import (
        transpose_scale, generate_modal_rotations,
        invert_scale, reverse_scale
    )

    variants = []

    # Add some modal rotations
    if num_variants >= 1:
        modes = generate_modal_rotations(base_scale)
        if len(modes) > 1:
            variants.append(modes[1])  # Second mode

    # Add transpositions
    if num_variants >= 2:
        variants.append(transpose_scale(base_scale, 7))  # Perfect fifth

    if num_variants >= 3:
        variants.append(transpose_scale(base_scale, 5))  # Perfect fourth

    # Add inversion
    if num_variants >= 4:
        variants.append(invert_scale(base_scale))

    # Add retrograde
    if num_variants >= 5:
        variants.append(reverse_scale(base_scale))

    return variants[:num_variants]


def create_scale_catalog() -> Dict[str, List[str]]:
    """
    Create a catalog of all available scales organized by category

    Returns:
        Dictionary mapping categories to lists of scale names
    """
    catalog = {
        "Equal Temperaments": [
            "12-TET (standard)", "17-TET", "19-TET", "22-TET (Shrutar)",
            "24-TET (quarter tones)", "31-TET", "34-TET", "41-TET",
            "53-TET", "72-TET (twelfth tones)"
        ],
        "Historical Temperaments": [
            "Pythagorean", "Meantone (Quarter-comma)",
            "Werckmeister I-VI", "Kirnberger II-III",
            "Valotti", "Young", "Neidhardt I & III",
            "Rameau", "Kellner (Bach)"
        ],
        "Just Intonation": [
            "5-limit JI", "7-limit JI", "11-limit JI",
            "Partch 43-tone", "Harmonic Series", "Subharmonic Series"
        ],
        "Wendy Carlos Scales": [
            "Alpha (9-EDO)", "Beta (11-EDO)",
            "Gamma (20.5-EDO)", "Lambda (non-octave)"
        ],
        "Exotic & Experimental": [
            "Bohlen-Pierce (13-EDTriT)", "Golden Ratio (phi-based)",
            "Stretched Octave (Railsback)"
        ],
        "Arabic Maqamat": [
            "Rast", "Bayati", "Hijaz", "Saba", "Nahawand",
            "Segah", "Huseyni", "Huzzam", "Karcigar"
        ],
        "Persian Dastgahs": [
            "Shur", "Homayun", "Segah", "Chahargah"
        ],
        "Indian Ragas": [
            "Bhairav", "Yaman", "Todi", "Bhairavi", "Marwa", "Purvi"
        ],
        "Indonesian Gamelan": [
            "Pelog", "Slendro", "Pelog Barang", "Pelog Bien"
        ],
        "Japanese Scales": [
            "Hirajoshi", "Insen", "Iwato", "Yo", "In"
        ],
        "Chinese Scales": [
            "Pentatonic", "Yu mode", "Zhi mode"
        ],
        "Other World Music": [
            "Thai Thang", "Thai Piphat",
            "Ethiopian Anchihoye", "Brazilian Samba/Toada",
            "Escala Enigmatica"
        ]
    }

    return catalog


def analyze_scale_family(scale: MicrotonalScale) -> Dict[str, any]:
    """
    Determine which family/tradition a scale belongs to

    Args:
        scale: Scale to analyze

    Returns:
        Analysis results with family classification
    """
    analysis = {
        'scale_name': scale.name,
        'num_degrees': len(scale.intervals_cents),
        'possible_families': [],
        'characteristics': []
    }

    num_degrees = len(scale.intervals_cents)

    # Check for pentatonic
    if num_degrees == 5:
        analysis['possible_families'].append('Pentatonic')
        analysis['characteristics'].append('Five-note scale')

    # Check for heptatonic (7-note)
    if num_degrees == 7:
        analysis['possible_families'].append('Heptatonic')
        analysis['characteristics'].append('Seven-note scale (common in Western music)')

    # Check for microtonal content
    has_microtones = any(
        abs(interval - round(interval / 100) * 100) > 10
        for interval in scale.intervals_cents
    )

    if has_microtones:
        analysis['possible_families'].append('Microtonal')
        analysis['characteristics'].append('Contains microtonal intervals')

    # Check for equal temperament
    if num_degrees > 0:
        expected_step = 1200.0 / num_degrees
        steps_between = []
        for i in range(len(scale.intervals_cents) - 1):
            step = scale.intervals_cents[i + 1] - scale.intervals_cents[i]
            steps_between.append(step)

        if steps_between:
            avg_step = sum(steps_between) / len(steps_between)
            variance = sum((s - avg_step) ** 2 for s in steps_between) / len(steps_between)

            if variance < 10:  # Very uniform
                analysis['possible_families'].append('Equal Temperament')
                analysis['characteristics'].append(f'Approximately {num_degrees}-EDO')

    return analysis


def calculate_scale_compatibility(
    scale1: MicrotonalScale,
    scale2: MicrotonalScale
) -> float:
    """
    Calculate how compatible two scales are for modulation

    Args:
        scale1: First scale
        scale2: Second scale

    Returns:
        Compatibility score (0.0 = incompatible, 1.0 = highly compatible)
    """
    # Find common pitches
    common = find_common_pitches(scale1, scale2, tolerance_cents=10.0)

    # Calculate overlap percentage
    max_degrees = max(len(scale1.intervals_cents), len(scale2.intervals_cents))
    overlap_ratio = len(common) / max_degrees if max_degrees > 0 else 0.0

    # Check interval similarity
    comparison = compare_scales(scale1, scale2)
    similarity = comparison['similarity_score']

    # Combine factors
    compatibility = (overlap_ratio * 0.6) + (similarity * 0.4)

    return compatibility


def export_scala_file(
    scale: MicrotonalScale,
    path: Union[str, Path],
    description: Optional[str] = None
) -> Path:
    """
    Export a microtonal scale to Scala (.scl) format.

    Scala is the industry-standard format for microtonal scales,
    widely supported by synthesizers and music software.

    Args:
        scale: MicrotonalScale to export
        path: Output file path (should end in .scl)
        description: Optional description line (defaults to scale name)

    Returns:
        Path to the created file

    Example:
        >>> from cancrizans.microtonal import create_tuning_system_scale, TuningSystem
        >>> scale = create_tuning_system_scale(TuningSystem.WERCKMEISTER_III, 60)
        >>> export_scala_file(scale, 'werckmeister.scl')
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if description is None:
        description = scale.name

    # Scala format:
    # Line 1: Description
    # Line 2: Number of notes (excluding 1/1)
    # Lines 3+: Each interval in cents or ratio format

    lines = []
    lines.append(f"! {description}")
    lines.append("!")

    # Count non-zero intervals (excluding the tonic)
    intervals = [c for c in scale.intervals_cents if c > 0.0]
    lines.append(str(len(intervals)))
    lines.append("!")

    # Write each interval in cents
    for cents in intervals:
        lines.append(f"{cents:.6f}")

    # Write file
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

    return path


def import_scala_file(
    path: Union[str, Path],
    tonic_midi: int = 60,
    name: Optional[str] = None
) -> MicrotonalScale:
    """
    Import a microtonal scale from Scala (.scl) format.

    Scala is the industry-standard format for microtonal scales.
    This function supports both cents and ratio formats.

    Args:
        path: Path to .scl file
        tonic_midi: MIDI note number for the tonic (default: 60 = middle C)
        name: Optional name override (defaults to description from file)

    Returns:
        MicrotonalScale object

    Example:
        >>> scale = import_scala_file('my_scale.scl', tonic_midi=60)
        >>> print(scale.name)
        >>> print(len(scale.intervals_cents))
    """
    path = Path(path)

    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Parse Scala format
    # Skip comment lines (starting with !)
    non_comment_lines = []
    description = None

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('!'):
            # First non-empty comment might be description
            if description is None and len(line) > 1:
                description = line[1:].strip()
            continue
        non_comment_lines.append(line)

    if len(non_comment_lines) < 2:
        raise ValueError("Invalid Scala file: too few lines")

    # First non-comment line is the description (if not already found)
    if description is None:
        description = non_comment_lines[0]
        non_comment_lines = non_comment_lines[1:]

    # Second line is the number of notes
    try:
        num_notes = int(non_comment_lines[0])
    except (ValueError, IndexError):
        raise ValueError("Invalid Scala file: cannot parse number of notes")

    # Remaining lines are the intervals
    interval_lines = non_comment_lines[1:num_notes + 1]

    intervals_cents = [0.0]  # Always start with tonic at 0 cents

    for interval_line in interval_lines:
        interval_line = interval_line.strip()
        if not interval_line:
            continue

        # Parse interval (can be cents with decimal point, or ratio)
        if '.' in interval_line:
            # Cents format
            try:
                cents = float(interval_line)
                intervals_cents.append(cents)
            except ValueError:
                raise ValueError(f"Invalid cents value: {interval_line}")
        elif '/' in interval_line:
            # Ratio format (e.g., "3/2" for perfect fifth)
            try:
                parts = interval_line.split('/')
                numerator = float(parts[0])
                denominator = float(parts[1])
                ratio = numerator / denominator
                # Convert ratio to cents: 1200 * log2(ratio)
                cents = 1200.0 * math.log2(ratio)
                intervals_cents.append(cents)
            except (ValueError, IndexError, ZeroDivisionError):
                raise ValueError(f"Invalid ratio value: {interval_line}")
        else:
            # Integer cents
            try:
                cents = float(interval_line)
                intervals_cents.append(cents)
            except ValueError:
                raise ValueError(f"Invalid interval value: {interval_line}")

    # Use provided name or description from file
    scale_name = name if name is not None else description

    return MicrotonalScale(
        name=scale_name,
        intervals_cents=sorted(set(intervals_cents)),
        tonic_midi=tonic_midi
    )


# ============================================================================
# Microtonal Chord Theory
# ============================================================================

@dataclass
class MicrotonalChord:
    """Represents a chord built from microtonal intervals"""
    root: MicrotonalPitch
    intervals_cents: List[float]
    quality: str  # "consonant", "dissonant", "ambiguous"
    tension_score: float  # 0.0 = consonant, 1.0+ = dissonant
    chord_type: Optional[str] = None  # "triad", "tetrad", "cluster", etc.


def build_microtonal_chord(
    scale: MicrotonalScale,
    root_degree: int,
    num_notes: int = 3,
    skip_pattern: Optional[List[int]] = None
) -> MicrotonalChord:
    """
    Build a chord from a microtonal scale

    Args:
        scale: Source scale
        root_degree: Scale degree for chord root (0 = tonic)
        num_notes: Number of notes in chord
        skip_pattern: Pattern of scale degrees to skip (e.g., [0, 2, 4] for triad)
                     If None, uses consecutive scale degrees

    Returns:
        MicrotonalChord object
    """
    if root_degree >= len(scale.intervals_cents):
        raise ValueError(f"Root degree {root_degree} out of range")

    # Determine chord intervals
    if skip_pattern is None:
        # Use consecutive scale degrees
        skip_pattern = list(range(num_notes))

    chord_intervals = []
    for skip in skip_pattern[:num_notes]:
        degree = (root_degree + skip) % len(scale.intervals_cents)
        interval = scale.intervals_cents[degree]

        # Adjust for octave wrapping
        while interval < scale.intervals_cents[root_degree]:
            interval += 1200.0

        chord_intervals.append(interval - scale.intervals_cents[root_degree])

    # Calculate root pitch
    root_pitch = MicrotonalPitch(
        midi_note=scale.tonic_midi,
        cent_deviation=scale.intervals_cents[root_degree]
    )

    # Analyze chord quality
    tension = _calculate_chord_tension(chord_intervals)
    quality = _determine_chord_quality(tension)
    chord_type = _classify_chord_type(chord_intervals, num_notes)

    return MicrotonalChord(
        root=root_pitch,
        intervals_cents=chord_intervals,
        quality=quality,
        tension_score=tension,
        chord_type=chord_type
    )


def _calculate_chord_tension(intervals: List[float]) -> float:
    """Calculate tension/dissonance of chord intervals"""
    if len(intervals) < 2:
        return 0.0

    # Check for consonant intervals (octaves, fifths, fourths, thirds)
    consonant_ratios = {
        (2, 1): 0.0,   # Octave
        (3, 2): 0.1,   # Perfect fifth
        (4, 3): 0.15,  # Perfect fourth
        (5, 4): 0.2,   # Major third
        (6, 5): 0.25,  # Minor third
        (5, 3): 0.3,   # Major sixth
    }

    tension = 0.0
    num_intervals = 0

    for interval in intervals:
        if interval == 0.0:
            continue

        # Convert to ratio
        ratio = 2 ** (interval / 1200.0)

        # Find nearest simple ratio
        min_tension = 1.0
        for (num, den), base_tension in consonant_ratios.items():
            simple_ratio = num / den
            if abs(ratio - simple_ratio) < 0.05:  # Within 5%
                min_tension = min(min_tension, base_tension)

        # Penalize small intervals (semitones and smaller)
        if interval < 100:
            min_tension += 0.5

        tension += min_tension
        num_intervals += 1

    return tension / num_intervals if num_intervals > 0 else 0.0


def _determine_chord_quality(tension: float) -> str:
    """Determine chord quality from tension score"""
    if tension < 0.3:
        return "consonant"
    elif tension < 0.6:
        return "ambiguous"
    else:
        return "dissonant"


def _classify_chord_type(intervals: List[float], num_notes: int) -> str:
    """Classify chord type based on structure"""
    if num_notes == 2:
        return "dyad"
    elif num_notes == 3:
        return "triad"
    elif num_notes == 4:
        return "tetrad"
    elif num_notes == 5:
        return "pentad"
    elif num_notes >= 6:
        # Check if it's a cluster (all intervals < 200 cents)
        max_interval = max(intervals) if intervals else 0
        if max_interval < 200:
            return "cluster"
        return "polychord"

    return "chord"


def analyze_chord_consonance(chord: MicrotonalChord) -> Dict[str, any]:
    """
    Analyze the consonance properties of a microtonal chord

    Args:
        chord: Chord to analyze

    Returns:
        Dictionary with analysis results
    """
    analysis = {
        'quality': chord.quality,
        'tension_score': chord.tension_score,
        'chord_type': chord.chord_type,
        'num_notes': len(chord.intervals_cents),
        'interval_analysis': [],
        'harmonic_series_alignment': 0.0
    }

    # Analyze each interval
    for i, interval in enumerate(chord.intervals_cents):
        if interval == 0.0:
            continue

        ratio = 2 ** (interval / 1200.0)
        interval_info = {
            'cents': interval,
            'ratio': ratio,
            'simple_ratio_approximation': _find_simple_ratio(ratio)
        }
        analysis['interval_analysis'].append(interval_info)

    # Check alignment with harmonic series
    if len(chord.intervals_cents) > 1:
        alignment = _check_harmonic_series_alignment(chord.intervals_cents)
        analysis['harmonic_series_alignment'] = alignment

    return analysis


def _find_simple_ratio(ratio: float, max_denominator: int = 16) -> Optional[Tuple[int, int]]:
    """Find simple ratio approximation"""
    best_error = float('inf')
    best_ratio = None

    for den in range(1, max_denominator + 1):
        num = round(ratio * den)
        if num == 0:
            continue

        test_ratio = num / den
        error = abs(ratio - test_ratio)

        if error < best_error:
            best_error = error
            best_ratio = (num, den)

    if best_error < 0.01:  # Within 1%
        return best_ratio
    return None


def _check_harmonic_series_alignment(intervals: List[float]) -> float:
    """Check how well intervals align with harmonic series"""
    if not intervals:
        return 0.0

    # Harmonic series ratios: 1:2:3:4:5:6:7:8...
    harmonic_ratios = [i for i in range(1, 17)]

    alignment_score = 0.0
    for interval in intervals:
        if interval == 0.0:
            continue

        ratio = 2 ** (interval / 1200.0)

        # Find nearest harmonic
        min_distance = float('inf')
        for h in harmonic_ratios:
            distance = abs(ratio - h)
            min_distance = min(min_distance, distance)

        # Convert to score (closer = higher score)
        if min_distance < 0.1:
            alignment_score += 1.0 - min_distance

    return alignment_score / len([i for i in intervals if i != 0.0])


def generate_microtonal_chord_progression(
    scale: MicrotonalScale,
    num_chords: int = 4,
    chord_size: int = 3,
    progression_type: str = "ascending"
) -> List[MicrotonalChord]:
    """
    Generate a chord progression from a microtonal scale

    Args:
        scale: Source scale
        num_chords: Number of chords in progression
        chord_size: Notes per chord
        progression_type: "ascending", "descending", "circle_of_fifths", "random"

    Returns:
        List of microtonal chords
    """
    import random

    progression = []
    num_degrees = len(scale.intervals_cents)

    if progression_type == "ascending":
        root_degrees = [i % num_degrees for i in range(0, num_chords * 2, 2)]
    elif progression_type == "descending":
        root_degrees = [i % num_degrees for i in range(num_degrees - 1, num_degrees - 1 - num_chords * 2, -2)]
    elif progression_type == "circle_of_fifths":
        # Find interval closest to perfect fifth (700 cents)
        fifth_degree = min(range(num_degrees),
                          key=lambda d: abs(scale.intervals_cents[d] - 700))
        root_degrees = [(i * fifth_degree) % num_degrees for i in range(num_chords)]
    elif progression_type == "random":
        root_degrees = [random.randint(0, num_degrees - 1) for _ in range(num_chords)]
    else:
        raise ValueError(f"Unknown progression type: {progression_type}")

    for root_degree in root_degrees[:num_chords]:
        # Build tertian harmony (skip every other scale degree)
        skip_pattern = [i * 2 for i in range(chord_size)]
        chord = build_microtonal_chord(scale, root_degree, chord_size, skip_pattern)
        progression.append(chord)

    return progression


# ============================================================================
# Advanced Microtonal Transformations
# ============================================================================

def morph_scales(
    scale1: MicrotonalScale,
    scale2: MicrotonalScale,
    num_steps: int = 10,
    interpolation: str = "linear"
) -> List[MicrotonalScale]:
    """
    Create a smooth morphing sequence between two scales

    Args:
        scale1: Starting scale
        scale2: Ending scale
        num_steps: Number of intermediate steps
        interpolation: "linear", "ease_in", "ease_out", "ease_in_out"

    Returns:
        List of scales forming a morph sequence
    """
    morph_sequence = [scale1]

    for step in range(1, num_steps + 1):
        # Calculate interpolation weight
        t = step / (num_steps + 1)

        # Apply easing function
        if interpolation == "ease_in":
            t = t * t
        elif interpolation == "ease_out":
            t = 1 - (1 - t) * (1 - t)
        elif interpolation == "ease_in_out":
            t = 3 * t * t - 2 * t * t * t
        # else: linear (no change to t)

        # Blend scales with interpolated weight
        morphed = blend_scales(scale1, scale2, t)
        morph_sequence.append(morphed)

    morph_sequence.append(scale2)

    return morph_sequence


def stretch_scale(
    scale: MicrotonalScale,
    stretch_factor: float,
    preserve_octave: bool = True
) -> MicrotonalScale:
    """
    Stretch or compress all intervals in a scale

    Args:
        scale: Source scale
        stretch_factor: Multiplier for intervals (>1 = stretch, <1 = compress)
        preserve_octave: If True, scale octave back to 1200 cents

    Returns:
        Transformed scale
    """
    stretched_intervals = [0.0]

    for interval in scale.intervals_cents[1:]:  # Skip tonic
        stretched = interval * stretch_factor
        stretched_intervals.append(stretched)

    # Normalize to preserve octave if requested
    if preserve_octave and stretched_intervals:
        max_interval = max(stretched_intervals)
        if max_interval > 0:
            octave_ratio = 1200.0 / max_interval
            stretched_intervals = [i * octave_ratio for i in stretched_intervals]

    return MicrotonalScale(
        name=f"{scale.name} (stretch {stretch_factor:.2f}x)",
        intervals_cents=stretched_intervals,
        tonic_midi=scale.tonic_midi
    )


def extract_scale_subset(
    scale: MicrotonalScale,
    num_degrees: int,
    method: str = "even"
) -> MicrotonalScale:
    """
    Extract a subset of scale degrees

    Args:
        scale: Source scale
        num_degrees: Number of degrees to extract
        method: "even" (evenly spaced), "low" (lowest degrees), "high" (highest degrees)

    Returns:
        New scale with subset of degrees
    """
    total_degrees = len(scale.intervals_cents)

    if num_degrees >= total_degrees:
        return scale

    if method == "even":
        # Evenly spaced degrees
        step = total_degrees / num_degrees
        indices = [int(i * step) for i in range(num_degrees)]
    elif method == "low":
        indices = list(range(num_degrees))
    elif method == "high":
        indices = list(range(total_degrees - num_degrees, total_degrees))
    else:
        raise ValueError(f"Unknown method: {method}")

    subset_intervals = [scale.intervals_cents[i] for i in indices]

    return MicrotonalScale(
        name=f"{scale.name} ({num_degrees}-subset)",
        intervals_cents=subset_intervals,
        tonic_midi=scale.tonic_midi
    )


def create_equal_division_scale(
    num_divisions: int,
    interval_cents: float = 1200.0,
    tonic_midi: int = 60
) -> MicrotonalScale:
    """
    Create a scale with equal divisions of an interval

    Args:
        num_divisions: Number of equal divisions
        interval_cents: Interval to divide (default: 1200 = octave)
        tonic_midi: MIDI note for tonic

    Returns:
        Equal division scale

    Example:
        >>> # 19-TET (19 equal divisions of octave)
        >>> scale = create_equal_division_scale(19)
        >>> # Bohlen-Pierce (13 equal divisions of 3:1 tritave)
        >>> bp_scale = create_equal_division_scale(13, 1901.955)  # 1200 * log2(3)
    """
    step_size = interval_cents / num_divisions
    intervals = [i * step_size for i in range(num_divisions + 1)]

    interval_name = "octave" if abs(interval_cents - 1200.0) < 1 else f"{interval_cents:.0f}c"

    return MicrotonalScale(
        name=f"{num_divisions}-ED{interval_name}",
        intervals_cents=intervals,
        tonic_midi=tonic_midi
    )


def rotate_scale_intervals(
    scale: MicrotonalScale,
    rotation_cents: float
) -> MicrotonalScale:
    """
    Rotate all intervals by a fixed amount

    Args:
        scale: Source scale
        rotation_cents: Amount to rotate (in cents)

    Returns:
        Rotated scale
    """
    rotated_intervals = []

    for interval in scale.intervals_cents:
        rotated = (interval + rotation_cents) % 1200.0
        rotated_intervals.append(rotated)

    return MicrotonalScale(
        name=f"{scale.name} (rotated {rotation_cents:.0f}c)",
        intervals_cents=sorted(set(rotated_intervals)),
        tonic_midi=scale.tonic_midi
    )


def merge_scales(
    *scales: MicrotonalScale,
    tolerance_cents: float = 5.0
) -> MicrotonalScale:
    """
    Merge multiple scales into one, combining all unique intervals

    Args:
        *scales: Scales to merge
        tolerance_cents: Intervals within this tolerance are considered identical

    Returns:
        Merged scale containing all unique intervals
    """
    if not scales:
        raise ValueError("At least one scale required")

    all_intervals = []
    for scale in scales:
        all_intervals.extend(scale.intervals_cents)

    # Remove duplicates within tolerance
    unique_intervals = [0.0]
    for interval in sorted(set(all_intervals)):
        if interval == 0.0:
            continue

        # Check if this interval is close to any existing one
        is_duplicate = False
        for existing in unique_intervals:
            if abs(interval - existing) < tolerance_cents:
                is_duplicate = True
                break

        if not is_duplicate:
            unique_intervals.append(interval)

    scale_names = " + ".join(s.name for s in scales[:3])
    if len(scales) > 3:
        scale_names += f" + {len(scales) - 3} more"

    return MicrotonalScale(
        name=f"Merged: {scale_names}",
        intervals_cents=sorted(unique_intervals),
        tonic_midi=scales[0].tonic_midi
    )
