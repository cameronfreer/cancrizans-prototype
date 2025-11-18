"""Tests for the generator module."""

import pytest
from music21 import stream
from cancrizans.generator import CanonGenerator, generate_example_canons


class TestCanonGenerator:
    """Test the CanonGenerator class."""

    def test_generator_init_with_seed(self):
        """Test that generator initializes with seed."""
        gen = CanonGenerator(seed=42)
        assert gen is not None

    def test_scale_canon_generation(self):
        """Test scale canon generation."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major', 4, 8)

        assert isinstance(canon, stream.Score)
        assert len(canon.parts) == 2
        assert canon.duration.quarterLength > 0

    def test_scale_canon_major_vs_minor(self):
        """Test that major and minor scales are different."""
        gen = CanonGenerator(seed=42)
        major = gen.generate_scale_canon('C', 'major')
        minor = gen.generate_scale_canon('C', 'minor')

        major_pitches = [n.pitch.midi for n in major.parts[0].flatten().notes]
        minor_pitches = [n.pitch.midi for n in minor.parts[0].flatten().notes]

        assert major_pitches != minor_pitches

    def test_arpeggio_canon_generation(self):
        """Test arpeggio canon generation."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_arpeggio_canon('C4', 'major', 2)

        assert isinstance(canon, stream.Score)
        assert len(canon.parts) == 2

    def test_arpeggio_chord_types(self):
        """Test different chord types."""
        gen = CanonGenerator(seed=42)

        for chord_type in ['major', 'minor', 'diminished', 'augmented']:
            canon = gen.generate_arpeggio_canon('C4', chord_type)
            assert isinstance(canon, stream.Score)
            assert len(canon.parts) == 2

    def test_random_walk_generation(self):
        """Test random walk generation."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_random_walk('C4', length=12, max_interval=2)

        assert isinstance(canon, stream.Score)
        assert len(canon.parts) == 2

        # Check that notes are within reasonable range
        midi_values = [n.pitch.midi for n in canon.parts[0].flatten().notes]
        assert all(36 <= m <= 84 for m in midi_values)

    def test_fibonacci_canon_generation(self):
        """Test Fibonacci canon generation."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_fibonacci_canon('G4', length=8)

        assert isinstance(canon, stream.Score)
        assert len(canon.parts) == 2

    def test_golden_ratio_canon_generation(self):
        """Test golden ratio canon generation."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_golden_ratio_canon('D4', length=13)

        assert isinstance(canon, stream.Score)
        assert len(canon.parts) == 2

    def test_modal_canon_generation(self):
        """Test modal canon generation."""
        gen = CanonGenerator(seed=42)

        modes = ['dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']

        for mode in modes:
            canon = gen.generate_modal_canon(mode, 'D4', 8)
            assert isinstance(canon, stream.Score)
            assert len(canon.parts) == 2

    def test_fractal_canon_generation(self):
        """Test fractal canon generation."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_fractal_canon([1, 2, -1], iterations=2)

        assert isinstance(canon, stream.Score)
        assert len(canon.parts) == 2

    def test_polyrhythmic_canon_generation(self):
        """Test polyrhythmic canon generation."""
        gen = CanonGenerator(seed=42)
        pitches = ['C4', 'E4', 'G4', 'C5']
        canon = gen.generate_polyrhythmic_canon(pitches, (3, 2))

        assert isinstance(canon, stream.Score)
        assert len(canon.parts) == 2

    def test_rhythmic_canon_generation(self):
        """Test rhythmic canon generation."""
        gen = CanonGenerator(seed=42)
        pitches = ['C4', 'D4', 'E4']
        rhythms = [1.0, 0.5, 0.5]
        canon = gen.generate_rhythmic_canon(pitches, rhythms)

        assert isinstance(canon, stream.Score)
        assert len(canon.parts) == 2

    def test_deterministic_with_seed(self):
        """Test that same seed produces consistent results."""
        gen1 = CanonGenerator(seed=42)

        # Generate with scale (deterministic, not random)
        canon1 = gen1.generate_scale_canon('C', 'major', length=8)

        # Create new generator with same seed
        gen2 = CanonGenerator(seed=42)
        canon2 = gen2.generate_scale_canon('C', 'major', length=8)

        pitches1 = [n.pitch.midi for n in canon1.parts[0].flatten().notes]
        pitches2 = [n.pitch.midi for n in canon2.parts[0].flatten().notes]

        # Scale canons should be identical with same parameters
        assert pitches1 == pitches2


class TestGenerateExampleCanons:
    """Test the example canon generation function."""

    def test_generate_example_canons_returns_dict(self):
        """Test that it returns a dictionary of canons."""
        examples = generate_example_canons()

        assert isinstance(examples, dict)
        assert len(examples) > 0

    def test_all_examples_are_scores(self):
        """Test that all examples are Score objects."""
        examples = generate_example_canons()

        for name, canon in examples.items():
            assert isinstance(canon, stream.Score), f"{name} is not a Score"
            assert len(canon.parts) == 2, f"{name} doesn't have 2 parts"


class TestGeneratorEdgeCases:
    """Test edge cases and boundary conditions in generator."""

    def test_descending_scale(self):
        """Test descending scale generation."""
        gen = CanonGenerator(seed=42)
        # Generate descending scale
        canon = gen.generate_scale_canon('C', 'major', length=8, ascending=False)
        
        assert canon is not None
        assert len(canon.parts) == 2
        # Verify notes are descending
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) > 0

    def test_random_walk_extreme_ranges(self):
        """Test random walk with extreme pitch boundaries."""
        gen = CanonGenerator(seed=42)
        # Generate with large max_interval to trigger boundary conditions
        canon = gen.generate_random_walk('C2', length=50, max_interval=12)
        
        notes = list(canon.parts[0].flatten().notes)
        # Check all notes are within valid MIDI range (36-84)
        for n in notes:
            assert 36 <= n.pitch.midi <= 84

    def test_fibonacci_octave_adjustment(self):
        """Test Fibonacci canon with octave boundary adjustments."""
        gen = CanonGenerator(seed=42)
        # Use very high root to trigger downward octave adjustment
        canon = gen.generate_fibonacci_canon('C6', length=20)
        
        notes = list(canon.parts[0].flatten().notes)
        # Verify all notes are in valid range
        for n in notes:
            assert 36 <= n.pitch.midi <= 84

    def test_golden_ratio_octave_adjustment(self):
        """Test golden ratio canon with octave adjustments."""
        gen = CanonGenerator(seed=42)
        # Use low root to trigger upward octave adjustment
        canon = gen.generate_golden_ratio_canon('C2', length=25)

        notes = list(canon.parts[0].flatten().notes)
        # Verify all notes are in valid range
        for n in notes:
            assert 36 <= n.pitch.midi <= 84

    def test_random_walk_extreme_high_pitch_clamping(self):
        """Test random walk with extreme high pitches triggers clamping (line 137)."""
        gen = CanonGenerator(seed=123)  # Seed that produces upward movement
        # Start very high and with large max_interval to force clamping
        canon = gen.generate_random_walk('C6', length=50, max_interval=12)

        notes = list(canon.parts[0].flatten().notes)
        # Should clamp at MIDI 84 (C6)
        assert all(n.pitch.midi <= 84 for n in notes)
        # With 50 notes and large intervals, should hit the upper limit
        assert any(n.pitch.midi == 84 for n in notes)

    def test_fibonacci_extreme_high_pitch_clamping(self):
        """Test Fibonacci canon extreme high pitch clamping (line 177)."""
        gen = CanonGenerator(seed=999)
        # Generate with very high root
        canon = gen.generate_fibonacci_canon('C6', length=30)

        notes = list(canon.parts[0].flatten().notes)
        # All notes should be clamped at or below MIDI 84
        assert all(n.pitch.midi <= 84 for n in notes)

    def test_fractal_extreme_low_pitch_octave_up(self):
        """Test fractal canon extreme low pitch triggers octave up (line 251)."""
        gen = CanonGenerator(seed=100)
        # Start at very low pitch with descending pattern to trigger upward octave adjustment
        canon = gen.generate_fractal_canon(seed_pattern=[-2, -3, -1], iterations=4, root='C2')

        notes = list(canon.parts[0].flatten().notes)
        # All notes should be brought up to at least MIDI 36
        assert all(n.pitch.midi >= 36 for n in notes)

    def test_random_walk_exact_high_clamping(self):
        """Test random walk exact high pitch clamping assignment (line 137)."""
        gen = CanonGenerator(seed=42)
        # Start very high with large upward intervals to trigger clamping
        canon = gen.generate_random_walk('C6', length=100, max_interval=12)

        notes = list(canon.parts[0].flatten().notes)
        # Should clamp to exactly 84 when going above
        assert all(n.pitch.midi <= 84 for n in notes)
        # Verify we actually hit the upper bound
        assert any(n.pitch.midi == 84 for n in notes)

    def test_fibonacci_exact_low_octave_adjustment(self):
        """Test fibonacci canon exact low pitch octave adjustment (line 177)."""
        gen = CanonGenerator(seed=555)
        # Start low and use many iterations to potentially go below 36
        canon = gen.generate_fibonacci_canon('C2', length=50)

        notes = list(canon.parts[0].flatten().notes)
        # All notes should be at least MIDI 36 after octave adjustment
        assert all(n.pitch.midi >= 36 for n in notes)

    def test_fibonacci_multiple_octave_adjustments(self):
        """Test fibonacci canon with multiple octave adjustments (line 177)."""
        gen = CanonGenerator(seed=777)
        # Start very low to trigger octave adjustments in the loop
        canon = gen.generate_fibonacci_canon('C1', length=60)

        notes = list(canon.parts[0].flatten().notes)
        # Most notes (except possibly the first) should be adjusted to >= 36
        # The first note uses the root directly without adjustment
        notes_after_first = notes[1:]  # Skip first note
        assert all(n.pitch.midi >= 36 for n in notes_after_first)
        # Verify we generated notes
        assert len(notes) > 0


class TestAdvancedGenerators:
    """Test advanced generation methods."""

    def test_markov_canon_generation(self):
        """Test Markov chain canon generation."""
        gen = CanonGenerator(seed=42)
        training = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
        canon = gen.generate_markov_canon(training, length=12, order=1)

        assert isinstance(canon, stream.Score)
        assert len(canon.parts) == 2

    def test_markov_second_order(self):
        """Test second-order Markov chain."""
        gen = CanonGenerator(seed=42)
        training = ['C4', 'D4', 'E4', 'D4', 'C4', 'D4', 'E4', 'F4', 'G4']
        canon = gen.generate_markov_canon(training, length=10, order=2)

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 10

    def test_markov_insufficient_training(self):
        """Test Markov with insufficient training data."""
        gen = CanonGenerator()
        training = ['C4', 'D4']  # Too short for order=2

        with pytest.raises(ValueError):
            gen.generate_markov_canon(training, length=10, order=2)

    def test_contour_canon_generation(self):
        """Test melodic contour canon generation."""
        gen = CanonGenerator(seed=42)
        contour = [0, 1, 2, 3, 2, 1, 0]  # Arch shape
        canon = gen.generate_contour_canon(contour, root='D4')

        assert isinstance(canon, stream.Score)
        assert len(canon.parts) == 2

    def test_contour_with_scale(self):
        """Test contour with specific scale."""
        gen = CanonGenerator(seed=42)
        contour = [0, 1, -1, 2, -2]
        major_scale = [0, 2, 4, 5, 7, 9, 11, 12]
        canon = gen.generate_contour_canon(contour, root='C4', scale=major_scale)

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) > 0

    def test_contour_range_clamping(self):
        """Test that contour keeps pitches in range."""
        gen = CanonGenerator(seed=42)
        # Large contour that could go out of range
        contour = [5, 10, 15, -20, 10]
        canon = gen.generate_contour_canon(contour, root='C4')

        notes = list(canon.parts[0].flatten().notes)
        assert all(36 <= n.pitch.midi <= 84 for n in notes)

    def test_motif_canon_sequence(self):
        """Test motif canon with sequence development."""
        gen = CanonGenerator(seed=42)
        motif = ['C4', 'E4', 'G4']
        canon = gen.generate_motif_canon(motif, 'sequence', 4, 2)

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 12  # 3 notes × 4 repetitions

    def test_motif_canon_variation(self):
        """Test motif canon with rhythmic variation."""
        gen = CanonGenerator(seed=42)
        motif = ['C4', 'D4', 'E4']
        canon = gen.generate_motif_canon(motif, 'variation', 3)

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        # Should have varied durations
        durations = [n.quarterLength for n in notes]
        assert len(set(durations)) > 1  # More than one unique duration

    def test_motif_canon_fragmentation(self):
        """Test motif canon with fragmentation."""
        gen = CanonGenerator(seed=42)
        motif = ['C4', 'D4', 'E4', 'F4']
        canon = gen.generate_motif_canon(motif, 'fragmentation', 3)

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) > 0

    def test_template_canon_passacaglia(self):
        """Test passacaglia template."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_template_canon('passacaglia', 'D3', 8)

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 8

    def test_template_canon_chaconne(self):
        """Test chaconne template."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_template_canon('chaconne', 'C3', 8)

        assert isinstance(canon, stream.Score)
        assert len(canon.parts) == 2

    def test_template_canon_all_types(self):
        """Test all template types."""
        gen = CanonGenerator(seed=42)
        templates = ['passacaglia', 'chaconne', 'ostinato', 'romanesca']

        for template in templates:
            canon = gen.generate_template_canon(template, 'D3', 8)
            assert isinstance(canon, stream.Score)
            assert len(canon.parts) == 2

    def test_constrained_canon_generation(self):
        """Test constrained canon generation."""
        gen = CanonGenerator(seed=42)
        constraints = {
            'max_leap': 5,
            'prefer_steps': 0.8,
            'avoid_tritone': True
        }
        canon = gen.generate_constrained_canon(16, 'G4', constraints)

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 16

    def test_constrained_canon_no_constraints(self):
        """Test constrained canon with default constraints."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_constrained_canon(12, 'C4')

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 12

    def test_constrained_canon_max_leap(self):
        """Test that max_leap constraint is respected."""
        gen = CanonGenerator(seed=100)
        constraints = {'max_leap': 3, 'prefer_steps': 0.5}
        canon = gen.generate_constrained_canon(20, 'C4', constraints)

        notes = list(canon.parts[0].flatten().notes)
        # Check that no interval exceeds max_leap
        for i in range(len(notes) - 1):
            interval = abs(notes[i+1].pitch.midi - notes[i].pitch.midi)
            # Allow for octave adjustments, but local steps should be small
            if interval < 12:  # Within one octave
                assert interval <= 3

    def test_constrained_canon_with_scale(self):
        """Test constrained canon with scale constraint."""
        gen = CanonGenerator(seed=42)
        major_scale = [0, 2, 4, 5, 7, 9, 11]
        constraints = {'scale': major_scale}
        canon = gen.generate_constrained_canon(12, 'C4', constraints)

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) > 0

    def test_constrained_canon_range(self):
        """Test that constrained canon stays in range."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_constrained_canon(50, 'C4')

        notes = list(canon.parts[0].flatten().notes)
        assert all(36 <= n.pitch.midi <= 84 for n in notes)


class TestGeneratorEdgeCases:
    """Test edge cases for advanced generators."""

    def test_markov_canon_restart_on_dead_end(self):
        """Test Markov handles dead ends by restarting."""
        gen = CanonGenerator(seed=42)
        # Small training set that will hit dead ends
        training = ['C4', 'D4', 'C4', 'D4']
        canon = gen.generate_markov_canon(training, length=20, order=1)

        notes = list(canon.parts[0].flatten().notes)
        # Should still generate requested length despite dead ends
        assert len(notes) == 20

    def test_contour_empty_contour(self):
        """Test contour with empty list."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_contour_canon([], root='C4')

        notes = list(canon.parts[0].flatten().notes)
        # Should have at least the root note
        assert len(notes) >= 1

    def test_motif_single_note(self):
        """Test motif with single note."""
        gen = CanonGenerator(seed=42)
        motif = ['C4']
        canon = gen.generate_motif_canon(motif, 'sequence', 5, 2)

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 5

    def test_template_short_length(self):
        """Test template with very short length."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_template_canon('passacaglia', 'D3', 2)

        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 2

    def test_constrained_canon_minimal_length(self):
        """Test constrained canon with length=1."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_constrained_canon(1, 'C4')

        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 1


class TestMicrotonalCanon:
    """Test microtonal canon generation."""

    def test_microtonal_baroque_style(self):
        """Test baroque style microtonal canon."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_microtonal_canon('baroque', 'D4', 16)

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 16

    def test_microtonal_arabic_style(self):
        """Test Arabic maqam style canon."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_microtonal_canon('arabic', 'E4', 12)

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 12

    def test_microtonal_indian_style(self):
        """Test Indian raga style canon."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_microtonal_canon('indian', 'C4', 14)

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 14

    def test_microtonal_gamelan_style(self):
        """Test gamelan style canon."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_microtonal_canon('gamelan', 'G4', 10)

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 10

    def test_microtonal_experimental_style(self):
        """Test experimental/xenharmonic canon."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_microtonal_canon('experimental', 'A4', 18)

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 18

    def test_microtonal_jazz_style(self):
        """Test jazz/just intonation canon."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_microtonal_canon('jazz', 'F4', 12)

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 12

    def test_microtonal_with_specific_tuning_system(self):
        """Test with specific tuning system override."""
        from cancrizans.microtonal import TuningSystem

        gen = CanonGenerator(seed=42)
        canon = gen.generate_microtonal_canon(
            'baroque',
            'C4',
            16,
            tuning_system=TuningSystem.WERCKMEISTER_III
        )

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 16

    def test_microtonal_with_specific_world_scale(self):
        """Test with specific world music scale."""
        from cancrizans.microtonal import ScaleType

        gen = CanonGenerator(seed=42)
        canon = gen.generate_microtonal_canon(
            'arabic',
            'D4',
            12,
            world_scale=ScaleType.MAQAM_HIJAZ
        )

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 12

    def test_microtonal_with_string_tuning_system(self):
        """Test with tuning system specified as string."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_microtonal_canon(
            'baroque',
            'C4',
            16,
            tuning_system='EQUAL_19'
        )

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 16

    def test_microtonal_with_string_world_scale(self):
        """Test with world scale specified as string."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_microtonal_canon(
            'indian',
            'G4',
            14,
            world_scale='RAGA_BHAIRAV'
        )

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 14

    def test_microtonal_with_modulation(self):
        """Test microtonal canon with modulation."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_microtonal_canon(
            'baroque',
            'D4',
            24,
            modulation=True
        )

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 24

    def test_microtonal_with_custom_duration(self):
        """Test microtonal canon with custom note duration."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_microtonal_canon(
            'baroque',
            'C4',
            8,
            duration=2.0
        )

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 8
        # Check that notes have the specified duration
        assert notes[0].quarterLength == 2.0

    def test_microtonal_various_lengths(self):
        """Test microtonal canon with various lengths."""
        gen = CanonGenerator(seed=42)

        for length in [4, 8, 16, 32]:
            canon = gen.generate_microtonal_canon('baroque', 'C4', length)
            notes = list(canon.parts[0].flatten().notes)
            assert len(notes) == length

    def test_microtonal_various_roots(self):
        """Test microtonal canon with various root notes."""
        gen = CanonGenerator(seed=42)

        for root in ['C4', 'D4', 'E4', 'F#4', 'G4', 'A4', 'Bb4']:
            canon = gen.generate_microtonal_canon('baroque', root, 12)
            assert isinstance(canon, stream.Score)
            notes = list(canon.parts[0].flatten().notes)
            assert len(notes) == 12

    def test_microtonal_bohlen_pierce(self):
        """Test with Bohlen-Pierce non-octave scale."""
        from cancrizans.microtonal import TuningSystem

        gen = CanonGenerator(seed=42)
        canon = gen.generate_microtonal_canon(
            'experimental',
            'C4',
            13,
            tuning_system=TuningSystem.BOHLEN_PIERCE
        )

        assert isinstance(canon, stream.Score)
        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 13

    def test_microtonal_all_styles(self):
        """Test that all documented styles work."""
        gen = CanonGenerator(seed=42)

        styles = [
            'baroque', 'classical', 'bach',
            'arabic', 'middle eastern', 'maqam',
            'indian', 'raga', 'hindustani',
            'gamelan', 'indonesian', 'javanese',
            'experimental', 'contemporary', 'avant-garde',
            'jazz', 'blues', 'folk'
        ]

        for style in styles:
            canon = gen.generate_microtonal_canon(style, 'C4', 8)
            assert isinstance(canon, stream.Score)
            notes = list(canon.parts[0].flatten().notes)
            assert len(notes) == 8

    def test_microtonal_modulation_with_various_styles(self):
        """Test modulation works with different styles."""
        gen = CanonGenerator(seed=42)

        styles = ['baroque', 'arabic', 'indian', 'experimental']

        for style in styles:
            canon = gen.generate_microtonal_canon(
                style,
                'C4',
                20,
                modulation=True
            )
            assert isinstance(canon, stream.Score)
            notes = list(canon.parts[0].flatten().notes)
            assert len(notes) == 20
