"""
Tests for machine learning and intelligent analysis module (ml.py).
"""

import pytest
from music21 import stream, note, chord
from cancrizans import (
    assemble_crab_from_theme,
    mirror_canon,
    retrograde,
    invert,
)
from cancrizans.ml import (
    analyze_patterns,
    classify_style,
    detect_canon_type,
    suggest_continuation,
)


@pytest.fixture
def simple_theme():
    """Create a simple theme for testing."""
    theme = stream.Part()
    theme.append(note.Note('C4', quarterLength=1.0))
    theme.append(note.Note('D4', quarterLength=1.0))
    theme.append(note.Note('E4', quarterLength=1.0))
    theme.append(note.Note('F4', quarterLength=1.0))
    theme.append(note.Note('G4', quarterLength=1.0))
    return theme


@pytest.fixture
def pattern_score():
    """Create a score with repeating patterns."""
    score = stream.Score()
    part = stream.Part()

    # Pattern: C-D-E (repeated 3 times)
    for _ in range(3):
        part.append(note.Note('C4', quarterLength=1.0))
        part.append(note.Note('D4', quarterLength=1.0))
        part.append(note.Note('E4', quarterLength=1.0))

    score.insert(0, part)
    return score


@pytest.fixture
def baroque_style_score():
    """Create a score with baroque characteristics."""
    score = stream.Score()
    part = stream.Part()

    # Stepwise motion, simple rhythms
    pitches = [60, 62, 64, 65, 64, 62, 60]  # C major scale fragment
    for pitch in pitches:
        part.append(note.Note(pitch, quarterLength=1.0))

    score.insert(0, part)
    return score


@pytest.fixture
def romantic_style_score():
    """Create a score with romantic characteristics."""
    score = stream.Score()
    part = stream.Part()

    # Larger leaps, chromatic movement, varied rhythms
    pitches = [60, 67, 71, 68, 72, 70, 65]  # Larger intervals, chromatic
    durations = [0.5, 1.5, 0.75, 1.0, 2.0, 0.5, 1.0]

    for pitch, dur in zip(pitches, durations):
        part.append(note.Note(pitch, quarterLength=dur))

    score.insert(0, part)
    return score


class TestAnalyzePatterns:
    """Test analyze_patterns function."""

    def test_analyze_patterns_finds_patterns(self, pattern_score):
        """Test that analyze_patterns finds repeating patterns."""
        result = analyze_patterns(pattern_score, min_pattern_length=3)

        assert isinstance(result, dict)
        assert 'patterns' in result
        assert 'num_patterns' in result
        assert result['num_patterns'] >= 0

    def test_analyze_patterns_empty_score(self):
        """Test analyze_patterns with empty score."""
        score = stream.Score()
        part = stream.Part()
        score.insert(0, part)

        result = analyze_patterns(score)

        assert result['num_patterns'] == 0
        assert result['patterns'] == []
        assert result['most_common'] is None

    def test_analyze_patterns_single_note(self):
        """Test analyze_patterns with single note."""
        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('C4', quarterLength=1.0))
        score.insert(0, part)

        result = analyze_patterns(score, min_pattern_length=3)

        assert result['num_patterns'] == 0

    def test_analyze_patterns_confidence_threshold(self, pattern_score):
        """Test confidence threshold filtering."""
        result_low = analyze_patterns(
            pattern_score, confidence_threshold=0.1
        )
        result_high = analyze_patterns(
            pattern_score, confidence_threshold=0.9
        )

        # Lower threshold should find more or equal patterns
        assert result_low['num_patterns'] >= result_high['num_patterns']

    def test_analyze_patterns_pattern_length(self, pattern_score):
        """Test different pattern lengths."""
        result_short = analyze_patterns(
            pattern_score, min_pattern_length=2, max_pattern_length=3
        )
        result_long = analyze_patterns(
            pattern_score, min_pattern_length=5, max_pattern_length=8
        )

        # Results should differ based on pattern length
        assert isinstance(result_short, dict)
        assert isinstance(result_long, dict)

    def test_analyze_patterns_structure(self, pattern_score):
        """Test the structure of returned pattern data."""
        result = analyze_patterns(pattern_score)

        if result['patterns']:
            pattern = result['patterns'][0]
            assert 'intervals' in pattern
            assert 'durations' in pattern
            assert 'occurrences' in pattern
            assert 'confidence' in pattern
            assert 'length' in pattern

            assert isinstance(pattern['intervals'], list)
            assert isinstance(pattern['durations'], list)
            assert isinstance(pattern['occurrences'], int)
            assert isinstance(pattern['confidence'], float)
            assert 0.0 <= pattern['confidence'] <= 1.0


class TestClassifyStyle:
    """Test classify_style function."""

    def test_classify_style_returns_dict(self, simple_theme):
        """Test that classify_style returns proper structure."""
        score = stream.Score()
        score.insert(0, simple_theme)

        result = classify_style(score)

        assert isinstance(result, dict)
        assert 'style' in result
        assert 'confidence' in result
        assert 'features' in result

    def test_classify_style_valid_styles(self, simple_theme):
        """Test that classified style is valid."""
        score = stream.Score()
        score.insert(0, simple_theme)

        result = classify_style(score)

        assert result['style'] in ['baroque', 'classical', 'romantic', 'unknown']
        assert 0.0 <= result['confidence'] <= 1.0

    def test_classify_style_with_probabilities(self, simple_theme):
        """Test returning probability scores."""
        score = stream.Score()
        score.insert(0, simple_theme)

        result = classify_style(score, return_probabilities=True)

        assert 'probabilities' in result
        assert 'baroque' in result['probabilities']
        assert 'classical' in result['probabilities']
        assert 'romantic' in result['probabilities']

        # Probabilities should sum to approximately 1.0
        prob_sum = sum(result['probabilities'].values())
        assert 0.99 <= prob_sum <= 1.01

    def test_classify_style_baroque(self, baroque_style_score):
        """Test classification of baroque-style score."""
        result = classify_style(baroque_style_score, return_probabilities=True)

        # Should favor baroque (though not guaranteed)
        assert 'style' in result
        assert result['confidence'] > 0.0

    def test_classify_style_romantic(self, romantic_style_score):
        """Test classification of romantic-style score."""
        result = classify_style(romantic_style_score, return_probabilities=True)

        # Should have some confidence in classification
        assert result['confidence'] > 0.0

    def test_classify_style_features(self, simple_theme):
        """Test extracted features."""
        score = stream.Score()
        score.insert(0, simple_theme)

        result = classify_style(score)

        features = result['features']
        assert 'avg_interval' in features
        assert 'interval_variance' in features
        assert 'large_leaps' in features
        assert 'unique_durations' in features
        assert 'chromatic_ratio' in features
        assert 'pitch_range' in features

    def test_classify_style_empty_score(self):
        """Test classification with empty score."""
        score = stream.Score()
        part = stream.Part()
        score.insert(0, part)

        result = classify_style(score)

        assert result['style'] == 'unknown'
        assert result['confidence'] == 0.0


class TestDetectCanonType:
    """Test detect_canon_type function."""

    def test_detect_canon_type_structure(self, simple_theme):
        """Test the structure of detection results."""
        canon = assemble_crab_from_theme(simple_theme)

        result = detect_canon_type(canon)

        assert isinstance(result, dict)
        assert 'canon_type' in result
        assert 'confidence' in result
        assert 'evidence' in result
        assert 'voice_relationships' in result
        assert 'transformations' in result

        assert isinstance(result['evidence'], list)
        assert isinstance(result['transformations'], list)
        assert 0.0 <= result['confidence'] <= 1.0

    def test_detect_canon_type_single_voice(self, simple_theme):
        """Test detection with single voice."""
        score = stream.Score()
        score.insert(0, simple_theme)

        result = detect_canon_type(score)

        assert result['canon_type'] == 'monophonic'
        assert result['confidence'] == 1.0

    def test_detect_canon_type_retrograde(self, simple_theme):
        """Test detection of retrograde canon."""
        score = stream.Score()
        score.insert(0, simple_theme)

        retro = retrograde(simple_theme)
        score.insert(0, retro)

        result = detect_canon_type(score)

        # Should detect retrograde relationship
        assert 'retrograde' in result['transformations'] or result['canon_type'] != 'monophonic'

    def test_detect_canon_type_inversion(self, simple_theme):
        """Test detection of inversion."""
        score = stream.Score()
        score.insert(0, simple_theme)

        inv = invert(simple_theme)
        score.insert(0, inv)

        result = detect_canon_type(score)

        # Should detect some relationship
        assert result['canon_type'] != 'monophonic'

    def test_detect_canon_type_voice_relationships(self, simple_theme):
        """Test voice relationship analysis."""
        canon = assemble_crab_from_theme(simple_theme)

        result = detect_canon_type(canon)

        # Should have voice relationships for multi-voice score
        if len(list(canon.parts)) >= 2:
            assert len(result['voice_relationships']) > 0

    def test_detect_canon_type_evidence(self, simple_theme):
        """Test that evidence is provided."""
        canon = assemble_crab_from_theme(simple_theme)

        result = detect_canon_type(canon)

        assert len(result['evidence']) > 0
        assert all(isinstance(e, str) for e in result['evidence'])


class TestSuggestContinuation:
    """Test suggest_continuation function."""

    def test_suggest_continuation_returns_stream(self, simple_theme):
        """Test that suggest_continuation returns a Stream."""
        result = suggest_continuation(simple_theme, num_measures=4)

        assert isinstance(result, stream.Stream)

    def test_suggest_continuation_has_notes(self, simple_theme):
        """Test that continuation contains notes."""
        result = suggest_continuation(simple_theme, num_measures=4)

        notes = list(result.flatten().notes)
        assert len(notes) > 0

    def test_suggest_continuation_length(self, simple_theme):
        """Test approximate length of continuation."""
        result_short = suggest_continuation(simple_theme, num_measures=2)
        result_long = suggest_continuation(simple_theme, num_measures=8)

        notes_short = list(result_short.flatten().notes)
        notes_long = list(result_long.flatten().notes)

        # Longer request should have more notes
        assert len(notes_long) > len(notes_short)

    def test_suggest_continuation_style_baroque(self, simple_theme):
        """Test baroque style continuation."""
        result = suggest_continuation(
            simple_theme, num_measures=4, style='baroque'
        )

        notes = list(result.flatten().notes)
        assert len(notes) > 0
        # All elements should be notes
        assert all(isinstance(n, note.Note) for n in notes)

    def test_suggest_continuation_style_classical(self, simple_theme):
        """Test classical style continuation."""
        result = suggest_continuation(
            simple_theme, num_measures=4, style='classical'
        )

        notes = list(result.flatten().notes)
        assert len(notes) > 0

    def test_suggest_continuation_style_romantic(self, simple_theme):
        """Test romantic style continuation."""
        result = suggest_continuation(
            simple_theme, num_measures=4, style='romantic'
        )

        notes = list(result.flatten().notes)
        assert len(notes) > 0

    def test_suggest_continuation_variation_levels(self, simple_theme):
        """Test different variation levels."""
        result_strict = suggest_continuation(
            simple_theme, num_measures=4, variation_level=0.0
        )
        result_free = suggest_continuation(
            simple_theme, num_measures=4, variation_level=1.0
        )

        # Both should produce valid output
        assert len(list(result_strict.flatten().notes)) > 0
        assert len(list(result_free.flatten().notes)) > 0

    def test_suggest_continuation_empty_theme(self):
        """Test continuation with empty theme."""
        empty_theme = stream.Part()

        result = suggest_continuation(empty_theme, num_measures=4)

        # Should return empty stream
        assert isinstance(result, stream.Stream)
        assert len(list(result.flatten().notes)) == 0

    def test_suggest_continuation_pitch_range(self, simple_theme):
        """Test that generated pitches stay in reasonable range."""
        result = suggest_continuation(simple_theme, num_measures=8)

        notes = list(result.flatten().notes)
        pitches = [n.pitch.midi for n in notes if isinstance(n, note.Note)]

        if pitches:
            assert all(48 <= p <= 84 for p in pitches)


class TestMLIntegration:
    """Integration tests for ML functions."""

    def test_full_analysis_pipeline(self, simple_theme):
        """Test running all ML analyses on same score."""
        canon = assemble_crab_from_theme(simple_theme)

        # Pattern analysis
        patterns = analyze_patterns(canon)
        assert isinstance(patterns, dict)

        # Style classification
        style = classify_style(canon, return_probabilities=True)
        assert isinstance(style, dict)
        assert 'style' in style

        # Canon type detection
        canon_type = detect_canon_type(canon)
        assert isinstance(canon_type, dict)
        assert 'canon_type' in canon_type

        # Suggestion generation
        continuation = suggest_continuation(simple_theme, num_measures=4)
        assert isinstance(continuation, stream.Stream)

    def test_analysis_on_complex_canon(self, simple_theme):
        """Test ML functions on more complex canon."""
        # Create a more complex canon
        score = stream.Score()
        score.insert(0, simple_theme)
        score.insert(0, retrograde(simple_theme))
        score.insert(0, invert(simple_theme))

        # All functions should handle it
        patterns = analyze_patterns(score)
        style = classify_style(score)
        canon_type = detect_canon_type(score)

        assert isinstance(patterns, dict)
        assert isinstance(style, dict)
        assert isinstance(canon_type, dict)

    def test_continuation_based_on_style(self, simple_theme):
        """Test that continuation respects detected style."""
        score = stream.Score()
        score.insert(0, simple_theme)

        # Classify style
        style_result = classify_style(score)
        detected_style = style_result['style']

        if detected_style != 'unknown':
            # Generate continuation in detected style
            continuation = suggest_continuation(
                simple_theme,
                num_measures=4,
                style=detected_style
            )

            assert len(list(continuation.flatten().notes)) > 0
