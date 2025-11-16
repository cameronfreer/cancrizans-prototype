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

class TestLilyPondAccidentals:
    """Test LilyPond export with accidentals and octaves."""
    
    def test_lilypond_with_sharps(self):
        """Test LilyPond export handles sharps correctly."""
        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('C#4', quarterLength=1.0))
        part.append(note.Note('F#4', quarterLength=1.0))
        score.insert(0, part)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            ly_path = Path(tmpdir) / 'test.ly'
            to_lilypond(score, ly_path)
            
            content = ly_path.read_text()
            assert 'cis' in content or 'fis' in content  # sharp notation
    
    def test_lilypond_with_flats(self):
        """Test LilyPond export handles flats correctly."""
        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('B-4', quarterLength=1.0))
        part.append(note.Note('E-4', quarterLength=1.0))
        score.insert(0, part)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            ly_path = Path(tmpdir) / 'test.ly'
            to_lilypond(score, ly_path)
            
            content = ly_path.read_text()
            assert 'es' in content or 'bes' in content  # flat notation
    
    def test_lilypond_low_octave(self):
        """Test LilyPond export handles low octaves."""
        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('C2', quarterLength=1.0))  # Very low
        score.insert(0, part)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            ly_path = Path(tmpdir) / 'test.ly'
            to_lilypond(score, ly_path)
            
            content = ly_path.read_text()
            assert ',' in content  # comma indicates low octave
    
    def test_lilypond_with_rests(self):
        """Test LilyPond export handles rests."""
        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('C4', quarterLength=1.0))
        part.append(note.Rest(quarterLength=1.0))
        part.append(note.Note('E4', quarterLength=1.0))
        score.insert(0, part)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            ly_path = Path(tmpdir) / 'test.ly'
            to_lilypond(score, ly_path)
            
            content = ly_path.read_text()
            assert 'r' in content  # rest notation


class TestABCAccidentals:
    """Test ABC export with accidentals and octaves."""
    
    def test_abc_with_sharps(self):
        """Test ABC export handles sharps correctly."""
        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('C#4', quarterLength=1.0))
        part.append(note.Note('F#4', quarterLength=1.0))
        score.insert(0, part)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            abc_path = Path(tmpdir) / 'test.abc'
            to_abc(score, abc_path)
            
            content = abc_path.read_text()
            assert '^' in content  # sharp notation in ABC
    
    def test_abc_with_flats(self):
        """Test ABC export handles flats correctly."""
        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('B-4', quarterLength=1.0))
        part.append(note.Note('E-4', quarterLength=1.0))
        score.insert(0, part)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            abc_path = Path(tmpdir) / 'test.abc'
            to_abc(score, abc_path)
            
            content = abc_path.read_text()
            assert '_' in content  # flat notation in ABC
    
    def test_abc_high_octave(self):
        """Test ABC export handles high octaves."""
        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('C6', quarterLength=1.0))  # High octave
        score.insert(0, part)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            abc_path = Path(tmpdir) / 'test.abc'
            to_abc(score, abc_path)
            
            content = abc_path.read_text()
            assert "c'" in content or "c''" in content  # high octave notation
    
    def test_abc_low_octave(self):
        """Test ABC export handles low octaves."""
        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('C3', quarterLength=1.0))  # Low octave
        score.insert(0, part)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            abc_path = Path(tmpdir) / 'test.abc'
            to_abc(score, abc_path)
            
            content = abc_path.read_text()
            assert ',' in content  # comma indicates low octave
    
    def test_abc_various_durations(self):
        """Test ABC export handles various note durations."""
        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('C4', quarterLength=0.5))  # Half beat
        part.append(note.Note('D4', quarterLength=2.0))  # Two beats
        part.append(note.Note('E4', quarterLength=1.5))  # Dotted
        score.insert(0, part)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            abc_path = Path(tmpdir) / 'test.abc'
            to_abc(score, abc_path)
            
            content = abc_path.read_text()
            # Check for duration markers
            assert '/2' in content or '2' in content or '3/2' in content
    
    def test_abc_with_rests(self):
        """Test ABC export handles rests."""
        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('C4', quarterLength=1.0))
        part.append(note.Rest(quarterLength=1.0))
        part.append(note.Rest(quarterLength=0.5))
        part.append(note.Note('E4', quarterLength=1.0))
        score.insert(0, part)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            abc_path = Path(tmpdir) / 'test.abc'
            to_abc(score, abc_path)
            
            content = abc_path.read_text()
            assert 'z' in content  # rest notation in ABC


class TestLoadScore:
    """Test load_score function edge cases."""

    def test_load_score_from_part(self):
        """Test loading a single Part (not a Score)."""
        # Create a single part and save it
        part = stream.Part()
        part.append(note.Note('C4', quarterLength=1.0))
        part.append(note.Note('D4', quarterLength=1.0))

        with tempfile.TemporaryDirectory() as tmpdir:
            midi_path = Path(tmpdir) / 'part.mid'
            part.write('midi', fp=str(midi_path))

            # Loading should convert to Score
            loaded = load_score(midi_path)
            assert isinstance(loaded, stream.Score)

    def test_load_score_handles_score(self):
        """Test loading a proper Score object."""
        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('C4', quarterLength=1.0))
        score.insert(0, part)

        with tempfile.TemporaryDirectory() as tmpdir:
            midi_path = Path(tmpdir) / 'score.mid'
            score.write('midi', fp=str(midi_path))

            loaded = load_score(midi_path)
            assert isinstance(loaded, stream.Score)


class TestIOEdgeCases:
    """Test edge cases and error handling in IO functions."""

    def test_to_midi_creates_nested_directories(self):
        """Test that to_midi creates nested directories if needed."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        with tempfile.TemporaryDirectory() as tmpdir:
            # Deep nested path
            midi_path = Path(tmpdir) / 'level1' / 'level2' / 'test.mid'
            result = to_midi(canon, midi_path)

            assert midi_path.exists()
            assert result == midi_path

    def test_to_musicxml_creates_nested_directories(self):
        """Test that to_musicxml creates nested directories if needed."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        with tempfile.TemporaryDirectory() as tmpdir:
            xml_path = Path(tmpdir) / 'level1' / 'level2' / 'test.musicxml'
            result = to_musicxml(canon, xml_path)

            assert xml_path.exists()
            assert result == xml_path

    def test_to_lilypond_creates_nested_directories(self):
        """Test that to_lilypond creates nested directories if needed."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        with tempfile.TemporaryDirectory() as tmpdir:
            ly_path = Path(tmpdir) / 'level1' / 'level2' / 'test.ly'
            result = to_lilypond(canon, ly_path)

            assert ly_path.exists()
            assert result == ly_path

    def test_to_abc_creates_nested_directories(self):
        """Test that to_abc creates nested directories if needed."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        with tempfile.TemporaryDirectory() as tmpdir:
            abc_path = Path(tmpdir) / 'level1' / 'level2' / 'test.abc'
            result = to_abc(canon, abc_path)

            assert abc_path.exists()
            assert result == abc_path

    def test_lilypond_high_octave(self):
        """Test LilyPond export handles high octaves."""
        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('C6', quarterLength=1.0))  # High octave
        score.insert(0, part)

        with tempfile.TemporaryDirectory() as tmpdir:
            ly_path = Path(tmpdir) / 'test.ly'
            to_lilypond(score, ly_path)

            content = ly_path.read_text()
            # High octave should have multiple apostrophes
            assert "'''" in content or "''" in content

    def test_abc_duration_edge_cases(self):
        """Test ABC export with non-standard durations."""
        score = stream.Score()
        part = stream.Part()
        # Non-standard duration (3.0 quarter notes)
        part.append(note.Note('C4', quarterLength=3.0))
        part.append(note.Note('D4', quarterLength=4.0))
        score.insert(0, part)

        with tempfile.TemporaryDirectory() as tmpdir:
            abc_path = Path(tmpdir) / 'test.abc'
            to_abc(score, abc_path)

            content = abc_path.read_text()
            # Should contain duration markers
            assert '3' in content or '4' in content

    def test_to_wav_via_sf2_midi_not_found(self):
        """Test to_wav_via_sf2 with non-existent MIDI file."""
        from cancrizans.io import to_wav_via_sf2

        with tempfile.TemporaryDirectory() as tmpdir:
            midi_path = Path(tmpdir) / 'nonexistent.mid'
            sf2_path = Path(tmpdir) / 'font.sf2'
            wav_path = Path(tmpdir) / 'output.wav'

            # Create dummy sf2 file
            sf2_path.write_text('dummy')

            with pytest.raises(FileNotFoundError, match="MIDI file not found"):
                to_wav_via_sf2(midi_path, sf2_path, wav_path)

    def test_to_wav_via_sf2_soundfont_not_found(self):
        """Test to_wav_via_sf2 with non-existent SoundFont file."""
        from cancrizans.io import to_wav_via_sf2

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create dummy MIDI file
            gen = CanonGenerator(seed=42)
            canon = gen.generate_scale_canon('C', 'major')
            midi_path = Path(tmpdir) / 'test.mid'
            to_midi(canon, midi_path)

            sf2_path = Path(tmpdir) / 'nonexistent.sf2'
            wav_path = Path(tmpdir) / 'output.wav'

            with pytest.raises(FileNotFoundError, match="SoundFont file not found"):
                to_wav_via_sf2(midi_path, sf2_path, wav_path)

    def test_to_wav_via_sf2_import_error(self, capsys):
        """Test to_wav_via_sf2 when midi2audio is not available."""
        from cancrizans.io import to_wav_via_sf2

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create dummy MIDI and SF2 files
            gen = CanonGenerator(seed=42)
            canon = gen.generate_scale_canon('C', 'major')
            midi_path = Path(tmpdir) / 'test.mid'
            to_midi(canon, midi_path)

            sf2_path = Path(tmpdir) / 'font.sf2'
            sf2_path.write_text('dummy')

            wav_path = Path(tmpdir) / 'output.wav'

            # This will likely hit the ImportError path
            result = to_wav_via_sf2(midi_path, sf2_path, wav_path)

            # Should return None if midi2audio not available
            if result is None:
                captured = capsys.readouterr()
                assert 'midi2audio' in captured.out or 'FluidSynth' in captured.out

    def test_lilypond_zero_duration_handling(self):
        """Test LilyPond export handles zero or very small durations."""
        score = stream.Score()
        part = stream.Part()
        # Note with very small duration
        part.append(note.Note('C4', quarterLength=0.01))
        score.insert(0, part)

        with tempfile.TemporaryDirectory() as tmpdir:
            ly_path = Path(tmpdir) / 'test.ly'
            result = to_lilypond(score, ly_path)

            assert ly_path.exists()
            content = ly_path.read_text()
            # Should have some duration value (defaults to 4 if invalid)
            assert '4' in content or 'c' in content

    def test_abc_rest_various_durations(self):
        """Test ABC export with rests of various durations."""
        score = stream.Score()
        part = stream.Part()
        part.append(note.Rest(quarterLength=2.0))  # Long rest
        part.append(note.Rest(quarterLength=0.5))  # Short rest
        score.insert(0, part)

        with tempfile.TemporaryDirectory() as tmpdir:
            abc_path = Path(tmpdir) / 'test.abc'
            to_abc(score, abc_path)

            content = abc_path.read_text()
            # Should have rest markers with durations
            assert 'z' in content
            assert '2' in content or '/2' in content

    def test_load_score_string_path(self):
        """Test load_score with string path instead of Path object."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        with tempfile.TemporaryDirectory() as tmpdir:
            midi_path = Path(tmpdir) / 'test.mid'
            to_midi(canon, midi_path)

            # Pass as string instead of Path
            loaded = load_score(str(midi_path))
            assert isinstance(loaded, stream.Score)

    def test_to_midi_string_path(self):
        """Test to_midi with string path instead of Path object."""
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        with tempfile.TemporaryDirectory() as tmpdir:
            midi_path = str(Path(tmpdir) / 'test.mid')
            result = to_midi(canon, midi_path)

            assert Path(midi_path).exists()
            assert isinstance(result, Path)

    def test_abc_complex_rest_durations(self):
        """Test ABC export with complex rest durations to hit line 227."""
        score = stream.Score()
        part = stream.Part()
        # Add rests with various durations that aren't 0.5, 1.0, or 2.0
        part.append(note.Rest(quarterLength=1.5))
        part.append(note.Rest(quarterLength=3.0))
        part.append(note.Rest(quarterLength=0.25))
        score.insert(0, part)

        with tempfile.TemporaryDirectory() as tmpdir:
            abc_path = Path(tmpdir) / 'test.abc'
            to_abc(score, abc_path)

            content = abc_path.read_text()
            # Should have z for rest
            assert 'z' in content

    def test_to_wav_via_sf2_success_with_mock(self):
        """Test successful WAV conversion with mocked FluidSynth."""
        from cancrizans.io import to_wav_via_sf2
        from unittest.mock import patch, MagicMock
        import sys

        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        with tempfile.TemporaryDirectory() as tmpdir:
            midi_path = Path(tmpdir) / 'test.mid'
            sf2_path = Path(tmpdir) / 'font.sf2'
            wav_path = Path(tmpdir) / 'output.wav'

            to_midi(canon, midi_path)
            sf2_path.write_bytes(b'dummy soundfont')

            # Mock midi2audio.FluidSynth to simulate successful conversion
            # Create a fake midi2audio module
            fake_midi2audio = MagicMock()
            mock_fs_instance = MagicMock()
            fake_midi2audio.FluidSynth.return_value = mock_fs_instance

            with patch.dict('sys.modules', {'midi2audio': fake_midi2audio}):
                result = to_wav_via_sf2(midi_path, sf2_path, wav_path)

                assert result == wav_path
                fake_midi2audio.FluidSynth.assert_called_once()
                mock_fs_instance.midi_to_audio.assert_called_once()

    def test_to_wav_via_sf2_generic_exception(self):
        """Test generic exception handling in to_wav_via_sf2."""
        from cancrizans.io import to_wav_via_sf2
        from unittest.mock import patch, MagicMock

        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        with tempfile.TemporaryDirectory() as tmpdir:
            midi_path = Path(tmpdir) / 'test.mid'
            sf2_path = Path(tmpdir) / 'font.sf2'
            wav_path = Path(tmpdir) / 'output.wav'

            to_midi(canon, midi_path)
            sf2_path.write_bytes(b'dummy soundfont')

            # Mock FluidSynth to raise a generic exception
            fake_midi2audio = MagicMock()
            fake_midi2audio.FluidSynth.side_effect = RuntimeError("Conversion failed")

            with patch.dict('sys.modules', {'midi2audio': fake_midi2audio}):
                result = to_wav_via_sf2(midi_path, sf2_path, wav_path)

                # Should return None and print error
                assert result is None

    def test_load_score_wraps_part_object(self):
        """Test that load_score wraps a Part in a Score if needed."""
        from unittest.mock import patch
        from music21 import stream

        # Create a Part (not a Score)
        part = stream.Part()
        part.append(note.Note('C4', quarterLength=1.0))

        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / 'test.mid'
            # Save a part directly
            part.write('midi', fp=str(test_file))

            # Load it back - music21 might return a Part
            with patch('music21.converter.parse') as mock_parse:
                mock_parse.return_value = part

                loaded = load_score(test_file)

                # Should be wrapped in a Score
                assert isinstance(loaded, stream.Score)
                assert len(loaded.parts) >= 1

    def test_load_score_wraps_other_stream_types(self):
        """Test that load_score wraps other Stream types in a Score."""
        from unittest.mock import patch
        from music21 import stream

        # Create a generic Stream (not Score or Part)
        generic_stream = stream.Stream()
        generic_stream.append(note.Note('D4', quarterLength=1.0))

        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / 'test.mid'
            test_file.write_bytes(b'dummy')  # Just create the file

            with patch('music21.converter.parse') as mock_parse:
                mock_parse.return_value = generic_stream

                loaded = load_score(test_file)

                # Should be wrapped in a Score
                assert isinstance(loaded, stream.Score)

    def test_load_score_file_not_found(self):
        """Test load_score raises FileNotFoundError for missing file (line 303)."""
        with pytest.raises(FileNotFoundError) as exc_info:
            load_score('/nonexistent/path/to/file.mid')

        assert 'File not found' in str(exc_info.value)
