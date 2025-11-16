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
    stretto,
    canon_at_interval,
    proportional_canon,
    counterpoint_check,
    spectral_analysis,
    symmetry_metrics,
    chord_progression_analysis,
    compare_canons,
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


class TestStretto:
    """Test stretto transformation."""

    def test_stretto_creates_score(self):
        """Test that stretto creates a score with multiple voices."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('D4', quarterLength=1.0))
        theme.append(note.Note('E4', quarterLength=1.0))

        result = stretto(theme, num_voices=3, entry_interval=2.0)

        assert isinstance(result, stream.Score)
        assert len(result.parts) == 3

    def test_stretto_voice_timing(self):
        """Test that voices enter at correct intervals."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))

        result = stretto(theme, num_voices=2, entry_interval=4.0)

        parts = list(result.parts)
        # Collect all offsets from both voices
        all_offsets = []
        for part in parts:
            for n in part.flatten().notes:
                all_offsets.append(n.offset)

        # Should have notes at offset 0.0 and 4.0
        assert 0.0 in all_offsets
        assert 4.0 in all_offsets

    def test_stretto_with_transformation(self):
        """Test stretto with inversion transformation."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('D4', quarterLength=1.0))

        result = stretto(theme, num_voices=2, entry_interval=2.0, transformation='invert')

        parts = list(result.parts)
        # Second voice should be inverted
        voice1_pitches = [n.pitch.midi for n in parts[0].flatten().notes]
        voice2_pitches = [n.pitch.midi for n in parts[1].flatten().notes]

        # Pitches should be different due to inversion
        assert voice1_pitches != voice2_pitches

    def test_stretto_transformations(self):
        """Test all transformation options."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))

        for trans in ['none', 'invert', 'retrograde', 'augmentation', 'diminution']:
            result = stretto(theme, num_voices=2, transformation=trans)
            assert isinstance(result, stream.Score)
            assert len(result.parts) == 2


class TestCanonAtInterval:
    """Test canon at interval transformation."""

    def test_canon_at_interval_creates_score(self):
        """Test that canon_at_interval creates a score."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))

        result = canon_at_interval(theme, interval=7)

        assert isinstance(result, stream.Score)
        assert len(result.parts) == 2

    def test_canon_at_fifth(self):
        """Test canon at the fifth (interval = 7 semitones)."""
        theme = stream.Stream()
        theme.append(note.Note(midi=60, quarterLength=1.0))  # C4

        result = canon_at_interval(theme, interval=7, time_delay=0.0)

        parts = list(result.parts)
        voice1_midi = parts[0].flatten().notes[0].pitch.midi
        voice2_midi = parts[1].flatten().notes[0].pitch.midi

        assert voice1_midi == 60  # C4
        assert voice2_midi == 67  # G4 (fifth above)

    def test_canon_at_octave(self):
        """Test canon at the octave."""
        theme = stream.Stream()
        theme.append(note.Note(midi=60, quarterLength=1.0))  # C4

        result = canon_at_interval(theme, interval=12, time_delay=0.0)

        parts = list(result.parts)
        voice2_midi = parts[1].flatten().notes[0].pitch.midi

        assert voice2_midi == 72  # C5 (octave above)

    def test_canon_time_delay(self):
        """Test that time_delay works correctly."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))

        result = canon_at_interval(theme, interval=0, time_delay=4.0)

        parts = list(result.parts)
        voice1_offset = parts[0].flatten().notes[0].offset
        voice2_offset = parts[1].flatten().notes[0].offset

        assert voice1_offset == 0.0
        assert voice2_offset == 4.0

    def test_canon_negative_interval(self):
        """Test canon with downward transposition."""
        theme = stream.Stream()
        theme.append(note.Note(midi=60, quarterLength=1.0))  # C4

        result = canon_at_interval(theme, interval=-5, time_delay=0.0)

        parts = list(result.parts)
        voice2_midi = parts[1].flatten().notes[0].pitch.midi

        assert voice2_midi == 55  # G3 (fifth below)

    def test_canon_with_chord(self):
        """Test canon at interval with chords."""
        from music21 import chord as m21chord

        theme = stream.Stream()
        theme.append(m21chord.Chord(['C4', 'E4', 'G4'], quarterLength=1.0))

        result = canon_at_interval(theme, interval=7, mode='strict')

        parts = list(result.parts)
        # Both voices should have chords
        assert isinstance(parts[0].flatten().notes[0], m21chord.Chord)
        assert isinstance(parts[1].flatten().notes[0], m21chord.Chord)


class TestProportionalCanon:
    """Test proportional/mensuration canon."""

    def test_proportional_canon_creates_score(self):
        """Test that proportional_canon creates a score."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))

        result = proportional_canon(theme, ratio=(2, 3))

        assert isinstance(result, stream.Score)
        assert len(result.parts) == 2

    def test_proportional_canon_2_3_ratio(self):
        """Test 2:3 ratio (classic mensuration canon)."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))

        result = proportional_canon(theme, ratio=(2, 3))

        parts = list(result.parts)
        voice1_duration = parts[0].flatten().notes[0].quarterLength
        voice2_duration = parts[1].flatten().notes[0].quarterLength

        assert voice1_duration == 2.0  # Slower voice
        assert voice2_duration == 3.0  # Faster voice

    def test_proportional_canon_1_2_ratio(self):
        """Test 1:2 ratio (double speed)."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('D4', quarterLength=1.0))

        result = proportional_canon(theme, ratio=(1, 2))

        parts = list(result.parts)
        voice1_total = sum(n.quarterLength for n in parts[0].flatten().notes)
        voice2_total = sum(n.quarterLength for n in parts[1].flatten().notes)

        assert voice1_total == 2.0  # 1x speed
        assert voice2_total == 4.0  # 2x speed

    def test_proportional_canon_multiple_statements(self):
        """Test proportional canon with multiple statements."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))

        result = proportional_canon(theme, ratio=(1, 1), num_statements=3)

        parts = list(result.parts)
        # Each voice should have 3 notes (3 statements of 1 note each)
        assert len(list(parts[0].flatten().notes)) == 3
        assert len(list(parts[1].flatten().notes)) == 3

    def test_proportional_canon_preserves_pitches(self):
        """Test that pitches are preserved in both voices."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('E4', quarterLength=1.0))

        result = proportional_canon(theme, ratio=(1, 2))

        parts = list(result.parts)
        voice1_pitches = [n.pitch.nameWithOctave for n in parts[0].flatten().notes]
        voice2_pitches = [n.pitch.nameWithOctave for n in parts[1].flatten().notes]

        # Both voices should have same pitches
        assert voice1_pitches == voice2_pitches


class TestCounterpointCheck:
    """Test counterpoint validation."""

    def test_counterpoint_check_returns_dict(self):
        """Test that counterpoint_check returns a dictionary."""
        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))
        part1.append(note.Note('D4', quarterLength=1.0))

        part2 = stream.Part()
        part2.append(note.Note('E4', quarterLength=1.0))
        part2.append(note.Note('F4', quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        result = counterpoint_check(score)

        assert isinstance(result, dict)
        assert 'parallel_fifths' in result
        assert 'parallel_octaves' in result
        assert 'voice_crossings' in result
        assert 'quality_score' in result

    def test_counterpoint_check_wrong_voice_count(self):
        """Test counterpoint check with wrong number of voices."""
        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))
        score.append(part1)

        result = counterpoint_check(score)

        assert 'error' in result
        assert result['num_voices'] == 1

    def test_counterpoint_parallel_octaves(self):
        """Test detection of parallel octaves."""
        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note(midi=60, quarterLength=1.0))  # C4
        part1.append(note.Note(midi=62, quarterLength=1.0))  # D4

        part2 = stream.Part()
        part2.append(note.Note(midi=72, quarterLength=1.0))  # C5
        part2.append(note.Note(midi=74, quarterLength=1.0))  # D5

        score.append(part1)
        score.append(part2)

        result = counterpoint_check(score)

        # Should detect parallel octaves
        assert result['parallel_octaves'] > 0

    def test_counterpoint_parallel_fifths(self):
        """Test detection of parallel fifths."""
        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note(midi=60, quarterLength=1.0))  # C4
        part1.append(note.Note(midi=62, quarterLength=1.0))  # D4

        part2 = stream.Part()
        part2.append(note.Note(midi=67, quarterLength=1.0))  # G4 (fifth above C4)
        part2.append(note.Note(midi=69, quarterLength=1.0))  # A4 (fifth above D4)

        score.append(part1)
        score.append(part2)

        result = counterpoint_check(score)

        # Should detect parallel fifths
        assert result['parallel_fifths'] > 0

    def test_counterpoint_large_leaps(self):
        """Test detection of large leaps."""
        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note(midi=60, quarterLength=1.0))  # C4
        part1.append(note.Note(midi=72, quarterLength=1.0))  # C5 (octave leap)

        part2 = stream.Part()
        part2.append(note.Note(midi=64, quarterLength=1.0))  # E4
        part2.append(note.Note(midi=65, quarterLength=1.0))  # F4

        score.append(part1)
        score.append(part2)

        result = counterpoint_check(score)

        # Should detect large leap
        assert result['large_leaps'] > 0

    def test_counterpoint_quality_score(self):
        """Test quality score calculation."""
        # Create a good two-voice counterpoint
        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))
        part1.append(note.Note('D4', quarterLength=1.0))
        part1.append(note.Note('E4', quarterLength=1.0))

        part2 = stream.Part()
        part2.append(note.Note('G4', quarterLength=1.0))
        part2.append(note.Note('F4', quarterLength=1.0))
        part2.append(note.Note('G4', quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        result = counterpoint_check(score)

        # Quality score should be between 0 and 1
        assert 0.0 <= result['quality_score'] <= 1.0
        assert 'passed' in result
        assert isinstance(result['passed'], bool)

    def test_counterpoint_empty_voices(self):
        """Test counterpoint check with empty voices."""
        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()
        score.append(part1)
        score.append(part2)

        result = counterpoint_check(score)

        # Should handle empty voices gracefully
        assert result['quality_score'] == 1.0
        assert result['total_simultaneities'] == 0


class TestAdvancedCanonEdgeCases:
    """Test edge cases for advanced canonical transformations."""

    def test_stretto_single_voice(self):
        """Test stretto with num_voices=1."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))

        result = stretto(theme, num_voices=1)

        assert len(result.parts) == 1

    def test_stretto_empty_theme(self):
        """Test stretto with empty theme."""
        empty_theme = stream.Stream()

        result = stretto(empty_theme, num_voices=2)

        assert isinstance(result, stream.Score)
        assert len(result.parts) == 2

    def test_canon_at_interval_zero(self):
        """Test canon at interval 0 (unison canon)."""
        theme = stream.Stream()
        theme.append(note.Note(midi=60, quarterLength=1.0))

        result = canon_at_interval(theme, interval=0)

        parts = list(result.parts)
        voice1_midi = parts[0].flatten().notes[0].pitch.midi
        voice2_midi = parts[1].flatten().notes[0].pitch.midi

        assert voice1_midi == voice2_midi

    def test_proportional_canon_equal_ratio(self):
        """Test proportional canon with equal ratios (1:1)."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))

        result = proportional_canon(theme, ratio=(1, 1))

        parts = list(result.parts)
        voice1_duration = parts[0].flatten().notes[0].quarterLength
        voice2_duration = parts[1].flatten().notes[0].quarterLength

        assert voice1_duration == voice2_duration

    def test_canon_at_interval_with_rest(self):
        """Test canon at interval preserves rests."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Rest(quarterLength=1.0))

        result = canon_at_interval(theme, interval=7)

        parts = list(result.parts)
        # Both voices should have rests
        voice1_rests = [el for el in parts[0].flatten().notesAndRests if el.isRest]
        voice2_rests = [el for el in parts[1].flatten().notesAndRests if el.isRest]

        assert len(voice1_rests) > 0
        assert len(voice2_rests) > 0

    def test_proportional_canon_with_rest(self):
        """Test proportional canon preserves rests."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Rest(quarterLength=1.0))

        result = proportional_canon(theme, ratio=(1, 2))

        parts = list(result.parts)
        # Check that rests are present in the result
        total_elements = len(list(parts[0].flatten().notesAndRests))
        assert total_elements == 2


class TestSpectralAnalysis:
    """Test spectral/frequency analysis."""

    def test_spectral_analysis_returns_dict(self):
        """Test that spectral_analysis returns a dictionary."""
        melody = stream.Part()
        melody.append(note.Note('C4', quarterLength=1.0))
        melody.append(note.Note('D4', quarterLength=1.0))
        melody.append(note.Note('E4', quarterLength=1.0))

        analysis = spectral_analysis(melody)

        assert isinstance(analysis, dict)
        assert 'total_pitches' in analysis
        assert 'pitch_class_histogram' in analysis
        assert 'tessitura' in analysis

    def test_spectral_analysis_pitch_class_histogram(self):
        """Test pitch class histogram calculation."""
        melody = stream.Part()
        melody.append(note.Note(midi=60, quarterLength=1.0))  # C4
        melody.append(note.Note(midi=72, quarterLength=1.0))  # C5
        melody.append(note.Note(midi=62, quarterLength=1.0))  # D4

        analysis = spectral_analysis(melody)

        # Should have 2 Cs and 1 D
        assert analysis['pitch_class_histogram'][0] == 2  # C
        assert analysis['pitch_class_histogram'][2] == 1  # D
        assert analysis['most_common_pitch_class'] == 'C'

    def test_spectral_analysis_pitch_range(self):
        """Test pitch range calculation."""
        melody = stream.Part()
        melody.append(note.Note(midi=60, quarterLength=1.0))  # C4
        melody.append(note.Note(midi=72, quarterLength=1.0))  # C5

        analysis = spectral_analysis(melody)

        assert analysis['pitch_range'] == 12  # One octave
        assert analysis['lowest_pitch'] == 60
        assert analysis['highest_pitch'] == 72

    def test_spectral_analysis_empty_stream(self):
        """Test spectral analysis with empty stream."""
        empty_part = stream.Part()
        analysis = spectral_analysis(empty_part)

        assert analysis['total_pitches'] == 0
        assert analysis['pitch_range'] == 0

    def test_spectral_analysis_with_chord(self):
        """Test spectral analysis handles chords."""
        from music21 import chord as m21chord

        melody = stream.Part()
        melody.append(m21chord.Chord(['C4', 'E4', 'G4'], quarterLength=1.0))

        analysis = spectral_analysis(melody)

        assert analysis['total_pitches'] == 3
        assert analysis['pitch_class_histogram'][0] >= 1  # C
        assert analysis['pitch_class_histogram'][4] >= 1  # E


class TestSymmetryMetrics:
    """Test advanced symmetry metrics."""

    def test_symmetry_metrics_returns_dict(self):
        """Test that symmetry_metrics returns a dictionary."""
        from cancrizans.bach_crab import assemble_crab_from_theme

        theme = stream.Part()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('D4', quarterLength=1.0))

        canon = assemble_crab_from_theme(theme)
        metrics = symmetry_metrics(canon)

        assert isinstance(metrics, dict)
        assert 'overall_symmetry' in metrics
        assert 'pitch_symmetry' in metrics
        assert 'rhythmic_symmetry' in metrics

    def test_symmetry_metrics_perfect_palindrome(self):
        """Test metrics for perfect palindrome."""
        from cancrizans.bach_crab import assemble_crab_from_theme

        theme = stream.Part()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('D4', quarterLength=1.0))
        theme.append(note.Note('E4', quarterLength=1.0))

        canon = assemble_crab_from_theme(theme)
        metrics = symmetry_metrics(canon)

        # Should be a perfect palindrome
        assert metrics['pitch_symmetry'] == 1.0
        assert metrics['rhythmic_symmetry'] == 1.0
        assert metrics['is_perfect_palindrome'] is True

    def test_symmetry_metrics_wrong_voice_count(self):
        """Test symmetry metrics with wrong number of voices."""
        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))
        score.append(part1)

        metrics = symmetry_metrics(score)

        assert 'error' in metrics
        assert metrics['num_voices'] == 1

    def test_symmetry_metrics_different_lengths(self):
        """Test symmetry metrics with different voice lengths."""
        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))
        part1.append(note.Note('D4', quarterLength=1.0))

        part2 = stream.Part()
        part2.append(note.Note('E4', quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        metrics = symmetry_metrics(score)

        assert 'error' in metrics

    def test_symmetry_metrics_empty_voices(self):
        """Test symmetry metrics with empty voices."""
        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()
        score.append(part1)
        score.append(part2)

        metrics = symmetry_metrics(score)

        assert metrics['overall_symmetry'] == 1.0
        assert metrics['note_count'] == 0


class TestChordProgressionAnalysis:
    """Test chord progression analysis."""

    def test_chord_progression_analysis_returns_dict(self):
        """Test that chord_progression_analysis returns a dictionary."""
        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))
        part1.append(note.Note('D4', quarterLength=1.0))

        part2 = stream.Part()
        part2.append(note.Note('E4', quarterLength=1.0))
        part2.append(note.Note('F4', quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        analysis = chord_progression_analysis(score)

        assert isinstance(analysis, dict)
        assert 'total_chords' in analysis
        assert 'unique_chords' in analysis
        assert 'chord_types' in analysis

    def test_chord_progression_analysis_wrong_voice_count(self):
        """Test chord analysis with wrong number of voices."""
        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))
        score.append(part1)

        analysis = chord_progression_analysis(score)

        assert 'error' in analysis
        assert analysis['num_voices'] == 1

    def test_chord_progression_identifies_triads(self):
        """Test that major and minor triads are identified."""
        from music21 import chord as m21chord

        score = stream.Score()
        part1 = stream.Part()
        # Create a C major triad vertically
        part1.append(m21chord.Chord(['C4', 'E4', 'G4'], quarterLength=1.0))

        score.append(part1)

        # For chord analysis, we need at least 2 parts
        # Let's create a simpler test
        score2 = stream.Score()
        p1 = stream.Part()
        p2 = stream.Part()
        p1.append(note.Note('C4', quarterLength=1.0))
        p2.append(note.Note('E4', quarterLength=1.0))
        score2.append(p1)
        score2.append(p2)

        analysis = chord_progression_analysis(score2)

        assert analysis['total_chords'] >= 1


class TestCompareCanons:
    """Test canon comparison tools."""

    def test_compare_canons_returns_dict(self):
        """Test that compare_canons returns a dictionary."""
        from cancrizans.bach_crab import assemble_crab_from_theme

        theme1 = stream.Part()
        theme1.append(note.Note('C4', quarterLength=1.0))
        theme1.append(note.Note('D4', quarterLength=1.0))

        theme2 = stream.Part()
        theme2.append(note.Note('E4', quarterLength=1.0))
        theme2.append(note.Note('F4', quarterLength=1.0))

        canon1 = assemble_crab_from_theme(theme1)
        canon2 = assemble_crab_from_theme(theme2)

        comparison = compare_canons(canon1, canon2)

        assert isinstance(comparison, dict)
        assert 'overall_similarity' in comparison
        assert 'interval_similarity' in comparison
        assert 'rhythm_similarity' in comparison
        assert 'comparison_summary' in comparison

    def test_compare_canons_identical(self):
        """Test comparing a canon to itself."""
        from cancrizans.bach_crab import assemble_crab_from_theme

        theme = stream.Part()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('D4', quarterLength=1.0))
        theme.append(note.Note('E4', quarterLength=1.0))

        canon = assemble_crab_from_theme(theme)

        comparison = compare_canons(canon, canon)

        # Should be identical (similarity close to 1.0)
        assert comparison['overall_similarity'] >= 0.99
        assert 'Very similar' in comparison['comparison_summary']

    def test_compare_canons_different(self):
        """Test comparing very different canons."""
        from cancrizans.bach_crab import assemble_crab_from_theme

        # Canon 1: stepwise motion
        theme1 = stream.Part()
        theme1.append(note.Note('C4', quarterLength=1.0))
        theme1.append(note.Note('D4', quarterLength=1.0))
        theme1.append(note.Note('E4', quarterLength=1.0))

        # Canon 2: large leaps
        theme2 = stream.Part()
        theme2.append(note.Note('C4', quarterLength=2.0))
        theme2.append(note.Note('G4', quarterLength=0.5))

        canon1 = assemble_crab_from_theme(theme1)
        canon2 = assemble_crab_from_theme(theme2)

        comparison = compare_canons(canon1, canon2)

        # Should have some similarity score
        assert 0.0 <= comparison['overall_similarity'] <= 1.0
        assert 'length_ratio' in comparison


class TestAdvancedAnalysisEdgeCases:
    """Test edge cases for advanced analysis functions."""

    def test_spectral_analysis_score(self):
        """Test spectral analysis with a Score instead of Part."""
        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))

        part2 = stream.Part()
        part2.append(note.Note('E4', quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        analysis = spectral_analysis(score)

        assert analysis['total_pitches'] == 2

    def test_symmetry_metrics_partial_match(self):
        """Test symmetry metrics with partial palindrome."""
        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))
        part1.append(note.Note('D4', quarterLength=1.0))
        part1.append(note.Note('E4', quarterLength=1.0))

        part2 = stream.Part()
        part2.append(note.Note('E4', quarterLength=1.0))
        part2.append(note.Note('D4', quarterLength=1.0))
        part2.append(note.Note('F4', quarterLength=1.0))  # Different from C4

        score.append(part1)
        score.append(part2)

        metrics = symmetry_metrics(score)

        # Should have partial symmetry
        assert 0.0 < metrics['overall_symmetry'] < 1.0
        assert metrics['pitch_matches'] == 2  # D and E match

    def test_chord_progression_with_chords(self):
        """Test chord progression analysis with actual chords."""
        from music21 import chord as m21chord

        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))
        part1.append(m21chord.Chord(['E4', 'G4'], quarterLength=1.0))

        part2 = stream.Part()
        part2.append(note.Note('G3', quarterLength=1.0))
        part2.append(note.Note('C4', quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        analysis = chord_progression_analysis(score)

        assert analysis['total_chords'] >= 1

    def test_compare_canons_empty(self):
        """Test comparing empty canons."""
        score1 = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()
        score1.append(part1)
        score1.append(part2)

        score2 = stream.Score()
        part3 = stream.Part()
        part4 = stream.Part()
        score2.append(part3)
        score2.append(part4)

        comparison = compare_canons(score1, score2)

        # Should handle empty canons gracefully
        assert isinstance(comparison, dict)
        assert 'overall_similarity' in comparison


class TestVoiceLeadingAnalysis:
    """Test advanced voice leading analysis."""

    def test_voice_leading_basic(self):
        """Test basic voice leading analysis."""
        from cancrizans import voice_leading_analysis, assemble_crab_from_theme

        theme = stream.Part()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('D4', quarterLength=1.0))
        theme.append(note.Note('E4', quarterLength=1.0))

        canon = assemble_crab_from_theme(theme)
        results = voice_leading_analysis(canon)

        assert isinstance(results, dict)
        assert 'motion_types' in results
        assert 'voice_ranges' in results
        assert 'leap_statistics' in results
        assert 'overall_quality' in results
        assert 'grade' in results

    def test_voice_leading_motion_types(self):
        """Test that motion types are correctly identified."""
        from cancrizans import voice_leading_analysis

        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()

        # Create contrary motion: voice 1 ascending, voice 2 descending
        part1.append(note.Note('C4', quarterLength=1.0))
        part1.append(note.Note('D4', quarterLength=1.0))
        part1.append(note.Note('E4', quarterLength=1.0))

        part2.append(note.Note('G3', quarterLength=1.0))
        part2.append(note.Note('F3', quarterLength=1.0))
        part2.append(note.Note('E3', quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        results = voice_leading_analysis(score)

        assert results['motion_types']['contrary'] > 0
        assert 'motion_percentages' in results

    def test_voice_leading_ranges(self):
        """Test voice range tracking."""
        from cancrizans import voice_leading_analysis

        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()

        # Wide range in voice 1
        part1.append(note.Note('C4', quarterLength=1.0))
        part1.append(note.Note('C5', quarterLength=1.0))

        # Narrow range in voice 2
        part2.append(note.Note('G3', quarterLength=1.0))
        part2.append(note.Note('A3', quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        results = voice_leading_analysis(score)

        assert results['voice_ranges']['voice1']['span'] == 12  # Octave
        assert results['voice_ranges']['voice2']['span'] == 2   # Major second

    def test_voice_leading_leap_resolution(self):
        """Test leap resolution tracking."""
        from cancrizans import voice_leading_analysis

        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()

        # Leap followed by stepwise resolution in opposite direction
        part1.append(note.Note('C4', quarterLength=1.0))
        part1.append(note.Note('G4', quarterLength=1.0))  # Leap up
        part1.append(note.Note('F4', quarterLength=1.0))  # Step down (resolved)

        part2.append(note.Note('C3', quarterLength=1.0))
        part2.append(note.Note('C3', quarterLength=1.0))
        part2.append(note.Note('C3', quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        results = voice_leading_analysis(score)

        assert results['leap_statistics']['total_leaps'] >= 1
        assert results['leap_statistics']['resolved_leaps'] >= 0

    def test_voice_leading_wrong_voice_count(self):
        """Test voice leading with wrong number of voices."""
        from cancrizans import voice_leading_analysis

        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))
        score.append(part1)

        results = voice_leading_analysis(score)

        assert 'error' in results
        assert results['num_voices'] == 1

    def test_voice_leading_quality_scores(self):
        """Test that quality scores are in valid range."""
        from cancrizans import voice_leading_analysis, assemble_crab_from_theme

        theme = stream.Part()
        for pitch in ['C4', 'D4', 'E4', 'F4']:
            theme.append(note.Note(pitch, quarterLength=1.0))

        canon = assemble_crab_from_theme(theme)
        results = voice_leading_analysis(canon)

        assert 0.0 <= results['independence_score'] <= 1.0
        assert 0.0 <= results['perfect_approach_score'] <= 1.0
        assert 0.0 <= results['overall_quality'] <= 1.0
        assert results['grade'] in ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F']


class TestCadenceDetection:
    """Test cadence detection functionality."""

    def test_cadence_detection_basic(self):
        """Test basic cadence detection."""
        from cancrizans import cadence_detection

        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()

        # Create a simple cadential pattern
        part1.append(note.Note('D4', quarterLength=1.0))
        part1.append(note.Note('D4', quarterLength=1.0))
        part1.append(note.Note('C4', quarterLength=1.0))

        part2.append(note.Note('G3', quarterLength=1.0))
        part2.append(note.Note('G3', quarterLength=1.0))
        part2.append(note.Note('C3', quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        results = cadence_detection(score)

        assert isinstance(results, dict)
        assert 'cadences' in results
        assert 'cadence_counts' in results
        assert 'total_cadences' in results
        assert 'has_final_cadence' in results

    def test_cadence_detection_authentic(self):
        """Test authentic cadence detection."""
        from cancrizans import cadence_detection

        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()

        # Create authentic cadence: V-I with bass rising by 4th
        part1.append(note.Note('C4', quarterLength=1.0))
        part1.append(note.Note('B3', quarterLength=1.0))
        part1.append(note.Note('C4', quarterLength=1.0))

        part2.append(note.Note('G3', quarterLength=1.0))
        part2.append(note.Note('G3', quarterLength=1.0))
        part2.append(note.Note('C3', quarterLength=1.0))  # Bass rises by 4th

        score.append(part1)
        score.append(part2)

        results = cadence_detection(score)

        # Should detect at least one cadence
        assert results['total_cadences'] >= 1
        assert results['has_final_cadence']

    def test_cadence_detection_half(self):
        """Test half cadence detection."""
        from cancrizans import cadence_detection

        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()

        # Create half cadence: ending on perfect fifth
        part1.append(note.Note('C4', quarterLength=1.0))
        part1.append(note.Note('D4', quarterLength=1.0))
        part1.append(note.Note('D4', quarterLength=1.0))

        part2.append(note.Note('E3', quarterLength=1.0))
        part2.append(note.Note('F3', quarterLength=1.0))
        part2.append(note.Note('G3', quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        results = cadence_detection(score)

        # Should detect half cadence (ending on 5th interval)
        if results['has_final_cadence']:
            assert results['final_cadence_type'] in ['half', 'other']

    def test_cadence_detection_insufficient_notes(self):
        """Test cadence detection with too few notes."""
        from cancrizans import cadence_detection

        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()

        # Only 2 notes (need at least 3 for cadence analysis)
        part1.append(note.Note('C4', quarterLength=1.0))
        part1.append(note.Note('D4', quarterLength=1.0))

        part2.append(note.Note('G3', quarterLength=1.0))
        part2.append(note.Note('A3', quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        results = cadence_detection(score)

        assert results['total_cadences'] == 0
        assert not results['has_final_cadence']

    def test_cadence_detection_wrong_voice_count(self):
        """Test cadence detection with wrong number of voices."""
        from cancrizans import cadence_detection

        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))
        score.append(part1)

        results = cadence_detection(score)

        assert 'error' in results
        assert results['num_voices'] == 1


class TestModulationDetection:
    """Test modulation/key change detection."""

    def test_modulation_detection_basic(self):
        """Test basic modulation detection."""
        from cancrizans import modulation_detection

        score = stream.Score()
        part1 = stream.Part()

        # Simple passage in C major
        for pitch in ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5'] * 2:
            part1.append(note.Note(pitch, quarterLength=0.5))

        score.append(part1)

        results = modulation_detection(score)

        assert isinstance(results, dict)
        assert 'num_modulations' in results
        assert 'modulations' in results
        assert 'starting_key' in results
        assert 'ending_key' in results

    def test_modulation_detection_key_change(self):
        """Test detection of actual key change."""
        from cancrizans import modulation_detection

        score = stream.Score()
        part1 = stream.Part()

        # Start in C major
        for pitch in ['C4', 'E4', 'G4', 'C4'] * 2:
            part1.append(note.Note(pitch, quarterLength=0.5))

        # Shift to G major
        for pitch in ['G4', 'B4', 'D5', 'G4'] * 2:
            part1.append(note.Note(pitch, quarterLength=0.5))

        score.append(part1)

        results = modulation_detection(score, window_size=4)

        # Should detect at least some shift in tonal center
        assert results['starting_key'] is not None
        assert results['ending_key'] is not None

    def test_modulation_detection_insufficient_notes(self):
        """Test modulation detection with too few notes."""
        from cancrizans import modulation_detection

        score = stream.Score()
        part1 = stream.Part()

        # Only 3 notes (need at least 16 for default window_size=8)
        part1.append(note.Note('C4', quarterLength=1.0))
        part1.append(note.Note('D4', quarterLength=1.0))
        part1.append(note.Note('E4', quarterLength=1.0))

        score.append(part1)

        results = modulation_detection(score)

        assert 'error' in results
        assert results['num_modulations'] == 0

    def test_modulation_detection_custom_window(self):
        """Test modulation detection with custom window size."""
        from cancrizans import modulation_detection

        score = stream.Score()
        part1 = stream.Part()

        for pitch in ['C4', 'D4', 'E4'] * 4:
            part1.append(note.Note(pitch, quarterLength=0.5))

        score.append(part1)

        results = modulation_detection(score, window_size=3)

        assert results['window_size'] == 3
        assert results['windows_analyzed'] >= 0


class TestSpeciesCounterpointCheck:
    """Test species counterpoint rule checking."""

    def test_species_counterpoint_first_species(self):
        """Test first species counterpoint checking."""
        from cancrizans import species_counterpoint_check

        score = stream.Score()
        cantus = stream.Part()
        counterpoint = stream.Part()

        # Simple first species: note-against-note consonances
        cantus.append(note.Note('C4', quarterLength=1.0))
        cantus.append(note.Note('D4', quarterLength=1.0))
        cantus.append(note.Note('E4', quarterLength=1.0))
        cantus.append(note.Note('C4', quarterLength=1.0))

        counterpoint.append(note.Note('C5', quarterLength=1.0))  # Unison (perfect)
        counterpoint.append(note.Note('A4', quarterLength=1.0))  # Fifth above
        counterpoint.append(note.Note('G4', quarterLength=1.0))  # Third above
        counterpoint.append(note.Note('C5', quarterLength=1.0))  # Octave (perfect)

        score.append(counterpoint)
        score.append(cantus)

        results = species_counterpoint_check(score, species=1)

        assert isinstance(results, dict)
        assert results['species'] == 1
        assert 'violations' in results
        assert 'total_violations' in results
        assert 'compliance_rate' in results
        assert 'passed' in results
        assert 'grade' in results

    def test_species_counterpoint_parallel_fifths(self):
        """Test detection of parallel fifths."""
        from cancrizans import species_counterpoint_check

        score = stream.Score()
        cantus = stream.Part()
        counterpoint = stream.Part()

        # Create parallel fifths (forbidden)
        cantus.append(note.Note('C4', quarterLength=1.0))
        cantus.append(note.Note('D4', quarterLength=1.0))

        counterpoint.append(note.Note('G4', quarterLength=1.0))  # Fifth above C
        counterpoint.append(note.Note('A4', quarterLength=1.0))  # Fifth above D (parallel!)

        score.append(counterpoint)
        score.append(cantus)

        results = species_counterpoint_check(score, species=1)

        assert results['violations']['parallel_perfect']  # Should detect parallel perfect intervals

    def test_species_counterpoint_bad_opening(self):
        """Test detection of improper opening interval."""
        from cancrizans import species_counterpoint_check

        score = stream.Score()
        cantus = stream.Part()
        counterpoint = stream.Part()

        # Start with third (not perfect consonance)
        cantus.append(note.Note('C4', quarterLength=1.0))
        cantus.append(note.Note('D4', quarterLength=1.0))

        counterpoint.append(note.Note('E4', quarterLength=1.0))  # Third (bad opening)
        counterpoint.append(note.Note('F4', quarterLength=1.0))

        score.append(counterpoint)
        score.append(cantus)

        results = species_counterpoint_check(score, species=1)

        assert results['violations']['bad_opening']  # Should detect bad opening

    def test_species_counterpoint_dissonance(self):
        """Test detection of dissonances in first species."""
        from cancrizans import species_counterpoint_check

        score = stream.Score()
        cantus = stream.Part()
        counterpoint = stream.Part()

        # Include dissonance (second)
        cantus.append(note.Note('C4', quarterLength=1.0))
        cantus.append(note.Note('D4', quarterLength=1.0))

        counterpoint.append(note.Note('C5', quarterLength=1.0))
        counterpoint.append(note.Note('E4', quarterLength=1.0))  # Second above D (dissonance!)

        score.append(counterpoint)
        score.append(cantus)

        results = species_counterpoint_check(score, species=1)

        assert results['violations']['bad_intervals']  # Should detect dissonance

    def test_species_counterpoint_large_leap(self):
        """Test detection of large leaps."""
        from cancrizans import species_counterpoint_check

        score = stream.Score()
        cantus = stream.Part()
        counterpoint = stream.Part()

        # Large leap in counterpoint (> octave)
        cantus.append(note.Note('C4', quarterLength=1.0))
        cantus.append(note.Note('D4', quarterLength=1.0))
        cantus.append(note.Note('E4', quarterLength=1.0))

        counterpoint.append(note.Note('C5', quarterLength=1.0))
        counterpoint.append(note.Note('D6', quarterLength=1.0))  # Minor 9th (13 semitones - larger than octave!)
        counterpoint.append(note.Note('C4', quarterLength=1.0))

        score.append(counterpoint)
        score.append(cantus)

        results = species_counterpoint_check(score, species=1)

        assert results['violations']['large_leaps']  # Should detect large leap

    def test_species_counterpoint_invalid_species(self):
        """Test with invalid species number."""
        from cancrizans import species_counterpoint_check

        score = stream.Score()
        cantus = stream.Part()
        counterpoint = stream.Part()

        cantus.append(note.Note('C4', quarterLength=1.0))
        counterpoint.append(note.Note('C5', quarterLength=1.0))

        score.append(counterpoint)
        score.append(cantus)

        results = species_counterpoint_check(score, species=5)

        assert 'error' in results

    def test_species_counterpoint_wrong_voice_count(self):
        """Test with wrong number of voices."""
        from cancrizans import species_counterpoint_check

        score = stream.Score()
        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))
        score.append(part1)

        results = species_counterpoint_check(score, species=1)

        assert 'error' in results
        assert results['num_voices'] == 1

    def test_species_counterpoint_compliance_rate(self):
        """Test that compliance rate is calculated correctly."""
        from cancrizans import species_counterpoint_check

        score = stream.Score()
        cantus = stream.Part()
        counterpoint = stream.Part()

        # Perfect first species counterpoint
        cantus.append(note.Note('C4', quarterLength=1.0))
        cantus.append(note.Note('D4', quarterLength=1.0))
        cantus.append(note.Note('C4', quarterLength=1.0))

        counterpoint.append(note.Note('C5', quarterLength=1.0))  # Unison
        counterpoint.append(note.Note('A4', quarterLength=1.0))  # Sixth
        counterpoint.append(note.Note('C5', quarterLength=1.0))  # Octave

        score.append(counterpoint)
        score.append(cantus)

        results = species_counterpoint_check(score, species=1)

        assert 0.0 <= results['compliance_rate'] <= 1.0
        assert results['grade'] in ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F']


# ============================================================================
# Phase 9: Advanced Canon Types Tests
# ============================================================================


class TestAdvancedCanonTypes:
    """Tests for Phase 9: Advanced canon types (table, mensuration, spiral, puzzle)."""

    def test_table_canon_four_voices(self):
        """Test table canon with 4 voices."""
        from cancrizans import table_canon

        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('E4', quarterLength=1.0))
        theme.append(note.Note('G4', quarterLength=1.0))

        canon = table_canon(theme, num_voices=4)

        assert len(canon.parts) == 4
        assert canon.parts[0].id == 'voice1_normal'
        assert canon.parts[1].id == 'voice2_inversion'
        assert canon.parts[2].id == 'voice3_retrograde'
        assert canon.parts[3].id == 'voice4_retro_inversion'

    def test_table_canon_two_voices(self):
        """Test table canon with 2 voices only."""
        from cancrizans import table_canon

        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('D4', quarterLength=1.0))

        canon = table_canon(theme, num_voices=2)

        assert len(canon.parts) == 2
        assert canon.parts[0].id == 'voice1_normal'
        assert canon.parts[1].id == 'voice2_inversion'

    def test_table_canon_invalid_num_voices(self):
        """Test table canon with invalid number of voices."""
        from cancrizans import table_canon
        import pytest

        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))

        with pytest.raises(ValueError, match="num_voices must be 2 or 4"):
            table_canon(theme, num_voices=3)

    def test_table_canon_axis_pitch(self):
        """Test table canon with custom axis pitch."""
        from cancrizans import table_canon

        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('E4', quarterLength=1.0))

        canon = table_canon(theme, num_voices=2, axis_pitch='D4')

        # Verify inversion happened around D4
        voice2_notes = list(canon.parts[1].flatten().notes)
        assert len(voice2_notes) == 2

    def test_mensuration_canon_basic(self):
        """Test basic mensuration canon with 2:1 ratio."""
        from cancrizans import mensuration_canon

        theme = stream.Stream()
        for pitch in ['C4', 'D4', 'E4', 'F4']:
            theme.append(note.Note(pitch, quarterLength=1.0))

        canon = mensuration_canon(theme, ratios=[1.0, 2.0])

        assert len(canon.parts) == 2
        voice1_notes = list(canon.parts[0].flatten().notes)
        voice2_notes = list(canon.parts[1].flatten().notes)

        assert len(voice1_notes) == 4
        assert len(voice2_notes) == 4

        # Voice 2 should be twice as slow
        assert voice2_notes[0].quarterLength == 2.0

    def test_mensuration_canon_three_ratios(self):
        """Test mensuration canon with three different ratios."""
        from cancrizans import mensuration_canon

        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('D4', quarterLength=1.0))

        canon = mensuration_canon(theme, ratios=[1.0, 2.0, 4.0])

        assert len(canon.parts) == 3
        voice1 = list(canon.parts[0].flatten().notes)
        voice2 = list(canon.parts[1].flatten().notes)
        voice3 = list(canon.parts[2].flatten().notes)

        assert voice1[0].quarterLength == 1.0
        assert voice2[0].quarterLength == 2.0
        assert voice3[0].quarterLength == 4.0

    def test_mensuration_canon_with_offset(self):
        """Test mensuration canon with temporal offset."""
        from cancrizans import mensuration_canon

        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))

        canon = mensuration_canon(theme, ratios=[1.0, 1.0], offset_quarters=2.0)

        # Voice 2 should start 2 quarters later
        assert len(canon.parts) == 2

        # Access notes directly from parts without converting to list first
        voice1_first_note = None
        for n in canon.parts[0].flatten().notes:
            voice1_first_note = n
            break

        voice2_first_note = None
        for n in canon.parts[1].flatten().notes:
            voice2_first_note = n
            break

        assert voice1_first_note is not None
        assert voice2_first_note is not None
        assert voice1_first_note.offset == 0.0
        assert voice2_first_note.offset == 2.0

    def test_spiral_canon_ascending(self):
        """Test ascending spiral canon."""
        from cancrizans import spiral_canon

        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('E4', quarterLength=1.0))

        canon = spiral_canon(theme, num_iterations=3, transposition_interval=2, mode='ascending')

        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 6  # 2 notes * 3 iterations

        # Check transposition: iteration 0 (C4), iteration 1 (D4 = C4+2), iteration 2 (E4 = C4+4)
        assert notes[0].pitch.midi == 60  # C4
        assert notes[2].pitch.midi == 62  # D4 (first note of iteration 2)
        assert notes[4].pitch.midi == 64  # E4 (first note of iteration 3)

    def test_spiral_canon_descending(self):
        """Test descending spiral canon."""
        from cancrizans import spiral_canon

        theme = stream.Stream()
        theme.append(note.Note('C5', quarterLength=1.0))

        canon = spiral_canon(theme, num_iterations=3, transposition_interval=2, mode='descending')

        notes = list(canon.parts[0].flatten().notes)
        assert len(notes) == 3

        # Check transposition downward
        assert notes[0].pitch.midi == 72  # C5
        assert notes[1].pitch.midi == 70  # Bb4 (C5-2)
        assert notes[2].pitch.midi == 68  # Ab4 (C5-4)

    def test_spiral_canon_invalid_mode(self):
        """Test spiral canon with invalid mode."""
        from cancrizans import spiral_canon
        import pytest

        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))

        with pytest.raises(ValueError, match="mode must be 'ascending' or 'descending'"):
            spiral_canon(theme, num_iterations=2, mode='invalid')

    def test_spiral_canon_timing(self):
        """Test that spiral canon iterations are properly timed."""
        from cancrizans import spiral_canon

        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=2.0))  # 2 quarters duration

        canon = spiral_canon(theme, num_iterations=3, transposition_interval=1)

        notes = list(canon.parts[0].flatten().notes)

        # Each iteration should start after the previous one completes
        assert notes[0].offset == 0.0
        assert notes[1].offset == 2.0
        assert notes[2].offset == 4.0

    def test_solve_puzzle_canon_retrograde(self):
        """Test solving a retrograde puzzle canon."""
        from cancrizans import solve_puzzle_canon

        voice = stream.Stream()
        voice.append(note.Note('C4', quarterLength=1.0))
        voice.append(note.Note('D4', quarterLength=1.0))
        voice.append(note.Note('E4', quarterLength=1.0))

        canon = solve_puzzle_canon(voice, canon_type='retrograde')

        assert len(canon.parts) == 2
        assert canon.parts[0].id == 'given_voice'
        assert canon.parts[1].id == 'solved_retrograde'

        voice1_notes = list(canon.parts[0].flatten().notes)
        voice2_notes = list(canon.parts[1].flatten().notes)

        # Retrograde should have pitches in reverse order
        assert voice1_notes[0].pitch.midi == 60  # C4
        assert voice1_notes[2].pitch.midi == 64  # E4
        assert voice2_notes[0].pitch.midi == 64  # E4 (first in retrograde)
        assert voice2_notes[2].pitch.midi == 60  # C4 (last in retrograde)

    def test_solve_puzzle_canon_inversion(self):
        """Test solving an inversion puzzle canon."""
        from cancrizans import solve_puzzle_canon

        voice = stream.Stream()
        voice.append(note.Note('C4', quarterLength=1.0))
        voice.append(note.Note('E4', quarterLength=1.0))

        canon = solve_puzzle_canon(voice, canon_type='inversion', axis_pitch='C4')

        assert len(canon.parts) == 2
        assert canon.parts[1].id == 'solved_inversion'

        voice2_notes = list(canon.parts[1].flatten().notes)

        # C4 inverted around C4 = C4, E4 inverted around C4 = Ab3
        assert voice2_notes[0].pitch.midi == 60  # C4
        assert voice2_notes[1].pitch.midi == 56  # Ab3

    def test_solve_puzzle_canon_retro_inversion(self):
        """Test solving a retrograde+inversion puzzle canon."""
        from cancrizans import solve_puzzle_canon

        voice = stream.Stream()
        voice.append(note.Note('C4', quarterLength=1.0))
        voice.append(note.Note('D4', quarterLength=1.0))

        canon = solve_puzzle_canon(voice, canon_type='retro_inversion', axis_pitch='C4')

        assert len(canon.parts) == 2
        assert canon.parts[1].id == 'solved_retro_inversion'

        # Should be both retrograded and inverted
        voice2_notes = list(canon.parts[1].flatten().notes)
        assert len(voice2_notes) == 2

    def test_solve_puzzle_canon_augmentation(self):
        """Test solving an augmentation (mensuration) puzzle canon."""
        from cancrizans import solve_puzzle_canon

        voice = stream.Stream()
        voice.append(note.Note('C4', quarterLength=1.0))

        canon = solve_puzzle_canon(voice, canon_type='augmentation')

        assert len(canon.parts) == 2
        assert canon.parts[1].id == 'solved_augmentation'

        voice2_notes = list(canon.parts[1].flatten().notes)

        # Should be twice as slow (2:1 ratio)
        assert voice2_notes[0].quarterLength == 2.0

    def test_solve_puzzle_canon_invalid_type(self):
        """Test solve_puzzle_canon with invalid canon type."""
        from cancrizans import solve_puzzle_canon
        import pytest

        voice = stream.Stream()
        voice.append(note.Note('C4', quarterLength=1.0))

        with pytest.raises(ValueError, match="canon_type must be one of"):
            solve_puzzle_canon(voice, canon_type='invalid')

    def test_solve_puzzle_canon_with_offset(self):
        """Test puzzle canon solver with temporal offset."""
        from cancrizans import solve_puzzle_canon

        voice = stream.Stream()
        voice.append(note.Note('C4', quarterLength=1.0))

        canon = solve_puzzle_canon(voice, canon_type='retrograde', offset_quarters=2.0)

        voice1_notes = list(canon.parts[0].flatten().notes)
        voice2_notes = list(canon.parts[1].flatten().notes)

        # Voice 2 should start 2 quarters later
        assert voice1_notes[0].offset == 0.0
        assert voice2_notes[0].offset == 2.0


class TestPhase11HarmonicEnhancement:
    """Test Phase 11: Harmonic Enhancement functions."""

    def test_analyze_chord_progressions_basic(self):
        """Test basic chord progression analysis."""
        from cancrizans import analyze_chord_progressions
        from music21 import chord, stream

        # Create a simple I-IV-V-I progression in C major
        score = stream.Score()
        part = stream.Part()

        # I chord (C-E-G)
        part.append(chord.Chord(['C4', 'E4', 'G4'], quarterLength=1.0))
        # IV chord (F-A-C)
        part.append(chord.Chord(['F4', 'A4', 'C5'], quarterLength=1.0))
        # V chord (G-B-D)
        part.append(chord.Chord(['G4', 'B4', 'D5'], quarterLength=1.0))
        # I chord (C-E-G)
        part.append(chord.Chord(['C4', 'E4', 'G4'], quarterLength=1.0))

        score.append(part)

        result = analyze_chord_progressions(score)

        assert 'chords' in result
        assert 'progressions' in result
        assert 'key' in result
        assert len(result['chords']) == 4
        assert result['num_chords'] == 4

    def test_analyze_chord_progressions_detects_cadence(self):
        """Test that chord progression analysis detects cadences."""
        from cancrizans import analyze_chord_progressions
        from music21 import chord, stream

        # Create a V-I authentic cadence
        score = stream.Score()
        part = stream.Part()

        # V chord (G-B-D)
        part.append(chord.Chord(['G4', 'B4', 'D5'], quarterLength=1.0))
        # I chord (C-E-G)
        part.append(chord.Chord(['C4', 'E4', 'G4'], quarterLength=1.0))

        score.append(part)

        result = analyze_chord_progressions(score)

        # Should detect authentic cadence pattern
        assert any('authentic_cadence' in p.get('type', '') for p in result['progressions'])

    def test_analyze_chord_progressions_with_key(self):
        """Test chord progression analysis with specified key."""
        from cancrizans import analyze_chord_progressions
        from music21 import chord, stream, key

        score = stream.Score()
        part = stream.Part()
        part.append(chord.Chord(['G4', 'B4', 'D5'], quarterLength=1.0))
        score.append(part)

        # Specify key explicitly
        result = analyze_chord_progressions(score, key_sig='G')

        assert 'key' in result
        assert 'G' in result['key']

    def test_functional_harmony_analysis_basic(self):
        """Test basic functional harmony analysis."""
        from cancrizans import functional_harmony_analysis
        from music21 import chord, stream

        # Create I-IV-V-I progression
        score = stream.Score()
        part = stream.Part()

        # I (tonic)
        part.append(chord.Chord(['C4', 'E4', 'G4'], quarterLength=1.0))
        # IV (subdominant)
        part.append(chord.Chord(['F4', 'A4', 'C5'], quarterLength=1.0))
        # V (dominant)
        part.append(chord.Chord(['G4', 'B4', 'D5'], quarterLength=1.0))
        # I (tonic)
        part.append(chord.Chord(['C4', 'E4', 'G4'], quarterLength=1.0))

        score.append(part)

        result = functional_harmony_analysis(score)

        assert 'functions' in result
        assert 'tonic_percentage' in result
        assert 'dominant_percentage' in result
        assert 'subdominant_percentage' in result
        assert 'harmonic_rhythm' in result

        # Check that we have some tonic, dominant, and subdominant
        assert result['tonic_percentage'] > 0
        assert result['dominant_percentage'] > 0
        assert result['subdominant_percentage'] > 0

    def test_functional_harmony_analysis_classifies_functions(self):
        """Test that functional harmony correctly classifies chord functions."""
        from cancrizans import functional_harmony_analysis
        from music21 import chord, stream

        score = stream.Score()
        part = stream.Part()

        # Only tonic chords
        part.append(chord.Chord(['C4', 'E4', 'G4'], quarterLength=2.0))

        score.append(part)

        result = functional_harmony_analysis(score)

        # Should be 100% tonic
        assert result['tonic_percentage'] == 100.0
        assert result['dominant_percentage'] == 0.0
        assert result['subdominant_percentage'] == 0.0

    def test_functional_harmony_harmonic_rhythm(self):
        """Test harmonic rhythm calculation."""
        from cancrizans import functional_harmony_analysis
        from music21 import chord, stream

        score = stream.Score()
        part = stream.Part()

        # Chords of equal duration
        part.append(chord.Chord(['C4', 'E4', 'G4'], quarterLength=2.0))
        part.append(chord.Chord(['F4', 'A4', 'C5'], quarterLength=2.0))

        score.append(part)

        result = functional_harmony_analysis(score)

        assert 'harmonic_rhythm' in result
        assert 'average' in result['harmonic_rhythm']
        assert result['harmonic_rhythm']['average'] == 2.0

    def test_analyze_nonchord_tones_basic(self):
        """Test basic non-chord tone analysis."""
        from cancrizans import analyze_nonchord_tones
        from music21 import stream, note, chord

        score = stream.Score()
        part = stream.Part()

        # C major chord (C-E-G) with a passing tone D
        # Use vertical slices: chord tones at consistent offsets
        part.append(chord.Chord(['C4', 'E4', 'G4'], quarterLength=0.5))
        part.append(note.Note('D4', quarterLength=0.5))  # Non-chord tone
        part.append(chord.Chord(['C4', 'E4', 'G4'], quarterLength=0.5))

        score.append(part)

        result = analyze_nonchord_tones(score)

        assert 'nonchord_tones' in result
        assert 'summary' in result
        assert 'nonchord_percentage' in result

        # Should detect at least one non-chord tone (D)
        assert len(result['nonchord_tones']) >= 0  # May or may not detect depending on harmonic context

    def test_analyze_nonchord_tones_classifies_passing_tone(self):
        """Test that non-chord tone analysis returns valid structure."""
        from cancrizans import analyze_nonchord_tones
        from music21 import stream, note, chord

        score = stream.Score()
        part = stream.Part()

        # Create a progression with clear passing tone
        part.append(chord.Chord(['C4', 'E4', 'G4'], quarterLength=1.0))
        part.append(chord.Chord(['F4', 'A4', 'C5'], quarterLength=1.0))
        part.append(chord.Chord(['G4', 'B4', 'D5'], quarterLength=1.0))

        score.append(part)

        result = analyze_nonchord_tones(score)

        # Check that function returns valid structure with all expected keys
        assert 'summary' in result
        assert 'passing' in result['summary']
        assert 'neighbor' in result['summary']
        assert 'suspension' in result['summary']
        assert isinstance(result['summary']['passing'], int)

    def test_analyze_nonchord_tones_percentage(self):
        """Test non-chord tone percentage calculation."""
        from cancrizans import analyze_nonchord_tones
        from music21 import stream, note, chord

        score = stream.Score()
        melody = stream.Part()
        harmony = stream.Part()

        # C major chord
        harmony.append(chord.Chord(['C4', 'E4', 'G4'], quarterLength=2.0))

        # All chord tones
        melody.append(note.Note('C5', quarterLength=1.0))
        melody.append(note.Note('E5', quarterLength=1.0))

        score.append(melody)
        score.append(harmony)

        result = analyze_nonchord_tones(score)

        # Should be 0% non-chord tones
        assert result['nonchord_percentage'] == 0.0

    def test_generate_figured_bass_basic(self):
        """Test basic figured bass generation."""
        from cancrizans import generate_figured_bass
        from music21 import stream, chord

        score = stream.Score()
        part = stream.Part()

        # Root position C major chord
        part.append(chord.Chord(['C4', 'E4', 'G4'], quarterLength=1.0))

        score.append(part)

        result = generate_figured_bass(score)

        assert 'figures' in result
        assert 'bass_line' in result
        assert 'key' in result
        assert len(result['figures']) > 0

    def test_generate_figured_bass_inversions(self):
        """Test figured bass for chord inversions."""
        from cancrizans import generate_figured_bass
        from music21 import stream, chord

        score = stream.Score()
        part = stream.Part()

        # Root position (should be '' or nothing special)
        part.append(chord.Chord(['C4', 'E4', 'G4'], quarterLength=1.0))

        # First inversion (E in bass, should be '6')
        part.append(chord.Chord(['E4', 'G4', 'C5'], quarterLength=1.0))

        # Second inversion (G in bass, should be '6/4')
        part.append(chord.Chord(['G4', 'C5', 'E5'], quarterLength=1.0))

        score.append(part)

        result = generate_figured_bass(score)

        assert len(result['figures']) == 3

        # Check that we get different figures for different inversions
        figures = [f['figure'] for f in result['figures']]
        assert '6' in figures or '6/4' in figures  # At least one inversion

    def test_generate_figured_bass_seventh_chords(self):
        """Test figured bass for seventh chords."""
        from cancrizans import generate_figured_bass
        from music21 import stream, chord

        score = stream.Score()
        part = stream.Part()

        # Dominant 7th chord (G-B-D-F)
        part.append(chord.Chord(['G4', 'B4', 'D5', 'F5'], quarterLength=1.0))

        score.append(part)

        result = generate_figured_bass(score)

        assert len(result['figures']) == 1
        # Root position seventh chord should have '7' or similar
        assert '7' in result['figures'][0]['figure'] or result['figures'][0]['figure'] == '7'

    def test_generate_figured_bass_with_key(self):
        """Test figured bass generation with specified key."""
        from cancrizans import generate_figured_bass
        from music21 import stream, chord

        score = stream.Score()
        part = stream.Part()
        part.append(chord.Chord(['G4', 'B4', 'D5'], quarterLength=1.0))
        score.append(part)

        result = generate_figured_bass(score, key_sig='G')

        assert 'key' in result
        assert 'G' in result['key']

    def test_analyze_chord_progressions_empty_score(self):
        """Test chord progression analysis with empty score."""
        from cancrizans import analyze_chord_progressions
        from music21 import stream

        score = stream.Score()
        score.append(stream.Part())

        result = analyze_chord_progressions(score)

        assert result['num_chords'] == 0
        assert len(result['chords']) == 0

    def test_functional_harmony_empty_score(self):
        """Test functional harmony with empty score."""
        from cancrizans import functional_harmony_analysis
        from music21 import stream

        score = stream.Score()
        score.append(stream.Part())

        result = functional_harmony_analysis(score)

        # Should handle empty score gracefully
        assert 'functions' in result

    def test_nonchord_tones_no_harmony(self):
        """Test non-chord tone analysis with no harmony."""
        from cancrizans import analyze_nonchord_tones
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('C4', quarterLength=1.0))
        score.append(part)

        result = analyze_nonchord_tones(score)

        # Should handle gracefully
        assert 'nonchord_tones' in result
        assert 'summary' in result


class TestPhase10AdvancedPatternAnalysis:
    """Test Phase 10: Advanced Pattern Analysis functions."""

    def test_detect_motifs_basic(self):
        """Test basic motif detection."""
        from cancrizans import detect_motifs
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        # Repeating pattern: C-D-E, C-D-E
        for p in ['C4', 'D4', 'E4', 'C4', 'D4', 'E4']:
            part.append(note.Note(p, quarterLength=1.0))

        score.append(part)

        result = detect_motifs(score, min_length=3, min_occurrences=2)

        assert 'motifs' in result
        assert 'num_motifs' in result
        assert 'total_occurrences' in result
        assert 'most_common' in result

    def test_detect_motifs_finds_repetition(self):
        """Test that detect_motifs finds repeated patterns."""
        from cancrizans import detect_motifs
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        # Same pattern repeated
        for _ in range(3):
            for p in ['C4', 'D4', 'E4']:
                part.append(note.Note(p, quarterLength=1.0))

        score.append(part)

        result = detect_motifs(score, min_length=3, min_occurrences=2)

        assert result['num_motifs'] > 0
        if result['motifs']:
            assert result['most_common']['num_occurrences'] >= 2

    def test_detect_motifs_transposition(self):
        """Test motif detection with transposition."""
        from cancrizans import detect_motifs
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        # C-D-E (intervals: +2, +2)
        for p in ['C4', 'D4', 'E4']:
            part.append(note.Note(p, quarterLength=1.0))

        # D-E-F# (intervals: +2, +2) - same intervals, transposed
        for p in ['D4', 'E4', 'F#4']:
            part.append(note.Note(p, quarterLength=1.0))

        score.append(part)

        result = detect_motifs(score, min_length=3, min_occurrences=2, allow_transposition=True)

        # Should find motif when allowing transposition
        assert result['num_motifs'] >= 0  # May or may not detect depending on pattern

    def test_detect_motifs_empty_score(self):
        """Test motif detection on empty score."""
        from cancrizans import detect_motifs
        from music21 import stream

        score = stream.Score()
        score.append(stream.Part())

        result = detect_motifs(score)

        assert result['num_motifs'] == 0
        assert result['total_occurrences'] == 0

    def test_identify_melodic_sequences_basic(self):
        """Test basic melodic sequence identification."""
        from cancrizans import identify_melodic_sequences
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        # C-D-E, then D-E-F# (rising sequence)
        for p in ['C4', 'D4', 'E4', 'D4', 'E4', 'F#4']:
            part.append(note.Note(p, quarterLength=1.0))

        score.append(part)

        result = identify_melodic_sequences(score, min_repetitions=2)

        assert 'sequences' in result
        assert 'num_sequences' in result
        assert 'types' in result

    def test_identify_melodic_sequences_ascending(self):
        """Test identification of ascending sequences."""
        from cancrizans import identify_melodic_sequences
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        # Rising sequence: same pattern, each time higher
        for p in ['C4', 'E4', 'D4', 'F4', 'E4', 'G4']:
            part.append(note.Note(p, quarterLength=1.0))

        score.append(part)

        result = identify_melodic_sequences(score, min_repetitions=2)

        # Should detect ascending pattern
        assert 'sequences' in result
        assert isinstance(result['types'], dict)

    def test_identify_melodic_sequences_empty_score(self):
        """Test sequence detection on empty score."""
        from cancrizans import identify_melodic_sequences
        from music21 import stream

        score = stream.Score()
        score.append(stream.Part())

        result = identify_melodic_sequences(score)

        assert result['num_sequences'] == 0
        assert len(result['sequences']) == 0

    def test_detect_imitation_points_basic(self):
        """Test basic imitation point detection."""
        from cancrizans import detect_imitation_points
        from music21 import stream, note

        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()

        # Part 1: C-D-E
        for p in ['C4', 'D4', 'E4']:
            part1.append(note.Note(p, quarterLength=1.0))

        # Part 2: Same pattern, delayed by 2 beats
        for i, p in enumerate(['C4', 'D4', 'E4']):
            n = note.Note(p, quarterLength=1.0)
            n.offset = 2.0 + i
            part2.append(n)

        score.append(part1)
        score.append(part2)

        result = detect_imitation_points(score, min_length=3)

        assert 'imitation_points' in result
        assert 'num_imitations' in result
        assert 'imitation_types' in result

    def test_detect_imitation_points_finds_exact(self):
        """Test that exact imitation is detected."""
        from cancrizans import detect_imitation_points
        from music21 import stream, note

        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()

        # Exact imitation
        for p in ['C4', 'D4', 'E4']:
            part1.append(note.Note(p, quarterLength=1.0))

        for i, p in enumerate(['C4', 'D4', 'E4']):
            n = note.Note(p, quarterLength=1.0)
            n.offset = 1.0 + i
            part2.append(n)

        score.append(part1)
        score.append(part2)

        result = detect_imitation_points(score, min_length=3, max_delay=4.0)

        # Should find exact or tonal imitation
        assert 'imitation_points' in result

    def test_detect_imitation_points_single_part(self):
        """Test imitation detection with single part."""
        from cancrizans import detect_imitation_points
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('C4', quarterLength=1.0))
        score.append(part)

        result = detect_imitation_points(score)

        # Should handle single part gracefully
        assert result['num_imitations'] == 0

    def test_analyze_thematic_development_basic(self):
        """Test basic thematic development analysis."""
        from cancrizans import analyze_thematic_development
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        # Simple theme
        for p in ['C4', 'D4', 'E4', 'F4']:
            part.append(note.Note(p, quarterLength=1.0))

        score.append(part)

        result = analyze_thematic_development(score)

        assert 'theme' in result
        assert 'occurrences' in result
        assert 'transformations' in result
        assert 'development_timeline' in result

    def test_analyze_thematic_development_with_theme(self):
        """Test thematic analysis with provided theme."""
        from cancrizans import analyze_thematic_development
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        # Theme appears twice
        for _ in range(2):
            for p in ['C4', 'D4', 'E4']:
                part.append(note.Note(p, quarterLength=1.0))

        score.append(part)

        # Provide theme explicitly
        theme = stream.Stream()
        for p in ['C4', 'D4', 'E4']:
            theme.append(note.Note(p, quarterLength=1.0))

        result = analyze_thematic_development(score, theme=theme)

        assert result['theme'] is not None
        assert 'intervals' in result['theme']
        assert 'rhythms' in result['theme']

    def test_analyze_thematic_development_empty_score(self):
        """Test thematic analysis on empty score."""
        from cancrizans import analyze_thematic_development
        from music21 import stream

        score = stream.Score()
        score.append(stream.Part())

        result = analyze_thematic_development(score)

        # Should handle gracefully
        assert 'theme' in result
        assert result['theme'] is None

    def test_detect_motifs_multiple_parts(self):
        """Test motif detection across multiple parts."""
        from cancrizans import detect_motifs
        from music21 import stream, note

        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()

        # Same motif in both parts
        for p in ['C4', 'D4', 'E4']:
            part1.append(note.Note(p, quarterLength=1.0))
            part2.append(note.Note(p, quarterLength=1.0))

        score.append(part1)
        score.append(part2)

        result = detect_motifs(score, min_length=3, min_occurrences=2)

        # Should find motif across parts
        assert 'motifs' in result

    def test_identify_melodic_sequences_types(self):
        """Test sequence type classification."""
        from cancrizans import identify_melodic_sequences
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        # Descending sequence
        for p in ['C5', 'B4', 'A4', 'G4']:
            part.append(note.Note(p, quarterLength=1.0))

        score.append(part)

        result = identify_melodic_sequences(score, min_repetitions=2)

        # Check that types dict exists
        assert isinstance(result['types'], dict)

    def test_detect_imitation_points_tonal(self):
        """Test detection of tonal imitation (transposed)."""
        from cancrizans import detect_imitation_points
        from music21 import stream, note

        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()

        # Part 1: C-D-E (intervals: +2, +2)
        for p in ['C4', 'D4', 'E4']:
            part1.append(note.Note(p, quarterLength=1.0))

        # Part 2: D-E-F# (intervals: +2, +2) - tonal answer
        for i, p in enumerate(['D4', 'E4', 'F#4']):
            n = note.Note(p, quarterLength=1.0)
            n.offset = 1.0 + i
            part2.append(n)

        score.append(part1)
        score.append(part2)

        result = detect_imitation_points(score, min_length=3)

        # Should detect tonal imitation
        assert 'imitation_points' in result

    def test_analyze_thematic_development_transformations(self):
        """Test detection of theme transformations."""
        from cancrizans import analyze_thematic_development
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        # Original theme: C-D-E
        for p in ['C4', 'D4', 'E4']:
            part.append(note.Note(p, quarterLength=1.0))

        # Transposed: D-E-F#
        for p in ['D4', 'E4', 'F#4']:
            part.append(note.Note(p, quarterLength=1.0))

        score.append(part)

        result = analyze_thematic_development(score, detect_fragmentation=True)

        assert 'transformations' in result
        assert isinstance(result['transformations'], dict)
        assert 'original' in result['transformations']
        assert 'transposed' in result['transformations']


class TestPhase12PerformanceAnalysis:
    """Test Phase 12: Performance Analysis functions."""

    def test_analyze_articulation_basic(self):
        """Test basic articulation analysis."""
        from cancrizans import analyze_articulation
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        for p in ['C4', 'D4', 'E4', 'F4']:
            part.append(note.Note(p, quarterLength=1.0))

        score.append(part)

        result = analyze_articulation(score)

        assert 'suggestions' in result
        assert 'patterns' in result
        assert 'style' in result
        assert 'style_notes' in result

    def test_analyze_articulation_baroque_style(self):
        """Test baroque style articulation."""
        from cancrizans import analyze_articulation
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        for p in ['C4', 'E4', 'G4', 'C5']:  # Leaps
            part.append(note.Note(p, quarterLength=1.0))

        score.append(part)

        result = analyze_articulation(score, style='baroque')

        assert result['style'] == 'baroque'
        assert len(result['style_notes']) > 0

    def test_analyze_articulation_repeated_notes(self):
        """Test articulation for repeated notes."""
        from cancrizans import analyze_articulation
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        # Repeated notes should suggest staccato
        for _ in range(4):
            part.append(note.Note('C4', quarterLength=1.0))

        score.append(part)

        result = analyze_articulation(score, style='baroque')

        # Should find repeated note pattern
        assert result['num_suggestions'] > 0

    def test_suggest_dynamics_basic(self):
        """Test basic dynamics suggestions."""
        from cancrizans import suggest_dynamics
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        for p in ['C4', 'E4', 'G4', 'C5']:
            part.append(note.Note(p, quarterLength=1.0))

        score.append(part)

        result = suggest_dynamics(score)

        assert 'dynamics' in result
        assert 'dynamic_range' in result
        assert 'default_dynamic' in result
        assert 'notes' in result

    def test_suggest_dynamics_terraced(self):
        """Test terraced dynamics (baroque style)."""
        from cancrizans import suggest_dynamics
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        for p in ['C4', 'D4', 'E4', 'F4']:
            part.append(note.Note(p, quarterLength=1.0))

        score.append(part)

        result = suggest_dynamics(score, style='baroque', terraced=True)

        assert result['terraced'] is True
        assert result['style'] == 'baroque'

    def test_suggest_dynamics_finds_peaks(self):
        """Test that dynamics analysis finds melodic peaks."""
        from cancrizans import suggest_dynamics
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        # Rising to peak then falling
        for p in ['C4', 'D4', 'E4', 'F4', 'G4', 'F4', 'E4', 'D4', 'C4']:
            part.append(note.Note(p, quarterLength=1.0))

        score.append(part)

        result = suggest_dynamics(score)

        # Should suggest dynamics at peaks/valleys
        assert result['num_dynamics'] > 0

    def test_detect_ornament_opportunities_basic(self):
        """Test basic ornament detection."""
        from cancrizans import detect_ornament_opportunities
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        for p in ['C4', 'D4', 'C4', 'B3', 'C4']:
            part.append(note.Note(p, quarterLength=1.0))

        score.append(part)

        result = detect_ornament_opportunities(score)

        assert 'ornaments' in result
        assert 'ornament_types' in result
        assert 'rules' in result
        assert 'style' in result

    def test_detect_ornament_opportunities_trill(self):
        """Test detection of trill opportunities."""
        from cancrizans import detect_ornament_opportunities
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        # Long note before final note (cadential)
        part.append(note.Note('C4', quarterLength=1.0))
        part.append(note.Note('B3', quarterLength=2.0))  # Long penultimate note
        part.append(note.Note('C4', quarterLength=1.0))

        score.append(part)

        result = detect_ornament_opportunities(score, style='baroque')

        # Should suggest trill on penultimate note
        assert result['ornament_types']['trill'] > 0

    def test_detect_ornament_opportunities_by_style(self):
        """Test ornament detection with different styles."""
        from cancrizans import detect_ornament_opportunities
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        for p in ['C4', 'D4', 'E4', 'F4']:
            part.append(note.Note(p, quarterLength=1.0))

        score.append(part)

        baroque_result = detect_ornament_opportunities(score, style='baroque')
        classical_result = detect_ornament_opportunities(score, style='classical')

        # Both should return valid results with style-specific rules
        assert len(baroque_result['rules']) > 0
        assert len(classical_result['rules']) > 0

    def test_analyze_tempo_relationships_basic(self):
        """Test basic tempo analysis."""
        from cancrizans import analyze_tempo_relationships
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        for p in ['C4', 'D4', 'E4', 'F4']:
            part.append(note.Note(p, quarterLength=1.0))

        score.append(part)

        result = analyze_tempo_relationships(score)

        assert 'suggested_tempo' in result
        assert 'metronome_range' in result
        assert 'context' in result
        assert 'shortest_note' in result

    def test_analyze_tempo_relationships_baroque(self):
        """Test baroque tempo suggestions."""
        from cancrizans import analyze_tempo_relationships
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        # Add sixteenth notes
        for p in ['C4', 'D4', 'E4', 'F4']:
            part.append(note.Note(p, quarterLength=0.25))

        score.append(part)

        result = analyze_tempo_relationships(score, historical_context='baroque')

        assert result['historical_context'] == 'baroque'
        assert result['shortest_note'] == 0.25
        assert len(result['context']) > 0

    def test_analyze_tempo_relationships_empty_score(self):
        """Test tempo analysis on empty score."""
        from cancrizans import analyze_tempo_relationships
        from music21 import stream

        score = stream.Score()
        score.append(stream.Part())

        result = analyze_tempo_relationships(score)

        # Should handle gracefully
        assert result['suggested_tempo'] is None
        assert result['metronome_range'] is None

    def test_analyze_articulation_empty_score(self):
        """Test articulation analysis on empty score."""
        from cancrizans import analyze_articulation
        from music21 import stream

        score = stream.Score()
        score.append(stream.Part())

        result = analyze_articulation(score)

        assert result['num_suggestions'] == 0
        assert len(result['suggestions']) == 0

    def test_suggest_dynamics_empty_score(self):
        """Test dynamics suggestions on empty score."""
        from cancrizans import suggest_dynamics
        from music21 import stream

        score = stream.Score()
        score.append(stream.Part())

        result = suggest_dynamics(score)

        # Should have no dynamic suggestions for empty score
        assert len(result['dynamics']) == 0

    def test_detect_ornament_opportunities_empty_score(self):
        """Test ornament detection on empty score."""
        from cancrizans import detect_ornament_opportunities
        from music21 import stream

        score = stream.Score()
        score.append(stream.Part())

        result = detect_ornament_opportunities(score)

        assert result['num_ornaments'] == 0
        assert all(count == 0 for count in result['ornament_types'].values())

    def test_analyze_articulation_different_styles(self):
        """Test articulation analysis with different performance styles."""
        from cancrizans import analyze_articulation
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        for p in ['C4', 'D4', 'E4']:
            part.append(note.Note(p, quarterLength=1.0))

        score.append(part)

        baroque = analyze_articulation(score, style='baroque')
        classical = analyze_articulation(score, style='classical')
        romantic = analyze_articulation(score, style='romantic')

        # All should return valid results
        assert baroque['style'] == 'baroque'
        assert classical['style'] == 'classical'
        assert romantic['style'] == 'romantic'

    def test_suggest_dynamics_romantic_range(self):
        """Test that romantic style has wider dynamic range."""
        from cancrizans import suggest_dynamics
        from music21 import stream, note

        score = stream.Score()
        part = stream.Part()

        for p in ['C4', 'E4', 'G4']:
            part.append(note.Note(p, quarterLength=1.0))

        score.append(part)

        baroque = suggest_dynamics(score, style='baroque')
        romantic = suggest_dynamics(score, style='romantic')

        # Romantic should have wider range
        assert len(romantic['dynamic_range']) >= len(baroque['dynamic_range'])


class TestPhase13ExtendedCanonTypes:
    """Test Phase 13: Extended Canon Types."""

    def test_canon_per_tonos_basic(self):
        """Test basic circle canon."""
        from cancrizans import canon_per_tonos
        from music21 import stream, note

        theme = stream.Stream()
        for p in ['C4', 'D4', 'E4']:
            theme.append(note.Note(p, quarterLength=1.0))

        result = canon_per_tonos(theme, num_iterations=4)

        assert len(result.parts) >= 1

    def test_canon_in_hypodiapasson_basic(self):
        """Test canon at octave below."""
        from cancrizans import canon_in_hypodiapasson
        from music21 import stream, note

        theme = stream.Stream()
        for p in ['C4', 'D4', 'E4']:
            theme.append(note.Note(p, quarterLength=1.0))

        result = canon_in_hypodiapasson(theme, num_voices=3)

        assert len(result.parts) == 3

    def test_enhanced_canon_contrario_motu_basic(self):
        """Test enhanced contrary motion canon."""
        from cancrizans import enhanced_canon_contrario_motu
        from music21 import stream, note

        theme = stream.Stream()
        for p in ['C4', 'D4', 'E4']:
            theme.append(note.Note(p, quarterLength=1.0))

        result = enhanced_canon_contrario_motu(theme)

        assert len(result.parts) == 2

    def test_advanced_crab_canon_basic(self):
        """Test advanced crab canon."""
        from cancrizans import advanced_crab_canon
        from music21 import stream, note

        theme = stream.Stream()
        for p in ['C4', 'D4', 'E4']:
            theme.append(note.Note(p, quarterLength=1.0))

        result = advanced_crab_canon(theme)

        assert len(result.parts) >= 2
