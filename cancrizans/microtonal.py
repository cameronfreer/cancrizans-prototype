"""
Microtonal & Cross-Cultural Canon Systems

This module provides support for microtonal scales, world music systems,
xenharmonic canons, and non-Western musical traditions.

Phase 18 - v0.35.0
"""

from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass, replace
from enum import Enum
import math
from music21 import stream, note, pitch, interval
from music21.pitch import Microtone


class TuningSystem(Enum):
    """Historical and contemporary tuning systems"""
    # Equal temperaments (common microtonal divisions)
    EQUAL_12 = "12-tone equal temperament"
    EQUAL_17 = "17-tone equal temperament"
    EQUAL_19 = "19-tone equal temperament"
    EQUAL_22 = "22-tone equal temperament (Shrutar)"
    EQUAL_24 = "24-tone equal temperament (quarter tones)"
    EQUAL_31 = "31-tone equal temperament"
    EQUAL_34 = "34-tone equal temperament"
    EQUAL_41 = "41-tone equal temperament"
    EQUAL_53 = "53-tone equal temperament"
    EQUAL_72 = "72-tone equal temperament (twelfth tones)"

    # Just intonation systems
    JUST_INTONATION_5 = "5-limit just intonation"
    JUST_INTONATION_7 = "7-limit just intonation"
    JUST_INTONATION_11 = "11-limit just intonation"
    PARTCH_43 = "Harry Partch 43-tone scale"

    # Historical temperaments
    PYTHAGOREAN = "Pythagorean tuning"
    MEANTONE = "Quarter-comma meantone"

    # Well temperaments
    WERCKMEISTER_I = "Werckmeister I (correct temperament)"
    WERCKMEISTER_II = "Werckmeister II"
    WERCKMEISTER_III = "Werckmeister III"
    WERCKMEISTER_IV = "Werckmeister IV"
    WERCKMEISTER_V = "Werckmeister V"
    WERCKMEISTER_VI = "Werckmeister VI (Septenarius)"
    VALOTTI = "Valotti temperament"
    KIRNBERGER_II = "Kirnberger II"
    KIRNBERGER_III = "Kirnberger III"
    YOUNG = "Young temperament"
    NEIDHARDT_I = "Neidhardt I (1724)"
    NEIDHARDT_III = "Neidhardt III (1732)"
    RAMEAU = "Rameau temperament"
    KELLNER = "Kellner (Bach's temperament)"

    # Wendy Carlos scales
    ALPHA = "Alpha scale (Carlos)"
    BETA = "Beta scale (Carlos)"
    GAMMA = "Gamma scale (Carlos)"

    # Non-octave scales
    BOHLEN_PIERCE = "Bohlen-Pierce scale"

    # Exotic and experimental
    GOLDEN_RATIO = "Golden ratio (phi) tuning"
    HARMONIC_SERIES = "Harmonic series tuning"
    STRETCHED_OCTAVE = "Stretched octave (Railsback curve)"
    LAMBDA = "Wendy Carlos Lambda scale"
    PHI_BASED = "Phi-based non-octave tuning"


class ScaleType(Enum):
    """World music scale types"""
    # Middle Eastern (Arabic)
    MAQAM_RAST = "Arabic maqam Rast"
    MAQAM_BAYATI = "Arabic maqam Bayati"
    MAQAM_HIJAZ = "Arabic maqam Hijaz"
    MAQAM_SABA = "Arabic maqam Saba"
    MAQAM_NAHAWAND = "Arabic maqam Nahawand"

    # Turkish/Ottoman
    MAQAM_SEGAH = "Turkish maqam Segah"
    MAQAM_HUSEYNI = "Turkish maqam Huseyni"
    MAQAM_HUZZAM = "Turkish maqam Huzzam"
    MAQAM_KARCIGAR = "Turkish maqam Karcigar"

    # Persian
    DASTGAH_SHUR = "Persian dastgah Shur"
    DASTGAH_HOMAYUN = "Persian dastgah Homayun"
    DASTGAH_SEGAH = "Persian dastgah Segah"
    DASTGAH_CHAHARGAH = "Persian dastgah Chahargah"

    # Indian (Hindustani)
    RAGA_BHAIRAV = "Hindustani raga Bhairav"
    RAGA_YAMAN = "Hindustani raga Yaman"
    RAGA_TODI = "Hindustani raga Todi"
    RAGA_BHAIRAVI = "Hindustani raga Bhairavi"
    RAGA_MARWA = "Hindustani raga Marwa"
    RAGA_PURVI = "Hindustani raga Purvi"

    # Indonesian
    PELOG = "Javanese Pelog"
    SLENDRO = "Javanese Slendro"
    PELOG_BARANG = "Javanese Pelog Barang"
    PELOG_BIEN = "Javanese Pelog Bien"

    # Japanese
    HIRAJOSHI = "Japanese Hirajoshi"
    INSEN = "Japanese Insen"
    IWATO = "Japanese Iwato"
    YO = "Japanese Yo scale"
    IN = "Japanese In scale"

    # Chinese
    PENTATONIC_CHINESE = "Chinese pentatonic"
    YU = "Chinese Yu mode"
    ZHI = "Chinese Zhi mode"

    # Thai
    THAI_THANG = "Thai thang scale"
    THAI_PIPHAT = "Thai piphat (7-tone)"

    # African
    AKEBONO = "West African pentatonic"
    RAGA_TODI_AFRICAN = "North African modal"
    ETHIOPIAN_ANCHIHOYE = "Ethiopian Anchihoye"

    # Latin American
    ESCALA_ENIGMATICA = "Escala Enigmatica"
    SAMBA_TOADA = "Brazilian Samba/Toada"


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
        tuning_system=TuningSystem.JUST_INTONATION_5
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

        # Turkish Maqamat (53-TET approximations)
        ScaleType.MAQAM_SEGAH: [0, 180, 360, 495, 700, 880, 1065],
        ScaleType.MAQAM_HUSEYNI: [0, 200, 360, 500, 700, 880, 1040],
        ScaleType.MAQAM_HUZZAM: [0, 135, 360, 495, 700, 815, 1040],
        ScaleType.MAQAM_KARCIGAR: [0, 200, 315, 500, 700, 880, 995],

        # Persian Dastgahs
        ScaleType.DASTGAH_SHUR: [0, 150, 350, 500, 700, 850, 1050],
        ScaleType.DASTGAH_HOMAYUN: [0, 150, 350, 450, 700, 800, 1050],
        ScaleType.DASTGAH_SEGAH: [0, 135, 360, 495, 700, 850, 1040],
        ScaleType.DASTGAH_CHAHARGAH: [0, 200, 400, 500, 700, 900, 1100],

        # Indian Ragas (approximate)
        ScaleType.RAGA_BHAIRAV: [0, 100, 400, 500, 700, 800, 1100],
        ScaleType.RAGA_YAMAN: [0, 200, 400, 600, 700, 900, 1100],
        ScaleType.RAGA_TODI: [0, 100, 300, 600, 700, 800, 1100],
        ScaleType.RAGA_BHAIRAVI: [0, 100, 300, 500, 700, 800, 1000],
        ScaleType.RAGA_MARWA: [0, 100, 400, 600, 700, 900, 1100],
        ScaleType.RAGA_PURVI: [0, 100, 400, 600, 700, 800, 1100],

        # Javanese (approximate - actual gamelan tuning varies by ensemble)
        ScaleType.PELOG: [0, 136, 384, 600, 816, 1032],  # 5-note approximation
        ScaleType.SLENDRO: [0, 240, 480, 720, 960],  # 5-note equal divisions
        ScaleType.PELOG_BARANG: [0, 265, 520, 785, 1050],  # Variant tuning
        ScaleType.PELOG_BIEN: [0, 120, 360, 600, 840, 1080],  # Another variant

        # Japanese
        ScaleType.HIRAJOSHI: [0, 200, 300, 700, 800],
        ScaleType.INSEN: [0, 100, 500, 700, 1000],
        ScaleType.IWATO: [0, 100, 500, 600, 1000],
        ScaleType.YO: [0, 200, 400, 700, 900],  # Major pentatonic
        ScaleType.IN: [0, 100, 400, 500, 800],  # Minor pentatonic variant

        # Chinese
        ScaleType.PENTATONIC_CHINESE: [0, 200, 400, 700, 900],
        ScaleType.YU: [0, 200, 400, 500, 700, 900, 1100],  # Yu mode (major-like)
        ScaleType.ZHI: [0, 200, 400, 700, 900, 1100],  # Zhi mode (6-note)

        # Thai
        ScaleType.THAI_THANG: [0, 200, 400, 600, 700, 900, 1100],  # 7-tone equal
        ScaleType.THAI_PIPHAT: [0, 171, 343, 514, 686, 857, 1029],  # 7-equal approximation

        # African
        ScaleType.AKEBONO: [0, 200, 300, 700, 800],  # West African pentatonic
        ScaleType.RAGA_TODI_AFRICAN: [0, 100, 350, 450, 700, 850, 1050],  # North African
        ScaleType.ETHIOPIAN_ANCHIHOYE: [0, 200, 400, 500, 700, 900, 1000],  # Ethiopian mode

        # Latin American
        ScaleType.ESCALA_ENIGMATICA: [0, 100, 400, 600, 800, 1000, 1100],  # Verdi scale
        ScaleType.SAMBA_TOADA: [0, 200, 300, 500, 700, 800, 1000],  # Brazilian traditional
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
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.GAMMA
    )


def alpha_scale(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create Wendy Carlos' Alpha scale (9 equal divisions of octave)

    The Alpha scale divides the octave into 9 equal steps of 133.33... cents.
    This creates a scale with nearly just minor and major thirds.

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    divisions = 9
    step_cents = 1200.0 / divisions
    intervals = [i * step_cents for i in range(divisions)]

    return MicrotonalScale(
        name="Alpha Scale (Carlos)",
        intervals_cents=intervals,
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.ALPHA
    )


def beta_scale(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create Wendy Carlos' Beta scale (11 equal divisions of octave)

    The Beta scale divides the octave into 11 equal steps of 109.09... cents.
    This creates a scale with excellent approximations to several just intervals.

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    divisions = 11
    step_cents = 1200.0 / divisions
    intervals = [i * step_cents for i in range(divisions)]

    return MicrotonalScale(
        name="Beta Scale (Carlos)",
        intervals_cents=intervals,
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.BETA
    )


def create_meantone_scale(comma_fraction: float = 0.25, tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create quarter-comma meantone temperament

    Meantone temperament adjusts fifths to make major thirds pure (5:4 ratio).
    Quarter-comma meantone was the most common tuning in Renaissance music.

    Args:
        comma_fraction: Fraction of syntonic comma to temper the fifth (0.25 for quarter-comma)
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    # Syntonic comma = 81/80 ≈ 21.506 cents
    syntonic_comma_cents = 1200.0 * math.log2(81/80)

    # Pure fifth is 701.955 cents; temper it by comma_fraction of syntonic comma
    fifth_cents = 1200.0 * math.log2(3/2) - (comma_fraction * syntonic_comma_cents)

    # Build chromatic scale from chain of fifths
    # Order: F C G D A E B F# C# G# D# A#
    fifths_from_c = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    intervals = []
    for fifths_count in fifths_from_c:
        cents = (fifths_count * fifth_cents) % 1200.0
        intervals.append(cents)

    return MicrotonalScale(
        name=f"Meantone ({comma_fraction}-comma)",
        intervals_cents=sorted(intervals),
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.MEANTONE
    )


def create_werckmeister_iii(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create Werckmeister III (1691) well temperament

    One of the most famous well temperaments. Four fifths (C-G, G-D, D-A, B-F#)
    are tempered by 1/4 Pythagorean comma, while the rest are pure.

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    # Pythagorean comma ≈ 23.460 cents
    pythagorean_comma = 1200.0 * math.log2(531441/524288)

    # Pure fifth
    pure_fifth = 1200.0 * math.log2(3/2)

    # Tempered fifth (reduced by 1/4 Pythagorean comma)
    tempered_fifth = pure_fifth - (pythagorean_comma / 4)

    # Build scale using circle of fifths
    # Starting from C, specify which fifths are tempered
    # Tempered: C-G, G-D, D-A, B-F#
    # Pure: all others

    notes_fifths = {
        'C': 0,
        'G': tempered_fifth,  # C-G tempered
        'D': 2 * tempered_fifth,  # C-G-D both tempered
        'A': 3 * tempered_fifth,  # C-G-D-A all tempered
        'E': 3 * tempered_fifth + pure_fifth,  # A-E pure
        'B': 3 * tempered_fifth + 2 * pure_fifth,  # A-E-B pure
        'F#': 4 * tempered_fifth + 2 * pure_fifth,  # B-F# tempered
        'C#': 4 * tempered_fifth + 3 * pure_fifth,  # F#-C# pure
        'G#': 4 * tempered_fifth + 4 * pure_fifth,  # C#-G# pure
        'D#': 4 * tempered_fifth + 5 * pure_fifth,  # G#-D# pure (=Eb)
        'A#': 4 * tempered_fifth + 6 * pure_fifth,  # D#-A# pure (=Bb)
        'F': 4 * tempered_fifth + 7 * pure_fifth,  # A#-F pure
    }

    # Convert to chromatic scale cents (mod 1200)
    chromatic_order = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    intervals = [notes_fifths[note] % 1200.0 for note in chromatic_order]

    return MicrotonalScale(
        name="Werckmeister III",
        intervals_cents=intervals,
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.WERCKMEISTER_III
    )


def create_werckmeister_i(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create Werckmeister I "correct temperament" (1691)

    Also known as "correct temperament no. 1".
    Complex distribution of comma fractions.

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    # Werckmeister I cent values (from historical sources)
    notes_cents = {
        'C': 0.0,
        'C#': 90.225,
        'D': 192.180,
        'D#': 294.135,
        'E': 390.225,
        'F': 498.045,
        'F#': 588.270,
        'G': 696.090,
        'G#': 792.180,
        'A': 888.270,
        'A#': 996.090,
        'B': 1092.180,
    }

    chromatic_order = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    intervals = [notes_cents[note] for note in chromatic_order]

    return MicrotonalScale(
        name="Werckmeister I",
        intervals_cents=intervals,
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.WERCKMEISTER_I
    )


def create_werckmeister_ii(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create Werckmeister II (1691)

    Another variant of Werckmeister's well temperaments.
    Different distribution of comma fractions than I or III.

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    # Werckmeister II cent values
    notes_cents = {
        'C': 0.0,
        'C#': 93.900,
        'D': 195.800,
        'D#': 297.800,
        'E': 393.900,
        'F': 501.800,
        'F#': 591.700,
        'G': 699.700,
        'G#': 795.800,
        'A': 891.700,
        'A#': 999.700,
        'B': 1095.800,
    }

    chromatic_order = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    intervals = [notes_cents[note] for note in chromatic_order]

    return MicrotonalScale(
        name="Werckmeister II",
        intervals_cents=intervals,
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.WERCKMEISTER_II
    )


def create_werckmeister_iv(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create Werckmeister IV (1691)

    Werckmeister's fourth well temperament variant.
    Distributes the Pythagorean comma differently.

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    # Werckmeister IV cent values
    notes_cents = {
        'C': 0.0,
        'C#': 82.400,
        'D': 196.090,
        'D#': 294.135,
        'E': 386.315,
        'F': 498.045,
        'F#': 588.270,
        'G': 694.135,
        'G#': 792.180,
        'A': 890.225,
        'A#': 996.090,
        'B': 1088.270,
    }

    chromatic_order = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    intervals = [notes_cents[note] for note in chromatic_order]

    return MicrotonalScale(
        name="Werckmeister IV",
        intervals_cents=intervals,
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.WERCKMEISTER_IV
    )


def create_werckmeister_v(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create Werckmeister V (1691)

    Fifth variant of Werckmeister's well temperaments.
    Equal beating temperament.

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    pythagorean_comma = 1200.0 * math.log2(531441/524288)
    pure_fifth = 1200.0 * math.log2(3/2)

    # All fifths tempered equally by 1/12 Pythagorean comma
    tempered_fifth = pure_fifth - (pythagorean_comma / 12)

    # Build chromatic scale
    notes_fifths = {
        'C': 0,
        'G': tempered_fifth,
        'D': 2 * tempered_fifth,
        'A': 3 * tempered_fifth,
        'E': 4 * tempered_fifth,
        'B': 5 * tempered_fifth,
        'F#': 6 * tempered_fifth,
        'C#': 7 * tempered_fifth,
        'G#': 8 * tempered_fifth,
        'D#': 9 * tempered_fifth,
        'A#': 10 * tempered_fifth,
        'F': 11 * tempered_fifth,
    }

    chromatic_order = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    intervals = [notes_fifths[note] % 1200.0 for note in chromatic_order]

    return MicrotonalScale(
        name="Werckmeister V",
        intervals_cents=intervals,
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.WERCKMEISTER_V
    )


def create_werckmeister_vi(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create Werckmeister VI "Septenarius" (1691)

    The seventh (septenarius) of Werckmeister's temperaments.
    Based on division into seven parts.

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    pythagorean_comma = 1200.0 * math.log2(531441/524288)
    pure_fifth = 1200.0 * math.log2(3/2)
    tempered_fifth = pure_fifth - (pythagorean_comma / 7)

    # Seven fifths tempered, five pure
    notes_fifths = {
        'C': 0,
        'G': tempered_fifth,
        'D': 2 * tempered_fifth,
        'A': 3 * tempered_fifth,
        'E': 4 * tempered_fifth,
        'B': 5 * tempered_fifth,
        'F#': 6 * tempered_fifth,
        'C#': 7 * tempered_fifth,
        'G#': 7 * tempered_fifth + pure_fifth,
        'D#': 7 * tempered_fifth + 2 * pure_fifth,
        'A#': 7 * tempered_fifth + 3 * pure_fifth,
        'F': 7 * tempered_fifth + 4 * pure_fifth,
    }

    chromatic_order = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    intervals = [notes_fifths[note] % 1200.0 for note in chromatic_order]

    return MicrotonalScale(
        name="Werckmeister VI (Septenarius)",
        intervals_cents=intervals,
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.WERCKMEISTER_VI
    )


def create_just_intonation_7_limit(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create 7-limit just intonation scale

    Extends 5-limit JI with ratios involving prime factor 7.
    Includes harmonic seventh (7:4) and subminor seventh (7:6).

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    # Common 7-limit ratios for chromatic scale
    ratios = [
        (1, 1),    # Unison
        (16, 15),  # Minor semitone
        (9, 8),    # Major second
        (7, 6),    # Subminor third
        (5, 4),    # Major third
        (4, 3),    # Perfect fourth
        (7, 5),    # Tritone (septimal)
        (3, 2),    # Perfect fifth
        (8, 5),    # Minor sixth
        (5, 3),    # Major sixth
        (7, 4),    # Harmonic seventh
        (15, 8),   # Major seventh
    ]

    scale = create_just_intonation_scale(ratios)
    return replace(scale, name="7-limit Just Intonation", tuning_system=TuningSystem.JUST_INTONATION_7, tonic_midi=tonic_midi)


def create_just_intonation_11_limit(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create 11-limit just intonation scale

    Extends to prime factor 11, adding more complex harmonics.
    Includes 11:8 (superfourth) and 11:6 intervals.

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    # Common 11-limit ratios
    ratios = [
        (1, 1),    # Unison
        (16, 15),  # Minor semitone
        (9, 8),    # Major second
        (7, 6),    # Subminor third
        (5, 4),    # Major third
        (11, 8),   # Superfourth
        (4, 3),    # Perfect fourth
        (11, 7),   # Undecimal augmented fifth
        (3, 2),    # Perfect fifth
        (8, 5),    # Minor sixth
        (5, 3),    # Major sixth
        (7, 4),    # Harmonic seventh
    ]

    scale = create_just_intonation_scale(ratios)
    return replace(scale, name="11-limit Just Intonation", tuning_system=TuningSystem.JUST_INTONATION_11, tonic_midi=tonic_midi)


def create_partch_43_tone(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create Harry Partch's 43-tone scale

    Partch's comprehensive 11-limit just intonation system.
    Uses ratios from his "Genesis of a Music".

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    # Partch's 43-tone scale (partial - main ratios)
    ratios = [
        (1, 1), (81, 80), (33, 32), (21, 20), (16, 15), (12, 11), (11, 10),
        (10, 9), (9, 8), (8, 7), (7, 6), (32, 27), (6, 5), (11, 9), (5, 4),
        (14, 11), (9, 7), (21, 16), (4, 3), (27, 20), (11, 8), (7, 5), (10, 7),
        (16, 11), (40, 27), (3, 2), (32, 21), (14, 9), (11, 7), (8, 5), (18, 11),
        (5, 3), (27, 16), (12, 7), (7, 4), (16, 9), (9, 5), (20, 11), (11, 6),
        (15, 8), (40, 21), (64, 33), (160, 81)
    ]

    scale = create_just_intonation_scale(ratios)
    return replace(scale, name="Partch 43-tone", tuning_system=TuningSystem.PARTCH_43, tonic_midi=tonic_midi)


def create_valotti_temperament(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create Valotti temperament (1754)

    A circulating temperament with six tempered fifths.
    Very similar to Young temperament.

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    pythagorean_comma = 1200.0 * math.log2(531441/524288)
    pure_fifth = 1200.0 * math.log2(3/2)
    tempered_fifth = pure_fifth - (pythagorean_comma / 6)

    # Six fifths F-C-G-D-A-E are tempered by 1/6 comma, rest are pure
    notes_fifths = {
        'C': 0,
        'G': tempered_fifth,
        'D': 2 * tempered_fifth,
        'A': 3 * tempered_fifth,
        'E': 4 * tempered_fifth,
        'B': 4 * tempered_fifth + pure_fifth,
        'F#': 4 * tempered_fifth + 2 * pure_fifth,
        'C#': 4 * tempered_fifth + 3 * pure_fifth,
        'G#': 4 * tempered_fifth + 4 * pure_fifth,
        'D#': 4 * tempered_fifth + 5 * pure_fifth,
        'A#': 4 * tempered_fifth + 6 * pure_fifth,
        'F': tempered_fifth - pure_fifth,  # Going backwards
    }

    chromatic_order = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    intervals = [notes_fifths[note] % 1200.0 for note in chromatic_order]

    return MicrotonalScale(
        name="Valotti",
        intervals_cents=intervals,
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.VALOTTI
    )


def create_kirnberger_iii(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create Kirnberger III temperament (1779)

    A well temperament with four pure fifths and mixed temperament.
    Widely used in 18th century Germany.

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    syntonic_comma = 1200.0 * math.log2(81/80)
    pure_fifth = 1200.0 * math.log2(3/2)

    # Complex mixture: C-G-D-A pure, but D uses syntonic comma adjustment
    # Four fifths tempered by 1/4 syntonic comma
    notes_cents = {
        'C': 0.0,
        'C#': 90.225,
        'D': 193.157,
        'D#': 294.135,
        'E': 386.314,
        'F': 498.045,
        'F#': 588.270,
        'G': 696.090,
        'G#': 792.180,
        'A': 889.735,
        'A#': 996.090,
        'B': 1088.269,
    }

    chromatic_order = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    intervals = [notes_cents[note] for note in chromatic_order]

    return MicrotonalScale(
        name="Kirnberger III",
        intervals_cents=intervals,
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.KIRNBERGER_III
    )


def create_young_temperament(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create Young temperament (1799)

    Thomas Young's well temperament, very similar to Valotti.
    Six consecutive fifths tempered.

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    # Young II is most common
    notes_cents = {
        'C': 0.0,
        'C#': 93.9,
        'D': 195.8,
        'D#': 297.8,
        'E': 391.7,
        'F': 499.9,
        'F#': 593.9,
        'G': 695.8,
        'G#': 797.8,
        'A': 891.7,
        'A#': 999.9,
        'B': 1093.9,
    }

    chromatic_order = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    intervals = [notes_cents[note] for note in chromatic_order]

    return MicrotonalScale(
        name="Young",
        intervals_cents=intervals,
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.YOUNG
    )


def create_kirnberger_ii(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create Kirnberger II temperament (1776)

    Simpler than Kirnberger III, with specific pure intervals.

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    notes_cents = {
        'C': 0.0,
        'C#': 90.225,
        'D': 203.910,
        'D#': 294.135,
        'E': 386.314,
        'F': 498.045,
        'F#': 588.270,
        'G': 701.955,
        'G#': 792.180,
        'A': 884.359,
        'A#': 1003.910,
        'B': 1088.269,
    }

    chromatic_order = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    intervals = [notes_cents[note] for note in chromatic_order]

    return MicrotonalScale(
        name="Kirnberger II",
        intervals_cents=intervals,
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.KIRNBERGER_II
    )


def create_neidhardt_i(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create Neidhardt I temperament (1724)

    One of Johann Georg Neidhardt's circulating temperaments.
    Also known as "Dorf" (village) temperament.

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    notes_cents = {
        'C': 0.0,
        'C#': 94.135,
        'D': 196.090,
        'D#': 298.045,
        'E': 392.180,
        'F': 501.955,
        'F#': 592.180,
        'G': 698.045,
        'G#': 796.090,
        'A': 894.135,
        'A#': 1000.000,
        'B': 1094.135,
    }

    chromatic_order = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    intervals = [notes_cents[note] for note in chromatic_order]

    return MicrotonalScale(
        name="Neidhardt I",
        intervals_cents=intervals,
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.NEIDHARDT_I
    )


def create_neidhardt_iii(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create Neidhardt III temperament (1732)

    Also known as "Stadt" (town/city) temperament.
    More refined than Neidhardt I.

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    notes_cents = {
        'C': 0.0,
        'C#': 92.180,
        'D': 196.090,
        'D#': 296.090,
        'E': 392.180,
        'F': 498.045,
        'F#': 590.225,
        'G': 696.090,
        'G#': 794.135,
        'A': 894.135,
        'A#': 996.090,
        'B': 1092.180,
    }

    chromatic_order = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    intervals = [notes_cents[note] for note in chromatic_order]

    return MicrotonalScale(
        name="Neidhardt III",
        intervals_cents=intervals,
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.NEIDHARDT_III
    )


def create_rameau_temperament(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create Rameau temperament (1726)

    Jean-Philippe Rameau's modified meantone temperament.

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    notes_cents = {
        'C': 0.0,
        'C#': 90.225,
        'D': 193.157,
        'D#': 294.135,
        'E': 386.314,
        'F': 498.045,
        'F#': 588.270,
        'G': 696.579,
        'G#': 792.180,
        'A': 889.735,
        'A#': 996.090,
        'B': 1088.269,
    }

    chromatic_order = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    intervals = [notes_cents[note] for note in chromatic_order]

    return MicrotonalScale(
        name="Rameau",
        intervals_cents=intervals,
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.RAMEAU
    )


def create_kellner_temperament(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create Kellner temperament (1975/1681)

    Herbert Anton Kellner's proposed "Bach temperament".
    Based on analysis of Bach's title page decorations.

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    pythagorean_comma = 1200.0 * math.log2(531441/524288)
    pure_fifth = 1200.0 * math.log2(3/2)
    tempered_fifth = pure_fifth - (pythagorean_comma / 5)

    # Five fifths tempered by 1/5 Pythagorean comma
    notes_fifths = {
        'C': 0,
        'G': tempered_fifth,
        'D': 2 * tempered_fifth,
        'A': 3 * tempered_fifth,
        'E': 4 * tempered_fifth,
        'B': 4 * tempered_fifth + pure_fifth,
        'F#': 4 * tempered_fifth + 2 * pure_fifth,
        'C#': 4 * tempered_fifth + 3 * pure_fifth,
        'G#': 4 * tempered_fifth + 4 * pure_fifth,
        'D#': 4 * tempered_fifth + 5 * pure_fifth,
        'A#': 4 * tempered_fifth + 6 * pure_fifth,
        'F': 4 * tempered_fifth + 7 * pure_fifth,
    }

    chromatic_order = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    intervals = [notes_fifths[note] % 1200.0 for note in chromatic_order]

    return MicrotonalScale(
        name="Kellner (Bach)",
        intervals_cents=intervals,
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.KELLNER
    )


def create_harmonic_series_scale(fundamental_midi: int = 60, num_harmonics: int = 16) -> MicrotonalScale:
    """
    Create scale from harmonic series

    Uses the natural harmonic overtone series starting from a fundamental.

    Args:
        fundamental_midi: MIDI note for fundamental
        num_harmonics: Number of harmonics to include (default: 16)

    Returns:
        Microtonal scale
    """
    ratios = [(i, 1) for i in range(1, num_harmonics + 1)]
    scale = create_just_intonation_scale(ratios)

    return replace(
        scale,
        name=f"Harmonic Series ({num_harmonics} partials)",
        tonic_midi=fundamental_midi,
        tuning_system=TuningSystem.HARMONIC_SERIES
    )


def create_golden_ratio_scale(tonic_midi: int = 60, num_steps: int = 13) -> MicrotonalScale:
    """
    Create scale based on golden ratio (phi ≈ 1.618)

    Non-octave scale where the "pseudo-octave" is phi instead of 2:1.

    Args:
        tonic_midi: MIDI note for tonic
        num_steps: Number of equal divisions of phi

    Returns:
        Microtonal scale
    """
    phi = (1 + math.sqrt(5)) / 2  # ≈ 1.618
    phi_cents = 1200.0 * math.log2(phi)  # ≈ 833.09 cents

    step_cents = phi_cents / num_steps
    intervals = [i * step_cents for i in range(num_steps)]

    return MicrotonalScale(
        name=f"Golden Ratio ({num_steps}-EDPhi)",
        intervals_cents=intervals,
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.PHI_BASED
    )


def create_lambda_scale(tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create Wendy Carlos' Lambda scale

    Non-octave scale with 16 equal divisions of a slightly flat perfect fifth.

    Args:
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    # Lambda uses 16 divisions of a 695 cent fifth
    fifth_cents = 695.0
    divisions = 16
    step_cents = fifth_cents / divisions

    intervals = [i * step_cents for i in range(divisions)]

    return MicrotonalScale(
        name="Lambda Scale (Carlos)",
        intervals_cents=intervals,
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.LAMBDA
    )


def create_stretched_octave_scale(tonic_midi: int = 60, stretch_cents: float = 2.0) -> MicrotonalScale:
    """
    Create scale with stretched octaves (Railsback curve)

    Simulates piano inharmonicity where octaves are slightly sharp.

    Args:
        tonic_midi: MIDI note for tonic
        stretch_cents: Amount to stretch octave in cents (typical: 1-5 cents)

    Returns:
        Microtonal scale
    """
    octave_cents = 1200.0 + stretch_cents
    step_cents = octave_cents / 12

    intervals = [i * step_cents for i in range(12)]

    return MicrotonalScale(
        name=f"Stretched 12-TET (+{stretch_cents:.1f}¢)",
        intervals_cents=intervals,
        tonic_midi=tonic_midi,
        tuning_system=TuningSystem.STRETCHED_OCTAVE
    )


def transpose_scale(scale: MicrotonalScale, semitones: float) -> MicrotonalScale:
    """
    Transpose a microtonal scale by a given number of semitones

    Args:
        scale: Scale to transpose
        semitones: Number of semitones to transpose (can be fractional)

    Returns:
        Transposed scale
    """
    cents_shift = semitones * 100.0
    new_intervals = [(interval + cents_shift) % 1200.0 for interval in scale.intervals_cents]
    new_tonic = int(scale.tonic_midi + semitones)

    return MicrotonalScale(
        name=f"{scale.name} (transposed {semitones:+.2f} semitones)",
        intervals_cents=sorted(new_intervals),
        tonic_midi=new_tonic,
        tuning_system=scale.tuning_system
    )


def invert_scale(scale: MicrotonalScale, axis_cents: Optional[float] = None) -> MicrotonalScale:
    """
    Invert a microtonal scale around an axis

    Args:
        scale: Scale to invert
        axis_cents: Inversion axis in cents (default: center of scale range)

    Returns:
        Inverted scale
    """
    if axis_cents is None:
        axis_cents = sum(scale.intervals_cents) / len(scale.intervals_cents)

    inverted_intervals = [2 * axis_cents - interval for interval in scale.intervals_cents]

    # Normalize to 0-1200 range and sort
    normalized = [(interval % 1200.0) for interval in inverted_intervals]

    return MicrotonalScale(
        name=f"{scale.name} (inverted)",
        intervals_cents=sorted(normalized),
        tonic_midi=scale.tonic_midi,
        tuning_system=scale.tuning_system
    )


def reverse_scale(scale: MicrotonalScale) -> MicrotonalScale:
    """
    Reverse (retrograde) a microtonal scale

    Args:
        scale: Scale to reverse

    Returns:
        Reversed scale
    """
    # Reverse the intervals (excluding tonic which stays at 0)
    reversed_intervals = [0.0] + [1200.0 - interval for interval in reversed(scale.intervals_cents[1:])]

    return MicrotonalScale(
        name=f"{scale.name} (reversed)",
        intervals_cents=reversed_intervals,
        tonic_midi=scale.tonic_midi,
        tuning_system=scale.tuning_system
    )


def scale_subset(scale: MicrotonalScale, indices: List[int]) -> MicrotonalScale:
    """
    Extract a subset of scale degrees

    Args:
        scale: Source scale
        indices: List of scale degree indices to extract

    Returns:
        New scale with only specified degrees
    """
    subset_intervals = [scale.intervals_cents[i] for i in indices if i < len(scale.intervals_cents)]

    return MicrotonalScale(
        name=f"{scale.name} (subset)",
        intervals_cents=sorted(subset_intervals),
        tonic_midi=scale.tonic_midi,
        tuning_system=scale.tuning_system
    )


def compare_scales(scale1: MicrotonalScale, scale2: MicrotonalScale) -> Dict[str, any]:
    """
    Compare two microtonal scales

    Args:
        scale1: First scale
        scale2: Second scale

    Returns:
        Dictionary with comparison metrics
    """
    # Find common pitches (within 5 cents tolerance)
    tolerance_cents = 5.0
    common_pitches = []

    for interval1 in scale1.intervals_cents:
        for interval2 in scale2.intervals_cents:
            if abs(interval1 - interval2) < tolerance_cents:
                common_pitches.append((interval1, interval2))
                break

    # Calculate average deviation
    if common_pitches:
        avg_deviation = sum(abs(p1 - p2) for p1, p2 in common_pitches) / len(common_pitches)
    else:
        avg_deviation = float('inf')

    return {
        'scale1_name': scale1.name,
        'scale2_name': scale2.name,
        'scale1_degrees': len(scale1.intervals_cents),
        'scale2_degrees': len(scale2.intervals_cents),
        'common_pitches': len(common_pitches),
        'common_percentage': len(common_pitches) / max(len(scale1.intervals_cents), len(scale2.intervals_cents)) * 100,
        'average_deviation_cents': avg_deviation,
        'similarity_score': 1.0 - min(1.0, avg_deviation / 50.0) if avg_deviation != float('inf') else 0.0
    }


def find_common_pitches(scale1: MicrotonalScale, scale2: MicrotonalScale, tolerance_cents: float = 5.0) -> List[Tuple[float, float]]:
    """
    Find pitches shared between two scales

    Args:
        scale1: First scale
        scale2: Second scale
        tolerance_cents: Maximum difference in cents to consider pitches the same

    Returns:
        List of (scale1_pitch, scale2_pitch) tuples for common pitches
    """
    common = []

    for interval1 in scale1.intervals_cents:
        for interval2 in scale2.intervals_cents:
            if abs(interval1 - interval2) <= tolerance_cents:
                common.append((interval1, interval2))
                break

    return common


def scale_complexity_score(scale: MicrotonalScale) -> float:
    """
    Calculate complexity score for a scale

    Higher scores indicate more complex interval relationships.

    Args:
        scale: Scale to analyze

    Returns:
        Complexity score (0.0 - 1.0+)
    """
    if len(scale.intervals_cents) <= 1:
        return 0.0

    # Calculate interval variety
    intervals_between_degrees = []
    for i in range(len(scale.intervals_cents) - 1):
        diff = scale.intervals_cents[i + 1] - scale.intervals_cents[i]
        intervals_between_degrees.append(diff)

    # Add wrap-around interval
    if scale.intervals_cents:
        wrap_interval = 1200.0 - scale.intervals_cents[-1]
        intervals_between_degrees.append(wrap_interval)

    # Calculate variance and uniqueness
    if not intervals_between_degrees:
        return 0.0

    avg_interval = sum(intervals_between_degrees) / len(intervals_between_degrees)
    variance = sum((interval - avg_interval) ** 2 for interval in intervals_between_degrees) / len(intervals_between_degrees)

    unique_intervals = len(set(round(interval, 1) for interval in intervals_between_degrees))
    uniqueness_ratio = unique_intervals / len(intervals_between_degrees)

    # Combine metrics
    complexity = (variance / 10000.0) * uniqueness_ratio

    return min(1.0, complexity)


def export_scala_file(scale: MicrotonalScale, filepath: str, description: Optional[str] = None) -> None:
    """
    Export scale to Scala (.scl) file format

    The Scala format is the industry standard for microtonal scale definitions.

    Args:
        scale: Scale to export
        filepath: Path to output .scl file
        description: Optional description (defaults to scale name)

    Example:
        >>> scale = create_equal_temperament(19)
        >>> export_scala_file(scale, "19tet.scl", "19-tone equal temperament")
    """
    if description is None:
        description = scale.name

    with open(filepath, 'w') as f:
        # Header
        f.write(f"! {filepath}\n")
        f.write(f"!\n")
        f.write(f"{description}\n")

        # Number of notes (excluding tonic)
        num_notes = len(scale.intervals_cents) - 1  # Exclude 0.0 tonic
        f.write(f" {num_notes}\n")
        f.write("!\n")

        # Write intervals (skip first 0.0, write up to octave)
        for interval_cents in scale.intervals_cents[1:]:
            if interval_cents >= 1200.0:
                break  # Stop at octave
            # Scala format: cents values have decimal point
            f.write(f" {interval_cents:.6f}\n")

        # Write octave
        f.write(" 2/1\n")


def import_scala_file(filepath: str, tonic_midi: int = 60) -> MicrotonalScale:
    """
    Import scale from Scala (.scl) file format

    Args:
        filepath: Path to .scl file
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale

    Example:
        >>> scale = import_scala_file("bohlen-pierce.scl", tonic_midi=60)
    """
    intervals_cents = [0.0]  # Always start with tonic
    description = ""

    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Parse file
    line_idx = 0

    # Skip comments at start
    while line_idx < len(lines) and lines[line_idx].strip().startswith('!'):
        line_idx += 1

    # Get description
    if line_idx < len(lines):
        description = lines[line_idx].strip()
        line_idx += 1

    # Get number of notes
    while line_idx < len(lines) and (lines[line_idx].strip().startswith('!') or not lines[line_idx].strip()):
        line_idx += 1

    if line_idx < len(lines):
        num_notes = int(lines[line_idx].strip())
        line_idx += 1

    # Read intervals
    notes_read = 0
    while line_idx < len(lines) and notes_read < num_notes:
        line = lines[line_idx].strip()
        line_idx += 1

        # Skip comments and empty lines
        if not line or line.startswith('!'):
            continue

        # Parse interval (can be cents or ratio)
        if '/' in line:
            # Ratio format (e.g., "3/2")
            parts = line.split('/')
            numerator = float(parts[0])
            denominator = float(parts[1])
            cents = 1200.0 * math.log2(numerator / denominator)
        elif '.' in line:
            # Cents format (e.g., "701.955")
            cents = float(line)
        else:
            # Integer cents
            cents = float(line)

        intervals_cents.append(cents)
        notes_read += 1

    return MicrotonalScale(
        name=description if description else "Imported Scala Scale",
        intervals_cents=sorted(intervals_cents),
        tonic_midi=tonic_midi
    )


def generate_modal_rotations(scale: MicrotonalScale) -> List[MicrotonalScale]:
    """
    Generate all modal rotations of a scale

    Creates modes by rotating the scale degrees (like Ionian, Dorian, etc. in 12-TET).

    Args:
        scale: Base scale to rotate

    Returns:
        List of modal scales
    """
    modes = []
    intervals = scale.intervals_cents

    for mode_num in range(len(intervals)):
        # Rotate intervals
        rotated = intervals[mode_num:] + intervals[:mode_num]

        # Normalize to start at 0
        if rotated:
            first_interval = rotated[0]
            normalized = [interval - first_interval for interval in rotated]

            # Wrap negative values
            normalized = [(interval % 1200.0) if interval < 0 else interval for interval in normalized]

            modes.append(MicrotonalScale(
                name=f"{scale.name} - Mode {mode_num + 1}",
                intervals_cents=sorted(normalized),
                tonic_midi=scale.tonic_midi,
                tuning_system=scale.tuning_system
            ))

    return modes


def create_subharmonic_series_scale(fundamental_midi: int = 60, num_subharmonics: int = 16) -> MicrotonalScale:
    """
    Create scale from subharmonic (undertone) series

    The subharmonic series is the mirror of the harmonic series.
    Uses ratios like 1/1, 1/2, 1/3, 1/4, etc.

    Args:
        fundamental_midi: MIDI note for fundamental
        num_subharmonics: Number of subharmonics to include

    Returns:
        Microtonal scale
    """
    ratios = [(1, i) for i in range(1, num_subharmonics + 1)]
    scale = create_just_intonation_scale(ratios)

    return replace(
        scale,
        name=f"Subharmonic Series ({num_subharmonics} partials)",
        tonic_midi=fundamental_midi
    )


def create_scale_from_ratios(ratios: List[Tuple[int, int]], name: str = "Custom Ratios", tonic_midi: int = 60) -> MicrotonalScale:
    """
    Create a custom scale from a list of frequency ratios

    Args:
        ratios: List of (numerator, denominator) tuples
        name: Name for the scale
        tonic_midi: MIDI note for tonic

    Returns:
        Microtonal scale
    """
    scale = create_just_intonation_scale(ratios)
    return replace(scale, name=name, tonic_midi=tonic_midi)


def create_interval_matrix(scale: MicrotonalScale) -> List[List[float]]:
    """
    Create interval matrix showing all intervals between scale degrees

    Args:
        scale: Scale to analyze

    Returns:
        2D matrix where matrix[i][j] is the interval from degree i to degree j in cents
    """
    intervals = scale.intervals_cents
    n = len(intervals)
    matrix = []

    for i in range(n):
        row = []
        for j in range(n):
            interval = (intervals[j] - intervals[i]) % 1200.0
            row.append(interval)
        matrix.append(row)

    return matrix


def calculate_consonance_dissonance(interval_cents: float) -> float:
    """
    Calculate consonance/dissonance score for an interval

    Uses a simplified model based on critical band theory and simple ratios.
    Returns value from 0.0 (max dissonance) to 1.0 (max consonance).

    Args:
        interval_cents: Interval size in cents

    Returns:
        Consonance score (0.0 = dissonant, 1.0 = consonant)
    """
    # Perfect consonances (unison, octave, fifth, fourth)
    perfect_intervals = [0, 498, 702, 1200]
    perfect_tolerance = 10

    # Imperfect consonances (major/minor thirds and sixths)
    imperfect_intervals = [316, 386, 814, 884]  # Minor 3rd, Major 3rd, Minor 6th, Major 6th
    imperfect_tolerance = 15

    # Check perfect consonances
    for perfect in perfect_intervals:
        if abs(interval_cents - perfect) < perfect_tolerance:
            return 1.0 - (abs(interval_cents - perfect) / perfect_tolerance) * 0.1

    # Check imperfect consonances
    for imperfect in imperfect_intervals:
        if abs(interval_cents - imperfect) < imperfect_tolerance:
            return 0.85 - (abs(interval_cents - imperfect) / imperfect_tolerance) * 0.15

    # Check for very small intervals (dissonant)
    if interval_cents < 100:
        return 0.2 + (interval_cents / 100) * 0.3

    # Default: moderate dissonance
    return 0.4


def create_consonance_profile(scale: MicrotonalScale) -> Dict[str, any]:
    """
    Create consonance profile for all intervals in a scale

    Analyzes the consonance/dissonance of all intervals between scale degrees.

    Args:
        scale: Scale to analyze

    Returns:
        Dictionary with consonance analysis
    """
    matrix = create_interval_matrix(scale)
    consonance_matrix = []

    all_consonances = []
    for row in matrix:
        consonance_row = []
        for interval in row:
            consonance = calculate_consonance_dissonance(interval)
            consonance_row.append(consonance)
            if interval > 0:  # Exclude unisons
                all_consonances.append(consonance)
        consonance_matrix.append(consonance_row)

    avg_consonance = sum(all_consonances) / len(all_consonances) if all_consonances else 0.0

    return {
        'scale_name': scale.name,
        'average_consonance': avg_consonance,
        'consonance_matrix': consonance_matrix,
        'interval_matrix': matrix,
        'most_consonant_interval': max(all_consonances) if all_consonances else 0.0,
        'most_dissonant_interval': min(all_consonances) if all_consonances else 0.0
    }


def calculate_pitch_bend_for_microtone(cent_deviation: float, bend_range_semitones: int = 2) -> int:
    """
    Calculate MIDI pitch bend value for microtonal deviation

    Args:
        cent_deviation: Deviation in cents from 12-TET pitch
        bend_range_semitones: Pitch bend range in semitones (default: 2)

    Returns:
        MIDI pitch bend value (0-16383, center is 8192)
    """
    # Pitch bend range: 0-16383, center = 8192
    # Bend range is typically ±2 semitones = ±200 cents
    max_cents = bend_range_semitones * 100

    # Clamp to range
    cent_deviation = max(-max_cents, min(max_cents, cent_deviation))

    # Calculate bend value
    bend_proportion = cent_deviation / max_cents
    bend_value = int(8192 + (bend_proportion * 8191))

    return bend_value


def generate_midi_pitch_bends(scale: MicrotonalScale, bend_range: int = 2) -> Dict[int, int]:
    """
    Generate MIDI pitch bend values for all scale degrees

    Args:
        scale: Microtonal scale
        bend_range: Pitch bend range in semitones (default: 2)

    Returns:
        Dictionary mapping scale degree index to pitch bend value
    """
    pitch_bends = {}

    for i, interval_cents in enumerate(scale.intervals_cents):
        # Get the base MIDI note and cent deviation
        midi_note = int(interval_cents / 100)
        cent_deviation = interval_cents % 100

        # Calculate pitch bend
        bend_value = calculate_pitch_bend_for_microtone(cent_deviation, bend_range)
        pitch_bends[i] = bend_value

    return pitch_bends


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
    scores[TuningSystem.JUST_INTONATION_5] = 1.0 - (sum(just_errors) / (len(just_errors) * 50.0))

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
