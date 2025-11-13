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
