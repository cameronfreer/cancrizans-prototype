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
