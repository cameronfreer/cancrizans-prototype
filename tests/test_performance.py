"""
Tests for interactive performance and real-time MIDI processing

Phase 17 - v0.34.0
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import time
from music21 import stream, note
import mido

from cancrizans.performance import (
    LiveMIDIProcessor,
    LoopStation,
    TransformMode,
    PerformanceConfig,
    ControllerMapping,
    MIDIEvent,
    list_midi_ports,
    create_performance_preset,
    export_performance_session
)


class TestMIDIEvent:
    """Test MIDIEvent dataclass"""

    def test_creation(self):
        """Test creating MIDI event"""
        msg = mido.Message('note_on', note=60, velocity=64)
        event = MIDIEvent(timestamp=1.5, message=msg)

        assert event.timestamp == 1.5
        assert event.message.type == 'note_on'
        assert event.message.note == 60
        assert event.transformed is False

    def test_transformed_flag(self):
        """Test transformed flag"""
        msg = mido.Message('note_on', note=60, velocity=64)
        event = MIDIEvent(timestamp=1.0, message=msg, transformed=True)

        assert event.transformed is True


class TestPerformanceConfig:
    """Test PerformanceConfig dataclass"""

    def test_defaults(self):
        """Test default configuration"""
        config = PerformanceConfig()

        assert config.buffer_size == 1000
        assert config.latency_ms == 10.0
        assert config.quantize is False
        assert config.loop_enabled is False
        assert config.tempo == 120

    def test_custom_config(self):
        """Test custom configuration"""
        config = PerformanceConfig(
            buffer_size=500,
            tempo=140,
            quantize=True,
            quantize_division=0.5
        )

        assert config.buffer_size == 500
        assert config.tempo == 140
        assert config.quantize is True
        assert config.quantize_division == 0.5


class TestControllerMapping:
    """Test ControllerMapping dataclass"""

    def test_creation(self):
        """Test creating controller mapping"""
        mapping = ControllerMapping(
            cc_number=1,
            parameter="inversion_axis",
            min_value=48.0,
            max_value=72.0,
            curve="linear"
        )

        assert mapping.cc_number == 1
        assert mapping.parameter == "inversion_axis"
        assert mapping.min_value == 48.0
        assert mapping.max_value == 72.0
        assert mapping.curve == "linear"


class TestLiveMIDIProcessor:
    """Test LiveMIDIProcessor class"""

    def test_initialization(self):
        """Test processor initialization"""
        processor = LiveMIDIProcessor()

        assert processor.config.tempo == 120
        assert processor.transform_mode == TransformMode.NONE
        assert processor.is_running is False
        assert len(processor.events) == 0

    def test_custom_config(self):
        """Test initialization with custom config"""
        config = PerformanceConfig(tempo=140, buffer_size=500)
        processor = LiveMIDIProcessor(config=config)

        assert processor.config.tempo == 140
        assert processor.config.buffer_size == 500

    def test_set_transform_mode_inversion(self):
        """Test setting inversion transform mode"""
        processor = LiveMIDIProcessor()
        processor.set_transform_mode(TransformMode.INVERSION, inversion_axis=64)

        assert processor.transform_mode == TransformMode.INVERSION
        assert processor.inversion_axis == 64

    def test_set_transform_mode_transpose(self):
        """Test setting transpose transform mode"""
        processor = LiveMIDIProcessor()
        processor.set_transform_mode(TransformMode.TRANSPOSE, semitones=5)

        assert processor.transform_mode == TransformMode.TRANSPOSE
        assert processor.transpose_semitones == 5

    def test_apply_transformation_none(self):
        """Test no transformation"""
        processor = LiveMIDIProcessor()
        msg = mido.Message('note_on', note=60, velocity=64)

        result = processor._apply_transformation(msg, 1.0)

        assert result.note == 60

    def test_apply_transformation_inversion(self):
        """Test inversion transformation"""
        processor = LiveMIDIProcessor()
        processor.set_transform_mode(TransformMode.INVERSION, inversion_axis=60)

        msg = mido.Message('note_on', note=64, velocity=64)
        result = processor._apply_transformation(msg, 1.0)

        # 64 inverted around 60 = 2*60 - 64 = 56
        assert result.note == 56

    def test_apply_transformation_transpose(self):
        """Test transpose transformation"""
        processor = LiveMIDIProcessor()
        processor.set_transform_mode(TransformMode.TRANSPOSE, semitones=7)

        msg = mido.Message('note_on', note=60, velocity=64)
        result = processor._apply_transformation(msg, 1.0)

        assert result.note == 67

    def test_apply_transformation_mirror(self):
        """Test mirror transformation"""
        processor = LiveMIDIProcessor()
        processor.set_transform_mode(TransformMode.MIRROR, inversion_axis=60)

        msg = mido.Message('note_on', note=65, velocity=64)
        result = processor._apply_transformation(msg, 1.0)

        # Mirror = inversion: 2*60 - 65 = 55
        assert result.note == 55

    def test_apply_transformation_clamping(self):
        """Test pitch clamping to MIDI range"""
        processor = LiveMIDIProcessor()
        processor.set_transform_mode(TransformMode.TRANSPOSE, semitones=100)

        msg = mido.Message('note_on', note=60, velocity=64)
        result = processor._apply_transformation(msg, 1.0)

        # 60 + 100 = 160, clamped to 127
        assert result.note == 127

    def test_apply_transformation_non_note(self):
        """Test transformation passes through non-note messages"""
        processor = LiveMIDIProcessor()
        processor.set_transform_mode(TransformMode.INVERSION, inversion_axis=60)

        msg = mido.Message('control_change', control=1, value=64)
        result = processor._apply_transformation(msg, 1.0)

        assert result.type == 'control_change'
        assert result.control == 1

    def test_add_controller_mapping(self):
        """Test adding controller mapping"""
        processor = LiveMIDIProcessor()
        mapping = ControllerMapping(
            cc_number=1,
            parameter="inversion_axis",
            min_value=48.0,
            max_value=72.0
        )

        processor.add_controller_mapping(mapping)

        assert 1 in processor.controller_mappings
        assert processor.controller_mappings[1].parameter == "inversion_axis"

    def test_handle_controller_linear(self):
        """Test handling controller with linear curve"""
        processor = LiveMIDIProcessor()
        mapping = ControllerMapping(
            cc_number=1,
            parameter="inversion_axis",
            min_value=48.0,
            max_value=72.0,
            curve="linear"
        )
        processor.add_controller_mapping(mapping)

        # CC value 64 (halfway) should map to 60 (halfway between 48 and 72)
        msg = mido.Message('control_change', control=1, value=64)
        processor._handle_controller(msg)

        assert abs(processor.inversion_axis - 60) < 1

    def test_handle_controller_transpose(self):
        """Test controller mapping to transpose"""
        processor = LiveMIDIProcessor()
        mapping = ControllerMapping(
            cc_number=2,
            parameter="transpose",
            min_value=-12.0,
            max_value=12.0
        )
        processor.add_controller_mapping(mapping)

        # CC value 127 (max) should map to 12
        msg = mido.Message('control_change', control=2, value=127)
        processor._handle_controller(msg)

        assert processor.transpose_semitones == 12

    def test_get_recorded_stream_empty(self):
        """Test getting stream from empty recording"""
        processor = LiveMIDIProcessor()
        s = processor.get_recorded_stream()

        assert isinstance(s, stream.Stream)
        assert len([n for n in s.flatten().notes]) == 0

    def test_get_recorded_stream_with_notes(self):
        """Test getting stream with recorded notes"""
        processor = LiveMIDIProcessor()

        # Simulate recorded events
        processor.events = [
            MIDIEvent(0.0, mido.Message('note_on', note=60, velocity=64)),
            MIDIEvent(0.5, mido.Message('note_off', note=60, velocity=0)),
            MIDIEvent(0.5, mido.Message('note_on', note=64, velocity=64)),
            MIDIEvent(1.0, mido.Message('note_off', note=64, velocity=0))
        ]

        s = processor.get_recorded_stream()
        notes = list(s.flatten().notes)

        assert len(notes) == 2
        assert notes[0].pitch.midi == 60
        assert notes[1].pitch.midi == 64

    def test_get_performance_metrics_empty(self):
        """Test metrics for empty performance"""
        processor = LiveMIDIProcessor()
        metrics = processor.get_performance_metrics()

        assert metrics['total_events'] == 0
        assert metrics['note_count'] == 0
        assert metrics['transform_mode'] == 'none'

    def test_get_performance_metrics_with_events(self):
        """Test metrics with recorded events"""
        processor = LiveMIDIProcessor()
        processor.transform_mode = TransformMode.INVERSION

        processor.events = [
            MIDIEvent(0.0, mido.Message('note_on', note=60, velocity=64), transformed=True),
            MIDIEvent(0.5, mido.Message('note_off', note=60, velocity=0)),
            MIDIEvent(0.5, mido.Message('note_on', note=64, velocity=64), transformed=True),
            MIDIEvent(1.5, mido.Message('note_off', note=64, velocity=0))
        ]

        metrics = processor.get_performance_metrics()

        assert metrics['total_events'] == 4
        assert metrics['transformed_events'] == 2
        assert metrics['note_count'] == 2
        assert metrics['transform_mode'] == 'inversion'
        assert metrics['average_pitch'] == 62.0
        assert metrics['pitch_range'] == (60, 64)

    def test_stop_capture(self):
        """Test stopping capture"""
        processor = LiveMIDIProcessor()
        processor.is_running = True

        processor.stop_capture()

        assert processor.is_running is False


class TestLoopStation:
    """Test LoopStation class"""

    def test_initialization(self):
        """Test loop station initialization"""
        loop = LoopStation(bars=4, tempo=120)

        assert loop.bars == 4
        assert loop.tempo == 120
        assert len(loop.tracks) == 0
        assert loop.is_recording is False

    def test_loop_length_calculation(self):
        """Test loop length calculation"""
        loop = LoopStation(bars=4, tempo=120)

        # 4 bars * 4 beats/bar * 0.5 seconds/beat = 8 seconds
        assert loop.loop_length == 8.0

    def test_add_track(self):
        """Test adding track"""
        loop = LoopStation()
        track_idx = loop.add_track(TransformMode.INVERSION)

        assert track_idx == 0
        assert len(loop.tracks) == 1
        assert loop.track_transforms[0] == TransformMode.INVERSION

    def test_add_multiple_tracks(self):
        """Test adding multiple tracks"""
        loop = LoopStation()

        idx1 = loop.add_track(TransformMode.NONE)
        idx2 = loop.add_track(TransformMode.RETROGRADE)
        idx3 = loop.add_track(TransformMode.TRANSPOSE)

        assert idx1 == 0
        assert idx2 == 1
        assert idx3 == 2
        assert len(loop.tracks) == 3

    def test_start_recording(self):
        """Test starting recording"""
        loop = LoopStation()
        loop.add_track()

        loop.start_recording(0)

        assert loop.is_recording is True
        assert loop.current_track == 0

    def test_stop_recording(self):
        """Test stopping recording"""
        loop = LoopStation()
        loop.add_track()
        loop.start_recording(0)

        loop.stop_recording()

        assert loop.is_recording is False

    def test_record_event(self):
        """Test recording event"""
        loop = LoopStation()
        loop.add_track()
        loop.start_recording(0)

        msg = mido.Message('note_on', note=60, velocity=64)
        loop.record_event(msg)

        assert len(loop.tracks[0]) == 1
        assert loop.tracks[0][0].message.note == 60

    def test_record_event_not_recording(self):
        """Test recording when not recording does nothing"""
        loop = LoopStation()
        loop.add_track()

        msg = mido.Message('note_on', note=60, velocity=64)
        loop.record_event(msg)

        assert len(loop.tracks[0]) == 0

    def test_clear_track(self):
        """Test clearing track"""
        loop = LoopStation()
        loop.add_track()
        loop.start_recording(0)

        msg = mido.Message('note_on', note=60, velocity=64)
        loop.record_event(msg)
        loop.stop_recording()

        assert len(loop.tracks[0]) == 1

        loop.clear_track(0)

        assert len(loop.tracks[0]) == 0

    def test_clear_invalid_track(self):
        """Test clearing invalid track does nothing"""
        loop = LoopStation()
        loop.add_track()

        loop.clear_track(5)  # Invalid index

        # Should not raise error

    def test_get_merged_stream_empty(self):
        """Test getting merged stream with no tracks"""
        loop = LoopStation()
        s = loop.get_merged_stream()

        assert isinstance(s, stream.Stream)
        assert len(list(s.flatten().notes)) == 0

    def test_get_merged_stream_with_notes(self):
        """Test getting merged stream with recorded notes"""
        loop = LoopStation()
        loop.add_track()
        loop.tracks[0] = [
            MIDIEvent(0.0, mido.Message('note_on', note=60, velocity=64)),
            MIDIEvent(0.5, mido.Message('note_off', note=60, velocity=0))
        ]

        s = loop.get_merged_stream()
        notes = list(s.flatten().notes)

        assert len(notes) == 1
        assert notes[0].pitch.midi == 60

    def test_get_loop_info(self):
        """Test getting loop information"""
        loop = LoopStation(bars=4, tempo=140)
        loop.add_track(TransformMode.INVERSION)
        loop.add_track(TransformMode.RETROGRADE)

        info = loop.get_loop_info()

        assert info['bars'] == 4
        assert info['tempo'] == 140
        assert info['track_count'] == 2
        assert len(info['tracks']) == 2
        assert info['tracks'][0]['transform'] == 'inversion'
        assert info['tracks'][1]['transform'] == 'retrograde'


class TestUtilityFunctions:
    """Test utility functions"""

    @patch('mido.get_input_names')
    @patch('mido.get_output_names')
    def test_list_midi_ports(self, mock_outputs, mock_inputs):
        """Test listing MIDI ports"""
        mock_inputs.return_value = ['Input 1', 'Input 2']
        mock_outputs.return_value = ['Output 1', 'Output 2']

        ports = list_midi_ports()

        assert 'inputs' in ports
        assert 'outputs' in ports
        assert len(ports['inputs']) == 2
        assert len(ports['outputs']) == 2

    def test_create_performance_preset_studio(self):
        """Test creating studio preset"""
        config = create_performance_preset('studio')

        assert config.latency_ms == 5.0
        assert config.quantize is False
        assert config.buffer_size == 2000

    def test_create_performance_preset_live(self):
        """Test creating live preset"""
        config = create_performance_preset('live')

        assert config.latency_ms == 10.0
        assert config.quantize is True
        assert config.metronome_enabled is True

    def test_create_performance_preset_lofi(self):
        """Test creating lofi preset"""
        config = create_performance_preset('lofi')

        assert config.latency_ms == 20.0
        assert config.quantize_division == 0.5

    def test_create_performance_preset_tight(self):
        """Test creating tight preset"""
        config = create_performance_preset('tight')

        assert config.latency_ms == 1.0
        assert config.buffer_size == 100

    def test_create_performance_preset_invalid(self):
        """Test creating invalid preset raises error"""
        with pytest.raises(ValueError, match="Unknown preset"):
            create_performance_preset('invalid')

    def test_export_performance_session_midi(self, tmp_path):
        """Test exporting performance session as MIDI"""
        processor = LiveMIDIProcessor()
        processor.events = [
            MIDIEvent(0.0, mido.Message('note_on', note=60, velocity=64)),
            MIDIEvent(0.5, mido.Message('note_off', note=60, velocity=0))
        ]

        output_path = tmp_path / "test_performance.mid"
        export_performance_session(processor, str(output_path), format='midi')

        assert output_path.exists()

    def test_export_performance_session_musicxml(self, tmp_path):
        """Test exporting performance session as MusicXML"""
        processor = LiveMIDIProcessor()
        processor.events = [
            MIDIEvent(0.0, mido.Message('note_on', note=60, velocity=64)),
            MIDIEvent(0.5, mido.Message('note_off', note=60, velocity=0))
        ]

        output_path = tmp_path / "test_performance.musicxml"
        export_performance_session(processor, str(output_path), format='musicxml')

        assert output_path.exists()

    def test_export_performance_session_invalid_format(self):
        """Test exporting with invalid format raises error"""
        processor = LiveMIDIProcessor()

        with pytest.raises(ValueError, match="Unknown format"):
            export_performance_session(processor, "/tmp/test.txt", format='invalid')


class TestTransformMode:
    """Test TransformMode enum"""

    def test_enum_values(self):
        """Test enum values"""
        assert TransformMode.NONE.value == "none"
        assert TransformMode.RETROGRADE.value == "retrograde"
        assert TransformMode.INVERSION.value == "inversion"
        assert TransformMode.AUGMENTATION.value == "augmentation"
        assert TransformMode.DIMINUTION.value == "diminution"
        assert TransformMode.MIRROR.value == "mirror"
        assert TransformMode.TRANSPOSE.value == "transpose"
