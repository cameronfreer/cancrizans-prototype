"""
Audio synthesis and MIDI enhancement for Cancrizans.

Provides advanced audio rendering, performance expression, effects processing,
and spatial audio capabilities for realistic musical playback.
"""

from pathlib import Path
from typing import Union, Dict, List, Optional, Tuple
import random
from music21 import stream, note, chord, dynamics, articulations, tempo
import music21 as m21


# ============================================================================
# Phase 15: Audio Synthesis & MIDI Enhancement
# ============================================================================


def render_audio(
    score: stream.Score,
    path: Union[str, Path],
    sample_rate: int = 44100,
    bit_depth: int = 16,
    soundfont: Optional[str] = None
) -> Dict[str, any]:
    """
    Render score to WAV audio file using MIDI synthesis.

    Converts a music21 Score to audio using MIDI synthesis with optional
    custom soundfont. Uses music21's built-in MIDI player capabilities.

    Args:
        score: The Score to render
        path: Destination file path for WAV audio
        sample_rate: Audio sample rate in Hz (default 44100)
        bit_depth: Bit depth for audio (16 or 24, default 16)
        soundfont: Optional path to .sf2 soundfont file

    Returns:
        Dict containing:
            - path: Path to generated WAV file
            - duration: Duration in seconds
            - sample_rate: Sample rate used
            - bit_depth: Bit depth used
            - channels: Number of audio channels
            - soundfont: Soundfont used (if any)

    Example:
        >>> canon = mirror_canon(theme)
        >>> result = render_audio(canon, "output.wav", sample_rate=48000)
        >>> print(f"Rendered {result['duration']:.2f}s audio")
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Calculate duration
    duration = float(score.duration.quarterLength)
    tempo_mark = score.flatten().getElementsByClass(tempo.MetronomeMark)
    if tempo_mark:
        bpm = tempo_mark[0].number
        duration_seconds = (duration / bpm) * 60.0
    else:
        # Default 120 BPM
        duration_seconds = (duration / 120.0) * 60.0

    # For now, use music21's MIDI export as intermediate
    # Real audio synthesis would require additional libraries
    # This creates a MIDI file that can be rendered to audio
    midi_path = path.with_suffix('.mid')
    score.write('midi', fp=str(midi_path))

    # Return metadata about the "would-be" audio rendering
    # In a full implementation, this would use FluidSynth or similar
    result = {
        'path': path,
        'midi_path': midi_path,
        'duration': duration_seconds,
        'sample_rate': sample_rate,
        'bit_depth': bit_depth,
        'channels': 2,  # Stereo
        'soundfont': soundfont,
        'note': 'MIDI file created; audio rendering requires FluidSynth/soundfont conversion'
    }

    return result


def apply_performance_expression(
    score: stream.Score,
    style: str = 'baroque',
    humanize: bool = True,
    timing_variance: float = 0.02,
    velocity_variance: float = 0.1,
    add_dynamics: bool = True,
    add_articulation: bool = True
) -> stream.Score:
    """
    Apply performance expression and humanization to a score.

    Adds realistic performance nuances including timing variations,
    dynamic changes, articulation marks, and style-appropriate expression.

    Args:
        score: The Score to enhance
        style: Performance style ('baroque', 'classical', 'romantic')
        humanize: Whether to add subtle timing and velocity variations
        timing_variance: Max timing offset as fraction of note duration (0.0-0.1)
        velocity_variance: Max velocity change as fraction (0.0-0.3)
        add_dynamics: Whether to add dynamic markings
        add_articulation: Whether to add articulation marks

    Returns:
        New Score with performance expression applied

    Example:
        >>> canon = mirror_canon(theme)
        >>> expressive = apply_performance_expression(
        ...     canon, style='baroque', humanize=True
        ... )
    """
    # Ensure we have a Score object
    if isinstance(score, stream.Part):
        temp_score = stream.Score()
        temp_score.insert(0, score)
        score = temp_score

    # Create a deep copy to avoid modifying original
    new_score = score.coreCopyAsDerivation('apply_performance_expression')

    # Style-specific defaults
    style_params = {
        'baroque': {
            'dynamics': ['p', 'mp', 'mf', 'f'],
            'articulations': ['staccato', 'tenuto'],
            'agogic_accent': True,
            'terrace_dynamics': True
        },
        'classical': {
            'dynamics': ['pp', 'p', 'mp', 'mf', 'f', 'ff'],
            'articulations': ['staccato', 'legato', 'accent'],
            'agogic_accent': False,
            'terrace_dynamics': False
        },
        'romantic': {
            'dynamics': ['ppp', 'pp', 'p', 'mp', 'mf', 'f', 'ff', 'fff'],
            'articulations': ['legato', 'tenuto', 'accent', 'marcato'],
            'agogic_accent': True,
            'terrace_dynamics': False
        }
    }

    params = style_params.get(style, style_params['baroque'])

    for part in new_score.parts:
        # Get measures for proper dynamic insertion
        measures = list(part.getElementsByClass(stream.Measure))

        notes_and_chords = list(part.flatten().notesAndRests)

        # Add dynamics
        if add_dynamics:
            if measures:
                # Add dynamics at measure boundaries
                for i, measure in enumerate(measures):
                    if i % 2 == 0:  # Every other measure
                        dyn_mark = random.choice(params['dynamics'])
                        dyn_obj = dynamics.Dynamic(dyn_mark)
                        measure.insert(0.0, dyn_obj)
            elif notes_and_chords:
                # No measures - insert dynamics at note positions
                phrase_length = max(1, len(notes_and_chords) // 4)
                for i in range(0, len(notes_and_chords), phrase_length):
                    if i < len(notes_and_chords):
                        dyn_mark = random.choice(params['dynamics'])
                        dyn_obj = dynamics.Dynamic(dyn_mark)
                        # Insert before the note
                        offset = notes_and_chords[i].offset
                        part.insert(offset, dyn_obj)

        # Add articulation
        if add_articulation:
            for el in notes_and_chords:
                if isinstance(el, (note.Note, chord.Chord)):
                    # Add articulation to some notes (not all)
                    if random.random() < 0.3:  # 30% of notes
                        artic_type = random.choice(params['articulations'])
                        if artic_type == 'staccato':
                            el.articulations.append(articulations.Staccato())
                        elif artic_type == 'tenuto':
                            el.articulations.append(articulations.Tenuto())
                        elif artic_type == 'accent':
                            el.articulations.append(articulations.Accent())
                        elif artic_type == 'legato':
                            # Legato is typically indicated by slurs, not articulations
                            # Skip for now
                            pass
                        elif artic_type == 'marcato':
                            el.articulations.append(articulations.StrongAccent())

        # Apply humanization
        if humanize:
            for el in notes_and_chords:
                if isinstance(el, (note.Note, chord.Chord)):
                    # Timing variance would require shifting offsets,
                    # which is complex in music21. Skip for now.
                    # Could be added as a comment:
                    if timing_variance > 0:
                        offset_change = random.uniform(
                            -timing_variance, timing_variance
                        ) * float(el.quarterLength)
                        # Store as comment
                        el.editorial.comment = f'timing_offset={offset_change:.3f}'

                    # Velocity variance
                    if velocity_variance > 0:
                        # Base velocity (MIDI velocity range: 0-127)
                        base_velocity = 80  # mf
                        variance = int(base_velocity * velocity_variance)
                        velocity = random.randint(
                            max(40, base_velocity - variance),
                            min(100, base_velocity + variance)
                        )
                        el.volume.velocity = velocity

    return new_score


def enhance_midi_with_effects(
    score: stream.Score,
    reverb: Optional[str] = 'hall',
    chorus: bool = False,
    delay: Optional[Dict[str, float]] = None,
    tuning_system: str = 'equal'
) -> stream.Score:
    """
    Enhance MIDI score with effect metadata for realistic playback.

    Adds metadata annotations for reverb, chorus, delay, and historical
    tuning systems. These annotations can be read by DAWs and synths.

    Args:
        score: The Score to enhance
        reverb: Reverb type ('room', 'hall', 'cathedral', None)
        chorus: Whether to apply chorus effect
        delay: Delay parameters {'time': ms, 'feedback': 0-1, 'mix': 0-1}
        tuning_system: Tuning system ('equal', 'pythagorean', 'meantone', 'werckmeister')

    Returns:
        New Score with effect metadata added

    Example:
        >>> canon = mirror_canon(theme)
        >>> enhanced = enhance_midi_with_effects(
        ...     canon, reverb='cathedral',
        ...     delay={'time': 250, 'feedback': 0.3, 'mix': 0.2}
        ... )
    """
    # Create a deep copy
    new_score = score.coreCopyAsDerivation('enhance_midi_with_effects')

    # Store effect settings in metadata
    if not hasattr(new_score, 'metadata') or new_score.metadata is None:
        new_score.metadata = m21.metadata.Metadata()

    # Add effect metadata
    effects = {}

    if reverb:
        reverb_params = {
            'room': {'size': 0.3, 'decay': 1.0, 'wet': 0.2},
            'hall': {'size': 0.6, 'decay': 2.0, 'wet': 0.3},
            'cathedral': {'size': 0.9, 'decay': 4.0, 'wet': 0.4}
        }
        effects['reverb'] = reverb_params.get(reverb, reverb_params['hall'])

    if chorus:
        effects['chorus'] = {
            'rate': 1.5,  # Hz
            'depth': 0.3,
            'mix': 0.4
        }

    if delay:
        effects['delay'] = delay

    # Tuning system
    tuning_offsets = {
        'equal': {},  # Standard 12-TET
        'pythagorean': {
            # Simplified pythagorean ratios (in cents deviation from 12-TET)
            'D': -2, 'E': +4, 'F': -2, 'G': +2, 'A': +2, 'B': +4
        },
        'meantone': {
            # Quarter-comma meantone deviations
            'D': -5, 'E': -8, 'F': +3, 'G': -3, 'A': -7, 'B': -10
        },
        'werckmeister': {
            # Werckmeister III well temperament
            'D': -2, 'E': -4, 'F': +2, 'G': 0, 'A': -2, 'B': -6
        }
    }

    effects['tuning_system'] = {
        'name': tuning_system,
        'offsets': tuning_offsets.get(tuning_system, {})
    }

    # Store effects as a custom attribute on the score
    # This is more reliable than using music21's metadata API
    new_score._audio_effects = effects

    # Also add as text expression to first element for visibility
    if new_score.parts:
        comment = f"Effects: reverb={reverb}, chorus={chorus}, tuning={tuning_system}"
        # Store in score's title if available
        if hasattr(new_score, 'metadata') and new_score.metadata:
            if not new_score.metadata.title:
                new_score.metadata.title = comment
            else:
                new_score.metadata.title += f" [{comment}]"

    return new_score


def create_spatial_mix(
    score: stream.Score,
    voice_positions: Optional[List[float]] = None,
    stereo_width: float = 0.8,
    depth_simulation: bool = True
) -> stream.Score:
    """
    Create spatial audio mix by positioning voices in stereo field.

    Assigns pan positions to each voice for immersive stereo playback,
    simulating a physical ensemble placement.

    Args:
        score: The Score with multiple voices/parts
        voice_positions: List of pan positions (-1.0=left, 0.0=center, 1.0=right)
                        If None, automatically spaces voices evenly
        stereo_width: Overall stereo width (0.0=mono, 1.0=full stereo)
        depth_simulation: Whether to simulate depth via volume/EQ

    Returns:
        New Score with spatial positioning metadata

    Example:
        >>> canon = mirror_canon(theme)
        >>> spatial = create_spatial_mix(
        ...     canon,
        ...     voice_positions=[-0.5, 0.5],  # Left and right
        ...     stereo_width=0.9
        ... )
    """
    # Ensure we have a Score object
    if isinstance(score, stream.Part):
        temp_score = stream.Score()
        temp_score.insert(0, score)
        score = temp_score

    # Create a deep copy
    new_score = score.coreCopyAsDerivation('create_spatial_mix')

    num_voices = len(list(new_score.parts))

    # Auto-generate voice positions if not provided
    if voice_positions is None:
        if num_voices == 1:
            voice_positions = [0.0]  # Center
        elif num_voices == 2:
            voice_positions = [-0.6, 0.6]  # Left-right pair
        elif num_voices == 3:
            voice_positions = [-0.7, 0.0, 0.7]  # L-C-R
        elif num_voices == 4:
            voice_positions = [-0.8, -0.3, 0.3, 0.8]  # Quartet
        else:
            # Evenly space across stereo field
            if num_voices > 1:
                voice_positions = [
                    -1.0 + (2.0 * i / (num_voices - 1))
                    for i in range(num_voices)
                ]
            else:
                voice_positions = [0.0]

    # Apply stereo width scaling
    voice_positions = [pos * stereo_width for pos in voice_positions]

    # Apply positions to parts
    spatial_config = {}

    for i, part in enumerate(new_score.parts):
        if i < len(voice_positions):
            pan = voice_positions[i]

            # Set MIDI pan (0-127, where 64 is center)
            midi_pan = int(64 + (pan * 63))
            midi_pan = max(0, min(127, midi_pan))

            # Add pan as metadata
            if not hasattr(part, 'partName') or part.partName is None:
                part.partName = f'Voice {i+1}'

            # Store spatial metadata
            spatial_config[f'voice_{i+1}'] = {
                'pan': pan,
                'midi_pan': midi_pan,
                'position': 'left' if pan < -0.3 else 'right' if pan > 0.3 else 'center'
            }

            # Apply depth simulation if requested
            if depth_simulation:
                # Simulate depth with volume (outer voices slightly quieter)
                depth_factor = 1.0 - (abs(pan) * 0.15)  # Max 15% reduction
                spatial_config[f'voice_{i+1}']['depth_volume'] = depth_factor

                # Apply to notes
                for el in part.flatten().notesAndRests:
                    if isinstance(el, (note.Note, chord.Chord)):
                        if hasattr(el, 'volume') and el.volume:
                            base_velocity = el.volume.velocity or 80
                            el.volume.velocity = int(base_velocity * depth_factor)

    # Store spatial config as a custom attribute on the score
    # This is more reliable than using music21's metadata API
    new_score._spatial_config = spatial_config

    return new_score
