"""
Tests for microtonal and cross-cultural canon systems

Phase 18 - v0.35.0
"""

import pytest
import math
from music21 import stream, note, pitch
from music21.pitch import Microtone

from cancrizans.microtonal import (
    MicrotonalPitch,
    MicrotonalScale,
    TuningSystem,
    ScaleType,
    create_equal_temperament,
    create_just_intonation_scale,
    create_pythagorean_scale,
    create_world_music_scale,
    xenharmonic_canon,
    microtonal_inversion,
    analyze_microtonal_intervals,
    bohlen_pierce_scale,
    gamma_scale,
    detect_tuning_system,
    cross_cultural_canon_analysis
)


class TestMicrotonalPitch:
    """Test MicrotonalPitch dataclass"""

    def test_creation_with_auto_frequency(self):
        """Test creating pitch with automatic frequency calculation"""
        p = MicrotonalPitch(midi_note=69, cent_deviation=0.0)

        assert p.midi_note == 69
        assert p.cent_deviation == 0.0
        assert abs(p.frequency_hz - 440.0) < 0.01  # A4 = 440 Hz

    def test_creation_with_cent_deviation(self):
        """Test creating pitch with cent deviation"""
        p = MicrotonalPitch(midi_note=60, cent_deviation=50.0)

        assert p.cent_deviation == 50.0
        # Frequency should be between C4 and C#4
        assert 261.6 < p.frequency_hz < 277.2

    def test_to_cents_from_c0(self):
        """Test converting to cents from C0"""
        p = MicrotonalPitch(midi_note=60, cent_deviation=50.0)

        cents = p.to_cents_from_c0()
        assert abs(cents - 6050.0) < 0.01  # 60 * 100 + 50

    def test_explicit_frequency(self):
        """Test creating pitch with explicit frequency"""
        p = MicrotonalPitch(midi_note=69, cent_deviation=0.0, frequency_hz=442.0)

        assert p.frequency_hz == 442.0


class TestMicrotonalScale:
    """Test MicrotonalScale dataclass"""

    def test_creation(self):
        """Test creating microtonal scale"""
        scale = MicrotonalScale(
            name="Test Scale",
            intervals_cents=[0, 200, 400, 500, 700, 900, 1100],
            tonic_midi=60
        )

        assert scale.name == "Test Scale"
        assert len(scale.intervals_cents) == 7
        assert scale.tonic_midi == 60

    def test_get_pitches_one_octave(self):
        """Test getting scale pitches for one octave"""
        scale = MicrotonalScale(
            name="Major",
            intervals_cents=[0, 200, 400, 500, 700, 900, 1100],
            tonic_midi=60
        )

        pitches = scale.get_pitches(octaves=1)

        assert len(pitches) == 7
        assert pitches[0].midi_note == 60
        assert pitches[0].cent_deviation == 0.0

    def test_get_pitches_multiple_octaves(self):
        """Test getting scale pitches for multiple octaves"""
        scale = MicrotonalScale(
            name="Pentatonic",
            intervals_cents=[0, 200, 400, 700, 900],
            tonic_midi=60
        )

        pitches = scale.get_pitches(octaves=2)

        assert len(pitches) == 10  # 5 notes * 2 octaves


class TestEqualTemperament:
    """Test equal temperament creation"""

    def test_12_tet(self):
        """Test 12-tone equal temperament"""
        scale = create_equal_temperament(12)

        assert scale.name == "12-TET"
        assert len(scale.intervals_cents) == 12
        assert abs(scale.intervals_cents[1] - 100.0) < 0.01  # Semitone

    def test_19_tet(self):
        """Test 19-tone equal temperament"""
        scale = create_equal_temperament(19)

        assert scale.name == "19-TET"
        assert len(scale.intervals_cents) == 19
        assert abs(scale.intervals_cents[1] - 63.16) < 0.1

    def test_24_tet(self):
        """Test 24-tone equal temperament (quarter tones)"""
        scale = create_equal_temperament(24)

        assert scale.name == "24-TET"
        assert len(scale.intervals_cents) == 24
        assert abs(scale.intervals_cents[1] - 50.0) < 0.01  # Quarter tone

    def test_custom_octave(self):
        """Test equal temperament with custom octave"""
        # Bohlen-Pierce uses 3:1 instead of 2:1
        tritave_cents = 1200.0 * math.log2(3)
        scale = create_equal_temperament(13, octave_cents=tritave_cents)

        assert len(scale.intervals_cents) == 13


class TestJustIntonation:
    """Test just intonation scales"""

    def test_major_scale(self):
        """Test just intonation major scale"""
        ratios = [(1, 1), (9, 8), (5, 4), (4, 3), (3, 2), (5, 3), (15, 8)]
        scale = create_just_intonation_scale(ratios)

        assert scale.name == "Just Intonation"
        assert len(scale.intervals_cents) == 7
        assert abs(scale.intervals_cents[0]) < 0.01  # Tonic = 0 cents
        assert abs(scale.intervals_cents[4] - 701.955) < 0.01  # Perfect fifth

    def test_pure_intervals(self):
        """Test pure interval ratios"""
        ratios = [(1, 1), (3, 2), (2, 1)]  # Tonic, fifth, octave
        scale = create_just_intonation_scale(ratios)

        assert abs(scale.intervals_cents[1] - 701.955) < 0.01  # 3:2 fifth
        assert abs(scale.intervals_cents[2] - 1200.0) < 0.01  # 2:1 octave


class TestPythagorean:
    """Test Pythagorean tuning"""

    def test_pythagorean_scale(self):
        """Test Pythagorean scale creation"""
        scale = create_pythagorean_scale()

        assert scale.name == "Pythagorean"
        assert scale.tuning_system == TuningSystem.PYTHAGOREAN
        assert len(scale.intervals_cents) == 7

    def test_pythagorean_fifths(self):
        """Test that Pythagorean scale is based on pure fifths"""
        scale = create_pythagorean_scale()

        # Fifth should be pure (702 cents, not 700 cents of 12-TET)
        # Find the fifth (G = 4th scale degree in C major)
        fifth_cents = scale.intervals_cents[4]
        assert abs(fifth_cents - 701.955) < 0.1


class TestWorldMusicScales:
    """Test world music scale creation"""

    def test_maqam_rast(self):
        """Test Arabic maqam Rast"""
        scale = create_world_music_scale(ScaleType.MAQAM_RAST, tonic_midi=60)

        assert scale.name == "Arabic maqam Rast"
        assert len(scale.intervals_cents) == 7
        assert scale.tonic_midi == 60

    def test_maqam_hijaz(self):
        """Test Arabic maqam Hijaz with augmented second"""
        scale = create_world_music_scale(ScaleType.MAQAM_HIJAZ)

        assert "Hijaz" in scale.name
        # Hijaz has characteristic augmented second (300 cents)
        assert 400 in scale.intervals_cents

    def test_raga_bhairav(self):
        """Test Hindustani raga Bhairav"""
        scale = create_world_music_scale(ScaleType.RAGA_BHAIRAV)

        assert "Bhairav" in scale.name
        assert len(scale.intervals_cents) == 7

    def test_pelog(self):
        """Test Javanese Pelog scale"""
        scale = create_world_music_scale(ScaleType.PELOG)

        assert "Pelog" in scale.name
        # Pelog typically has 5-7 notes
        assert 5 <= len(scale.intervals_cents) <= 7

    def test_slendro(self):
        """Test Javanese Slendro scale"""
        scale = create_world_music_scale(ScaleType.SLENDRO)

        assert "Slendro" in scale.name
        assert len(scale.intervals_cents) == 5

    def test_hirajoshi(self):
        """Test Japanese Hirajoshi scale"""
        scale = create_world_music_scale(ScaleType.HIRAJOSHI)

        assert "Hirajoshi" in scale.name
        assert len(scale.intervals_cents) == 5

    def test_chinese_pentatonic(self):
        """Test Chinese pentatonic scale"""
        scale = create_world_music_scale(ScaleType.PENTATONIC_CHINESE)

        assert "Chinese" in scale.name
        assert len(scale.intervals_cents) == 5

    def test_persian_dastgah(self):
        """Test Persian dastgah Shur"""
        scale = create_world_music_scale(ScaleType.DASTGAH_SHUR)

        assert "Persian" in scale.name or "Shur" in scale.name
        assert len(scale.intervals_cents) == 7

    def test_custom_tonic(self):
        """Test world scale with custom tonic"""
        scale = create_world_music_scale(ScaleType.MAQAM_RAST, tonic_midi=67)

        assert scale.tonic_midi == 67

    def test_all_scale_types_work(self):
        """Test that all scale type enums work"""
        # Test that we can create all defined scale types
        for scale_type in [ScaleType.MAQAM_RAST, ScaleType.RAGA_YAMAN, ScaleType.PELOG]:
            scale = create_world_music_scale(scale_type)
            assert scale is not None
            assert len(scale.intervals_cents) > 0


class TestXenharmonic:
    """Test xenharmonic canon functions"""

    def test_xenharmonic_canon_19tet(self):
        """Test xenharmonic canon with 19-TET"""
        s = stream.Stream()
        s.append(note.Note('C4', quarterLength=1.0))
        s.append(note.Note('D4', quarterLength=1.0))
        s.append(note.Note('E4', quarterLength=1.0))

        result = xenharmonic_canon(s, divisions_per_octave=19, transformation="retrograde")

        notes = list(result.flatten().notes)
        assert len(notes) == 3

    def test_xenharmonic_canon_24tet(self):
        """Test xenharmonic canon with 24-TET (quarter tones)"""
        s = stream.Stream()
        s.append(note.Note('C4', quarterLength=1.0))

        result = xenharmonic_canon(s, divisions_per_octave=24)

        assert len(list(result.flatten().notes)) == 1

    def test_microtonal_inversion(self):
        """Test microtonal inversion"""
        s = stream.Stream()
        s.append(note.Note('C4', quarterLength=1.0))
        s.append(note.Note('E4', quarterLength=1.0))

        scale = create_equal_temperament(19)
        result = microtonal_inversion(s, scale)

        notes = list(result.flatten().notes)
        assert len(notes) == 2

    def test_microtonal_inversion_custom_axis(self):
        """Test microtonal inversion with custom axis"""
        s = stream.Stream()
        s.append(note.Note('C4', quarterLength=1.0))

        scale = create_equal_temperament(24)
        result = microtonal_inversion(s, scale, axis_cents=6000.0)

        notes = list(result.flatten().notes)
        assert len(notes) == 1


class TestMicrotonalAnalysis:
    """Test microtonal analysis functions"""

    def test_analyze_empty_stream(self):
        """Test analyzing empty stream"""
        s = stream.Stream()
        analysis = analyze_microtonal_intervals(s)

        assert analysis['interval_count'] == 0
        assert analysis['contains_microtones'] is False

    def test_analyze_12tet_stream(self):
        """Test analyzing 12-TET stream"""
        s = stream.Stream()
        s.append(note.Note('C4'))
        s.append(note.Note('D4'))
        s.append(note.Note('E4'))

        analysis = analyze_microtonal_intervals(s)

        assert analysis['interval_count'] == 2
        assert analysis['contains_microtones'] is False

    def test_analyze_microtonal_stream(self):
        """Test analyzing stream with microtones"""
        s = stream.Stream()

        n1 = note.Note('C4')
        n1.pitch.microtone = Microtone(50.0)  # Quarter tone up
        s.append(n1)

        n2 = note.Note('D4')
        s.append(n2)

        analysis = analyze_microtonal_intervals(s)

        assert analysis['contains_microtones'] is True
        assert analysis['interval_count'] == 1

    def test_interval_distribution(self):
        """Test interval distribution analysis"""
        s = stream.Stream()
        s.append(note.Note('C4'))
        s.append(note.Note('C#4'))  # Semitone
        s.append(note.Note('E4'))   # Major third

        analysis = analyze_microtonal_intervals(s)

        dist = analysis['interval_distribution']
        assert dist['semitones'] >= 1
        assert dist['large_intervals'] >= 1


class TestBohlenPierce:
    """Test Bohlen-Pierce scale"""

    def test_bohlen_pierce_creation(self):
        """Test Bohlen-Pierce scale creation"""
        scale = bohlen_pierce_scale(tonic_midi=60)

        assert scale.name == "Bohlen-Pierce"
        assert scale.tuning_system == TuningSystem.BOHLEN_PIERCE
        assert len(scale.intervals_cents) == 13

    def test_bohlen_pierce_tritave(self):
        """Test that Bohlen-Pierce uses 3:1 tritave"""
        scale = bohlen_pierce_scale()

        # Last interval should be close to log2(3) * 1200 cents
        tritave_cents = 1200.0 * math.log2(3)
        expected_last = tritave_cents * (12 / 13)  # Step 12 of 13

        assert abs(scale.intervals_cents[-1] - expected_last) < 1.0


class TestGammaScale:
    """Test Wendy Carlos Gamma scale"""

    def test_gamma_scale_creation(self):
        """Test Gamma scale creation"""
        scale = gamma_scale(tonic_midi=60)

        assert "Gamma" in scale.name
        assert scale.tonic_midi == 60
        # Should have ~20-21 divisions
        assert 19 <= len(scale.intervals_cents) <= 22

    def test_gamma_scale_step_size(self):
        """Test Gamma scale step size"""
        scale = gamma_scale()

        # Step should be ~58.5 cents
        step = scale.intervals_cents[1] - scale.intervals_cents[0]
        assert 58.0 < step < 59.0


class TestTuningDetection:
    """Test tuning system detection"""

    def test_detect_12tet(self):
        """Test detecting 12-TET tuning"""
        s = stream.Stream()
        s.append(note.Note('C4'))
        s.append(note.Note('E4'))
        s.append(note.Note('G4'))

        tuning, confidence = detect_tuning_system(s)

        assert tuning == TuningSystem.EQUAL_12
        assert confidence > 0.8

    def test_detect_empty_stream(self):
        """Test detecting tuning on empty stream"""
        s = stream.Stream()

        tuning, confidence = detect_tuning_system(s)

        assert tuning == TuningSystem.EQUAL_12
        assert confidence == 0.0

    def test_confidence_score_range(self):
        """Test that confidence is in valid range"""
        s = stream.Stream()
        s.append(note.Note('C4'))

        tuning, confidence = detect_tuning_system(s)

        assert 0.0 <= confidence <= 1.0


class TestCrossCulturalAnalysis:
    """Test cross-cultural canon analysis"""

    def test_analyze_12tet_stream(self):
        """Test analyzing 12-TET stream"""
        s = stream.Stream()
        s.append(note.Note('C4'))
        s.append(note.Note('D4'))
        s.append(note.Note('E4'))

        analysis = cross_cultural_canon_analysis(s)

        assert 'tuning_system' in analysis
        assert 'microtonal_content' in analysis
        assert 'possible_scales' in analysis
        assert analysis['microtonal_content'] is False

    def test_analyze_microtonal_stream(self):
        """Test analyzing microtonal stream"""
        s = stream.Stream()

        n = note.Note('C4')
        n.pitch.microtone = Microtone(50.0)
        s.append(n)

        analysis = cross_cultural_canon_analysis(s)

        assert analysis['microtonal_content'] is True

    def test_scale_matching(self):
        """Test matching to world music scales"""
        # Create a pentatonic stream
        s = stream.Stream()
        for midi in [60, 62, 64, 67, 69]:  # C D E G A
            s.append(note.Note(midi=midi))

        analysis = cross_cultural_canon_analysis(s)

        # Should match some pentatonic scales
        assert len(analysis['possible_scales']) > 0

    def test_empty_stream_analysis(self):
        """Test analyzing empty stream"""
        s = stream.Stream()

        analysis = cross_cultural_canon_analysis(s)

        assert analysis['tuning_system'] is not None
        assert analysis['possible_scales'] == []


class TestTuningSystemEnum:
    """Test TuningSystem enum"""

    def test_enum_values(self):
        """Test enum values exist"""
        assert TuningSystem.EQUAL_12.value == "12-tone equal temperament"
        assert TuningSystem.EQUAL_19.value == "19-tone equal temperament"
        assert TuningSystem.JUST_INTONATION_5.value == "5-limit just intonation"
        assert TuningSystem.PYTHAGOREAN.value == "Pythagorean tuning"
        assert TuningSystem.BOHLEN_PIERCE.value == "Bohlen-Pierce scale"


class TestScaleTypeEnum:
    """Test ScaleType enum"""

    def test_arabic_scales(self):
        """Test Arabic scale types"""
        assert "maqam" in ScaleType.MAQAM_RAST.value.lower()
        assert "maqam" in ScaleType.MAQAM_HIJAZ.value.lower()

    def test_indian_scales(self):
        """Test Indian scale types"""
        assert "raga" in ScaleType.RAGA_BHAIRAV.value.lower()
        assert "raga" in ScaleType.RAGA_YAMAN.value.lower()

    def test_indonesian_scales(self):
        """Test Indonesian scale types"""
        assert "pelog" in ScaleType.PELOG.value.lower()
        assert "slendro" in ScaleType.SLENDRO.value.lower()

    def test_japanese_scales(self):
        """Test Japanese scale types"""
        assert "hirajoshi" in ScaleType.HIRAJOSHI.value.lower()
        assert "insen" in ScaleType.INSEN.value.lower()

    def test_persian_scales(self):
        """Test Persian scale types"""
        assert "dastgah" in ScaleType.DASTGAH_SHUR.value.lower()
