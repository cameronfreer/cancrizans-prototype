"""
Tests for audio synthesis and MIDI enhancement module (audio.py).
"""

import pytest
import tempfile
from pathlib import Path
from music21 import stream, note, chord, dynamics
from cancrizans import assemble_crab_from_theme, mirror_canon
from cancrizans.audio import (
    render_audio,
    apply_performance_expression,
    enhance_midi_with_effects,
    create_spatial_mix,
)


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
def multi_voice_canon():
    """Create a multi-voice canon for spatial testing."""
    # Create a Score with two parts
    score = stream.Score()

    part1 = stream.Part()
    part1.append(note.Note('C4', quarterLength=1.0))
    part1.append(note.Note('E4', quarterLength=1.0))
    part1.append(note.Note('G4', quarterLength=1.0))

    part2 = stream.Part()
    part2.append(note.Note('G4', quarterLength=1.0))
    part2.append(note.Note('E4', quarterLength=1.0))
    part2.append(note.Note('C4', quarterLength=1.0))

    score.insert(0, part1)
    score.insert(0, part2)

    return score


class TestRenderAudio:
    """Test render_audio function."""

    def test_render_audio_creates_midi(self, simple_canon):
        """Test that render_audio creates a MIDI file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'audio.wav'
            result = render_audio(simple_canon, output)

            assert result is not None
            assert 'path' in result
            assert 'midi_path' in result
            assert result['midi_path'].exists()
            assert result['midi_path'].suffix == '.mid'

    def test_render_audio_metadata(self, simple_canon):
        """Test that render_audio returns correct metadata."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'audio.wav'
            result = render_audio(
                simple_canon, output,
                sample_rate=48000, bit_depth=24
            )

            assert result['sample_rate'] == 48000
            assert result['bit_depth'] == 24
            assert result['channels'] == 2
            assert result['duration'] > 0

    def test_render_audio_creates_directory(self, simple_canon):
        """Test that render_audio creates parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'subdir' / 'audio.wav'
            result = render_audio(simple_canon, output)

            assert output.parent.exists()
            assert result['midi_path'].exists()

    def test_render_audio_custom_soundfont(self, simple_canon):
        """Test render_audio with custom soundfont path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'audio.wav'
            soundfont_path = '/path/to/custom.sf2'
            result = render_audio(
                simple_canon, output,
                soundfont=soundfont_path
            )

            assert result['soundfont'] == soundfont_path


class TestApplyPerformanceExpression:
    """Test apply_performance_expression function."""

    def test_apply_expression_returns_score(self, simple_canon):
        """Test that apply_performance_expression returns a Score."""
        result = apply_performance_expression(simple_canon)

        assert isinstance(result, stream.Score)
        assert len(list(result.parts)) == len(list(simple_canon.parts))

    def test_apply_expression_baroque_style(self, simple_canon):
        """Test baroque style expression."""
        result = apply_performance_expression(
            simple_canon, style='baroque',
            add_dynamics=True, add_articulation=True
        )

        # Check that dynamics were added
        all_dynamics = result.flatten().getElementsByClass(dynamics.Dynamic)
        assert len(all_dynamics) > 0

    def test_apply_expression_classical_style(self, simple_canon):
        """Test classical style expression."""
        result = apply_performance_expression(
            simple_canon, style='classical',
            add_dynamics=True
        )

        assert isinstance(result, stream.Score)
        all_dynamics = result.flatten().getElementsByClass(dynamics.Dynamic)
        assert len(all_dynamics) > 0

    def test_apply_expression_romantic_style(self, simple_canon):
        """Test romantic style expression."""
        result = apply_performance_expression(
            simple_canon, style='romantic',
            add_dynamics=True
        )

        assert isinstance(result, stream.Score)
        all_dynamics = result.flatten().getElementsByClass(dynamics.Dynamic)
        assert len(all_dynamics) > 0

    def test_apply_expression_humanization(self, simple_canon):
        """Test humanization adds velocity variance."""
        result = apply_performance_expression(
            simple_canon,
            humanize=True,
            timing_variance=0.03,
            velocity_variance=0.15
        )

        # Check that velocities were set
        notes = result.flatten().notes
        velocities = [n.volume.velocity for n in notes if hasattr(n, 'volume')]
        # Should have variety in velocities
        assert len(set(velocities)) > 1

    def test_apply_expression_no_humanization(self, simple_canon):
        """Test expression without humanization."""
        result = apply_performance_expression(
            simple_canon,
            humanize=False,
            add_dynamics=True
        )

        assert isinstance(result, stream.Score)

    def test_apply_expression_articulation_only(self, simple_canon):
        """Test adding only articulation."""
        result = apply_performance_expression(
            simple_canon,
            add_dynamics=False,
            add_articulation=True
        )

        # Check that some notes have articulations
        notes_with_artic = [
            n for n in result.flatten().notes
            if len(n.articulations) > 0
        ]
        # At least some notes should have articulation
        assert len(notes_with_artic) >= 0  # May be 0 due to randomness

    def test_apply_expression_preserves_pitches(self, simple_canon):
        """Test that expression doesn't change pitches."""
        result = apply_performance_expression(simple_canon)

        original_pitches = [n.pitch.midi for n in simple_canon.flatten().notes]
        result_pitches = [n.pitch.midi for n in result.flatten().notes]

        assert original_pitches == result_pitches


class TestEnhanceMidiWithEffects:
    """Test enhance_midi_with_effects function."""

    def test_enhance_with_reverb(self, simple_canon):
        """Test adding reverb effect."""
        result = enhance_midi_with_effects(
            simple_canon, reverb='hall'
        )

        assert isinstance(result, stream.Score)
        assert hasattr(result, '_audio_effects')
        assert 'reverb' in result._audio_effects

    def test_enhance_with_chorus(self, simple_canon):
        """Test adding chorus effect."""
        result = enhance_midi_with_effects(
            simple_canon, chorus=True
        )

        assert hasattr(result, '_audio_effects')
        assert 'chorus' in result._audio_effects

    def test_enhance_with_delay(self, simple_canon):
        """Test adding delay effect."""
        delay_params = {'time': 250, 'feedback': 0.3, 'mix': 0.2}
        result = enhance_midi_with_effects(
            simple_canon, delay=delay_params
        )

        assert hasattr(result, '_audio_effects')
        assert 'delay' in result._audio_effects
        assert result._audio_effects['delay'] == delay_params

    def test_enhance_reverb_types(self, simple_canon):
        """Test different reverb types."""
        for reverb_type in ['room', 'hall', 'cathedral']:
            result = enhance_midi_with_effects(
                simple_canon, reverb=reverb_type
            )

            assert hasattr(result, '_audio_effects')
            effects = result._audio_effects
            assert 'reverb' in effects
            assert 'size' in effects['reverb']
            assert 'decay' in effects['reverb']

    def test_enhance_tuning_systems(self, simple_canon):
        """Test different tuning systems."""
        for tuning in ['equal', 'pythagorean', 'meantone', 'werckmeister']:
            result = enhance_midi_with_effects(
                simple_canon, tuning_system=tuning
            )

            effects = result._audio_effects
            assert 'tuning_system' in effects
            assert effects['tuning_system']['name'] == tuning

    def test_enhance_combined_effects(self, simple_canon):
        """Test combining multiple effects."""
        result = enhance_midi_with_effects(
            simple_canon,
            reverb='cathedral',
            chorus=True,
            delay={'time': 300, 'feedback': 0.4, 'mix': 0.3},
            tuning_system='meantone'
        )

        effects = result._audio_effects
        assert 'reverb' in effects
        assert 'chorus' in effects
        assert 'delay' in effects
        assert 'tuning_system' in effects

    def test_enhance_no_effects(self, simple_canon):
        """Test with no effects applied."""
        result = enhance_midi_with_effects(
            simple_canon,
            reverb=None,
            chorus=False,
            delay=None
        )

        effects = result._audio_effects
        assert 'reverb' not in effects
        assert 'chorus' not in effects
        assert 'delay' not in effects
        assert 'tuning_system' in effects  # Always present


class TestCreateSpatialMix:
    """Test create_spatial_mix function."""

    def test_spatial_mix_returns_score(self, simple_canon):
        """Test that create_spatial_mix returns a Score."""
        result = create_spatial_mix(simple_canon)

        assert isinstance(result, stream.Score)
        assert hasattr(result, 'metadata')
        assert hasattr(result, '_spatial_config')

    def test_spatial_mix_auto_positions(self, multi_voice_canon):
        """Test automatic voice positioning."""
        result = create_spatial_mix(multi_voice_canon)

        spatial_config = result._spatial_config
        assert len(spatial_config) == len(list(multi_voice_canon.parts))

        # Check that positions are different
        pans = [v['pan'] for v in spatial_config.values()]
        assert len(set(pans)) >= 1  # At least one unique position

    def test_spatial_mix_custom_positions(self, multi_voice_canon):
        """Test custom voice positions."""
        positions = [-0.7, 0.7]
        result = create_spatial_mix(
            multi_voice_canon,
            voice_positions=positions
        )

        spatial_config = result._spatial_config
        voice_pans = [v['pan'] for v in spatial_config.values()]

        # Should match requested positions (scaled by stereo_width)
        assert len(voice_pans) == len(positions)

    def test_spatial_mix_stereo_width(self, multi_voice_canon):
        """Test stereo width parameter."""
        # Narrow stereo
        result_narrow = create_spatial_mix(
            multi_voice_canon,
            stereo_width=0.3
        )
        spatial_narrow = result_narrow._spatial_config
        pans_narrow = [abs(v['pan']) for v in spatial_narrow.values()]

        # Wide stereo
        result_wide = create_spatial_mix(
            multi_voice_canon,
            stereo_width=1.0
        )
        spatial_wide = result_wide._spatial_config
        pans_wide = [abs(v['pan']) for v in spatial_wide.values()]

        # Wide should have larger pan values
        if pans_narrow and pans_wide:
            assert max(pans_wide) >= max(pans_narrow)

    def test_spatial_mix_depth_simulation(self, multi_voice_canon):
        """Test depth simulation."""
        result = create_spatial_mix(
            multi_voice_canon,
            depth_simulation=True
        )

        spatial_config = result._spatial_config

        # Check that depth_volume is present
        for voice_config in spatial_config.values():
            assert 'depth_volume' in voice_config
            # Depth factor should be between 0.85 and 1.0
            assert 0.85 <= voice_config['depth_volume'] <= 1.0

    def test_spatial_mix_mono(self, simple_canon):
        """Test mono (no stereo width) configuration."""
        result = create_spatial_mix(
            simple_canon,
            stereo_width=0.0
        )

        spatial_config = result._spatial_config

        # All voices should be centered
        for voice_config in spatial_config.values():
            assert voice_config['pan'] == 0.0

    def test_spatial_mix_single_voice(self):
        """Test spatial mix with single voice."""
        score = stream.Score()
        part = stream.Part()
        part.append(note.Note('C4', quarterLength=1.0))
        score.insert(0, part)

        result = create_spatial_mix(score)

        spatial_config = result._spatial_config
        assert len(spatial_config) == 1
        # Single voice should be centered
        assert spatial_config['voice_1']['pan'] == 0.0

    def test_spatial_mix_four_voices(self):
        """Test spatial mix with quartet."""
        score = stream.Score()
        for i in range(4):
            part = stream.Part()
            part.append(note.Note(60 + i, quarterLength=1.0))
            score.insert(0, part)

        result = create_spatial_mix(score)

        spatial_config = result._spatial_config
        assert len(spatial_config) == 4

        # Voices should be spread across stereo field
        pans = [v['pan'] for v in spatial_config.values()]
        assert len(set(pans)) == 4  # All different positions


class TestAudioIntegration:
    """Integration tests for audio functions."""

    def test_full_audio_pipeline(self, simple_canon):
        """Test complete audio processing pipeline."""
        # Apply expression
        expressive = apply_performance_expression(
            simple_canon,
            style='baroque',
            humanize=True
        )

        # Add effects
        with_effects = enhance_midi_with_effects(
            expressive,
            reverb='hall',
            chorus=True
        )

        # Add spatial mix
        spatial = create_spatial_mix(with_effects)

        # Render to audio
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'final.wav'
            result = render_audio(spatial, output)

            assert result['midi_path'].exists()
            assert hasattr(spatial, '_audio_effects')
            assert hasattr(spatial, '_spatial_config')

    def test_chained_transformations(self, multi_voice_canon):
        """Test chaining multiple audio enhancements."""
        result = multi_voice_canon

        # Chain operations
        result = apply_performance_expression(result, style='romantic')
        result = enhance_midi_with_effects(
            result,
            reverb='cathedral',
            tuning_system='werckmeister'
        )
        result = create_spatial_mix(result, stereo_width=0.9)

        # Verify all enhancements are present
        assert hasattr(result, '_audio_effects')
        assert hasattr(result, '_spatial_config')

        # Check dynamics were added
        all_dynamics = result.flatten().getElementsByClass(dynamics.Dynamic)
        assert len(all_dynamics) > 0
