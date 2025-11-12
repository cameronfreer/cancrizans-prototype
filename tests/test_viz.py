"""
Tests for visualization module (viz.py).
"""

import pytest
import tempfile
from pathlib import Path
from PIL import Image
from music21 import stream, note, chord
from cancrizans import assemble_crab_from_theme
from cancrizans.viz import piano_roll, symmetry


@pytest.fixture
def simple_canon():
    """Create a simple crab canon for testing."""
    theme = stream.Part()
    theme.append(note.Note('C4', quarterLength=1.0))
    theme.append(note.Note('D4', quarterLength=1.0))
    theme.append(note.Note('E4', quarterLength=1.0))
    theme.append(note.Note('F4', quarterLength=1.0))
    return assemble_crab_from_theme(theme)


@pytest.fixture
def chord_canon():
    """Create a canon with chords."""
    theme = stream.Part()
    theme.append(chord.Chord(['C4', 'E4', 'G4'], quarterLength=1.0))
    theme.append(note.Note('D4', quarterLength=0.5))
    theme.append(note.Note('E4', quarterLength=0.5))
    return assemble_crab_from_theme(theme)


@pytest.fixture
def rest_canon():
    """Create a canon with rests."""
    theme = stream.Part()
    theme.append(note.Note('C4', quarterLength=1.0))
    theme.append(note.Rest(quarterLength=0.5))
    theme.append(note.Note('E4', quarterLength=1.0))
    return assemble_crab_from_theme(theme)


class TestPianoRoll:
    """Test piano_roll visualization function."""

    def test_piano_roll_creates_file(self, simple_canon):
        """Test that piano_roll creates an output file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'piano_roll.png'
            result = piano_roll(simple_canon, output)

            assert result == output
            assert output.exists()
            assert output.stat().st_size > 0

    def test_piano_roll_creates_directory(self, simple_canon):
        """Test that piano_roll creates parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'subdir' / 'piano_roll.png'
            result = piano_roll(simple_canon, output)

            assert result == output
            assert output.exists()
            assert output.parent.exists()

    def test_piano_roll_valid_image(self, simple_canon):
        """Test that piano_roll creates a valid PNG image."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'piano_roll.png'
            piano_roll(simple_canon, output)

            # Verify it's a valid image
            img = Image.open(output)
            assert img.format == 'PNG'
            assert img.size[0] > 0  # width
            assert img.size[1] > 0  # height

    def test_piano_roll_with_chords(self, chord_canon):
        """Test piano_roll handles chords correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'piano_roll.png'
            result = piano_roll(chord_canon, output)

            assert result.exists()
            img = Image.open(result)
            assert img.format == 'PNG'

    def test_piano_roll_with_rests(self, rest_canon):
        """Test piano_roll handles rests correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'piano_roll.png'
            result = piano_roll(rest_canon, output)

            assert result.exists()
            img = Image.open(result)
            assert img.format == 'PNG'

    def test_piano_roll_custom_dpi(self, simple_canon):
        """Test piano_roll with custom DPI setting."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_low = Path(tmpdir) / 'low_dpi.png'
            output_high = Path(tmpdir) / 'high_dpi.png'

            piano_roll(simple_canon, output_low, dpi=50)
            piano_roll(simple_canon, output_high, dpi=200)

            # Higher DPI should result in larger file size
            assert output_high.stat().st_size > output_low.stat().st_size

    def test_piano_roll_string_path(self, simple_canon):
        """Test piano_roll accepts string path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / 'piano_roll.png')
            result = piano_roll(simple_canon, output)

            assert isinstance(result, Path)
            assert result.exists()

    def test_piano_roll_multiple_voices(self):
        """Test piano_roll with multiple voices."""
        score = stream.Score()

        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))
        part1.append(note.Note('D4', quarterLength=1.0))

        part2 = stream.Part()
        part2.append(note.Note('E4', quarterLength=1.0))
        part2.append(note.Note('F4', quarterLength=1.0))

        part3 = stream.Part()
        part3.append(note.Note('G4', quarterLength=1.0))
        part3.append(note.Note('A4', quarterLength=1.0))

        score.insert(0, part1)
        score.insert(0, part2)
        score.insert(0, part3)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'piano_roll.png'
            result = piano_roll(score, output)

            assert result.exists()
            img = Image.open(result)
            assert img.format == 'PNG'


class TestSymmetry:
    """Test symmetry visualization function."""

    def test_symmetry_creates_file(self, simple_canon):
        """Test that symmetry creates an output file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'symmetry.png'
            result = symmetry(simple_canon, output)

            assert result == output
            assert output.exists()
            assert output.stat().st_size > 0

    def test_symmetry_creates_directory(self, simple_canon):
        """Test that symmetry creates parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'subdir' / 'symmetry.png'
            result = symmetry(simple_canon, output)

            assert result == output
            assert output.exists()
            assert output.parent.exists()

    def test_symmetry_valid_image(self, simple_canon):
        """Test that symmetry creates a valid PNG image."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'symmetry.png'
            symmetry(simple_canon, output)

            # Verify it's a valid image
            img = Image.open(output)
            assert img.format == 'PNG'
            assert img.size[0] > 0  # width
            assert img.size[1] > 0  # height

    def test_symmetry_with_chords(self, chord_canon):
        """Test symmetry handles chords correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'symmetry.png'
            result = symmetry(chord_canon, output)

            assert result.exists()
            img = Image.open(result)
            assert img.format == 'PNG'

    def test_symmetry_with_rests(self, rest_canon):
        """Test symmetry handles rests correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'symmetry.png'
            result = symmetry(rest_canon, output)

            assert result.exists()
            img = Image.open(result)
            assert img.format == 'PNG'

    def test_symmetry_custom_dpi(self, simple_canon):
        """Test symmetry with custom DPI setting."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_low = Path(tmpdir) / 'low_dpi.png'
            output_high = Path(tmpdir) / 'high_dpi.png'

            symmetry(simple_canon, output_low, dpi=50)
            symmetry(simple_canon, output_high, dpi=200)

            # Higher DPI should result in larger file size
            assert output_high.stat().st_size > output_low.stat().st_size

    def test_symmetry_string_path(self, simple_canon):
        """Test symmetry accepts string path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = str(Path(tmpdir) / 'symmetry.png')
            result = symmetry(simple_canon, output)

            assert isinstance(result, Path)
            assert result.exists()

    def test_symmetry_three_voices(self):
        """Test symmetry with non-standard number of voices."""
        score = stream.Score()

        part1 = stream.Part()
        part1.append(note.Note('C4', quarterLength=1.0))

        part2 = stream.Part()
        part2.append(note.Note('E4', quarterLength=1.0))

        part3 = stream.Part()
        part3.append(note.Note('G4', quarterLength=1.0))

        score.insert(0, part1)
        score.insert(0, part2)
        score.insert(0, part3)

        # Should still work but print a warning
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'symmetry.png'
            result = symmetry(score, output)

            assert result.exists()
            img = Image.open(result)
            assert img.format == 'PNG'

    def test_symmetry_single_voice(self):
        """Test symmetry with single voice."""
        score = stream.Score()

        part = stream.Part()
        part.append(note.Note('C4', quarterLength=1.0))
        part.append(note.Note('D4', quarterLength=1.0))

        score.insert(0, part)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'symmetry.png'
            result = symmetry(score, output)

            assert result.exists()
            img = Image.open(result)
            assert img.format == 'PNG'


class TestVisualizationIntegration:
    """Integration tests for visualization functions."""

    def test_both_visualizations_same_canon(self, simple_canon):
        """Test that both visualizations work on the same canon."""
        with tempfile.TemporaryDirectory() as tmpdir:
            piano_output = Path(tmpdir) / 'piano.png'
            sym_output = Path(tmpdir) / 'symmetry.png'

            piano_result = piano_roll(simple_canon, piano_output)
            sym_result = symmetry(simple_canon, sym_output)

            assert piano_result.exists()
            assert sym_result.exists()

            # Both should be valid images
            img1 = Image.open(piano_result)
            img2 = Image.open(sym_result)
            assert img1.format == 'PNG'
            assert img2.format == 'PNG'

    def test_visualizations_with_empty_parts(self):
        """Test visualizations handle empty parts gracefully."""
        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()

        # Add at least one note to avoid completely empty score
        part1.append(note.Note('C4', quarterLength=1.0))

        score.insert(0, part1)
        score.insert(0, part2)

        with tempfile.TemporaryDirectory() as tmpdir:
            piano_output = Path(tmpdir) / 'piano.png'
            sym_output = Path(tmpdir) / 'symmetry.png'

            piano_result = piano_roll(score, piano_output)
            sym_result = symmetry(score, sym_output)

            assert piano_result.exists()
            assert sym_result.exists()
