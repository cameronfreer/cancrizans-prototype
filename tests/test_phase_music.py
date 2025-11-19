"""
Comprehensive tests for Steve Reich phase music techniques

Tests for phase canon generation, tape loop simulation, phase analysis,
minimal pattern generation, and phase visualization.
"""

import pytest
import tempfile
from pathlib import Path
from music21 import stream, note, chord
from PIL import Image

from cancrizans import (
    phase_canon,
    tape_loop_phase,
    calculate_phase_offset,
    analyze_phase_relationships,
    generate_minimal_pattern,
    create_phase_progression,
    detect_phase_patterns,
    apply_gradual_tempo_shift,
)
from cancrizans.viz import visualize_phase_evolution


class TestPhaseCanon:
    """Test phase_canon function"""

    def test_phase_canon_basic(self):
        """Test basic phase canon creation"""
        # Create simple theme
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=0.5))
        theme.append(note.Note('E4', quarterLength=0.5))
        theme.append(note.Note('G4', quarterLength=0.5))
        theme.append(note.Note('E4', quarterLength=0.5))

        score = phase_canon(theme, num_voices=2, phase_shift_beats=0.125, duration_beats=16.0)

        assert isinstance(score, stream.Score)
        assert len(list(score.parts)) == 2

    def test_phase_canon_gradual_method(self):
        """Test gradual phase method"""
        theme = stream.Stream()
        theme.append(note.Note('D4', quarterLength=1.0))

        score = phase_canon(theme, num_voices=2, phase_method="gradual", duration_beats=8.0)

        assert isinstance(score, stream.Score)
        parts = list(score.parts)
        assert len(parts) == 2
        assert parts[0].id == "Voice_1"
        assert parts[1].id == "Voice_2"

    def test_phase_canon_stepped_method(self):
        """Test stepped phase method"""
        theme = stream.Stream()
        theme.append(note.Note('E4', quarterLength=0.5))
        theme.append(note.Note('G4', quarterLength=0.5))

        score = phase_canon(theme, num_voices=2, phase_method="stepped", duration_beats=8.0)

        assert isinstance(score, stream.Score)
        assert len(list(score.parts)) == 2

    def test_phase_canon_multiple_voices(self):
        """Test phase canon with multiple voices"""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=0.25))
        theme.append(note.Note('D4', quarterLength=0.25))
        theme.append(note.Note('E4', quarterLength=0.25))
        theme.append(note.Note('F4', quarterLength=0.25))

        score = phase_canon(theme, num_voices=4, phase_shift_beats=0.0625, duration_beats=16.0)

        assert isinstance(score, stream.Score)
        assert len(list(score.parts)) == 4

    def test_phase_canon_zero_duration_theme(self):
        """Test that zero-duration theme raises error"""
        theme = stream.Stream()

        with pytest.raises(ValueError, match="Theme must have non-zero duration"):
            phase_canon(theme, num_voices=2)

    def test_phase_canon_invalid_method(self):
        """Test that invalid phase method raises error"""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))

        with pytest.raises(ValueError, match="Unknown phase method"):
            phase_canon(theme, num_voices=2, phase_method="invalid")

    def test_phase_canon_with_chord(self):
        """Test phase canon with chords in theme"""
        theme = stream.Stream()
        theme.append(chord.Chord(['C4', 'E4', 'G4'], quarterLength=0.5))
        theme.append(chord.Chord(['F4', 'A4', 'C5'], quarterLength=0.5))

        score = phase_canon(theme, num_voices=2, duration_beats=8.0)

        assert isinstance(score, stream.Score)
        parts = list(score.parts)
        # Verify chords were copied
        for part in parts:
            has_chord = any(isinstance(el, chord.Chord) for el in part.flatten().notesAndRests)
            assert has_chord

    def test_phase_canon_long_duration(self):
        """Test phase canon with longer duration"""
        theme = stream.Stream()
        theme.append(note.Note('A4', quarterLength=0.5))

        score = phase_canon(theme, num_voices=2, duration_beats=64.0, phase_shift_beats=0.25)

        assert isinstance(score, stream.Score)
        parts = list(score.parts)
        assert all(p.duration.quarterLength > 60 for p in parts)


class TestTapeLoopPhase:
    """Test tape_loop_phase function"""

    def test_tape_loop_basic(self):
        """Test basic tape loop phasing"""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('G4', quarterLength=1.0))

        score = tape_loop_phase(theme, num_loops=2, duration_beats=16.0)

        assert isinstance(score, stream.Score)
        assert len(list(score.parts)) == 2

    def test_tape_loop_custom_speed_ratios(self):
        """Test tape loop with custom speed ratios"""
        theme = stream.Stream()
        theme.append(note.Note('D4', quarterLength=0.5))

        score = tape_loop_phase(theme, num_loops=3,
                               loop_speed_ratios=[1.0, 1.005, 1.01],
                               duration_beats=32.0)

        assert isinstance(score, stream.Score)
        parts = list(score.parts)
        assert len(parts) == 3
        # Check that part IDs contain speed information
        assert "speed:" in parts[0].id
        assert "speed:" in parts[1].id

    def test_tape_loop_mismatched_speed_ratios(self):
        """Test that mismatched speed ratios raise error"""
        theme = stream.Stream()
        theme.append(note.Note('E4', quarterLength=1.0))

        with pytest.raises(ValueError, match="Need .* speed ratios"):
            tape_loop_phase(theme, num_loops=3,
                           loop_speed_ratios=[1.0, 1.01],  # Only 2 ratios for 3 loops
                           duration_beats=16.0)

    def test_tape_loop_default_speed_ratios(self):
        """Test tape loop with default speed ratios"""
        theme = stream.Stream()
        theme.append(note.Note('F4', quarterLength=0.5))

        score = tape_loop_phase(theme, num_loops=3, duration_beats=16.0)

        parts = list(score.parts)
        assert len(parts) == 3

    def test_tape_loop_single_loop(self):
        """Test tape loop with single loop"""
        theme = stream.Stream()
        theme.append(note.Note('G4', quarterLength=1.0))

        score = tape_loop_phase(theme, num_loops=1,
                               loop_speed_ratios=[1.0],
                               duration_beats=8.0)

        assert len(list(score.parts)) == 1


class TestCalculatePhaseOffset:
    """Test calculate_phase_offset function"""

    def test_phase_offset_in_phase(self):
        """Test phase offset when voices are in phase"""
        offset = calculate_phase_offset(0.0, 0.0, 2.0)
        assert offset == 0.0

    def test_phase_offset_half_cycle(self):
        """Test phase offset at half cycle"""
        offset = calculate_phase_offset(0.0, 1.0, 2.0)
        assert abs(offset - 0.5) < 0.01

    def test_phase_offset_quarter_cycle(self):
        """Test phase offset at quarter cycle"""
        offset = calculate_phase_offset(0.0, 0.5, 2.0)
        assert abs(offset - 0.25) < 0.01

    def test_phase_offset_wrapping(self):
        """Test phase offset wrapping behavior"""
        # 1.5 / 2.0 = 0.75, which wraps to 0.25
        offset = calculate_phase_offset(0.0, 1.5, 2.0)
        assert abs(offset - 0.25) < 0.01

    def test_phase_offset_with_offset_times(self):
        """Test phase offset with different voice times"""
        offset = calculate_phase_offset(2.0, 3.0, 4.0)
        assert 0.0 <= offset <= 0.5

    def test_phase_offset_zero_pattern_length(self):
        """Test that zero pattern length raises error"""
        with pytest.raises(ValueError, match="Pattern length must be positive"):
            calculate_phase_offset(0.0, 1.0, 0.0)

    def test_phase_offset_negative_pattern_length(self):
        """Test that negative pattern length raises error"""
        with pytest.raises(ValueError, match="Pattern length must be positive"):
            calculate_phase_offset(0.0, 1.0, -2.0)


class TestAnalyzePhaseRelationships:
    """Test analyze_phase_relationships function"""

    def test_analyze_phase_basic(self):
        """Test basic phase relationship analysis"""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        score = phase_canon(theme, num_voices=2, duration_beats=16.0)

        analysis = analyze_phase_relationships(score, pattern_length=1.0, num_samples=50)

        assert 'num_voices' in analysis
        assert 'pattern_length' in analysis
        assert 'total_duration' in analysis
        assert 'phase_evolution' in analysis
        assert 'synchronization_points' in analysis
        assert 'average_phase_offset' in analysis
        assert analysis['num_voices'] == 2

    def test_analyze_phase_single_voice(self):
        """Test phase analysis with single voice"""
        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('C4', quarterLength=1.0))
        score.append(part)

        analysis = analyze_phase_relationships(score, pattern_length=1.0)

        assert analysis['num_voices'] == 1
        assert analysis['phase_evolution'] == []
        assert analysis['synchronization_points'] == []

    def test_analyze_phase_evolution_length(self):
        """Test that phase evolution has correct number of samples"""
        theme = stream.Stream()
        theme.append(note.Note('D4', quarterLength=0.5))
        score = phase_canon(theme, num_voices=2, duration_beats=8.0)

        analysis = analyze_phase_relationships(score, pattern_length=0.5, num_samples=20)

        assert len(analysis['phase_evolution']) == 20

    def test_analyze_phase_synchronization_detection(self):
        """Test synchronization point detection"""
        theme = stream.Stream()
        theme.append(note.Note('E4', quarterLength=1.0))
        score = phase_canon(theme, num_voices=2, phase_shift_beats=0.0, duration_beats=8.0)

        analysis = analyze_phase_relationships(score, pattern_length=1.0, num_samples=100)

        # With no phase shift, should have many sync points
        assert analysis['num_sync_points'] > 0


class TestGenerateMinimalPattern:
    """Test generate_minimal_pattern function"""

    def test_generate_minimal_pattern_basic(self):
        """Test basic minimal pattern generation"""
        pattern = generate_minimal_pattern(['C4', 'E4', 'G4'], note_duration=0.5, num_repetitions=1)

        assert isinstance(pattern, stream.Stream)
        notes = list(pattern.flatten().notes)
        assert len(notes) == 3
        assert all(n.quarterLength == 0.5 for n in notes)

    def test_generate_minimal_pattern_multiple_repetitions(self):
        """Test minimal pattern with multiple repetitions"""
        pattern = generate_minimal_pattern(['D4', 'F4'], note_duration=0.25, num_repetitions=4)

        notes = list(pattern.flatten().notes)
        assert len(notes) == 8  # 2 pitches * 4 repetitions

    def test_generate_minimal_pattern_reich_style(self):
        """Test Reich-style pattern (like 'Piano Phase')"""
        pattern = generate_minimal_pattern(['E4', 'F#4', 'B4', 'C#5', 'D5', 'F#4', 'E4', 'C#5', 'B4', 'F#4', 'D5', 'C#5'],
                                          note_duration=0.25, num_repetitions=2)

        notes = list(pattern.flatten().notes)
        assert len(notes) == 24  # 12 pitches * 2 repetitions
        assert all(n.quarterLength == 0.25 for n in notes)

    def test_generate_minimal_pattern_single_note(self):
        """Test minimal pattern with single pitch"""
        pattern = generate_minimal_pattern(['A4'], note_duration=1.0, num_repetitions=8)

        notes = list(pattern.flatten().notes)
        assert len(notes) == 8
        assert all(n.pitch.nameWithOctave == 'A4' for n in notes)

    def test_generate_minimal_pattern_no_repetitions(self):
        """Test minimal pattern with zero repetitions"""
        pattern = generate_minimal_pattern(['C4', 'E4'], note_duration=0.5, num_repetitions=0)

        notes = list(pattern.flatten().notes)
        assert len(notes) == 0


class TestCreatePhaseProgression:
    """Test create_phase_progression function"""

    def test_phase_progression_basic(self):
        """Test basic phase progression creation"""
        base_pattern = stream.Stream()
        base_pattern.append(note.Note('C4', quarterLength=0.5))
        base_pattern.append(note.Note('G4', quarterLength=0.5))

        progression = create_phase_progression(base_pattern, num_phases=4, phase_increment=0.25)

        assert len(progression) == 4
        assert all(isinstance(score, stream.Score) for score in progression)
        assert all(len(list(score.parts)) == 2 for score in progression)

    def test_phase_progression_increments(self):
        """Test that phase progression creates correct increments"""
        base_pattern = stream.Stream()
        base_pattern.append(note.Note('D4', quarterLength=1.0))

        progression = create_phase_progression(base_pattern, num_phases=8, phase_increment=0.125)

        assert len(progression) == 8
        # Each score should have 2 parts
        for i, score in enumerate(progression):
            parts = list(score.parts)
            assert len(parts) == 2
            assert parts[0].id == "Voice_1"
            assert parts[1].id == "Voice_2"

    def test_phase_progression_single_phase(self):
        """Test phase progression with single phase"""
        base_pattern = stream.Stream()
        base_pattern.append(note.Note('E4', quarterLength=0.5))

        progression = create_phase_progression(base_pattern, num_phases=1)

        assert len(progression) == 1


class TestDetectPhasePatterns:
    """Test detect_phase_patterns function"""

    def test_detect_phase_patterns_basic(self):
        """Test basic phase pattern detection"""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=0.5))
        theme.append(note.Note('E4', quarterLength=0.5))
        score = phase_canon(theme, num_voices=2, duration_beats=16.0)

        patterns = detect_phase_patterns(score, pattern_length=1.0, window_size=4)

        assert isinstance(patterns, list)
        assert len(patterns) > 0
        assert all('rhythmic_density' in p for p in patterns)
        assert all('synchronous_attacks' in p for p in patterns)
        assert all('complexity' in p for p in patterns)

    def test_detect_phase_patterns_single_voice(self):
        """Test pattern detection with single voice"""
        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('C4', quarterLength=1.0))
        part.append(note.Note('D4', quarterLength=1.0))
        score.append(part)

        patterns = detect_phase_patterns(score, pattern_length=1.0)

        assert patterns == []

    def test_detect_phase_patterns_window_analysis(self):
        """Test that pattern detection analyzes windows correctly"""
        theme = stream.Stream()
        for i in range(8):
            theme.append(note.Note('C4', quarterLength=0.25))

        score = phase_canon(theme, num_voices=2, duration_beats=16.0)
        patterns = detect_phase_patterns(score, pattern_length=2.0, window_size=8)

        assert all('start_time' in p for p in patterns)
        assert all('end_time' in p for p in patterns)
        assert all(p['end_time'] - p['start_time'] == 8 for p in patterns)


class TestApplyGradualTempoShift:
    """Test apply_gradual_tempo_shift function"""

    def test_tempo_shift_linear(self):
        """Test linear tempo shift"""
        part = stream.Part()
        part.append(note.Note('C4', quarterLength=1.0))
        part.append(note.Note('D4', quarterLength=1.0))
        part.append(note.Note('E4', quarterLength=1.0))

        shifted = apply_gradual_tempo_shift(part, start_tempo=120.0, end_tempo=124.0, interpolation="linear")

        assert isinstance(shifted, stream.Part)
        notes = list(shifted.flatten().notes)
        assert len(notes) == 3

    def test_tempo_shift_exponential(self):
        """Test exponential tempo shift"""
        part = stream.Part()
        part.append(note.Note('F4', quarterLength=0.5))
        part.append(note.Note('G4', quarterLength=0.5))

        shifted = apply_gradual_tempo_shift(part, start_tempo=120.0, end_tempo=121.0, interpolation="exponential")

        assert isinstance(shifted, stream.Part)
        assert len(list(shifted.flatten().notes)) == 2

    def test_tempo_shift_logarithmic(self):
        """Test logarithmic tempo shift"""
        part = stream.Part()
        part.append(note.Note('A4', quarterLength=1.0))
        part.append(note.Note('B4', quarterLength=1.0))

        shifted = apply_gradual_tempo_shift(part, start_tempo=120.0, end_tempo=119.0, interpolation="logarithmic")

        assert isinstance(shifted, stream.Part)
        notes = list(shifted.flatten().notes)
        assert len(notes) == 2

    def test_tempo_shift_empty_part(self):
        """Test tempo shift with empty part"""
        part = stream.Part()

        shifted = apply_gradual_tempo_shift(part, start_tempo=120.0, end_tempo=121.0)

        assert isinstance(shifted, stream.Part)
        assert len(list(shifted.flatten().notes)) == 0

    def test_tempo_shift_invalid_interpolation(self):
        """Test that invalid interpolation raises error"""
        part = stream.Part()
        part.append(note.Note('C4', quarterLength=1.0))

        with pytest.raises(ValueError, match="Unknown interpolation"):
            apply_gradual_tempo_shift(part, interpolation="invalid")

    def test_tempo_shift_preserves_pitches(self):
        """Test that tempo shift preserves pitches"""
        part = stream.Part()
        original_pitches = ['C4', 'D4', 'E4', 'F4']
        for pitch in original_pitches:
            part.append(note.Note(pitch, quarterLength=0.5))

        shifted = apply_gradual_tempo_shift(part, start_tempo=120.0, end_tempo=122.0)

        shifted_notes = list(shifted.flatten().notes)
        shifted_pitches = [n.pitch.nameWithOctave for n in shifted_notes]
        assert shifted_pitches == original_pitches

    def test_tempo_shift_with_chord(self):
        """Test tempo shift with chords"""
        part = stream.Part()
        part.append(chord.Chord(['C4', 'E4', 'G4'], quarterLength=1.0))
        part.append(chord.Chord(['F4', 'A4', 'C5'], quarterLength=1.0))

        shifted = apply_gradual_tempo_shift(part, start_tempo=120.0, end_tempo=121.0)

        chords_in_shifted = list(shifted.flatten().getElementsByClass(chord.Chord))
        assert len(chords_in_shifted) == 2


class TestPhaseVisualization:
    """Test visualize_phase_evolution function"""

    def test_visualize_phase_evolution_basic(self):
        """Test basic phase evolution visualization"""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        score = phase_canon(theme, num_voices=2, phase_shift_beats=0.125, duration_beats=16.0)

        analysis = analyze_phase_relationships(score, pattern_length=1.0, num_samples=50)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'phase_viz.png'
            result = visualize_phase_evolution(analysis, output)

            assert result.exists()
            img = Image.open(result)
            assert img.format == 'PNG'
            assert img.size[0] > 0
            assert img.size[1] > 0

    def test_visualize_phase_evolution_high_dpi(self):
        """Test phase visualization with high DPI"""
        theme = stream.Stream()
        theme.append(note.Note('D4', quarterLength=0.5))
        score = phase_canon(theme, num_voices=2, duration_beats=8.0)

        analysis = analyze_phase_relationships(score, pattern_length=0.5)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'phase_high_dpi.png'
            result = visualize_phase_evolution(analysis, output, dpi=150)

            assert result.exists()

    def test_visualize_phase_evolution_creates_dir(self):
        """Test that visualization creates parent directory"""
        theme = stream.Stream()
        theme.append(note.Note('E4', quarterLength=1.0))
        score = phase_canon(theme, num_voices=2, duration_beats=8.0)

        analysis = analyze_phase_relationships(score, pattern_length=1.0)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'subdir' / 'phase.png'
            result = visualize_phase_evolution(analysis, output)

            assert result.exists()
            assert result.parent.exists()


class TestIntegrationPhaseMusic:
    """Integration tests for phase music features"""

    def test_full_phase_workflow(self):
        """Test complete phase music workflow"""
        # Generate minimal Reich-style pattern
        pattern = generate_minimal_pattern(['E4', 'F#4', 'B4', 'C#5'], note_duration=0.25, num_repetitions=4)

        # Create phase canon
        score = phase_canon(pattern, num_voices=2, phase_shift_beats=0.0625, duration_beats=32.0)

        # Analyze phase relationships
        analysis = analyze_phase_relationships(score, pattern_length=1.0, num_samples=100)

        # Detect emergent patterns
        patterns = detect_phase_patterns(score, pattern_length=1.0, window_size=8)

        assert isinstance(score, stream.Score)
        assert analysis['num_voices'] == 2
        assert len(patterns) > 0

    def test_tape_loop_with_analysis(self):
        """Test tape loop with phase analysis"""
        theme = generate_minimal_pattern(['C4', 'G4', 'E4'], note_duration=0.5, num_repetitions=2)

        score = tape_loop_phase(theme, num_loops=2,
                               loop_speed_ratios=[1.0, 1.01],
                               duration_beats=32.0)

        patterns = detect_phase_patterns(score, pattern_length=1.5, window_size=4)

        assert len(list(score.parts)) == 2
        assert len(patterns) > 0

    def test_phase_progression_visualization(self):
        """Test creating and visualizing phase progression"""
        base_pattern = generate_minimal_pattern(['D4', 'F4', 'A4'], note_duration=0.5)

        progression = create_phase_progression(base_pattern, num_phases=8, phase_increment=0.125)

        # Analyze the final state
        final_score = progression[-1]
        analysis = analyze_phase_relationships(final_score, pattern_length=1.5)

        assert len(progression) == 8
        assert analysis['num_voices'] == 2

    def test_gradual_tempo_on_phased_score(self):
        """Test applying gradual tempo shift to phased score"""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=0.5))
        theme.append(note.Note('E4', quarterLength=0.5))

        score = phase_canon(theme, num_voices=2, duration_beats=16.0)

        # Apply tempo shift to first part
        parts = list(score.parts)
        shifted_part = apply_gradual_tempo_shift(parts[0], start_tempo=120.0, end_tempo=122.0)

        assert isinstance(shifted_part, stream.Part)
        assert len(list(shifted_part.flatten().notes)) > 0
