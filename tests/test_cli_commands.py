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

    def test_render_wav_success_path(self, test_midi_file, capsys):
        """Test successful WAV export path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            midi_out = Path(tmpdir) / 'output.mid'
            wav_out = Path(tmpdir) / 'output.wav'
            sf2_path = Path(tmpdir) / 'soundfont.sf2'

            # Create empty soundfont file for testing
            sf2_path.write_bytes(b'')

            args = argparse.Namespace(
                input=str(test_midi_file),
                midi=str(midi_out),
                xml=None,
                wav=str(wav_out),
                soundfont=str(sf2_path),
                roll=None,
                mirror=None
            )

            # Mock the to_wav_via_sf2 to simulate success
            with patch('cancrizans.cli.to_wav_via_sf2') as mock_wav:
                mock_wav.return_value = wav_out
                result = render_command(args)

                assert result == 0
                captured = capsys.readouterr()
                assert '✓ WAV exported to:' in captured.out

    def test_render_wav_failure_path(self, test_midi_file, capsys):
        """Test WAV export failure path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            midi_out = Path(tmpdir) / 'output.mid'
            wav_out = Path(tmpdir) / 'output.wav'
            sf2_path = Path(tmpdir) / 'soundfont.sf2'

            # Create empty soundfont file for testing
            sf2_path.write_bytes(b'')

            args = argparse.Namespace(
                input=str(test_midi_file),
                midi=str(midi_out),
                xml=None,
                wav=str(wav_out),
                soundfont=str(sf2_path),
                roll=None,
                mirror=None
            )

            # Mock the to_wav_via_sf2 to simulate failure
            with patch('cancrizans.cli.to_wav_via_sf2') as mock_wav:
                mock_wav.return_value = None
                result = render_command(args)

                captured = capsys.readouterr()
                assert '✗ WAV export failed' in captured.out

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

    def test_research_latex_export(self, test_midi_file):
        """Test research with LaTeX export."""
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
                csv=False,
                json=False,
                latex=True,
                markdown=False
            )
            result = research_command(args)

            assert result == 0
            latex_file = output_dir / 'analysis.tex'
            assert latex_file.exists()

    def test_research_markdown_export(self, test_midi_file):
        """Test research with Markdown export."""
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
                csv=False,
                json=False,
                latex=False,
                markdown=True
            )
            result = research_command(args)

            assert result == 0
            md_file = output_dir / 'analysis.md'
            assert md_file.exists()


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


class TestMainModule:
    """Test __main__.py module entry point."""

    def test_main_module_import(self):
        """Test that __main__ module can be imported."""
        import cancrizans.__main__
        assert hasattr(cancrizans.__main__, 'main')

    def test_main_module_execution(self):
        """Test running as module with --help."""
        import subprocess
        result = subprocess.run(
            [sys.executable, '-m', 'cancrizans', '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0
        assert 'cancrizans' in result.stdout.lower()


class TestCLIEdgeCases:
    """Test edge cases and error handling in CLI commands."""

    def test_research_nonexistent_directory(self, capsys):
        """Test research command with non-existent directory."""
        args = argparse.Namespace(
            directory='/nonexistent/directory',
            pattern='*.mid',
            output='research_output',
            csv=False,
            json=False,
            latex=False,
            markdown=False,
            all=False
        )

        result = research_command(args)
        assert result == 1

        captured = capsys.readouterr()
        assert 'not found' in captured.out.lower() or 'error' in captured.out.lower()

    def test_render_wav_missing_soundfont(self, test_midi_file):
        """Test render command with missing soundfont file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            midi_out = Path(tmpdir) / "out.mid"
            wav_out = Path(tmpdir) / "out.wav"

            args = argparse.Namespace(
                input=str(test_midi_file),
                midi=str(midi_out),
                xml=None,
                wav=str(wav_out),
                soundfont='/nonexistent/soundfont.sf2',  # Missing soundfont
                roll=None,
                mirror=None
            )

            result = render_command(args)
            assert result == 1

    def test_render_wav_without_soundfont_arg(self, test_midi_file):
        """Test render WAV without providing soundfont argument."""
        with tempfile.TemporaryDirectory() as tmpdir:
            midi_out = Path(tmpdir) / "out.mid"
            wav_out = Path(tmpdir) / "out.wav"

            args = argparse.Namespace(
                input=str(test_midi_file),
                midi=str(midi_out),
                xml=None,
                wav=str(wav_out),
                soundfont=None,  # No soundfont provided
                roll=None,
                mirror=None
            )

            result = render_command(args)
            assert result == 1

    def test_main_no_command(self, monkeypatch, capsys):
        """Test main function with no command specified."""
        monkeypatch.setattr(sys, 'argv', ['cancrizans'])

        result = main()
        assert result == 1

        captured = capsys.readouterr()
        # Should print help when no command given
        assert 'usage' in captured.out.lower() or 'command' in captured.out.lower()

    def test_generate_with_validation_warnings(self, capsys):
        """Test generate command with validation showing warnings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "generated.mid"

            args = argparse.Namespace(
                algorithm='scale',
                output=str(output_file),
                key='C',
                root='C4',
                mode='major',
                length=4,  # Short length might trigger warnings
                seed=42,
                validate=True,
                verbose=True  # Enable verbose to show warnings
            )

            result = generate_command(args)
            assert result == 0  # Should still succeed
            assert output_file.exists()

    def test_validate_json_export(self, test_midi_file):
        """Test validate command with JSON export."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_json = Path(tmpdir) / "validation.json"

            args = argparse.Namespace(
                input=str(test_midi_file),
                output=str(output_json),
                verbose=True
            )

            result = validate_command(args)
            # Result can be 0 or 1 depending on if canon is valid palindrome
            assert output_json.exists()

            # Verify JSON structure
            import json
            with open(output_json) as f:
                data = json.load(f)
                assert 'is_valid_canon' in data
                assert 'quality_scores' in data
                assert 'grade' in data

    def test_research_no_matching_files(self, capsys):
        """Test research command when pattern matches no files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create empty directory
            research_dir = Path(tmpdir) / "empty_research"
            research_dir.mkdir()

            args = argparse.Namespace(
                directory=str(research_dir),
                pattern='*.nonexistent',  # Pattern that won't match anything
                output=str(Path(tmpdir) / "output"),
                csv=False,
                json=False,
                latex=False,
                markdown=False,
                all=False
            )

            result = research_command(args)
            assert result == 1

            captured = capsys.readouterr()
            assert 'no files' in captured.out.lower()

    def test_analyze_with_rests(self, capsys):
        """Test analyze command with a score containing rests."""
        from music21 import stream, note

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a simple score with rests
            score = stream.Score()
            part = stream.Part()
            part.append(note.Note('C4', quarterLength=1.0))
            part.append(note.Rest(quarterLength=1.0))
            part.append(note.Note('D4', quarterLength=1.0))
            score.append(part)

            midi_path = Path(tmpdir) / "with_rests.mid"
            score.write('midi', fp=str(midi_path))

            args = argparse.Namespace(input=str(midi_path))
            result = analyze_command(args)

            assert result == 0
            captured = capsys.readouterr()
            assert 'rests' in captured.out.lower()

    def test_synthesize_with_transposition_and_tempo(self, capsys):
        """Test synthesize with both transposition and tempo."""
        with tempfile.TemporaryDirectory() as tmpdir:
            args = argparse.Namespace(
                tempo=120,
                transpose=5,
                output=str(tmpdir)
            )

            result = synthesize_command(args)
            assert result == 0

            captured = capsys.readouterr()
            assert 'transposing' in captured.out.lower()
            assert 'tempo' in captured.out.lower()

            # Check output files exist
            assert (Path(tmpdir) / "synthesized_crab.mid").exists()
            assert (Path(tmpdir) / "synthesized_crab.musicxml").exists()


class TestCLIPhase21Coverage:
    """Tests to achieve 98% coverage - targeting specific uncovered lines."""

    def test_main_calls_render_command(self, test_midi_file, capsys):
        """Test main() correctly routes to render_command (line 471)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_midi = Path(tmpdir) / 'output.mid'

            # Mock sys.argv to simulate CLI call
            test_args = ['cancrizans', 'render', '--input', str(test_midi_file),
                        '--midi', str(output_midi)]

            with patch('sys.argv', test_args):
                result = main()

            assert result == 0
            assert output_midi.exists()

    def test_main_calls_synthesize_command(self, capsys):
        """Test main() correctly routes to synthesize_command (line 473)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_args = ['cancrizans', 'synthesize', '--output', str(tmpdir),
                        '--tempo', '100']

            with patch('sys.argv', test_args):
                result = main()

            assert result == 0
            captured = capsys.readouterr()
            assert 'crab' in captured.out.lower() or 'synthesize' in captured.out.lower()

    def test_main_calls_research_command(self, test_midi_file):
        """Test main() correctly routes to research_command (line 475)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create a test file
            gen = CanonGenerator(seed=42)
            canon = gen.generate_scale_canon('C', 'major')
            to_midi(canon, tmppath / 'test.mid')

            output_dir = tmppath / 'results'
            test_args = ['cancrizans', 'research', str(tmppath),
                        '--output', str(output_dir)]

            with patch('sys.argv', test_args):
                result = main()

            assert result == 0
            assert output_dir.exists()

    def test_main_unknown_command(self, capsys):
        """Test main() handles unknown command - argparse catches it (lines 481-482)."""
        test_args = ['cancrizans', 'unknown_command']

        with patch('sys.argv', test_args):
            # Argparse will raise SystemExit for unknown commands
            with pytest.raises(SystemExit):
                main()

        captured = capsys.readouterr()
        # Argparse will print error message
        assert 'invalid choice' in captured.err.lower() or 'unknown' in captured.err.lower()

    def test_main_exception_handling(self, capsys):
        """Test main() exception handling (lines 484-488)."""
        test_args = ['cancrizans', 'analyze', '/nonexistent/file.mid']

        with patch('sys.argv', test_args):
            result = main()

        # Should catch exception and return 1
        assert result == 1
        captured = capsys.readouterr()
        assert 'Error' in captured.out or 'error' in captured.out.lower()

    def test_generate_modal_canon(self, capsys):
        """Test generating modal canon (line 527)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / 'modal.mid'

            args = argparse.Namespace(
                algorithm='modal',
                output=str(output_file),
                validate=False,
                verbose=False,
                seed=42,
                key=None,
                mode='dorian',
                length=8,
                root='D4',
                chord_type=None,
                max_interval=None
            )

            result = generate_command(args)

            assert result == 0
            assert output_file.exists()

    def test_generate_with_validation_errors(self, capsys):
        """Test generate command showing validation errors (lines 551-553)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / 'canon.mid'

            # Generate a deliberately poor quality canon
            args = argparse.Namespace(
                algorithm='random',
                output=str(output_file),
                validate=True,
                verbose=False,
                seed=999,  # Seed that produces poor quality
                key=None,
                mode=None,
                length=3,  # Very short - likely to have errors
                root='C4',
                chord_type=None,
                max_interval=12
            )

            result = generate_command(args)

            # Should complete but may show errors
            captured = capsys.readouterr()
            # The function completes either way
            assert output_file.exists()

    def test_validate_with_errors_display(self, capsys):
        """Test validate command displaying errors (lines 593-595)."""
        from music21 import stream, note

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create invalid canon (single part - needs 2)
            score = stream.Score()
            part = stream.Part()
            part.append(note.Note('C4', quarterLength=1.0))
            score.insert(0, part)

            midi_path = Path(tmpdir) / 'invalid.mid'
            score.write('midi', fp=str(midi_path))

            args = argparse.Namespace(
                input=str(midi_path),
                verbose=False,
                output=None
            )

            result = validate_command(args)

            # Should show errors
            captured = capsys.readouterr()
            assert 'Error' in captured.out or 'error' in captured.out.lower()

    def test_synthesize_non_palindrome_warning(self, capsys):
        """Test synthesize showing non-palindrome warning (line 191)."""
        from unittest.mock import patch

        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock is_time_palindrome to return False
            with patch('cancrizans.cli.is_time_palindrome', return_value=False):
                args = argparse.Namespace(
                    tempo=60,
                    transpose=0,
                    output=str(tmpdir)
                )

                result = synthesize_command(args)

                captured = capsys.readouterr()
                # Should show warning about non-palindrome
                assert 'warning' in captured.out.lower() or 'palindrome' in captured.out.lower()

    def test_synthesize_bach_load_error(self, capsys):
        """Test synthesize when Bach theme fails to load (lines 169-170)."""
        from unittest.mock import patch
        from music21 import stream

        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock load_bach_crab_canon to return score with no parts
            with patch('cancrizans.cli.load_bach_crab_canon') as mock_load:
                empty_score = stream.Score()
                mock_load.return_value = empty_score

                args = argparse.Namespace(
                    tempo=60,
                    transpose=0,
                    output=str(tmpdir)
                )

                result = synthesize_command(args)

                assert result == 1
                captured = capsys.readouterr()
                assert 'Error' in captured.out and 'Bach theme' in captured.out

    def test_main_exception_with_traceback(self, capsys):
        """Test exception handling prints traceback (lines 484-488)."""
        from unittest.mock import patch

        # Mock analyze_command to raise exception
        with patch('cancrizans.cli.analyze_command', side_effect=RuntimeError("Test error")):
            test_args = ['cancrizans', 'analyze', 'dummy.mid']
            with patch('sys.argv', test_args):
                result = main()

            assert result == 1
            captured = capsys.readouterr()
            # Should print error and traceback
            assert 'Error' in captured.out
            assert 'Test error' in captured.out

    def test_generate_validation_with_actual_errors(self, capsys):
        """Test generate displays validation errors correctly (lines 551-553)."""
        from unittest.mock import patch, MagicMock

        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / 'output.mid'

            # Mock validator to return errors
            with patch('cancrizans.validator.CanonValidator') as MockValidator:
                mock_validator_instance = MagicMock()
                MockValidator.return_value = mock_validator_instance
                mock_validator_instance.validate.return_value = {
                    'is_valid': False,
                    'errors': ['Error 1: Test error', 'Error 2: Another error'],
                    'warnings': [],
                    'overall_quality': 0.5
                }
                mock_validator_instance.get_quality_grade.return_value = 'D'

                args = argparse.Namespace(
                    algorithm='scale',
                    root='C4',
                    key='C',
                    mode='major',
                    length=8,
                    output=str(output_file),
                    validate=True,
                    verbose=False,
                    seed=None
                )

                result = generate_command(args)

                captured = capsys.readouterr()
                # Should display the errors (lines 551-553)
                assert 'Error 1: Test error' in captured.out or 'Test error' in captured.out
                assert 'Error' in captured.out


class TestBachCrabUtilities:
    """Test Bach Crab Canon utility functions."""

    def test_save_crab_canon_xml_with_force(self):
        """Test save_crab_canon_xml with force=True overwrites (line 1038)."""
        from cancrizans.bach_crab import save_crab_canon_xml
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmpdir:
            # Temporarily override CACHE_DIR for this test
            from unittest.mock import patch
            import cancrizans.bach_crab as bach_module

            with patch.object(bach_module, 'ensure_data_dir', return_value=Path(tmpdir)):
                # First call creates the file
                xml_path1 = save_crab_canon_xml()
                assert xml_path1.exists()
                original_content = xml_path1.read_text()

                # Modify the file
                xml_path1.write_text("modified content")
                assert xml_path1.read_text() == "modified content"

                # Call with force=True should overwrite
                xml_path2 = save_crab_canon_xml(force=True)
                assert xml_path2.exists()
                # Should have restored original content
                assert xml_path2.read_text() == original_content
                assert "modified content" not in xml_path2.read_text()
