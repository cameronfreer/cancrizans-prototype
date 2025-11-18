"""
Microtonal Utility Functions & Helpers

Additional utility functions for working with microtonal music,
including scale transformation, comparison, and visualization helpers.

Phase 18.5 - v0.35.1
"""

from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
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
