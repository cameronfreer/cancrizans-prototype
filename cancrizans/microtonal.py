"""
Microtonal & Cross-Cultural Canon Systems

This module provides support for microtonal scales, world music systems,
xenharmonic canons, and non-Western musical traditions.

Phase 18 - v0.35.0
"""

from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import math
from music21 import stream, note, pitch, interval
from music21.pitch import Microtone


class TuningSystem(Enum):
    """Historical and contemporary tuning systems"""
    EQUAL_12 = "12-tone equal temperament"
    EQUAL_19 = "19-tone equal temperament"
    EQUAL_24 = "24-tone equal temperament (quarter tones)"
    EQUAL_31 = "31-tone equal temperament"
    EQUAL_53 = "53-tone equal temperament"
    JUST_INTONATION = "5-limit just intonation"
    PYTHAGOREAN = "Pythagorean tuning"
    MEANTONE = "Quarter-comma meantone"
    WERCKMEISTER_III = "Werckmeister III"
    BOHLEN_PIERCE = "Bohlen-Pierce scale"


class ScaleType(Enum):
    """World music scale types"""
    # Middle Eastern
    MAQAM_RAST = "Arabic maqam Rast"
    MAQAM_BAYATI = "Arabic maqam Bayati"
    MAQAM_HIJAZ = "Arabic maqam Hijaz"
    MAQAM_SABA = "Arabic maqam Saba"
    MAQAM_NAHAWAND = "Arabic maqam Nahawand"

    # Indian
    RAGA_BHAIRAV = "Hindustani raga Bhairav"
    RAGA_YAMAN = "Hindustani raga Yaman"
    RAGA_TODI = "Hindustani raga Todi"
    RAGA_BHAIRAVI = "Hindustani raga Bhairavi"

    # Indonesian
    PELOG = "Javanese Pelog"
    SLENDRO = "Javanese Slendro"

    # Japanese
    HIRAJOSHI = "Japanese Hirajoshi"
    INSEN = "Japanese Insen"
    IWATO = "Japanese Iwato"

    # Chinese
    PENTATONIC_CHINESE = "Chinese pentatonic"

    # Persian
    DASTGAH_SHUR = "Persian dastgah Shur"
    DASTGAH_HOMAYUN = "Persian dastgah Homayun"


@dataclass
class MicrotonalPitch:
    """
    Represents a microtonal pitch with precise frequency

    Attributes:
        midi_note: Base MIDI note number
        cent_deviation: Deviation from equal temperament in cents (-100 to +100)
        frequency_hz: Exact frequency in Hz
    """
    midi_note: int
    cent_deviation: float = 0.0
    frequency_hz: Optional[float] = None

    def __post_init__(self):
        if self.frequency_hz is None:
            # Calculate frequency from MIDI + cents
            self.frequency_hz = 440.0 * (2 ** ((self.midi_note - 69 + self.cent_deviation / 100.0) / 12.0))

    def to_cents_from_c0(self) -> float:
        """Get pitch in cents from C0"""
        return self.midi_note * 100 + self.cent_deviation


@dataclass
class MicrotonalScale:
    """
    Defines a microtonal scale

    Attributes:
        name: Scale name
        intervals_cents: List of intervals in cents from tonic
        tonic_midi: MIDI note number of tonic
        tuning_system: Associated tuning system
    """
    name: str
    intervals_cents: List[float]
    tonic_midi: int = 60  # Middle C
    tuning_system: Optional[TuningSystem] = None

    def get_pitches(self, octaves: int = 1) -> List[MicrotonalPitch]:
        """
        Get all pitches in the scale

        Args:
            octaves: Number of octaves to generate

        Returns:
            List of microtonal pitches
        """
        pitches = []

        for octave in range(octaves):
            octave_offset = octave * 1200  # 1200 cents = 1 octave

            for interval_cents in self.intervals_cents:
                total_cents = interval_cents + octave_offset
                midi_semitones = int(total_cents / 100)
                cent_deviation = total_cents % 100

                pitch = MicrotonalPitch(
                    midi_note=self.tonic_midi + midi_semitones,
                    cent_deviation=cent_deviation
                )
                pitches.append(pitch)

        return pitches


def create_equal_temperament(divisions: int, octave_cents: float = 1200.0) -> MicrotonalScale:
    """
    Create N-tone equal temperament scale

    Args:
        divisions: Number of equal divisions per octave
        octave_cents: Size of octave in cents (1200.0 for standard octave)

    Returns:
        Microtonal scale

    Example:
        >>> scale = create_equal_temperament(19)  # 19-TET
        >>> scale = create_equal_temperament(13, 1200 * (3/2))  # Bohlen-Pierce (13-EDTriT)
    """
    step_cents = octave_cents / divisions
    intervals = [i * step_cents for i in range(divisions)]

    return MicrotonalScale(
        name=f"{divisions}-TET",
        intervals_cents=intervals,
        tuning_system=TuningSystem.EQUAL_12 if divisions == 12 else None
    )


def create_just_intonation_scale(ratios: List[Tuple[int, int]]) -> MicrotonalScale:
    """
    Create scale from just intonation ratios

    Args:
        ratios: List of (numerator, denominator) tuples

    Returns:
        Microtonal scale

    Example:
        >>> # Ptolemy's intense diatonic
        >>> ratios = [(1, 1), (9, 8), (5, 4), (4, 3), (3, 2), (5, 3), (15, 8)]
        >>> scale = create_just_intonation_scale(ratios)
    """
    intervals_cents = []

    for num, denom in ratios:
        ratio = num / denom
        cents = 1200.0 * math.log2(ratio)
        intervals_cents.append(cents)

    return MicrotonalScale(
        name="Just Intonation",
        intervals_cents=intervals_cents,
        tuning_system=TuningSystem.JUST_INTONATION
    )


def create_pythagorean_scale() -> MicrotonalScale:
    """
    Create Pythagorean tuning (based on 3:2 perfect fifths)

    Returns:
        Microtonal scale
    """
    # Build from stacked fifths
    fifth_cents = 1200.0 * math.log2(3/2)

    # Circle of fifths: F C G D A E B
    fifths_from_c = [0, 1, 2, 3, 4, -1, -2]  # C D E F G A B

    intervals = []
    for fifths in sorted(fifths_from_c):
        cents = (fifths * fifth_cents) % 1200.0
        intervals.append(cents)

    return MicrotonalScale(
        name="Pythagorean",
        intervals_cents=sorted(intervals),
        tuning_system=TuningSystem.PYTHAGOREAN
    )


def create_world_music_scale(scale_type: ScaleType, tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create world music scale

    Args:
        scale_type: Type of world music scale
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    scale_definitions = {
        # Arabic Maqamat (approximate quarter tones)
        ScaleType.MAQAM_RAST: [0, 200, 350, 500, 700, 900, 1050],
        ScaleType.MAQAM_BAYATI: [0, 150, 300, 500, 700, 850, 1000],
        ScaleType.MAQAM_HIJAZ: [0, 100, 400, 500, 700, 800, 1100],
        ScaleType.MAQAM_SABA: [0, 150, 300, 400, 600, 850, 1000],
        ScaleType.MAQAM_NAHAWAND: [0, 200, 300, 500, 700, 800, 1000],

        # Indian Ragas (approximate)
        ScaleType.RAGA_BHAIRAV: [0, 100, 400, 500, 700, 800, 1100],
        ScaleType.RAGA_YAMAN: [0, 200, 400, 600, 700, 900, 1100],
        ScaleType.RAGA_TODI: [0, 100, 300, 600, 700, 800, 1100],
        ScaleType.RAGA_BHAIRAVI: [0, 100, 300, 500, 700, 800, 1000],

        # Javanese (very approximate - actual gamelan tuning varies)
        ScaleType.PELOG: [0, 136, 384, 600, 816, 1032],  # 5-note approximation
        ScaleType.SLENDRO: [0, 240, 480, 720, 960],  # 5-note equal divisions

        # Japanese
        ScaleType.HIRAJOSHI: [0, 200, 300, 700, 800],
        ScaleType.INSEN: [0, 100, 500, 700, 1000],
        ScaleType.IWATO: [0, 100, 500, 600, 1000],

        # Chinese
        ScaleType.PENTATONIC_CHINESE: [0, 200, 400, 700, 900],

        # Persian
        ScaleType.DASTGAH_SHUR: [0, 150, 350, 500, 700, 850, 1050],
        ScaleType.DASTGAH_HOMAYUN: [0, 150, 350, 450, 700, 800, 1050],
    }

    if scale_type not in scale_definitions:
        raise ValueError(f"Unknown scale type: {scale_type}")

    return MicrotonalScale(
        name=scale_type.value,
        intervals_cents=scale_definitions[scale_type],
        tonic_midi=tonic_midi
    )


def xenharmonic_canon(
    base_stream: stream.Stream,
    divisions_per_octave: int = 19,
    transformation: str = "retrograde"
) -> stream.Stream:
    """
    Create xenharmonic canon using N-TET tuning

    Args:
        base_stream: Input stream in 12-TET
        divisions_per_octave: N for N-TET (e.g., 19, 24, 31)
        transformation: Transformation type ('retrograde', 'inversion', 'mirror')

    Returns:
        Transformed stream with microtonal pitches
    """
    scale = create_equal_temperament(divisions_per_octave)
    result = stream.Stream()

    # Map 12-TET pitches to N-TET
    step_cents = 1200.0 / divisions_per_octave

    for element in base_stream.flatten().notesAndRests:
        if isinstance(element, note.Note):
            # Map to closest N-TET pitch
            midi_float = element.pitch.midi + element.pitch.microtone.cents / 100.0
            cents_from_c0 = midi_float * 100.0

            # Quantize to N-TET
            steps = round(cents_from_c0 / step_cents)
            new_cents = steps * step_cents

            new_midi = int(new_cents / 100.0)
            new_cent_deviation = new_cents % 100.0

            n = note.Note()
            n.pitch.midi = new_midi
            n.pitch.microtone = Microtone(new_cent_deviation)
            n.quarterLength = element.quarterLength
            n.offset = element.offset

            result.append(n)
        else:
            result.append(element)

    # Apply transformation
    if transformation == "retrograde":
        result = result.sorted()
        total_length = result.highestTime
        for n in result.flatten().notes:
            n.offset = total_length - n.offset - n.quarterLength

    return result


def microtonal_inversion(
    s: stream.Stream,
    scale: MicrotonalScale,
    axis_cents: Optional[float] = None
) -> stream.Stream:
    """
    Invert stream within microtonal scale

    Args:
        s: Input stream
        scale: Microtonal scale to use
        axis_cents: Inversion axis in cents from C0 (default: middle of scale)

    Returns:
        Inverted stream
    """
    pitches = scale.get_pitches(octaves=8)
    pitch_cents = [p.to_cents_from_c0() for p in pitches]

    if axis_cents is None:
        axis_cents = (min(pitch_cents) + max(pitch_cents)) / 2.0

    result = stream.Stream()

    for element in s.flatten().notesAndRests:
        if isinstance(element, note.Note):
            # Get current pitch in cents
            current_cents = element.pitch.midi * 100.0 + element.pitch.microtone.cents

            # Invert around axis
            inverted_cents = 2 * axis_cents - current_cents

            # Find closest scale degree
            closest_idx = min(range(len(pitch_cents)), key=lambda i: abs(pitch_cents[i] - inverted_cents))
            closest_pitch = pitches[closest_idx]

            n = note.Note()
            n.pitch.midi = closest_pitch.midi_note
            n.pitch.microtone = Microtone(closest_pitch.cent_deviation)
            n.quarterLength = element.quarterLength
            n.offset = element.offset

            result.append(n)
        else:
            result.append(element)

    return result


def analyze_microtonal_intervals(s: stream.Stream) -> Dict[str, any]:
    """
    Analyze microtonal intervals in stream

    Args:
        s: Stream to analyze

    Returns:
        Dictionary with interval analysis
    """
    intervals_cents = []
    notes = list(s.flatten().notes)

    # Check if any notes have microtonal deviations (even with one note)
    contains_microtones = any(abs(n.pitch.microtone.cents) > 1.0 for n in notes)

    for i in range(len(notes) - 1):
        n1 = notes[i]
        n2 = notes[i + 1]

        cents1 = n1.pitch.midi * 100.0 + n1.pitch.microtone.cents
        cents2 = n2.pitch.midi * 100.0 + n2.pitch.microtone.cents

        interval_cents = abs(cents2 - cents1)
        intervals_cents.append(interval_cents)

    if not intervals_cents:
        return {
            'interval_count': 0,
            'smallest_interval_cents': 0,
            'largest_interval_cents': 0,
            'average_interval_cents': 0,
            'contains_microtones': contains_microtones
        }

    return {
        'interval_count': len(intervals_cents),
        'smallest_interval_cents': min(intervals_cents),
        'largest_interval_cents': max(intervals_cents),
        'average_interval_cents': sum(intervals_cents) / len(intervals_cents),
        'contains_microtones': contains_microtones,
        'interval_distribution': {
            'micro_intervals': sum(1 for i in intervals_cents if i < 100),  # < semitone
            'semitones': sum(1 for i in intervals_cents if 90 <= i < 110),
            'large_intervals': sum(1 for i in intervals_cents if i >= 200)
        }
    }


def bohlen_pierce_scale(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create Bohlen-Pierce scale (13 equal divisions of 3:1 "tritave")

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    # Bohlen-Pierce uses 3:1 instead of 2:1
    tritave_cents = 1200.0 * math.log2(3)  # ≈ 1901.955 cents
    step_cents = tritave_cents / 13

    intervals = [i * step_cents for i in range(13)]

    return MicrotonalScale(
        name="Bohlen-Pierce",
        intervals_cents=intervals,
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.BOHLEN_PIERCE
    )


def gamma_scale(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create Wendy Carlos' Gamma scale (20.5 equal divisions of octave)

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    divisions = 20.5
    step_cents = 1200.0 / divisions

    # Generate scale degrees
    intervals = []
    current = 0.0
    while current < 1200.0:
        intervals.append(current)
        current += step_cents

    return MicrotonalScale(
        name="Gamma Scale (Carlos)",
        intervals_cents=intervals,
        tonic_midi=tonic_midi
    )


def detect_tuning_system(s: stream.Stream) -> Tuple[TuningSystem, float]:
    """
    Detect most likely tuning system used in stream

    Args:
        s: Stream to analyze

    Returns:
        Tuple of (detected tuning system, confidence score 0-1)
    """
    notes = list(s.flatten().notes)

    if not notes:
        return TuningSystem.EQUAL_12, 0.0

    # Get all pitch classes in cents
    pitch_cents = []
    for n in notes:
        cents = (n.pitch.midi % 12) * 100.0 + n.pitch.microtone.cents
        pitch_cents.append(cents)

    # Test against different tuning systems
    scores = {}

    # 12-TET
    tet12_errors = [min(abs(cents - (i * 100)) for i in range(12)) for cents in pitch_cents]
    scores[TuningSystem.EQUAL_12] = 1.0 - (sum(tet12_errors) / (len(tet12_errors) * 50.0))

    # Pythagorean
    pyth_scale = create_pythagorean_scale()
    pyth_cents = pyth_scale.intervals_cents
    pyth_errors = [min(abs(cents - pc) for pc in pyth_cents) for cents in pitch_cents]
    scores[TuningSystem.PYTHAGOREAN] = 1.0 - (sum(pyth_errors) / (len(pyth_errors) * 50.0))

    # Just Intonation (5-limit)
    just_ratios = [(1, 1), (16, 15), (9, 8), (6, 5), (5, 4), (4, 3),
                   (45, 32), (3, 2), (8, 5), (5, 3), (9, 5), (15, 8)]
    just_scale = create_just_intonation_scale(just_ratios)
    just_cents = just_scale.intervals_cents
    just_errors = [min(abs(cents - jc) for jc in just_cents) for cents in pitch_cents]
    scores[TuningSystem.JUST_INTONATION] = 1.0 - (sum(just_errors) / (len(just_errors) * 50.0))

    # Find best match
    best_system = max(scores, key=scores.get)
    confidence = max(0.0, min(1.0, scores[best_system]))

    return best_system, confidence


def cross_cultural_canon_analysis(s: stream.Stream) -> Dict[str, any]:
    """
    Analyze stream for cross-cultural musical characteristics

    Args:
        s: Stream to analyze

    Returns:
        Dictionary with cultural analysis
    """
    analysis = {
        'tuning_system': None,
        'tuning_confidence': 0.0,
        'microtonal_content': False,
        'possible_scales': [],
        'interval_characteristics': {}
    }

    # Detect tuning
    tuning, confidence = detect_tuning_system(s)
    analysis['tuning_system'] = tuning.value
    analysis['tuning_confidence'] = confidence

    # Analyze intervals
    interval_data = analyze_microtonal_intervals(s)
    analysis['microtonal_content'] = interval_data['contains_microtones']
    analysis['interval_characteristics'] = interval_data

    # Check against world scales
    notes = list(s.flatten().notes)
    if notes:
        pitch_classes = sorted(set((n.pitch.midi % 12) * 100 + n.pitch.microtone.cents for n in notes))

        # Test against various world scales
        for scale_type in ScaleType:
            try:
                world_scale = create_world_music_scale(scale_type, tonic_midi=60)
                scale_pcs = [c % 1200 for c in world_scale.intervals_cents]

                # Calculate match
                errors = [min(abs(pc - spc) for spc in scale_pcs) for pc in pitch_classes]
                avg_error = sum(errors) / len(errors) if errors else float('inf')

                if avg_error < 30:  # Within 30 cents
                    analysis['possible_scales'].append({
                        'scale': scale_type.value,
                        'match_quality': 1.0 - (avg_error / 30.0)
                    })
            except:
                pass

    # Sort by match quality
    analysis['possible_scales'].sort(key=lambda x: x['match_quality'], reverse=True)

    return analysis
