"""Tests for the io module."""

import pytest
from pathlib import Path
import tempfile
from music21 import stream, note
from cancrizans.io import to_midi, to_musicxml, load_score
from cancrizans.generator import CanonGenerator


class TestMIDIIO:
    """Test MIDI input/output."""

    def test_to_midi_creates_file(self):
        """Test that MIDI file is created."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        with tempfile.TemporaryDirectory() as tmpdir:
            midi_path = Path(tmpdir) / 'test.mid'
            result = to_midi(canon, midi_path)

            assert midi_path.exists()
            assert result == midi_path

    def test_to_midi_and_load_roundtrip(self):
        """Test saving and loading MIDI."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        with tempfile.TemporaryDirectory() as tmpdir:
            midi_path = Path(tmpdir) / 'test.mid'
            to_midi(canon, midi_path)

            loaded = load_score(midi_path)

            assert isinstance(loaded, stream.Score)
            assert len(loaded.parts) == len(canon.parts)


class TestMusicXMLIO:
    """Test MusicXML input/output."""

    def test_to_musicxml_creates_file(self):
        """Test that MusicXML file is created."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        with tempfile.TemporaryDirectory() as tmpdir:
            xml_path = Path(tmpdir) / 'test.musicxml'
            result = to_musicxml(canon, xml_path)

            assert xml_path.exists()
            assert result == xml_path

    def test_to_musicxml_and_load_roundtrip(self):
        """Test saving and loading MusicXML."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        with tempfile.TemporaryDirectory() as tmpdir:
            xml_path = Path(tmpdir) / 'test.musicxml'
            to_musicxml(canon, xml_path)

            loaded = load_score(xml_path)

            assert isinstance(loaded, stream.Score)
            assert len(loaded.parts) == len(canon.parts)


class TestLoadScore:
    """Test score loading."""

    def test_load_score_midi(self):
        """Test loading MIDI file."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        with tempfile.TemporaryDirectory() as tmpdir:
            midi_path = Path(tmpdir) / 'test.mid'
            to_midi(canon, midi_path)

            loaded = load_score(midi_path)
            assert isinstance(loaded, stream.Score)

    def test_load_score_musicxml(self):
        """Test loading MusicXML file."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        with tempfile.TemporaryDirectory() as tmpdir:
            xml_path = Path(tmpdir) / 'test.musicxml'
            to_musicxml(canon, xml_path)

            loaded = load_score(xml_path)
            assert isinstance(loaded, stream.Score)

    def test_load_score_nonexistent_file(self):
        """Test loading nonexistent file raises error."""
        with pytest.raises(Exception):
            load_score(Path('/nonexistent/file.mid'))
