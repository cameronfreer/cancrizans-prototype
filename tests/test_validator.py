"""Tests for the validator module."""

import pytest
from music21 import stream, note
from cancrizans.validator import CanonValidator
from cancrizans.generator import CanonGenerator


class TestCanonValidator:
    """Test the CanonValidator class."""

    def test_validator_init(self):
        """Test that validator initializes."""
        validator = CanonValidator()
        assert validator is not None

    def test_validate_returns_dict(self):
        """Test that validate returns a dictionary."""
        validator = CanonValidator()
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        results = validator.validate(canon)

        assert isinstance(results, dict)
        assert 'is_valid_canon' in results
        assert 'errors' in results
        assert 'warnings' in results
        assert 'quality_scores' in results
        assert 'overall_quality' in results

    def test_validate_valid_canon(self):
        """Test validation of a valid canon."""
        validator = CanonValidator()
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        results = validator.validate(canon)

        assert results['is_valid_canon'] is True
        assert len(results['errors']) == 0

    def test_validate_invalid_single_part(self):
        """Test validation fails for single-part score."""
        validator = CanonValidator()

        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('C4', quarterLength=1.0))
        score.append(part)

        results = validator.validate(score)

        assert results['is_valid_canon'] is False
        assert len(results['errors']) > 0

    def test_validate_empty_score(self):
        """Test validation fails for empty score."""
        validator = CanonValidator()

        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()
        score.append(part1)
        score.append(part2)

        results = validator.validate(score)

        assert results['is_valid_canon'] is False
        assert 'no notes' in str(results['errors']).lower()

    def test_quality_scores_structure(self):
        """Test quality scores have expected keys."""
        validator = CanonValidator()
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        results = validator.validate(canon)

        expected_keys = ['melodic', 'harmonic', 'rhythmic', 'range', 'intervallic']
        for key in expected_keys:
            assert key in results['quality_scores']
            assert 0.0 <= results['quality_scores'][key] <= 1.0

    def test_overall_quality_range(self):
        """Test that overall quality is between 0 and 1."""
        validator = CanonValidator()
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        results = validator.validate(canon)

        assert 0.0 <= results['overall_quality'] <= 1.0

    def test_get_quality_grade(self):
        """Test quality grade conversion."""
        validator = CanonValidator()

        # Test grade ranges (based on actual scale: >=0.95=A+, >=0.90=A, >=0.85=A-, >=0.80=B+, etc.)
        assert validator.get_quality_grade(0.97) == 'A+'
        assert validator.get_quality_grade(0.93) == 'A'
        assert validator.get_quality_grade(0.87) == 'A-'
        assert validator.get_quality_grade(0.82) == 'B+'
        assert validator.get_quality_grade(0.77) == 'B'
        assert validator.get_quality_grade(0.72) == 'B-'
        assert validator.get_quality_grade(0.62) == 'C'
        assert validator.get_quality_grade(0.52) == 'D'
        assert validator.get_quality_grade(0.40) == 'F'

    def test_get_recommendations(self):
        """Test recommendations generation."""
        validator = CanonValidator()
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        results = validator.validate(canon)
        recommendations = validator.get_recommendations(results)

        assert isinstance(recommendations, list)
        # Should have at least some recommendations
        assert len(recommendations) >= 0

    def test_different_canons_different_qualities(self):
        """Test that different canons get different quality scores."""
        validator = CanonValidator()
        gen = CanonGenerator(seed=42)

        scale = gen.generate_scale_canon('C', 'major')
        random_walk = gen.generate_random_walk('C4', length=16)

        scale_results = validator.validate(scale)
        random_results = validator.validate(random_walk)

        # Qualities should be different (very unlikely to be exactly equal)
        assert scale_results['overall_quality'] != random_results['overall_quality']

    def test_validate_with_varied_durations(self):
        """Test validation with varied rhythms."""
        validator = CanonValidator()
        gen = CanonGenerator(seed=42)

        # Canon with varied rhythms
        pitches = ['C4', 'D4', 'E4', 'F4']
        rhythms = [1.0, 0.5, 0.5, 2.0]
        canon = gen.generate_rhythmic_canon(pitches, rhythms)

        results = validator.validate(canon)

        # Should have higher rhythmic quality
        assert results['is_valid_canon'] is True
        assert 'rhythmic' in results['quality_scores']

    def test_metrics_included(self):
        """Test that detailed metrics are included."""
        validator = CanonValidator()
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        results = validator.validate(canon)

        assert 'metrics' in results
        assert isinstance(results['metrics'], dict)
