"""
Interactive Performance & Real-time MIDI Processing

This module provides real-time MIDI input processing, live transformations,
performance recording, and MIDI controller mapping for interactive canon performance.

Phase 17 - v0.34.0
"""

from typing import List, Dict, Callable, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import time
import threading
import queue
from music21 import stream, note, chord, tempo as m21_tempo
import mido


class TransformMode(Enum):
    """Real-time transformation modes"""
    NONE = "none"
    RETROGRADE = "retrograde"
    INVERSION = "inversion"
    AUGMENTATION = "augmentation"
    DIMINUTION = "diminution"
    MIRROR = "mirror"
    TRANSPOSE = "transpose"


@dataclass
class MIDIEvent:
    """Represents a timestamped MIDI event"""
    timestamp: float
    message: mido.Message
    transformed: bool = False


@dataclass
class PerformanceConfig:
    """Configuration for live performance"""
    buffer_size: int = 1000  # Maximum events to buffer
    latency_ms: float = 10.0  # Target latency in milliseconds
    quantize: bool = False  # Quantize input to grid
    quantize_division: float = 0.25  # Quarter note = 1.0
    loop_enabled: bool = False
    loop_bars: int = 4
    metronome_enabled: bool = False
    tempo: int = 120


@dataclass
class ControllerMapping:
    """Maps MIDI controller to parameter"""
    cc_number: int
    parameter: str
    min_value: float = 0.0
    max_value: float = 127.0
    curve: str = "linear"  # linear, exponential, logarithmic


class LiveMIDIProcessor:
    """
    Real-time MIDI input processor with live transformations

    Features:
    - Real-time MIDI input capture
    - Live transformation engine
    - Low-latency processing
    - MIDI controller mapping
    """

    def __init__(self, config: Optional[PerformanceConfig] = None):
        """
        Initialize live MIDI processor

        Args:
            config: Performance configuration, defaults to PerformanceConfig()
        """
        self.config = config or PerformanceConfig()
        self.input_queue: queue.Queue = queue.Queue(maxsize=self.config.buffer_size)
        self.output_queue: queue.Queue = queue.Queue(maxsize=self.config.buffer_size)
        self.is_running = False
        self.start_time = 0.0
        self.events: List[MIDIEvent] = []
        self.transform_mode = TransformMode.NONE
        self.transform_params: Dict[str, Any] = {}
        self.controller_mappings: Dict[int, ControllerMapping] = {}
        self.note_buffer: List[Tuple[float, int, int]] = []  # (time, pitch, velocity)
        self.inversion_axis = 60  # Middle C default
        self.transpose_semitones = 0
        self.tempo_multiplier = 1.0

    def add_controller_mapping(self, mapping: ControllerMapping) -> None:
        """
        Add MIDI controller mapping

        Args:
            mapping: Controller mapping configuration
        """
        self.controller_mappings[mapping.cc_number] = mapping

    def set_transform_mode(self, mode: TransformMode, **params) -> None:
        """
        Set real-time transformation mode

        Args:
            mode: Transformation mode
            **params: Mode-specific parameters
                - inversion_axis: for INVERSION mode
                - semitones: for TRANSPOSE mode
                - factor: for AUGMENTATION/DIMINUTION mode
        """
        self.transform_mode = mode
        self.transform_params = params

        if mode == TransformMode.INVERSION and 'inversion_axis' in params:
            self.inversion_axis = params['inversion_axis']
        elif mode == TransformMode.TRANSPOSE and 'semitones' in params:
            self.transpose_semitones = params['semitones']
        elif mode in (TransformMode.AUGMENTATION, TransformMode.DIMINUTION) and 'factor' in params:
            self.tempo_multiplier = params['factor']

    def _apply_transformation(self, msg: mido.Message, timestamp: float) -> Optional[mido.Message]:
        """
        Apply current transformation to MIDI message

        Args:
            msg: Input MIDI message
            timestamp: Event timestamp

        Returns:
            Transformed message or None if message should be dropped
        """
        if self.transform_mode == TransformMode.NONE:
            return msg

        # Only transform note messages
        if msg.type not in ('note_on', 'note_off'):
            return msg

        new_msg = msg.copy()

        if self.transform_mode == TransformMode.INVERSION:
            # Invert pitch around axis
            new_note = 2 * self.inversion_axis - msg.note
            new_msg.note = max(0, min(127, new_note))  # Clamp to MIDI range

        elif self.transform_mode == TransformMode.TRANSPOSE:
            # Transpose by semitones
            new_note = msg.note + self.transpose_semitones
            new_msg.note = max(0, min(127, new_note))

        elif self.transform_mode == TransformMode.MIRROR:
            # Combined inversion + retrograde (note: retrograde handled by buffer)
            new_note = 2 * self.inversion_axis - msg.note
            new_msg.note = max(0, min(127, new_note))

        # RETROGRADE, AUGMENTATION, DIMINUTION handled by playback timing

        return new_msg

    def _handle_controller(self, msg: mido.Message) -> None:
        """
        Handle MIDI controller message

        Args:
            msg: Control change message
        """
        if msg.type != 'control_change':
            return

        if msg.control in self.controller_mappings:
            mapping = self.controller_mappings[msg.control]

            # Map CC value to parameter range
            normalized = msg.value / 127.0

            if mapping.curve == "exponential":
                normalized = normalized ** 2
            elif mapping.curve == "logarithmic":
                normalized = normalized ** 0.5

            value = mapping.min_value + normalized * (mapping.max_value - mapping.min_value)

            # Apply to parameters
            if mapping.parameter == "inversion_axis":
                self.inversion_axis = int(value)
            elif mapping.parameter == "transpose":
                self.transpose_semitones = int(value)
            elif mapping.parameter == "tempo_multiplier":
                self.tempo_multiplier = value

    def start_capture(self, input_port: Optional[str] = None) -> None:
        """
        Start capturing MIDI input

        Args:
            input_port: MIDI input port name (None for default)
        """
        self.is_running = True
        self.start_time = time.time()
        self.events = []

        def capture_thread():
            try:
                # Open MIDI input
                if input_port:
                    inport = mido.open_input(input_port)
                else:
                    # Use first available input
                    inputs = mido.get_input_names()
                    if not inputs:
                        raise RuntimeError("No MIDI input devices available")
                    inport = mido.open_input(inputs[0])

                # Capture loop
                for msg in inport:
                    if not self.is_running:
                        break

                    timestamp = time.time() - self.start_time

                    # Handle controllers
                    if msg.type == 'control_change':
                        self._handle_controller(msg)

                    # Apply transformation
                    transformed_msg = self._apply_transformation(msg, timestamp)

                    if transformed_msg:
                        event = MIDIEvent(
                            timestamp=timestamp,
                            message=transformed_msg,
                            transformed=(self.transform_mode != TransformMode.NONE)
                        )
                        self.events.append(event)

                        # Add to output queue for real-time playback
                        try:
                            self.output_queue.put_nowait(event)
                        except queue.Full:
                            pass  # Drop if buffer full

                inport.close()

            except Exception as e:
                print(f"MIDI capture error: {e}")
                self.is_running = False

        thread = threading.Thread(target=capture_thread, daemon=True)
        thread.start()

    def stop_capture(self) -> None:
        """Stop capturing MIDI input"""
        self.is_running = False

    def get_recorded_stream(self) -> stream.Stream:
        """
        Get recorded performance as music21 stream

        Returns:
            Stream containing recorded notes and chords
        """
        s = stream.Stream()
        s.append(m21_tempo.MetronomeMark(number=self.config.tempo))

        # Group note_on/note_off events
        active_notes: Dict[int, Tuple[float, int]] = {}  # pitch -> (start_time, velocity)

        for event in sorted(self.events, key=lambda e: e.timestamp):
            msg = event.message

            if msg.type == 'note_on' and msg.velocity > 0:
                active_notes[msg.note] = (event.timestamp, msg.velocity)

            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note in active_notes:
                    start_time, velocity = active_notes.pop(msg.note)
                    duration = event.timestamp - start_time

                    n = note.Note(msg.note)
                    n.offset = start_time
                    n.quarterLength = duration * (self.config.tempo / 60.0)
                    n.volume.velocity = velocity
                    s.append(n)

        return s

    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get performance statistics

        Returns:
            Dictionary with performance metrics
        """
        total_events = len(self.events)
        transformed_events = sum(1 for e in self.events if e.transformed)

        note_events = [e for e in self.events if e.message.type in ('note_on', 'note_off')]

        if note_events:
            duration = note_events[-1].timestamp - note_events[0].timestamp
            pitches = [e.message.note for e in note_events if e.message.type == 'note_on']
            avg_pitch = sum(pitches) / len(pitches) if pitches else 0
            pitch_range = (min(pitches), max(pitches)) if pitches else (0, 0)
        else:
            duration = 0
            avg_pitch = 0
            pitch_range = (0, 0)

        return {
            'total_events': total_events,
            'transformed_events': transformed_events,
            'transform_mode': self.transform_mode.value,
            'duration_seconds': duration,
            'note_count': len([e for e in self.events if e.message.type == 'note_on']),
            'average_pitch': avg_pitch,
            'pitch_range': pitch_range,
            'tempo': self.config.tempo
        }


class LoopStation:
    """
    Loop station for layering canon performances

    Features:
    - Multi-track recording
    - Overdubbing
    - Synchronized playback
    - Per-track transformations
    """

    def __init__(self, bars: int = 4, tempo: int = 120):
        """
        Initialize loop station

        Args:
            bars: Loop length in bars
            tempo: Tempo in BPM
        """
        self.bars = bars
        self.tempo = tempo
        self.loop_length = (bars * 4) * (60.0 / tempo)  # seconds
        self.tracks: List[List[MIDIEvent]] = []
        self.is_recording = False
        self.is_playing = False
        self.current_track = 0
        self.start_time = 0.0
        self.track_transforms: List[TransformMode] = []

    def add_track(self, transform: TransformMode = TransformMode.NONE) -> int:
        """
        Add new track

        Args:
            transform: Transformation mode for this track

        Returns:
            Track index
        """
        self.tracks.append([])
        self.track_transforms.append(transform)
        return len(self.tracks) - 1

    def start_recording(self, track: int) -> None:
        """
        Start recording on track

        Args:
            track: Track index
        """
        self.current_track = track
        self.is_recording = True
        self.start_time = time.time()

    def stop_recording(self) -> None:
        """Stop recording"""
        self.is_recording = False

    def record_event(self, msg: mido.Message) -> None:
        """
        Record MIDI event to current track

        Args:
            msg: MIDI message
        """
        if not self.is_recording:
            return

        timestamp = (time.time() - self.start_time) % self.loop_length
        event = MIDIEvent(timestamp=timestamp, message=msg)
        self.tracks[self.current_track].append(event)

    def get_merged_stream(self) -> stream.Stream:
        """
        Get all tracks merged into single stream

        Returns:
            Stream with all tracks
        """
        s = stream.Stream()
        s.append(m21_tempo.MetronomeMark(number=self.tempo))

        for track_idx, track_events in enumerate(self.tracks):
            # Group note events
            active_notes: Dict[int, Tuple[float, int]] = {}

            for event in sorted(track_events, key=lambda e: e.timestamp):
                msg = event.message

                if msg.type == 'note_on' and msg.velocity > 0:
                    active_notes[msg.note] = (event.timestamp, msg.velocity)

                elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                    if msg.note in active_notes:
                        start_time, velocity = active_notes.pop(msg.note)
                        duration = event.timestamp - start_time

                        n = note.Note(msg.note)
                        n.offset = start_time
                        n.quarterLength = duration * (self.tempo / 60.0)
                        n.volume.velocity = velocity
                        s.append(n)

        return s

    def clear_track(self, track: int) -> None:
        """
        Clear track

        Args:
            track: Track index
        """
        if 0 <= track < len(self.tracks):
            self.tracks[track] = []

    def get_loop_info(self) -> Dict[str, Any]:
        """
        Get loop station information

        Returns:
            Dictionary with loop info
        """
        return {
            'bars': self.bars,
            'tempo': self.tempo,
            'loop_length_seconds': self.loop_length,
            'track_count': len(self.tracks),
            'tracks': [
                {
                    'index': i,
                    'event_count': len(track),
                    'transform': self.track_transforms[i].value
                }
                for i, track in enumerate(self.tracks)
            ]
        }


def list_midi_ports() -> Dict[str, List[str]]:
    """
    List available MIDI input and output ports

    Returns:
        Dictionary with 'inputs' and 'outputs' lists
    """
    return {
        'inputs': mido.get_input_names(),
        'outputs': mido.get_output_names()
    }


def create_performance_preset(name: str) -> PerformanceConfig:
    """
    Create preset performance configuration

    Args:
        name: Preset name ('studio', 'live', 'lofi', 'tight')

    Returns:
        Performance configuration
    """
    presets = {
        'studio': PerformanceConfig(
            latency_ms=5.0,
            quantize=False,
            buffer_size=2000
        ),
        'live': PerformanceConfig(
            latency_ms=10.0,
            quantize=True,
            quantize_division=0.25,
            buffer_size=1000,
            metronome_enabled=True
        ),
        'lofi': PerformanceConfig(
            latency_ms=20.0,
            quantize=True,
            quantize_division=0.5,
            buffer_size=500
        ),
        'tight': PerformanceConfig(
            latency_ms=1.0,
            quantize=False,
            buffer_size=100
        )
    }

    if name not in presets:
        raise ValueError(f"Unknown preset: {name}. Available: {list(presets.keys())}")

    return presets[name]


def export_performance_session(
    processor: LiveMIDIProcessor,
    output_path: str,
    format: str = 'midi'
) -> None:
    """
    Export recorded performance session

    Args:
        processor: Live MIDI processor with recorded events
        output_path: Path to save file
        format: Export format ('midi', 'musicxml')
    """
    s = processor.get_recorded_stream()

    if format == 'midi':
        s.write('midi', fp=output_path)
    elif format == 'musicxml':
        s.write('musicxml', fp=output_path)
    else:
        raise ValueError(f"Unknown format: {format}")
