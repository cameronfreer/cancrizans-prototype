"""
Comprehensive tests for CLI commands (cli.py).

Tests all command-line interface functionality including:
- analyze, render, synthesize, generate, validate, research commands
- Argument parsing and validation
- File I/O and error handling
"""

import pytest
import tempfile
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO
import argparse

from cancrizans.cli import (
    analyze_command,
    render_command,
    synthesize_command,
    generate_command,
    validate_command,
    research_command,
    main
)
from cancrizans.generator import CanonGenerator
from cancrizans.io import to_midi, to_musicxml
from cancrizans import load_bach_crab_canon


@pytest.fixture
def test_midi_file():
    """Create a temporary MIDI file for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major', length=4)
        midi_path = Path(tmpdir) / 'test.mid'
        to_midi(canon, midi_path)
        yield midi_path


@pytest.fixture
def test_musicxml_file():
    """Create a temporary MusicXML file for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major', length=4)
        xml_path = Path(tmpdir) / 'test.musicxml'
        to_musicxml(canon, xml_path)
        yield xml_path


class TestAnalyzeCommand:
    """Test analyze command functionality."""

    def test_analyze_existing_file(self, test_midi_file, capsys):
        """Test analyzing an existing MIDI file."""
        args = argparse.Namespace(input=str(test_midi_file))
        result = analyze_command(args)

        assert result == 0
        captured = capsys.readouterr()
        assert "Analyzing:" in captured.out
        assert "Number of voices:" in captured.out
        assert "Palindrome Verification:" in captured.out

    def test_analyze_nonexistent_file(self, capsys):
        """Test analyzing a file that doesn't exist."""
        args = argparse.Namespace(input="/nonexistent/file.mid")
        result = analyze_command(args)

        assert result == 1
        captured = capsys.readouterr()
        assert "Error: File not found" in captured.out

    def test_analyze_shows_voice_count(self, test_midi_file, capsys):
        """Test that analyze shows correct voice count."""
        args = argparse.Namespace(input=str(test_midi_file))
        analyze_command(args)

        captured = capsys.readouterr()
        assert "Number of voices: 2" in captured.out  # Crab canon has 2 voices

    def test_analyze_shows_palindrome_status(self, test_midi_file, capsys):
        """Test that analyze shows palindrome verification."""
        args = argparse.Namespace(input=str(test_midi_file))
        analyze_command(args)

        captured = capsys.readouterr()
        assert "is_time_palindrome:" in captured.out

    def test_analyze_shows_duration(self, test_midi_file, capsys):
        """Test that analyze shows duration information."""
        args = argparse.Namespace(input=str(test_midi_file))
        analyze_command(args)

        captured = capsys.readouterr()
        assert "Total duration:" in captured.out
        assert "quarter notes" in captured.out


class TestRenderCommand:
    """Test render command functionality."""

    def test_render_midi_output(self, test_midi_file):
        """Test rendering MIDI output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'output.mid'
            args = argparse.Namespace(
                input=str(test_midi_file),
                midi=str(output),
                xml=None,
                wav=None,
                soundfont=None,
                roll=None,
                mirror=None
            )
            result = render_command(args)

            assert result == 0
            assert output.exists()

    def test_render_musicxml_output(self, test_midi_file):
        """Test rendering MusicXML output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'output.musicxml'
            args = argparse.Namespace(
                input=str(test_midi_file),
                midi=None,
                xml=str(output),
                wav=None,
                soundfont=None,
                roll=None,
                mirror=None
            )
            result = render_command(args)

            assert result == 0
            assert output.exists()

    def test_render_piano_roll(self, test_midi_file):
        """Test rendering piano roll visualization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'roll.png'
            args = argparse.Namespace(
                input=str(test_midi_file),
                midi=None,
                xml=None,
                wav=None,
                soundfont=None,
                roll=str(output),
                mirror=None
            )
            result = render_command(args)

            assert result == 0
            assert output.exists()

    def test_render_symmetry_plot(self, test_midi_file):
        """Test rendering symmetry plot."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'symmetry.png'
            args = argparse.Namespace(
                input=str(test_midi_file),
                midi=None,
                xml=None,
                wav=None,
                soundfont=None,
                roll=None,
                mirror=str(output)
            )
            result = render_command(args)

            assert result == 0
            assert output.exists()

    def test_render_without_input_uses_bach(self, capsys):
        """Test rendering without input loads Bach canon."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'output.mid'
            args = argparse.Namespace(
                input=None,
                midi=str(output),
                xml=None,
                wav=None,
                soundfont=None,
                roll=None,
                mirror=None
            )
            result = render_command(args)

            assert result == 0
            assert output.exists()
            captured = capsys.readouterr()
            assert "Loading Bach Crab Canon" in captured.out

    def test_render_multiple_outputs(self, test_midi_file):
        """Test rendering multiple output formats at once."""
        with tempfile.TemporaryDirectory() as tmpdir:
            midi_out = Path(tmpdir) / 'output.mid'
            xml_out = Path(tmpdir) / 'output.musicxml'
            roll_out = Path(tmpdir) / 'roll.png'

            args = argparse.Namespace(
                input=str(test_midi_file),
                midi=str(midi_out),
                xml=str(xml_out),
                wav=None,
                soundfont=None,
                roll=str(roll_out),
                mirror=None
            )
            result = render_command(args)

            assert result == 0
            assert midi_out.exists()
            assert xml_out.exists()
            assert roll_out.exists()

    def test_render_wav_without_midi_fails(self, test_midi_file, capsys):
        """Test that WAV export requires MIDI."""
        with tempfile.TemporaryDirectory() as tmpdir:
            wav_out = Path(tmpdir) / 'output.wav'
            args = argparse.Namespace(
                input=str(test_midi_file),
                midi=None,
                xml=None,
                wav=str(wav_out),
                soundfont='/fake/soundfont.sf2',
                roll=None,
                mirror=None
            )
            result = render_command(args)

            assert result == 1
            captured = capsys.readouterr()
            assert "WAV export requires MIDI" in captured.out


class TestSynthesizeCommand:
    """Test synthesize command functionality."""

    def test_synthesize_default(self, capsys):
        """Test basic synthesis."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'synth.mid'
            args = argparse.Namespace(
                transpose=0,
                tempo=None,
                output=str(output)
            )
            result = synthesize_command(args)

            assert result == 0
            assert output.exists()
            captured = capsys.readouterr()
            assert "Synthesizing crab canon" in captured.out

    def test_synthesize_with_transpose(self, capsys):
        """Test synthesis with transposition."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'synth.mid'
            args = argparse.Namespace(
                transpose=5,
                tempo=None,
                output=str(output)
            )
            result = synthesize_command(args)

            assert result == 0
            captured = capsys.readouterr()
            assert "Transposing by 5 semitones" in captured.out

    def test_synthesize_with_tempo(self, capsys):
        """Test synthesis with tempo setting."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'synth.mid'
            args = argparse.Namespace(
                transpose=0,
                tempo=120,
                output=str(output)
            )
            result = synthesize_command(args)

            assert result == 0
            captured = capsys.readouterr()
            assert "Tempo set to: 120 BPM" in captured.out

    def test_synthesize_verifies_palindrome(self, capsys):
        """Test that synthesis verifies palindrome property."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'synth.mid'
            args = argparse.Namespace(
                transpose=0,
                tempo=None,
                output=str(output)
            )
            synthesize_command(args)

            captured = capsys.readouterr()
            assert "Palindrome verification:" in captured.out


class TestGenerateCommand:
    """Test generate command functionality."""

    def test_generate_scale_algorithm(self):
        """Test generating with scale algorithm."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'canon.mid'
            args = argparse.Namespace(
                algorithm='scale',
                output=str(output),
                validate=False,
                verbose=False,
                seed=None,
                key='C',
                mode='major',
                length=8,
                root=None,
                chord_type=None,
                max_interval=None
            )
            result = generate_command(args)

            assert result == 0
            assert output.exists()

    def test_generate_arpeggio_algorithm(self):
        """Test generating with arpeggio algorithm."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'canon.mid'
            args = argparse.Namespace(
                algorithm='arpeggio',
                output=str(output),
                validate=False,
                verbose=False,
                seed=None,
                key=None,
                mode='major',
                length=None,
                root='C4',
                chord_type='major',
                max_interval=None
            )
            result = generate_command(args)

            assert result == 0
            assert output.exists()

    def test_generate_random_algorithm(self):
        """Test generating with random algorithm."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'canon.mid'
            args = argparse.Namespace(
                algorithm='random',
                output=str(output),
                validate=False,
                verbose=False,
                seed=None,
                key=None,
                mode=None,
                length=12,
                root=None,
                chord_type=None,
                max_interval=3
            )
            result = generate_command(args)

            assert result == 0
            assert output.exists()

    def test_generate_fibonacci_algorithm(self):
        """Test generating with fibonacci algorithm."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'canon.mid'
            args = argparse.Namespace(
                algorithm='fibonacci',
                output=str(output),
                validate=False,
                verbose=False,
                seed=None,
                key=None,
                mode=None,
                length=8,
                root='G4',
                chord_type=None,
                max_interval=None
            )
            result = generate_command(args)

            assert result == 0
            assert output.exists()

    def test_generate_with_validation(self, capsys):
        """Test generating with automatic validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'canon.mid'
            args = argparse.Namespace(
                algorithm='scale',
                output=str(output),
                validate=True,
                verbose=False,
                seed=None,
                key='C',
                mode='major',
                length=8,
                root=None,
                chord_type=None,
                max_interval=None
            )
            result = generate_command(args)

            assert result == 0
            captured = capsys.readouterr()
            assert "Quality Score:" in captured.out

    def test_generate_invalid_algorithm(self, capsys):
        """Test generating with invalid algorithm."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'canon.mid'
            args = argparse.Namespace(
                algorithm='invalid_algo',
                output=str(output),
                validate=False,
                verbose=False,
                seed=None,
                key=None,
                mode=None,
                length=None,
                root=None,
                chord_type=None,
                max_interval=None
            )
            result = generate_command(args)

            assert result == 1
            captured = capsys.readouterr()
            assert "Unknown algorithm" in captured.out


class TestValidateCommand:
    """Test validate command functionality."""

    def test_validate_midi_file(self, test_midi_file, capsys):
        """Test validating a MIDI file."""
        args = argparse.Namespace(
            input=str(test_midi_file),
            verbose=False,
            output=None
        )
        result = validate_command(args)

        assert result == 0
        captured = capsys.readouterr()
        assert "Overall Quality" in captured.out

    def test_validate_verbose_mode(self, test_midi_file, capsys):
        """Test validation with verbose output."""
        args = argparse.Namespace(
            input=str(test_midi_file),
            verbose=True,
            output=None
        )
        result = validate_command(args)

        assert result == 0
        captured = capsys.readouterr()
        assert "RECOMMENDATIONS" in captured.out

    def test_validate_nonexistent_file(self, capsys):
        """Test validating a nonexistent file."""
        args = argparse.Namespace(
            input="/nonexistent/file.mid",
            verbose=False,
            output=None
        )
        result = validate_command(args)

        assert result == 1
        captured = capsys.readouterr()
        assert "Error: File not found" in captured.out


class TestResearchCommand:
    """Test research command functionality."""

    def test_research_directory(self, test_midi_file):
        """Test research command on a directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create a few test files
            gen = CanonGenerator(seed=42)
            for i in range(3):
                canon = gen.generate_scale_canon('C', 'major', length=4)
                to_midi(canon, tmppath / f'canon{i}.mid')

            output_dir = tmppath / 'results'
            args = argparse.Namespace(
                directory=str(tmppath),
                pattern='*.mid',
                output=str(output_dir),
                all=True,
                csv=False,
                json=False,
                latex=False,
                markdown=False
            )
            result = research_command(args)

            assert result == 0
            assert output_dir.exists()

    def test_research_csv_export(self, test_midi_file):
        """Test research with CSV export."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create test file
            to_midi(load_bach_crab_canon(), tmppath / 'canon.mid')

            output_dir = tmppath / 'results'
            args = argparse.Namespace(
                directory=str(tmppath),
                pattern='*.mid',
                output=str(output_dir),
                all=False,
                csv=True,
                json=False,
                latex=False,
                markdown=False
            )
            result = research_command(args)

            assert result == 0
            csv_file = output_dir / 'analysis.csv'
            assert csv_file.exists()

    def test_research_json_export(self, test_midi_file):
        """Test research with JSON export."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            to_midi(load_bach_crab_canon(), tmppath / 'canon.mid')

            output_dir = tmppath / 'results'
            args = argparse.Namespace(
                directory=str(tmppath),
                pattern='*.mid',
                output=str(output_dir),
                all=False,
                csv=False,
                json=True,
                latex=False,
                markdown=False
            )
            result = research_command(args)

            assert result == 0
            json_file = output_dir / 'analysis.json'
            assert json_file.exists()

    def test_research_empty_directory(self, capsys):
        """Test research on empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / 'results'
            args = argparse.Namespace(
                directory=tmpdir,
                pattern='*.mid',
                output=str(output_dir),
                all=True,
                csv=False,
                json=False,
                latex=False,
                markdown=False
            )
            result = research_command(args)

            captured = capsys.readouterr()
            assert "No files found" in captured.out or result == 1


class TestMainFunction:
    """Test main entry point and argument parsing."""

    def test_main_with_help(self):
        """Test main with --help argument."""
        with patch('sys.argv', ['cancrizans', '--help']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            # --help exits with code 0
            assert exc_info.value.code == 0

    def test_main_no_arguments(self, capsys):
        """Test main with no arguments shows help."""
        with patch('sys.argv', ['cancrizans']):
            result = main()
            # Without subcommand, it shows usage but doesn't crash
            captured = capsys.readouterr()
            assert "usage:" in captured.out or result is not None

    def test_main_analyze_subcommand(self, test_midi_file):
        """Test main with analyze subcommand."""
        with patch('sys.argv', ['cancrizans', 'analyze', str(test_midi_file)]):
            result = main()
            assert result == 0

    def test_main_generate_subcommand(self):
        """Test main with generate subcommand."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'canon.mid'
            with patch('sys.argv', ['cancrizans', 'generate', 'scale', '--output', str(output)]):
                result = main()
                assert result == 0
                assert output.exists()

    def test_main_validate_subcommand(self, test_midi_file):
        """Test main with validate subcommand."""
        with patch('sys.argv', ['cancrizans', 'validate', str(test_midi_file)]):
            result = main()
            assert result == 0


class TestCLIIntegration:
    """Integration tests for CLI workflows."""

    def test_generate_then_validate_workflow(self, capsys):
        """Test generating a canon then validating it."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'canon.mid'

            # Generate
            gen_args = argparse.Namespace(
                algorithm='scale',
                output=str(output),
                validate=False,
                verbose=False,
                seed=None,
                key='C',
                mode='major',
                length=8,
                root=None,
                chord_type=None,
                max_interval=None
            )
            result1 = generate_command(gen_args)
            assert result1 == 0

            # Validate
            val_args = argparse.Namespace(
                input=str(output),
                verbose=True,
                output=None
            )
            result2 = validate_command(val_args)
            assert result2 == 0

            captured = capsys.readouterr()
            assert "Overall Quality" in captured.out

    def test_generate_then_analyze_workflow(self):
        """Test generating a canon then analyzing it."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'canon.mid'

            # Generate
            gen_args = argparse.Namespace(
                algorithm='fibonacci',
                output=str(output),
                validate=False,
                verbose=False,
                seed=None,
                key=None,
                mode=None,
                length=8,
                root='G4',
                chord_type=None,
                max_interval=None
            )
            result1 = generate_command(gen_args)
            assert result1 == 0

            # Analyze
            ana_args = argparse.Namespace(input=str(output))
            result2 = analyze_command(ana_args)
            assert result2 == 0

    def test_full_workflow(self):
        """Test complete workflow: generate -> validate -> render -> analyze."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            canon_file = tmppath / 'canon.mid'
            xml_file = tmppath / 'canon.musicxml'
            viz_file = tmppath / 'canon.png'

            # 1. Generate
            gen_args = argparse.Namespace(
                algorithm='golden',
                output=str(canon_file),
                validate=False,
                verbose=False,
                seed=None,
                key=None,
                mode=None,
                length=13,
                root='D4',
                chord_type=None,
                max_interval=None
            )
            assert generate_command(gen_args) == 0
            assert canon_file.exists()

            # 2. Validate
            val_args = argparse.Namespace(input=str(canon_file), verbose=False, output=None)
            assert validate_command(val_args) == 0

            # 3. Render
            render_args = argparse.Namespace(
                input=str(canon_file),
                midi=None,
                xml=str(xml_file),
                wav=None,
                soundfont=None,
                roll=str(viz_file),
                mirror=None
            )
            assert render_command(render_args) == 0
            assert xml_file.exists()
            assert viz_file.exists()

            # 4. Analyze
            ana_args = argparse.Namespace(input=str(canon_file))
            assert analyze_command(ana_args) == 0
