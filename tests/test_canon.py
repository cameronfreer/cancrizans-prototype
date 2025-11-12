"""Tests for the canon module."""

import pytest
from music21 import note, stream, pitch
from cancrizans.canon import (
    retrograde,
    invert,
    augmentation,
    diminution,
    mirror_canon,
    time_align,
    is_time_palindrome,
    pairwise_symmetry_map,
    interval_analysis,
    harmonic_analysis,
    rhythm_analysis,
)


class TestRetrograde:
    """Test retrograde transformation."""

    def test_retrograde_reverses_notes(self):
        """Test that retrograde reverses note order."""
        melody = stream.Part()
        melody.append(note.Note('C4', quarterLength=1.0))
        melody.append(note.Note('D4', quarterLength=1.0))
        melody.append(note.Note('E4', quarterLength=1.0))

        retro = retrograde(melody)

        original_pitches = [n.pitch.nameWithOctave for n in melody.notes]
        retro_pitches = [n.pitch.nameWithOctave for n in retro.notes]

        assert retro_pitches == original_pitches[::-1]

    def test_retrograde_preserves_durations(self):
        """Test that note durations are preserved."""
        melody = stream.Part()
        melody.append(note.Note('C4', quarterLength=1.0))
        melody.append(note.Note('D4', quarterLength=0.5))
        melody.append(note.Note('E4', quarterLength=2.0))

        retro = retrograde(melody)

        original_durs = [n.quarterLength for n in melody.notes]
        retro_durs = [n.quarterLength for n in retro.notes]

        assert retro_durs == original_durs[::-1]


class TestInversion:
    """Test inversion transformation."""

    def test_invert_around_axis(self):
        """Test pitch inversion around an axis."""
        melody = stream.Part()
        melody.append(note.Note(midi=60, quarterLength=1.0))  # C4
        melody.append(note.Note(midi=62, quarterLength=1.0))  # D4
        melody.append(note.Note(midi=64, quarterLength=1.0))  # E4

        inverted = invert(melody, axis_pitch='D4')  # MIDI 62

        original_midi = [n.pitch.midi for n in melody.notes]
        inverted_midi = [n.pitch.midi for n in inverted.notes]

        # 2 * 62 - original = inverted
        expected = [2 * 62 - m for m in original_midi]
        assert inverted_midi == expected

    def test_invert_preserves_rhythm(self):
        """Test that inversion preserves rhythm."""
        melody = stream.Part()
        melody.append(note.Note('C4', quarterLength=1.0))
        melody.append(note.Note('D4', quarterLength=0.5))

        inverted = invert(melody, axis_pitch='C4')

        original_durs = [n.quarterLength for n in melody.notes]
        inverted_durs = [n.quarterLength for n in inverted.notes]

        assert original_durs == inverted_durs


class TestAugmentationDiminution:
    """Test tempo transformations."""

    def test_augmentation_doubles_duration(self):
        """Test 2x augmentation doubles all durations."""
        melody = stream.Part()
        melody.append(note.Note('C4', quarterLength=1.0))
        melody.append(note.Note('D4', quarterLength=0.5))

        aug = augmentation(melody, factor=2)

        assert aug.notes[0].quarterLength == 2.0
        assert aug.notes[1].quarterLength == 1.0

    def test_diminution_halves_duration(self):
        """Test 2x diminution halves all durations."""
        melody = stream.Part()
        melody.append(note.Note('C4', quarterLength=2.0))
        melody.append(note.Note('D4', quarterLength=1.0))

        dim = diminution(melody, factor=2)

        assert dim.notes[0].quarterLength == 1.0
        assert dim.notes[1].quarterLength == 0.5

    def test_augmentation_preserves_pitches(self):
        """Test that augmentation doesn't change pitches."""
        melody = stream.Part()
        melody.append(note.Note('C4', quarterLength=1.0))
        melody.append(note.Note('E4', quarterLength=1.0))

        aug = augmentation(melody, factor=3)

        original_pitches = [n.pitch.nameWithOctave for n in melody.notes]
        aug_pitches = [n.pitch.nameWithOctave for n in aug.notes]

        assert original_pitches == aug_pitches


class TestMirrorCanon:
    """Test mirror canon creation."""

    def test_mirror_canon_creates_stream(self):
        """Test that mirror_canon returns a stream."""
        melody = stream.Part()
        melody.append(note.Note('C4', quarterLength=1.0))
        melody.append(note.Note('D4', quarterLength=1.0))

        canon = mirror_canon(melody)

        assert isinstance(canon, stream.Stream)

    def test_mirror_canon_preserves_theme(self):
        """Test that original theme is preserved."""
        melody = stream.Part()
        melody.append(note.Note('C4', quarterLength=1.0))
        melody.append(note.Note('D4', quarterLength=1.0))

        canon = mirror_canon(melody)
        # mirror_canon returns a Part, get all notes
        notes = list(canon.flatten().notes)

        # Should have notes (at least the theme)
        assert len(notes) > 0


class TestTimeAlign:
    """Test time alignment."""

    def test_time_align_creates_score(self):
        """Test that time_align creates a score with two parts."""
        voice_a = stream.Part()
        voice_a.append(note.Note('C4', quarterLength=1.0))
        voice_a.append(note.Note('D4', quarterLength=1.0))

        voice_b = stream.Part()
        voice_b.append(note.Note('E4', quarterLength=1.0))
        voice_b.append(note.Note('F4', quarterLength=1.0))

        aligned = time_align(voice_a, voice_b, offset_quarters=2.0)

        assert isinstance(aligned, stream.Score)
        assert len(aligned.parts) == 2


class TestPalindrome:
    """Test palindrome detection."""

    def test_is_time_palindrome_simple(self):
        """Test palindrome detection on simple canon."""
        from cancrizans.bach_crab import assemble_crab_from_theme

        theme = stream.Part()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('D4', quarterLength=1.0))

        canon = assemble_crab_from_theme(theme)

        assert is_time_palindrome(canon) is True

    def test_is_time_palindrome_non_palindrome(self):
        """Test that non-palindromes return False."""
        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))
        part1.append(note.Note('D4', quarterLength=1.0))

        part2 = stream.Part()
        part2.append(note.Note('E4', quarterLength=1.0))
        part2.append(note.Note('F4', quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        # Not a palindrome
        assert is_time_palindrome(score) is False


class TestPairwiseSymmetryMap:
    """Test pairwise symmetry mapping."""

    def test_pairwise_symmetry_map_returns_list(self):
        """Test that it returns a list."""
        from cancrizans.bach_crab import assemble_crab_from_theme

        theme = stream.Part()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('D4', quarterLength=1.0))

        canon = assemble_crab_from_theme(theme)
        symmetry_map = pairwise_symmetry_map(canon)

        assert isinstance(symmetry_map, list)

    def test_pairwise_symmetry_map_tuple_pairs(self):
        """Test that it returns tuple pairs."""
        from cancrizans.bach_crab import assemble_crab_from_theme

        theme = stream.Part()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('D4', quarterLength=1.0))

        canon = assemble_crab_from_theme(theme)
        symmetry_map = pairwise_symmetry_map(canon)

        assert len(symmetry_map) > 0
        assert isinstance(symmetry_map[0], tuple)


class TestIntervalAnalysis:
    """Test interval analysis."""

    def test_interval_analysis_returns_dict(self):
        """Test that interval analysis returns a dictionary."""
        melody = stream.Part()
        melody.append(note.Note('C4', quarterLength=1.0))
        melody.append(note.Note('D4', quarterLength=1.0))
        melody.append(note.Note('E4', quarterLength=1.0))

        analysis = interval_analysis(melody)

        assert isinstance(analysis, dict)
        assert 'total_intervals' in analysis
        assert 'average' in analysis

    def test_interval_analysis_calculates_correctly(self):
        """Test interval calculations."""
        melody = stream.Part()
        melody.append(note.Note(midi=60, quarterLength=1.0))  # C4
        melody.append(note.Note(midi=62, quarterLength=1.0))  # D4 (+2)
        melody.append(note.Note(midi=64, quarterLength=1.0))  # E4 (+2)

        analysis = interval_analysis(melody)

        assert analysis['total_intervals'] == 2
        assert analysis['average'] == 2.0


class TestHarmonicAnalysis:
    """Test harmonic analysis."""

    def test_harmonic_analysis_returns_dict(self):
        """Test that harmonic analysis returns a dictionary."""
        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))

        part2 = stream.Part()
        part2.append(note.Note('E4', quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        analysis = harmonic_analysis(score)

        assert isinstance(analysis, dict)


class TestRhythmAnalysis:
    """Test rhythm analysis."""

    def test_rhythm_analysis_returns_dict(self):
        """Test that rhythm analysis returns a dictionary."""
        melody = stream.Part()
        melody.append(note.Note('C4', quarterLength=1.0))
        melody.append(note.Note('D4', quarterLength=0.5))
        melody.append(note.Note('E4', quarterLength=2.0))

        analysis = rhythm_analysis(melody)

        assert isinstance(analysis, dict)
        assert 'total_events' in analysis
        assert 'average_duration' in analysis
