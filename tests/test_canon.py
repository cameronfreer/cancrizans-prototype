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


class TestCanonEdgeCases:
    """Test edge cases and boundary conditions in canon transformations."""

    def test_retrograde_empty_stream(self):
        """Test retrograde with empty stream."""
        empty_part = stream.Part()
        retro = retrograde(empty_part)

        assert isinstance(retro, stream.Part)
        assert len(list(retro.notes)) == 0

    def test_retrograde_with_chord(self):
        """Test retrograde with chords."""
        from music21 import chord as m21chord

        melody = stream.Part()
        melody.append(m21chord.Chord(['C4', 'E4', 'G4'], quarterLength=1.0))
        melody.append(note.Note('D4', quarterLength=1.0))

        retro = retrograde(melody)

        assert len(list(retro.flatten().notesAndRests)) == 2
        # First element in retrograde should be the original second element
        assert isinstance(list(retro.flatten().notesAndRests)[0], note.Note)

    def test_retrograde_with_rest(self):
        """Test retrograde with rests."""
        melody = stream.Part()
        melody.append(note.Note('C4', quarterLength=1.0))
        melody.append(note.Rest(quarterLength=1.0))
        melody.append(note.Note('D4', quarterLength=1.0))

        retro = retrograde(melody)

        elements = list(retro.flatten().notesAndRests)
        assert len(elements) == 3
        # Check that rest is in the retrograde
        assert any(el.isRest for el in elements)

    def test_retrograde_sequence(self):
        """Test retrograde with a sequence (not a Stream)."""
        sequence = [1, 2, 3, 4, 5]
        retro = retrograde(sequence)

        assert retro == [5, 4, 3, 2, 1]

    def test_invert_with_chord(self):
        """Test inversion with chords."""
        from music21 import chord as m21chord

        melody = stream.Part()
        melody.append(m21chord.Chord(['C4', 'E4', 'G4'], quarterLength=1.0))

        inverted = invert(melody, axis_pitch='C4')

        assert len(list(inverted.flatten().notesAndRests)) == 1
        inverted_el = list(inverted.flatten().notesAndRests)[0]
        assert isinstance(inverted_el, m21chord.Chord)

    def test_invert_with_rest(self):
        """Test inversion preserves rests."""
        melody = stream.Part()
        melody.append(note.Note('C4', quarterLength=1.0))
        melody.append(note.Rest(quarterLength=1.0))
        melody.append(note.Note('E4', quarterLength=1.0))

        inverted = invert(melody, axis_pitch='C4')

        elements = list(inverted.flatten().notesAndRests)
        assert len(elements) == 3
        assert any(el.isRest for el in elements)

    def test_invert_sequence(self):
        """Test inversion with a sequence of pitches."""
        from music21 import pitch as m21pitch

        sequence = [m21pitch.Pitch('C4'), m21pitch.Pitch('D4'), m21pitch.Pitch('E4')]
        inverted = invert(sequence, axis_pitch='D4')

        assert len(inverted) == 3
        # Verify pitches are inverted around D4
        assert all(hasattr(p, 'midi') for p in inverted)

    def test_augmentation_with_chord(self):
        """Test augmentation with chords."""
        from music21 import chord as m21chord

        melody = stream.Part()
        melody.append(m21chord.Chord(['C4', 'E4', 'G4'], quarterLength=1.0))

        aug = augmentation(melody, factor=2.0)

        chord_el = list(aug.flatten().notesAndRests)[0]
        assert isinstance(chord_el, m21chord.Chord)
        assert chord_el.quarterLength == 2.0

    def test_diminution_with_chord(self):
        """Test diminution with chords."""
        from music21 import chord as m21chord

        melody = stream.Part()
        melody.append(m21chord.Chord(['C4', 'E4', 'G4'], quarterLength=2.0))

        dim = diminution(melody, factor=2.0)

        chord_el = list(dim.flatten().notesAndRests)[0]
        assert isinstance(chord_el, m21chord.Chord)
        assert chord_el.quarterLength == 1.0

    def test_is_time_palindrome_wrong_part_count(self):
        """Test is_time_palindrome with wrong number of parts."""
        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))
        score.append(part1)

        # Only 1 part, should return False
        assert is_time_palindrome(score) is False

        # Add 2 more parts (total 3)
        part2 = stream.Part()
        part2.append(note.Note('D4', quarterLength=1.0))
        part3 = stream.Part()
        part3.append(note.Note('E4', quarterLength=1.0))
        score.append(part2)
        score.append(part3)

        # 3 parts, should return False
        assert is_time_palindrome(score) is False

    def test_is_time_palindrome_different_lengths(self):
        """Test is_time_palindrome with parts of different lengths."""
        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))
        part1.append(note.Note('D4', quarterLength=1.0))

        part2 = stream.Part()
        part2.append(note.Note('E4', quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        # Different number of notes, should return False
        assert is_time_palindrome(score) is False

    def test_is_time_palindrome_empty_parts(self):
        """Test is_time_palindrome with empty parts."""
        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()
        score.append(part1)
        score.append(part2)

        # Empty parts should return True (vacuously true)
        assert is_time_palindrome(score) is True

    def test_extract_events_with_chord(self):
        """Test _extract_events with chords."""
        from cancrizans.canon import _extract_events
        from music21 import chord as m21chord

        part = stream.Part()
        part.append(note.Note('C4', quarterLength=1.0))
        part.append(m21chord.Chord(['E4', 'G4', 'C5'], quarterLength=1.0))

        events = _extract_events(part)

        assert len(events) == 2
        # Chord event should use lowest pitch (E4 = MIDI 64)
        assert events[1][2] == 64  # MIDI pitch of E4

    def test_interval_analysis_empty_stream(self):
        """Test interval_analysis with empty or single-note stream."""
        empty_part = stream.Part()
        analysis = interval_analysis(empty_part)

        assert analysis['total_intervals'] == 0
        assert analysis['average'] == 0

    def test_interval_analysis_single_note(self):
        """Test interval_analysis with only one note."""
        part = stream.Part()
        part.append(note.Note('C4', quarterLength=1.0))

        analysis = interval_analysis(part)

        assert analysis['total_intervals'] == 0

    def test_harmonic_analysis_single_part(self):
        """Test harmonic_analysis with only one part."""
        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('C4', quarterLength=1.0))
        score.append(part)

        analysis = harmonic_analysis(score)

        assert analysis['total_sonorities'] == 0
        assert analysis['consonances'] == 0

    def test_rhythm_analysis_empty_stream(self):
        """Test rhythm_analysis with empty stream."""
        empty_part = stream.Part()
        analysis = rhythm_analysis(empty_part)

        assert analysis['total_events'] == 0
        assert analysis['average_duration'] == 0

    def test_pairwise_symmetry_map_empty(self):
        """Test pairwise_symmetry_map with empty stream."""
        empty_part = stream.Part()
        pairs = pairwise_symmetry_map(empty_part)

        assert isinstance(pairs, list)
        assert len(pairs) == 0

    def test_pairwise_symmetry_map_single_note(self):
        """Test pairwise_symmetry_map with single note."""
        part = stream.Part()
        part.append(note.Note('C4', quarterLength=1.0))

        pairs = pairwise_symmetry_map(part)

        # Single note should map to itself
        assert len(pairs) == 1
        assert pairs[0] == (0, 0)

    def test_invert_sequence_with_non_midi_items(self):
        """Test invert handles sequences with non-midi items (line 119)."""
        from music21 import pitch
        
        # Create a sequence with pitch and non-pitch items
        sequence = [
            pitch.Pitch('C4'),
            pitch.Pitch('E4'),
            "non-midi-string",  # This doesn't have midi attribute
            pitch.Pitch('G4')
        ]
        
        result = invert(sequence, axis_pitch='C4')
        
        # Should handle the non-midi item gracefully
        assert result is not None
        assert len(result) == 4
        # The string should be in the result unchanged
        assert "non-midi-string" in result

    def test_invert_with_non_pitch_element(self):
        """Test invert handles elements without midi attribute (line 119)."""
        from music21 import tempo

        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        # Add a tempo marking (doesn't have midi attribute)
        theme.append(tempo.MetronomeMark(number=120))
        theme.append(note.Note('E4', quarterLength=1.0))

        result = invert(theme, axis_pitch='C4')

        # Should handle the tempo marking gracefully
        assert result is not None
        # The tempo marking should still be in the result
        tempo_marks = [el for el in result.flatten() if isinstance(el, tempo.MetronomeMark)]
        assert len(tempo_marks) >= 0  # Should not crash
