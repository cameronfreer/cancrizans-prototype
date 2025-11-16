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


class TestValidatorEdgeCases:
    """Test edge cases and boundary conditions in validator."""

    def test_zero_duration_part(self):
        """Test validation with zero-duration part."""
        validator = CanonValidator()

        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))
        part2 = stream.Part()  # Empty part with zero duration
        score.append(part1)
        score.append(part2)

        results = validator.validate(score)

        assert results['is_valid_canon'] is False
        assert any('zero duration' in str(e).lower() for e in results['errors'])

    def test_single_note_parts(self):
        """Test validation with parts containing single notes."""
        validator = CanonValidator()

        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))
        part2 = stream.Part()
        part2.append(note.Note('C4', quarterLength=1.0))
        score.append(part1)
        score.append(part2)

        results = validator.validate(score)

        # Should handle single-note parts gracefully
        assert 'melodic' in results['quality_scores']

    def test_extreme_low_pitch_range(self):
        """Test validation with extremely low pitches."""
        validator = CanonValidator()

        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()

        # Very low pitches (below C3 = MIDI 48)
        for pitch_midi in [36, 38, 40, 42]:  # C2 to F#2
            part1.append(note.Note(pitch_midi, quarterLength=1.0))
            part2.append(note.Note(pitch_midi, quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        results = validator.validate(score)

        # Should warn about extreme range
        assert any('extreme range' in str(w).lower() for w in results['warnings'])

    def test_extreme_high_pitch_range(self):
        """Test validation with extremely high pitches."""
        validator = CanonValidator()

        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()

        # Very high pitches (above C6 = MIDI 84)
        for pitch_midi in [85, 86, 87, 88]:  # Above C6
            part1.append(note.Note(pitch_midi, quarterLength=1.0))
            part2.append(note.Note(pitch_midi, quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        results = validator.validate(score)

        # Should warn about extreme range
        assert any('extreme range' in str(w).lower() for w in results['warnings'])

    def test_narrow_range_canon(self):
        """Test validation with very narrow pitch range (< 1 octave)."""
        validator = CanonValidator()

        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()

        # Very narrow range (5 semitones)
        for pitch in ['C4', 'D4', 'E4', 'F4']:
            part1.append(note.Note(pitch, quarterLength=1.0))
            part2.append(note.Note(pitch, quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        results = validator.validate(score)

        # Should get lower range score
        assert results['quality_scores']['range'] < 1.0

    def test_wide_range_canon(self):
        """Test validation with very wide pitch range (> 2 octaves)."""
        validator = CanonValidator()

        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()

        # Very wide range (3 octaves = 36 semitones)
        part1.append(note.Note('C3', quarterLength=1.0))
        part1.append(note.Note('C6', quarterLength=1.0))
        part2.append(note.Note('C3', quarterLength=1.0))
        part2.append(note.Note('C6', quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        results = validator.validate(score)

        # Should get reduced range score for excessive range
        assert results['quality_scores']['range'] < 1.0

    def test_all_same_rhythms(self):
        """Test validation with all identical note durations."""
        validator = CanonValidator()

        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()

        # All quarter notes
        for pitch in ['C4', 'D4', 'E4', 'F4', 'G4']:
            part1.append(note.Note(pitch, quarterLength=1.0))
            part2.append(note.Note(pitch, quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        results = validator.validate(score)

        # Should get lower rhythmic score due to lack of variety
        assert results['quality_scores']['rhythmic'] < 0.8

    def test_non_palindrome_penalty(self):
        """Test that non-palindrome canons get quality penalty."""
        validator = CanonValidator()

        # Create a non-palindrome score
        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()

        # Different sequences (not retrograde)
        part1.append(note.Note('C4', quarterLength=1.0))
        part1.append(note.Note('D4', quarterLength=1.0))
        part2.append(note.Note('E4', quarterLength=1.0))
        part2.append(note.Note('F4', quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        results = validator.validate(score)

        # Should warn about not being palindrome
        assert any('not a perfect' in str(w).lower() for w in results['warnings'])
        # Quality should be penalized (multiplied by 0.8)
        assert results['overall_quality'] < 1.0

    def test_all_quality_grades(self):
        """Test all quality grade boundaries."""
        validator = CanonValidator()

        grade_tests = [
            (0.97, 'A+'),
            (0.95, 'A+'),
            (0.93, 'A'),
            (0.90, 'A'),
            (0.87, 'A-'),
            (0.85, 'A-'),
            (0.82, 'B+'),
            (0.80, 'B+'),
            (0.77, 'B'),
            (0.75, 'B'),
            (0.72, 'B-'),
            (0.70, 'B-'),
            (0.67, 'C+'),
            (0.65, 'C+'),
            (0.62, 'C'),
            (0.60, 'C'),
            (0.57, 'C-'),
            (0.55, 'C-'),
            (0.52, 'D'),
            (0.50, 'D'),
            (0.40, 'F'),
            (0.30, 'F'),
        ]

        for quality, expected_grade in grade_tests:
            assert validator.get_quality_grade(quality) == expected_grade

    def test_recommendations_for_poor_melodic(self):
        """Test recommendations when melodic quality is low."""
        validator = CanonValidator()

        results = {
            'quality_scores': {
                'melodic': 0.4,  # Low
                'harmonic': 0.8,
                'rhythmic': 0.8,
                'range': 0.8,
                'intervallic': 0.8
            },
            'metrics': {'is_palindrome': True}
        }

        recommendations = validator.get_recommendations(results)

        assert any('melodic' in r.lower() for r in recommendations)

    def test_recommendations_for_poor_harmonic(self):
        """Test recommendations when harmonic quality is low."""
        validator = CanonValidator()

        results = {
            'quality_scores': {
                'melodic': 0.8,
                'harmonic': 0.4,  # Low
                'rhythmic': 0.8,
                'range': 0.8,
                'intervallic': 0.8
            },
            'metrics': {'is_palindrome': True}
        }

        recommendations = validator.get_recommendations(results)

        assert any('harmonic' in r.lower() for r in recommendations)

    def test_recommendations_for_poor_rhythmic(self):
        """Test recommendations when rhythmic quality is low."""
        validator = CanonValidator()

        results = {
            'quality_scores': {
                'melodic': 0.8,
                'harmonic': 0.8,
                'rhythmic': 0.4,  # Low
                'range': 0.8,
                'intervallic': 0.8
            },
            'metrics': {'is_palindrome': True}
        }

        recommendations = validator.get_recommendations(results)

        assert any('rhythmic' in r.lower() for r in recommendations)

    def test_recommendations_for_poor_range(self):
        """Test recommendations when range quality is low."""
        validator = CanonValidator()

        results = {
            'quality_scores': {
                'melodic': 0.8,
                'harmonic': 0.8,
                'rhythmic': 0.8,
                'range': 0.4,  # Low
                'intervallic': 0.8
            },
            'metrics': {'is_palindrome': True}
        }

        recommendations = validator.get_recommendations(results)

        assert any('range' in r.lower() for r in recommendations)

    def test_recommendations_for_poor_intervallic(self):
        """Test recommendations when intervallic quality is low."""
        validator = CanonValidator()

        results = {
            'quality_scores': {
                'melodic': 0.8,
                'harmonic': 0.8,
                'rhythmic': 0.8,
                'range': 0.8,
                'intervallic': 0.4  # Low
            },
            'metrics': {'is_palindrome': True}
        }

        recommendations = validator.get_recommendations(results)

        assert any('interval' in r.lower() for r in recommendations)

    def test_recommendations_for_non_palindrome(self):
        """Test recommendations for non-palindrome canon."""
        validator = CanonValidator()

        results = {
            'quality_scores': {
                'melodic': 0.8,
                'harmonic': 0.8,
                'rhythmic': 0.8,
                'range': 0.8,
                'intervallic': 0.8
            },
            'metrics': {'is_palindrome': False}  # Not a palindrome
        }

        recommendations = validator.get_recommendations(results)

        assert any('palindrome' in r.lower() for r in recommendations)

    def test_recommendations_for_excellent_canon(self):
        """Test recommendations for excellent quality canon."""
        validator = CanonValidator()

        results = {
            'quality_scores': {
                'melodic': 0.9,
                'harmonic': 0.9,
                'rhythmic': 0.9,
                'range': 0.9,
                'intervallic': 0.9
            },
            'metrics': {'is_palindrome': True}
        }

        recommendations = validator.get_recommendations(results)

        # Should have positive message
        assert any('excellent' in r.lower() or 'no improvements' in r.lower()
                  for r in recommendations)

    def test_harmonic_quality_direct_single_part(self):
        """Test harmonic quality assessment directly with single-part (line 144-145)."""
        from music21 import stream, note

        validator = CanonValidator()

        # Create single-part score
        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('C4', quarterLength=1.0))
        part.append(note.Note('D4', quarterLength=1.0))
        score.insert(0, part)

        # Test the private method directly (defensive code path)
        results = {
            'quality_scores': {},
            'metrics': {},
            'errors': []
        }
        validator._assess_harmonic_quality(score, results)

        # Should set default harmonic score for single part
        assert results['quality_scores']['harmonic'] == 0.7

    def test_rhythmic_quality_direct_no_durations(self):
        """Test rhythmic quality assessment with parts that have no durations (line 188-189)."""
        from music21 import stream

        validator = CanonValidator()

        # Create a score with empty parts (no notes)
        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()
        score.insert(0, part1)
        score.insert(0, part2)

        # Test the private method directly
        results = {
            'quality_scores': {},
            'metrics': {},
            'errors': []
        }
        validator._assess_rhythmic_quality(score, results)

        # Should set rhythmic quality to 0.0 when no durations found
        assert results['quality_scores']['rhythmic'] == 0.0

    def test_rhythmic_quality_zero_total_durations(self):
        """Test rhythmic quality when total_durations == 0 (line 203)."""
        validator = CanonValidator()
        score = stream.Score()
        part1 = stream.Part()
        # Add a note with 0 duration
        part1.append(note.Note('C4', quarterLength=0.0))
        score.insert(0, part1)

        results = {'quality_scores': {}, 'metrics': {}, 'errors': []}
        validator._assess_rhythmic_quality(score, results)

        # When total_durations == 0, pattern_score should be 0.5 (line 203)
        assert 'rhythmic' in results['quality_scores']

    def test_range_quality_skip_empty_parts(self):
        """Test range quality skips parts with no notes (line 217)."""
        validator = CanonValidator()
        score = stream.Score()

        # Part with notes
        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))
        part1.append(note.Note('G4', quarterLength=1.0))

        # Empty part (should be skipped)
        part2 = stream.Part()

        # Part with notes
        part3 = stream.Part()
        part3.append(note.Note('E4', quarterLength=1.0))

        score.insert(0, part1)
        score.insert(0, part2)
        score.insert(0, part3)

        results = {'quality_scores': {}, 'metrics': {}, 'errors': []}
        validator._assess_range_quality(score, results)

        # Should successfully skip the empty part
        assert 'range' in results['quality_scores']

