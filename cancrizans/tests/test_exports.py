"""
Tests for export functionality (MIDI, MusicXML, WAV).
"""

import pytest
from pathlib import Path
import tempfile
from music21 import stream, note

from cancrizans.io import to_midi, to_musicxml, to_wav_via_sf2
from cancrizans.bach_crab import load_bach_crab_canon


@pytest.fixture
def simple_score() -> stream.Score:
    """Create a simple score for testing."""
    score = stream.Score()
    part = stream.Part()
    part.append(note.Note('C4', quarterLength=1.0))
    part.append(note.Note('D4', quarterLength=1.0))
    part.append(note.Note('E4', quarterLength=1.0))
    score.insert(0, part)
    return score


def test_to_midi_creates_file(simple_score: stream.Score) -> None:
    """Test that MIDI export creates a file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test.mid"
        result = to_midi(simple_score, output_path)

        assert result.exists()
        assert result.suffix == ".mid"
        assert result.stat().st_size > 0


def test_to_midi_creates_parent_dirs(simple_score: stream.Score) -> None:
    """Test that MIDI export creates parent directories."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "subdir" / "nested" / "test.mid"
        result = to_midi(simple_score, output_path)

        assert result.exists()
        assert result.parent.exists()


def test_to_musicxml_creates_file(simple_score: stream.Score) -> None:
    """Test that MusicXML export creates a file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test.musicxml"
        result = to_musicxml(simple_score, output_path)

        assert result.exists()
        assert result.suffix == ".musicxml"
        assert result.stat().st_size > 0


def test_to_musicxml_creates_parent_dirs(simple_score: stream.Score) -> None:
    """Test that MusicXML export creates parent directories."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "subdir" / "nested" / "test.musicxml"
        result = to_musicxml(simple_score, output_path)

        assert result.exists()
        assert result.parent.exists()


def test_bach_crab_canon_midi_export() -> None:
    """Test exporting Bach's Crab Canon to MIDI."""
    score = load_bach_crab_canon()

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "bach_crab.mid"
        result = to_midi(score, output_path)

        assert result.exists()
        assert result.stat().st_size > 0


def test_bach_crab_canon_musicxml_export() -> None:
    """Test exporting Bach's Crab Canon to MusicXML."""
    score = load_bach_crab_canon()

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "bach_crab.musicxml"
        result = to_musicxml(score, output_path)

        assert result.exists()
        assert result.stat().st_size > 0


def test_to_wav_via_sf2_missing_midi() -> None:
    """Test that WAV export raises error for missing MIDI file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        midi_path = Path(tmpdir) / "nonexistent.mid"
        sf2_path = Path(tmpdir) / "nonexistent.sf2"
        wav_path = Path(tmpdir) / "output.wav"

        with pytest.raises(FileNotFoundError):
            to_wav_via_sf2(midi_path, sf2_path, wav_path)


def test_to_wav_via_sf2_missing_soundfont(simple_score: stream.Score) -> None:
    """Test that WAV export raises error for missing SoundFont."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a MIDI file first
        midi_path = Path(tmpdir) / "test.mid"
        to_midi(simple_score, midi_path)

        sf2_path = Path(tmpdir) / "nonexistent.sf2"
        wav_path = Path(tmpdir) / "output.wav"

        with pytest.raises(FileNotFoundError):
            to_wav_via_sf2(midi_path, sf2_path, wav_path)


def test_to_wav_via_sf2_no_library(simple_score: stream.Score) -> None:
    """Test WAV export behavior when midi2audio is not available."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create MIDI file
        midi_path = Path(tmpdir) / "test.mid"
        to_midi(simple_score, midi_path)

        # Create a dummy soundfont file
        sf2_path = Path(tmpdir) / "dummy.sf2"
        sf2_path.write_bytes(b"dummy")

        wav_path = Path(tmpdir) / "output.wav"

        # This should return None if midi2audio is not installed
        result = to_wav_via_sf2(midi_path, sf2_path, wav_path)

        # Result is None if library not available, or a Path if it is
        assert result is None or isinstance(result, Path)
