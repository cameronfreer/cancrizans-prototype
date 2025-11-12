"""Tests for the io module."""

import pytest
from pathlib import Path
import tempfile
from music21 import stream, note
from cancrizans.io import to_midi, to_musicxml, to_lilypond, to_abc, load_score
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


class TestLilyPondIO:
    """Test LilyPond export."""

    def test_to_lilypond_creates_file(self):
        """Test that LilyPond file is created."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        with tempfile.TemporaryDirectory() as tmpdir:
            ly_path = Path(tmpdir) / 'test.ly'
            result = to_lilypond(canon, ly_path)

            assert ly_path.exists()
            assert result == ly_path
            assert ly_path.stat().st_size > 0

    def test_lilypond_content_structure(self):
        """Test that LilyPond content has correct structure."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        with tempfile.TemporaryDirectory() as tmpdir:
            ly_path = Path(tmpdir) / 'test.ly'
            to_lilypond(canon, ly_path)

            content = ly_path.read_text()

            # Check for essential LilyPond elements
            assert '\\version' in content
            assert '\\header' in content
            assert '\\score' in content
            assert '\\new Staff' in content

    def test_lilypond_contains_notes(self):
        """Test that LilyPond file contains note data."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major', 4, 4)

        with tempfile.TemporaryDirectory() as tmpdir:
            ly_path = Path(tmpdir) / 'test.ly'
            to_lilypond(canon, ly_path)

            content = ly_path.read_text()

            # Should contain notes (c, d, e, f, etc.)
            assert any(note in content for note in ["c'", "d'", "e'", "f'"])


class TestABCIO:
    """Test ABC notation export."""

    def test_to_abc_creates_file(self):
        """Test that ABC file is created."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        with tempfile.TemporaryDirectory() as tmpdir:
            abc_path = Path(tmpdir) / 'test.abc'
            result = to_abc(canon, abc_path)

            assert abc_path.exists()
            assert result == abc_path
            assert abc_path.stat().st_size > 0

    def test_abc_content_structure(self):
        """Test that ABC content has correct structure."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        with tempfile.TemporaryDirectory() as tmpdir:
            abc_path = Path(tmpdir) / 'test.abc'
            to_abc(canon, abc_path)

            content = abc_path.read_text()

            # Check for essential ABC elements
            assert 'X:' in content  # Reference number
            assert 'T:' in content  # Title
            assert 'M:' in content  # Meter
            assert 'K:' in content  # Key

    def test_abc_contains_notes(self):
        """Test that ABC file contains note data."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major', 4, 4)

        with tempfile.TemporaryDirectory() as tmpdir:
            abc_path = Path(tmpdir) / 'test.abc'
            to_abc(canon, abc_path)

            content = abc_path.read_text()

            # Should contain notes (C, D, E, F, etc.)
            assert any(note in content for note in ['C', 'D', 'E', 'F'])

    def test_abc_multiple_voices(self):
        """Test that ABC handles multiple voices."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        with tempfile.TemporaryDirectory() as tmpdir:
            abc_path = Path(tmpdir) / 'test.abc'
            to_abc(canon, abc_path)

            content = abc_path.read_text()

            # Should have voice markers for multiple parts
            if len(canon.parts) > 1:
                assert 'V:2' in content
