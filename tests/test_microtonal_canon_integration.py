"""
Tests for microtonal canon integration features (Phase 20).
"""

import pytest
from music21 import stream, note, converter
from pathlib import Path
import tempfile

from cancrizans.canon import (
    create_microtonal_canon,
    generate_world_music_canon,
    analyze_microtonal_intervals,
    cross_cultural_canon_analysis
)
from cancrizans.microtonal import TuningSystem, ScaleType


class TestCreateMicrotonalCanon:
    """Tests for create_microtonal_canon function."""

    def test_create_microtonal_canon_retrograde(self):
        """Test creating a retrograde canon with just intonation."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1))
        theme.append(note.Note('E4', quarterLength=1))
        theme.append(note.Note('G4', quarterLength=1))

        canon = create_microtonal_canon(
            theme,
            TuningSystem.JUST_INTONATION_5,
            canon_type='retrograde',
            tonic_midi=60
        )

        assert isinstance(canon, stream.Score)
        assert len(canon.parts) == 2
        assert canon.metadata.title is not None
        assert 'Retrograde' in canon.metadata.title

    def test_create_microtonal_canon_inversion(self):
        """Test creating an inversion canon."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1))
        theme.append(note.Note('D4', quarterLength=1))
        theme.append(note.Note('E4', quarterLength=1))

        canon = create_microtonal_canon(
            theme,
            TuningSystem.PYTHAGOREAN,
            canon_type='inversion'
        )

        assert len(canon.parts) == 2
        assert 'Inversion' in canon.metadata.title

    def test_create_microtonal_canon_augmentation(self):
        """Test creating an augmentation canon."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1))
        theme.append(note.Note('G4', quarterLength=1))

        canon = create_microtonal_canon(
            theme,
            TuningSystem.MEANTONE,
            canon_type='augmentation'
        )

        assert len(canon.parts) == 2
        assert 'Augmentation' in canon.metadata.title

    def test_create_microtonal_canon_werckmeister(self):
        """Test creating a canon with Werckmeister III temperament."""
        theme = stream.Stream()
        for pitch in ['C4', 'D4', 'E4', 'F4', 'G4']:
            theme.append(note.Note(pitch, quarterLength=0.5))

        canon = create_microtonal_canon(
            theme,
            TuningSystem.WERCKMEISTER_III,
            canon_type='retrograde'
        )

        assert len(canon.parts) == 2
        assert canon.duration.quarterLength > 0

    def test_create_microtonal_canon_7_limit_ji(self):
        """Test creating a canon with 7-limit just intonation."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1))
        theme.append(note.Note('E4', quarterLength=1))
        theme.append(note.Note('G4', quarterLength=1))
        theme.append(note.Note('Bb4', quarterLength=1))

        canon = create_microtonal_canon(
            theme,
            TuningSystem.JUST_INTONATION_7,
            canon_type='retrograde',
            apply_pitch_bends=False
        )

        assert len(canon.parts) == 2

    def test_create_microtonal_canon_invalid_type(self):
        """Test that invalid canon type raises error."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1))

        with pytest.raises(ValueError, match="Unknown canon_type"):
            create_microtonal_canon(
                theme,
                TuningSystem.EQUAL_12,
                canon_type='invalid_type'
            )


class TestGenerateWorldMusicCanon:
    """Tests for generate_world_music_canon function."""

    def test_generate_maqam_hijaz_canon(self):
        """Test generating an Arabic maqam Hijaz canon."""
        canon = generate_world_music_canon(
            ScaleType.MAQAM_HIJAZ,
            length=12,
            canon_type='retrograde'
        )

        assert isinstance(canon, stream.Score)
        assert len(canon.parts) == 2
        # Check that notes were generated
        notes = canon.flatten().notes
        assert len(notes) >= 12

    def test_generate_raga_bhairav_canon(self):
        """Test generating an Indian raga Bhairav canon."""
        canon = generate_world_music_canon(
            ScaleType.RAGA_BHAIRAV,
            length=16,
            canon_type='inversion'
        )

        assert len(canon.parts) == 2
        assert canon.duration.quarterLength > 0

    def test_generate_pelog_canon(self):
        """Test generating an Indonesian gamelan Pelog canon."""
        canon = generate_world_music_canon(
            ScaleType.PELOG,
            length=10,
            canon_type='retrograde',
            octave_range=1
        )

        assert len(canon.parts) == 2
        notes = canon.flatten().notes
        assert len(notes) >= 10

    def test_generate_slendro_canon(self):
        """Test generating an Indonesian gamelan Slendro canon."""
        canon = generate_world_music_canon(
            ScaleType.SLENDRO,
            length=8,
            canon_type='augmentation'
        )

        assert len(canon.parts) == 2

    def test_generate_japanese_in_scale_canon(self):
        """Test generating a Japanese In scale canon."""
        canon = generate_world_music_canon(
            ScaleType.IN,
            length=14,
            canon_type='retrograde',
            octave_range=3
        )

        assert len(canon.parts) == 2
        assert canon.duration.quarterLength > 0


class TestAnalyzeMicrotonalIntervals:
    """Tests for analyze_microtonal_intervals function."""

    def test_analyze_simple_melody(self):
        """Test analyzing intervals in a simple melody."""
        melody = stream.Stream()
        melody.append(note.Note('C4', quarterLength=1))
        melody.append(note.Note('E4', quarterLength=1))
        melody.append(note.Note('G4', quarterLength=1))

        analysis = analyze_microtonal_intervals(melody)

        assert 'cents_histogram' in analysis
        assert 'average_cents' in analysis
        assert 'just_ratios' in analysis
        assert 'complexity_score' in analysis
        assert 'tuning_deviation' in analysis
        assert analysis['total_intervals'] == 2

    def test_analyze_with_tuning_system(self):
        """Test analyzing with a specific tuning system."""
        melody = stream.Stream()
        for pitch in ['C4', 'D4', 'E4', 'F4', 'G4']:
            melody.append(note.Note(pitch, quarterLength=1))

        analysis = analyze_microtonal_intervals(
            melody,
            tuning_system=TuningSystem.JUST_INTONATION_5
        )

        assert 'tuning_deviation' in analysis
        assert isinstance(analysis['tuning_deviation'], float)
        assert analysis['tuning_deviation'] >= 0

    def test_analyze_just_intonation_ratios(self):
        """Test detection of just intonation ratios."""
        melody = stream.Stream()
        # Perfect fifth (3:2 ratio)
        melody.append(note.Note('C4', quarterLength=1))
        melody.append(note.Note('G4', quarterLength=1))
        # Perfect fourth (4:3 ratio)
        melody.append(note.Note('C4', quarterLength=1))

        analysis = analyze_microtonal_intervals(melody)

        # Should detect some just ratios (perfect fifth, fourth)
        assert len(analysis['just_ratios']) > 0

    def test_analyze_empty_stream(self):
        """Test analyzing an empty stream."""
        empty = stream.Stream()

        analysis = analyze_microtonal_intervals(empty)

        assert analysis['average_cents'] == 0.0
        assert len(analysis['just_ratios']) == 0
        assert analysis['complexity_score'] == 0.0

    def test_analyze_single_note(self):
        """Test analyzing a stream with single note."""
        single = stream.Stream()
        single.append(note.Note('C4', quarterLength=1))

        analysis = analyze_microtonal_intervals(single)

        # Single note should have no intervals
        assert 'total_intervals' in analysis
        assert 'average_cents' in analysis


class TestCrossCulturalCanonAnalysis:
    """Tests for cross_cultural_canon_analysis function."""

    def test_analyze_western_canon(self):
        """Test analyzing a Western canon against world scales."""
        canon = stream.Score()
        part = stream.Part()
        for pitch in ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']:
            part.append(note.Note(pitch, quarterLength=1))
        canon.append(part)

        analysis = cross_cultural_canon_analysis(canon)

        assert isinstance(analysis, dict)
        assert len(analysis) == 8  # Default tests 8 scales

        # Check that each result has required keys
        for scale_name, metrics in analysis.items():
            assert 'compatibility' in metrics
            assert 'tuning_deviation' in metrics
            assert 'average_cents' in metrics
            assert 'complexity_score' in metrics
            assert 'scale_consonance' in metrics
            assert 'just_ratios_found' in metrics

    def test_analyze_with_custom_scales(self):
        """Test analyzing with custom scale list."""
        canon = stream.Score()
        part = stream.Part()
        for pitch in ['C4', 'E4', 'G4', 'C5']:
            part.append(note.Note(pitch, quarterLength=1))
        canon.append(part)

        test_scales = [
            ScaleType.MAQAM_HIJAZ,
            ScaleType.PELOG,
            ScaleType.RAGA_BHAIRAV
        ]

        analysis = cross_cultural_canon_analysis(canon, test_scales=test_scales)

        assert len(analysis) == 3

    def test_compatibility_scores_range(self):
        """Test that compatibility scores are in valid range."""
        canon = stream.Score()
        part = stream.Part()
        for pitch in ['C4', 'D4', 'E4']:
            part.append(note.Note(pitch, quarterLength=1))
        canon.append(part)

        analysis = cross_cultural_canon_analysis(canon)

        for metrics in analysis.values():
            # Compatibility should be between 0 and 1
            assert 0.0 <= metrics['compatibility'] <= 1.0
            # Deviation should be non-negative
            assert metrics['tuning_deviation'] >= 0


class TestMicrotonalCanonIntegration:
    """Integration tests for the full microtonal canon workflow."""

    def test_full_workflow_just_intonation(self):
        """Test complete workflow: create theme, generate canon, analyze."""
        # Create theme
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1))
        theme.append(note.Note('E4', quarterLength=1))
        theme.append(note.Note('G4', quarterLength=1))
        theme.append(note.Note('C5', quarterLength=1))

        # Generate canon
        canon = create_microtonal_canon(
            theme,
            TuningSystem.JUST_INTONATION_5,
            canon_type='retrograde'
        )

        # Analyze
        analysis = analyze_microtonal_intervals(
            canon,
            tuning_system=TuningSystem.JUST_INTONATION_5
        )

        assert analysis['total_intervals'] > 0
        assert isinstance(analysis['tuning_deviation'], float)

    def test_full_workflow_world_music(self):
        """Test workflow with world music scale generation."""
        # Generate world music canon
        canon = generate_world_music_canon(
            ScaleType.MAQAM_HIJAZ,
            length=12,
            canon_type='inversion'
        )

        # Analyze cross-culturally
        analysis = cross_cultural_canon_analysis(canon)

        # Should have high compatibility with Arabic maqam
        assert 'Arabic maqam Hijaz' in analysis
        # Hijaz should have reasonable compatibility
        assert analysis['Arabic maqam Hijaz']['compatibility'] > 0

    def test_export_and_reimport(self):
        """Test exporting and re-importing a microtonal canon."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1))
        theme.append(note.Note('G4', quarterLength=1))

        canon = create_microtonal_canon(
            theme,
            TuningSystem.PYTHAGOREAN,
            canon_type='retrograde'
        )

        # Export to temporary file
        with tempfile.NamedTemporaryFile(suffix='.musicxml', delete=False) as f:
            temp_path = f.name

        try:
            canon.write('musicxml', temp_path)

            # Re-import
            reimported = converter.parse(temp_path)

            assert isinstance(reimported, stream.Score)
            assert len(reimported.parts) == 2
        finally:
            Path(temp_path).unlink(missing_ok=True)

    def test_different_tuning_systems(self):
        """Test creating canons with various tuning systems."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1))
        theme.append(note.Note('E4', quarterLength=1))

        tuning_systems = [
            TuningSystem.PYTHAGOREAN,
            TuningSystem.MEANTONE,
            TuningSystem.WERCKMEISTER_III,
            TuningSystem.JUST_INTONATION_7,
            TuningSystem.EQUAL_19,
            TuningSystem.BOHLEN_PIERCE
        ]

        for tuning in tuning_systems:
            canon = create_microtonal_canon(
                theme,
                tuning,
                canon_type='retrograde'
            )
            assert len(canon.parts) == 2
            assert tuning.value in canon.metadata.title
