"""
Input/output utilities for MIDI, MusicXML, and WAV export.
"""

from pathlib import Path
from typing import Union, Optional
import music21 as m21
from music21 import stream


def to_midi(score: stream.Score, path: Union[str, Path]) -> Path:
    """
    Export a score to MIDI format.

    Args:
        score: The Score to export
        path: Destination file path

    Returns:
        Path to the written MIDI file
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    mf = m21.midi.translate.music21ObjectToMidiFile(score)
    mf.open(str(path), 'wb')
    mf.write()
    mf.close()

    return path


def to_musicxml(score: stream.Score, path: Union[str, Path]) -> Path:
    """
    Export a score to MusicXML format.

    Args:
        score: The Score to export
        path: Destination file path

    Returns:
        Path to the written MusicXML file
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    score.write('musicxml', fp=str(path))

    return path


def to_wav_via_sf2(
    midi_path: Union[str, Path],
    sf2_path: Union[str, Path],
    wav_path: Union[str, Path]
) -> Optional[Path]:
    """
    Convert MIDI to WAV using a SoundFont file.

    This function requires either FluidSynth or the midi2audio library.
    If neither is available, it returns None and prints a message.

    Args:
        midi_path: Path to input MIDI file
        sf2_path: Path to SoundFont (.sf2) file
        wav_path: Path for output WAV file

    Returns:
        Path to the WAV file if successful, None otherwise
    """
    midi_path = Path(midi_path)
    sf2_path = Path(sf2_path)
    wav_path = Path(wav_path)

    if not midi_path.exists():
        raise FileNotFoundError(f"MIDI file not found: {midi_path}")

    if not sf2_path.exists():
        raise FileNotFoundError(f"SoundFont file not found: {sf2_path}")

    wav_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Try using midi2audio if available
        from midi2audio import FluidSynth

        fs = FluidSynth(sound_font=str(sf2_path))
        fs.midi_to_audio(str(midi_path), str(wav_path))

        return wav_path

    except ImportError:
        print(
            "WAV export requires midi2audio and FluidSynth.\n"
            "Install with: pip install midi2audio\n"
            "And ensure FluidSynth is installed on your system:\n"
            "  Ubuntu/Debian: sudo apt-get install fluidsynth\n"
            "  macOS: brew install fluid-synth\n"
            "  Windows: Download from https://www.fluidsynth.org/"
        )
        return None
    except Exception as e:
        print(f"Error converting MIDI to WAV: {e}")
        return None


def load_score(path: Union[str, Path]) -> stream.Score:
    """
    Load a score from a MusicXML or MIDI file.

    Args:
        path: Path to the file to load

    Returns:
        The loaded Score object
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    score = m21.converter.parse(str(path))

    # Ensure we have a Score object
    if isinstance(score, stream.Score):
        return score
    elif isinstance(score, stream.Part):
        # Wrap single part in a score
        s = stream.Score()
        s.insert(0, score)
        return s
    else:
        # Try to convert other types
        s = stream.Score()
        s.insert(0, score)
        return s
