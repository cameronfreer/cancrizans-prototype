"""
Tests for visualization module (viz.py).
"""

import pytest
import tempfile
from pathlib import Path
from PIL import Image
from music21 import stream, note, chord
from cancrizans import assemble_crab_from_theme
from cancrizans.viz import (
    piano_roll,
    symmetry,
    animate_transformation,
    visualize_3d_canon,
    visualize_voice_graph,
    export_analysis_figure,
)
from cancrizans import retrograde


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

    def test_piano_roll_with_non_note_elements(self):
        """Test piano roll skips non-note/chord elements (line 61)."""
        from music21 import expressions

        score = stream.Score()
        part = stream.Part()

        part.append(note.Note('C4', quarterLength=1.0))
        # Add a dynamic marking (not a note or chord)
        part.append(expressions.TextExpression('forte'))
        part.append(note.Note('E4', quarterLength=1.0))

        score.insert(0, part)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / 'piano.png'
            result = piano_roll(score, output_file)

            # Should handle non-note elements gracefully
            assert result.exists()

    def test_symmetry_with_non_note_elements(self):
        """Test symmetry plot skips non-note/chord elements (line 160)."""
        from music21 import expressions

        score = stream.Score()
        part1 = stream.Part()
        part2 = stream.Part()

        part1.append(note.Note('C4', quarterLength=1.0))
        part1.append(expressions.TextExpression('dolce'))
        part1.append(note.Note('E4', quarterLength=1.0))

        part2.append(note.Note('E4', quarterLength=1.0))
        part2.append(note.Note('C4', quarterLength=1.0))

        score.insert(0, part1)
        score.insert(0, part2)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / 'symmetry.png'
            result = symmetry(score, output_file)

            # Should handle non-note elements gracefully
            assert result.exists()


class TestPhase14AdvancedVisualization:
    """Test Phase 14 advanced visualization functions."""

    def test_animate_transformation_creates_gif(self, simple_canon):
        """Test that animate_transformation creates a GIF file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a transformation
            theme = stream.Part()
            theme.append(note.Note('C4', quarterLength=1.0))
            theme.append(note.Note('D4', quarterLength=1.0))
            theme.append(note.Note('E4', quarterLength=1.0))

            theme_score = stream.Score()
            theme_score.insert(0, theme)

            retro_score = retrograde(theme_score)

            output = Path(tmpdir) / 'animation.gif'
            result = animate_transformation(theme_score, retro_score, output)

            assert result == output
            assert output.exists()
            assert output.stat().st_size > 0

            # Verify it's a valid GIF
            img = Image.open(output)
            assert img.format == 'GIF'

    def test_animate_transformation_custom_frames(self, simple_canon):
        """Test animate_transformation with custom frame count."""
        with tempfile.TemporaryDirectory() as tmpdir:
            theme = stream.Part()
            theme.append(note.Note('C4', quarterLength=1.0))

            theme_score = stream.Score()
            theme_score.insert(0, theme)

            retro_score = retrograde(theme_score)

            output = Path(tmpdir) / 'animation.gif'
            result = animate_transformation(
                theme_score, retro_score, output,
                num_frames=10, duration=1.0, dpi=50
            )

            assert result.exists()
            img = Image.open(result)
            assert img.format == 'GIF'

    def test_visualize_3d_canon_creates_file(self, simple_canon):
        """Test that visualize_3d_canon creates an output file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / '3d_canon.png'
            result = visualize_3d_canon(simple_canon, output)

            assert result == output
            assert output.exists()
            assert output.stat().st_size > 0

            # Verify it's a valid image
            img = Image.open(output)
            assert img.format == 'PNG'

    def test_visualize_3d_canon_custom_rotation(self, simple_canon):
        """Test visualize_3d_canon with custom rotation angles."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / '3d_canon.png'
            result = visualize_3d_canon(
                simple_canon, output,
                rotation=(45, 135), dpi=50
            )

            assert result.exists()
            img = Image.open(result)
            assert img.format == 'PNG'

    def test_visualize_voice_graph_creates_file(self, simple_canon):
        """Test that visualize_voice_graph creates an output file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'voice_graph.png'
            result = visualize_voice_graph(simple_canon, output)

            assert result == output
            assert output.exists()
            assert output.stat().st_size > 0

            # Verify it's a valid image
            img = Image.open(output)
            assert img.format == 'PNG'

    def test_visualize_voice_graph_custom_similarity(self, simple_canon):
        """Test visualize_voice_graph with custom similarity threshold."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'voice_graph.png'
            result = visualize_voice_graph(
                simple_canon, output,
                min_similarity=0.5, dpi=50
            )

            assert result.exists()
            img = Image.open(result)
            assert img.format == 'PNG'

    def test_visualize_voice_graph_fallback(self, simple_canon):
        """Test that voice_graph fallback works without networkx."""
        # This test relies on the function's built-in fallback
        # if networkx is not available
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'voice_graph.png'
            result = visualize_voice_graph(simple_canon, output)

            # Should work regardless of networkx availability
            assert result.exists()

    def test_export_analysis_figure_piano_roll(self, simple_canon):
        """Test export_analysis_figure with piano_roll type."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_base = Path(tmpdir) / 'figure'
            results = export_analysis_figure(
                simple_canon, 'piano_roll', output_base,
                formats=['png'], dpi=100
            )

            assert len(results) == 1
            assert results[0].exists()
            assert results[0].suffix == '.png'

    def test_export_analysis_figure_multiple_formats(self, simple_canon):
        """Test export_analysis_figure with multiple formats."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_base = Path(tmpdir) / 'figure'
            results = export_analysis_figure(
                simple_canon, 'symmetry', output_base,
                formats=['png', 'pdf'], dpi=100
            )

            assert len(results) == 2
            assert all(r.exists() for r in results)

            # Check that we have both formats
            suffixes = {r.suffix for r in results}
            assert '.png' in suffixes
            assert '.pdf' in suffixes

    def test_export_analysis_figure_3d(self, simple_canon):
        """Test export_analysis_figure with 3d type."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_base = Path(tmpdir) / 'figure'
            results = export_analysis_figure(
                simple_canon, '3d', output_base,
                formats=['png'], dpi=50,
                rotation=(20, 60)
            )

            assert len(results) == 1
            assert results[0].exists()

    def test_export_analysis_figure_graph(self, simple_canon):
        """Test export_analysis_figure with graph type."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_base = Path(tmpdir) / 'figure'
            results = export_analysis_figure(
                simple_canon, 'graph', output_base,
                formats=['png'], dpi=50,
                min_similarity=0.5
            )

            assert len(results) == 1
            assert results[0].exists()

    def test_export_analysis_figure_default_formats(self, simple_canon):
        """Test export_analysis_figure with default formats."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_base = Path(tmpdir) / 'figure'
            results = export_analysis_figure(
                simple_canon, 'piano_roll', output_base,
                dpi=50
            )

            # Default is ['png', 'pdf']
            assert len(results) == 2
            suffixes = {r.suffix for r in results}
            assert '.png' in suffixes
            assert '.pdf' in suffixes

    def test_export_analysis_figure_invalid_type(self, simple_canon):
        """Test export_analysis_figure with invalid analysis type."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_base = Path(tmpdir) / 'figure'

            with pytest.raises(ValueError, match="Unknown analysis_type"):
                export_analysis_figure(
                    simple_canon, 'invalid_type', output_base,
                    formats=['png']
                )


class TestMicrotonalVisualization:
    """Test microtonal scale visualization functions."""

    def test_visualize_microtonal_scale_basic(self):
        """Test basic microtonal scale visualization."""
        from cancrizans.microtonal import create_tuning_system_scale, TuningSystem
        from cancrizans.viz import visualize_microtonal_scale

        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'scale.png'
            result = visualize_microtonal_scale(scale, output)

            assert result.exists()
            assert result == output

            # Check it's a valid image
            img = Image.open(result)
            assert img.format == 'PNG'
            assert img.size[0] > 0
            assert img.size[1] > 0

    def test_visualize_microtonal_scale_werckmeister(self):
        """Test visualizing Werckmeister III tuning."""
        from cancrizans.microtonal import create_tuning_system_scale, TuningSystem
        from cancrizans.viz import visualize_microtonal_scale

        scale = create_tuning_system_scale(TuningSystem.WERCKMEISTER_III, tonic_midi=60)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'werckmeister.png'
            result = visualize_microtonal_scale(scale, output)

            assert result.exists()

    def test_visualize_microtonal_scale_19tet(self):
        """Test visualizing 19-TET scale."""
        from cancrizans.microtonal import create_tuning_system_scale, TuningSystem
        from cancrizans.viz import visualize_microtonal_scale

        scale = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'tet19.png'
            result = visualize_microtonal_scale(scale, output)

            assert result.exists()

    def test_visualize_microtonal_scale_world_music(self):
        """Test visualizing world music scales."""
        from cancrizans.microtonal import create_world_music_scale, ScaleType
        from cancrizans.viz import visualize_microtonal_scale

        scale = create_world_music_scale(ScaleType.MAQAM_RAST, tonic_midi=60)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'maqam.png'
            result = visualize_microtonal_scale(scale, output)

            assert result.exists()

    def test_visualize_microtonal_scale_no_cents(self):
        """Test visualization without cent labels."""
        from cancrizans.microtonal import create_tuning_system_scale, TuningSystem
        from cancrizans.viz import visualize_microtonal_scale

        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'scale.png'
            result = visualize_microtonal_scale(scale, output, show_cents=False)

            assert result.exists()

    def test_visualize_microtonal_scale_no_tension(self):
        """Test visualization without tension display."""
        from cancrizans.microtonal import create_tuning_system_scale, TuningSystem
        from cancrizans.viz import visualize_microtonal_scale

        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'scale.png'
            result = visualize_microtonal_scale(scale, output, show_tension=False)

            assert result.exists()

    def test_visualize_microtonal_scale_high_dpi(self):
        """Test visualization with high DPI."""
        from cancrizans.microtonal import create_tuning_system_scale, TuningSystem
        from cancrizans.viz import visualize_microtonal_scale

        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'scale_hires.png'
            result = visualize_microtonal_scale(scale, output, dpi=300)

            assert result.exists()

    def test_visualize_microtonal_scale_creates_dir(self):
        """Test that visualization creates output directory."""
        from cancrizans.microtonal import create_tuning_system_scale, TuningSystem
        from cancrizans.viz import visualize_microtonal_scale

        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'subdir' / 'nested' / 'scale.png'
            result = visualize_microtonal_scale(scale, output)

            assert result.exists()
            assert result.parent.exists()

    def test_compare_microtonal_scales_basic(self):
        """Test basic scale comparison visualization."""
        from cancrizans.microtonal import create_tuning_system_scale, TuningSystem
        from cancrizans.viz import compare_microtonal_scales

        scales = [
            create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60),
            create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'comparison.png'
            result = compare_microtonal_scales(scales, output)

            assert result.exists()
            assert result == output

            # Check it's a valid image
            img = Image.open(result)
            assert img.format == 'PNG'
            assert img.size[0] > 0
            assert img.size[1] > 0

    def test_compare_microtonal_scales_three_scales(self):
        """Test comparing three scales."""
        from cancrizans.microtonal import create_tuning_system_scale, TuningSystem
        from cancrizans.viz import compare_microtonal_scales

        scales = [
            create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60),
            create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60),
            create_tuning_system_scale(TuningSystem.WERCKMEISTER_III, tonic_midi=60)
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'comparison3.png'
            result = compare_microtonal_scales(scales, output)

            assert result.exists()

    def test_compare_microtonal_scales_single_scale(self):
        """Test comparison with single scale."""
        from cancrizans.microtonal import create_tuning_system_scale, TuningSystem
        from cancrizans.viz import compare_microtonal_scales

        scales = [create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)]

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'single.png'
            result = compare_microtonal_scales(scales, output)

            assert result.exists()

    def test_compare_microtonal_scales_world_music(self):
        """Test comparing world music scales."""
        from cancrizans.microtonal import create_world_music_scale, ScaleType
        from cancrizans.viz import compare_microtonal_scales

        scales = [
            create_world_music_scale(ScaleType.MAQAM_RAST, tonic_midi=60),
            create_world_music_scale(ScaleType.RAGA_BHAIRAV, tonic_midi=60),
            create_world_music_scale(ScaleType.PELOG, tonic_midi=60)
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'world_comparison.png'
            result = compare_microtonal_scales(scales, output)

            assert result.exists()

    def test_compare_microtonal_scales_mixed_types(self):
        """Test comparing different scale types."""
        from cancrizans.microtonal import (
            create_tuning_system_scale,
            create_world_music_scale,
            TuningSystem,
            ScaleType
        )
        from cancrizans.viz import compare_microtonal_scales

        scales = [
            create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60),
            create_world_music_scale(ScaleType.MAQAM_RAST, tonic_midi=60),
            create_tuning_system_scale(TuningSystem.BOHLEN_PIERCE, tonic_midi=60)
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'mixed.png'
            result = compare_microtonal_scales(scales, output)

            assert result.exists()

    def test_compare_microtonal_scales_high_dpi(self):
        """Test comparison with high DPI."""
        from cancrizans.microtonal import create_tuning_system_scale, TuningSystem
        from cancrizans.viz import compare_microtonal_scales

        scales = [
            create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60),
            create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'comparison_hires.png'
            result = compare_microtonal_scales(scales, output, dpi=300)

            assert result.exists()

    def test_compare_microtonal_scales_creates_dir(self):
        """Test that comparison creates output directory."""
        from cancrizans.microtonal import create_tuning_system_scale, TuningSystem
        from cancrizans.viz import compare_microtonal_scales

        scales = [
            create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60),
            create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'nested' / 'comparison.png'
            result = compare_microtonal_scales(scales, output)

            assert result.exists()
            assert result.parent.exists()

    def test_compare_microtonal_scales_many_degrees(self):
        """Test comparing scales with many degrees."""
        from cancrizans.microtonal import create_tuning_system_scale, TuningSystem
        from cancrizans.viz import compare_microtonal_scales

        scales = [
            create_tuning_system_scale(TuningSystem.EQUAL_24, tonic_midi=60),
            create_tuning_system_scale(TuningSystem.EQUAL_31, tonic_midi=60),
            create_tuning_system_scale(TuningSystem.EQUAL_53, tonic_midi=60)
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'many_degrees.png'
            result = compare_microtonal_scales(scales, output)

            assert result.exists()
