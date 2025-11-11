"""
Tests for retrograde and inversion transformations.
"""

import pytest
from music21 import stream, note, pitch

from cancrizans.canon import retrograde, invert


def test_retrograde_simple_sequence() -> None:
    """Test retrograde on a simple list."""
    seq = [1, 2, 3, 4, 5]
    result = retrograde(seq)
    assert result == [5, 4, 3, 2, 1]


def test_retrograde_stream() -> None:
    """Test retrograde on a music21 Stream."""
    s = stream.Stream()
    s.append(note.Note('C4', quarterLength=1.0))
    s.append(note.Note('D4', quarterLength=1.0))
    s.append(note.Note('E4', quarterLength=1.0))

    result = retrograde(s)

    notes = list(result.flatten().notes)
    assert len(notes) == 3

    # Check pitches are in reverse order
    pitches = [n.pitch.nameWithOctave for n in notes]
    assert pitches == ['E4', 'D4', 'C4']


def test_retrograde_preserves_durations() -> None:
    """Test that retrograde preserves note durations."""
    s = stream.Stream()
    s.append(note.Note('C4', quarterLength=1.0))
    s.append(note.Note('D4', quarterLength=2.0))
    s.append(note.Note('E4', quarterLength=0.5))

    result = retrograde(s)

    notes = list(result.flatten().notes)
    durations = [n.quarterLength for n in notes]

    # Durations should be preserved (just reversed)
    assert durations == [0.5, 2.0, 1.0]


def test_retrograde_round_trip() -> None:
    """Test that applying retrograde twice returns to original."""
    s = stream.Stream()
    s.append(note.Note('C4', quarterLength=1.0))
    s.append(note.Note('D4', quarterLength=1.0))
    s.append(note.Note('E4', quarterLength=1.0))
    s.append(note.Note('F4', quarterLength=1.0))

    # Apply retrograde twice
    result = retrograde(retrograde(s))

    notes = list(result.flatten().notes)
    original_notes = list(s.flatten().notes)

    assert len(notes) == len(original_notes)

    # Check pitches match
    for n1, n2 in zip(notes, original_notes):
        assert n1.pitch.midi == n2.pitch.midi
        assert n1.quarterLength == n2.quarterLength


def test_invert_simple() -> None:
    """Test pitch inversion around C4."""
    s = stream.Stream()
    s.append(note.Note('C4', quarterLength=1.0))  # 0 semitones from axis
    s.append(note.Note('D4', quarterLength=1.0))  # +2 semitones
    s.append(note.Note('E4', quarterLength=1.0))  # +4 semitones

    result = invert(s, 'C4')

    notes = list(result.flatten().notes)
    assert len(notes) == 3

    # C4 inverts to C4 (on axis)
    assert notes[0].pitch.nameWithOctave == 'C4'

    # D4 (+2) inverts to Bb3 (-2)
    assert notes[1].pitch.midi == pitch.Pitch('C4').midi - 2

    # E4 (+4) inverts to Ab3 (-4)
    assert notes[2].pitch.midi == pitch.Pitch('C4').midi - 4


def test_invert_preserves_durations() -> None:
    """Test that inversion preserves note durations."""
    s = stream.Stream()
    s.append(note.Note('C4', quarterLength=1.0))
    s.append(note.Note('D4', quarterLength=2.0))
    s.append(note.Note('E4', quarterLength=0.5))

    result = invert(s, 'C4')

    notes = list(result.flatten().notes)
    durations = [n.quarterLength for n in notes]

    assert durations == [1.0, 2.0, 0.5]


def test_invert_round_trip() -> None:
    """Test that applying inversion twice returns to original."""
    s = stream.Stream()
    s.append(note.Note('C4', quarterLength=1.0))
    s.append(note.Note('D4', quarterLength=1.0))
    s.append(note.Note('E4', quarterLength=1.0))

    # Apply inversion twice around the same axis
    result = invert(invert(s, 'D4'), 'D4')

    notes = list(result.flatten().notes)
    original_notes = list(s.flatten().notes)

    assert len(notes) == len(original_notes)

    # Check pitches match (within 1 semitone for rounding)
    for n1, n2 in zip(notes, original_notes):
        assert abs(n1.pitch.midi - n2.pitch.midi) <= 1


def test_invert_with_different_axes() -> None:
    """Test inversion around different axis pitches."""
    s = stream.Stream()
    s.append(note.Note('C4', quarterLength=1.0))

    # Invert around C4
    result_c = invert(s, 'C4')
    notes_c = list(result_c.flatten().notes)
    assert notes_c[0].pitch.nameWithOctave == 'C4'

    # Invert around D4
    result_d = invert(s, 'D4')
    notes_d = list(result_d.flatten().notes)
    # C4 is 2 semitones below D4, so inverted it's 2 above: E4
    assert notes_d[0].pitch.midi == pitch.Pitch('D4').midi + 2
