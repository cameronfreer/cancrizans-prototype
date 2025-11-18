"""
Timbral Palindromes & Spectral Symmetry

This module creates palindromes in the spectral domain, exploring timbre,
harmonics, and sound design beyond traditional pitch-based canons.

Phase 19 - v0.36.0
"""

from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import math
import numpy as np
from music21 import stream, note, chord


class SpectralShape(Enum):
    """Spectral envelope shapes"""
    BRIGHT = "bright"  # Emphasized high harmonics
    DARK = "dark"  # Emphasized low harmonics
    HOLLOW = "hollow"  # Odd harmonics only
    NASAL = "nasal"  # Formant peak in mid-range
    REED = "reed"  # Sawtooth-like (all harmonics descending)
    BRASS = "brass"  # Strong low harmonics, moderate highs
    STRING = "string"  # Rich harmonic content
    FLUTE = "flute"  # Fundamental + few harmonics


@dataclass
class SpectralFrame:
    """
    Represents spectral content at a moment in time

    Attributes:
        fundamental_hz: Fundamental frequency in Hz
        harmonic_amplitudes: List of harmonic amplitudes (1st harmonic = fundamental)
        spectral_centroid: Center of mass of spectrum in Hz
        brightness: 0-1 measure of high-frequency content
        harmonic_count: Number of significant harmonics
    """
    fundamental_hz: float
    harmonic_amplitudes: List[float]
    spectral_centroid: Optional[float] = None
    brightness: Optional[float] = None
    harmonic_count: Optional[int] = None

    def __post_init__(self):
        if self.spectral_centroid is None:
            self.spectral_centroid = self._calculate_centroid()
        if self.brightness is None:
            self.brightness = self._calculate_brightness()
        if self.harmonic_count is None:
            self.harmonic_count = sum(1 for amp in self.harmonic_amplitudes if amp > 0.01)

    def _calculate_centroid(self) -> float:
        """Calculate spectral centroid"""
        if not self.harmonic_amplitudes:
            return self.fundamental_hz

        weighted_sum = sum(
            (i + 1) * self.fundamental_hz * amp
            for i, amp in enumerate(self.harmonic_amplitudes)
        )
        total_amp = sum(self.harmonic_amplitudes)

        return weighted_sum / total_amp if total_amp > 0 else self.fundamental_hz

    def _calculate_brightness(self) -> float:
        """Calculate brightness (0-1, proportion of energy in high harmonics)"""
        if len(self.harmonic_amplitudes) < 4:
            return 0.5

        # Energy in harmonics above the 4th
        high_energy = sum(self.harmonic_amplitudes[4:])
        total_energy = sum(self.harmonic_amplitudes)

        return high_energy / total_energy if total_energy > 0 else 0.0


@dataclass
class TimbralTrajectory:
    """
    Defines how timbre evolves over time

    Attributes:
        frames: List of spectral frames over time
        duration_seconds: Total duration
        is_palindrome: Whether trajectory is palindromic
    """
    frames: List[SpectralFrame]
    duration_seconds: float
    is_palindrome: bool = False

    def get_frame_at_time(self, time: float) -> SpectralFrame:
        """Get interpolated frame at specific time"""
        if not self.frames:
            raise ValueError("No frames in trajectory")

        if time <= 0:
            return self.frames[0]
        if time >= self.duration_seconds:
            return self.frames[-1]

        # Linear interpolation between frames
        frame_time = time / self.duration_seconds * (len(self.frames) - 1)
        idx = int(frame_time)

        if idx >= len(self.frames) - 1:
            return self.frames[-1]

        # Simple: return nearest frame (could do linear interpolation)
        return self.frames[idx]


def create_spectral_shape(
    shape: SpectralShape,
    fundamental_hz: float,
    num_harmonics: int = 16
) -> SpectralFrame:
    """
    Create spectral frame with characteristic shape

    Args:
        shape: Spectral envelope shape
        fundamental_hz: Fundamental frequency
        num_harmonics: Number of harmonics to generate

    Returns:
        Spectral frame
    """
    amplitudes = []

    for n in range(1, num_harmonics + 1):
        if shape == SpectralShape.BRIGHT:
            # Linear increase in amplitude
            amp = n / num_harmonics
        elif shape == SpectralShape.DARK:
            # Exponential decay
            amp = 1.0 / (n ** 2)
        elif shape == SpectralShape.HOLLOW:
            # Odd harmonics only (clarinet-like)
            amp = (1.0 / n) if n % 2 == 1 else 0.0
        elif shape == SpectralShape.NASAL:
            # Peak around 5th harmonic
            peak = 5
            amp = math.exp(-((n - peak) ** 2) / 8.0)
        elif shape == SpectralShape.REED:
            # Sawtooth: all harmonics with 1/n amplitude
            amp = 1.0 / n
        elif shape == SpectralShape.BRASS:
            # Strong low harmonics
            if n <= 4:
                amp = 1.0 - (n - 1) * 0.15
            else:
                amp = 1.0 / (n - 2)
        elif shape == SpectralShape.STRING:
            # Complex harmonic series
            amp = (1.0 / n) * (1.0 + 0.3 * math.sin(n * math.pi / 4))
        elif shape == SpectralShape.FLUTE:
            # Mostly fundamental
            amp = 1.0 if n == 1 else 0.1 / n
        else:
            amp = 1.0 / n

        amplitudes.append(amp)

    # Normalize
    max_amp = max(amplitudes) if amplitudes else 1.0
    amplitudes = [a / max_amp for a in amplitudes]

    return SpectralFrame(
        fundamental_hz=fundamental_hz,
        harmonic_amplitudes=amplitudes
    )


def create_timbral_palindrome(
    start_shape: SpectralShape,
    end_shape: SpectralShape,
    fundamental_hz: float,
    duration_seconds: float = 4.0,
    num_frames: int = 32,
    num_harmonics: int = 16
) -> TimbralTrajectory:
    """
    Create timbral trajectory that evolves and then reverses

    Args:
        start_shape: Initial spectral shape
        end_shape: Middle spectral shape (peak of evolution)
        fundamental_hz: Fundamental frequency
        duration_seconds: Total duration
        num_frames: Number of spectral frames
        num_harmonics: Harmonics per frame

    Returns:
        Timbral trajectory that is palindromic
    """
    frames = []

    # For palindrome with num_frames total:
    # - Even: e.g. 10 frames = 5 unique + 5 reversed = A B C D E D C B A (wait that's 9)
    # - Actually for 10: A B C D E F E D C B (no exact middle, but symmetric)
    # - Odd: e.g. 9 frames = 4 + 1 peak + 4 reversed = A B C D E D C B A

    is_odd = num_frames % 2 == 1
    half = num_frames // 2

    # Generate ascending frames
    num_ascending = half + 1 if is_odd else half

    for i in range(num_ascending):
        t = i / (num_ascending - 1) if num_ascending > 1 else 0

        # Interpolate between start and end shapes
        start_frame = create_spectral_shape(start_shape, fundamental_hz, num_harmonics)
        end_frame = create_spectral_shape(end_shape, fundamental_hz, num_harmonics)

        # Linear interpolation of harmonic amplitudes
        interpolated_amps = [
            (1 - t) * start_amp + t * end_amp
            for start_amp, end_amp in zip(start_frame.harmonic_amplitudes, end_frame.harmonic_amplitudes)
        ]

        frame = SpectralFrame(
            fundamental_hz=fundamental_hz,
            harmonic_amplitudes=interpolated_amps
        )
        frames.append(frame)

    # Mirror: reverse all but the last (peak) if odd, or all but last if even
    start_idx = num_ascending - 2 if is_odd else num_ascending - 1
    for i in range(start_idx, -1, -1):
        frames.append(frames[i])

    return TimbralTrajectory(
        frames=frames,
        duration_seconds=duration_seconds,
        is_palindrome=True
    )


def analyze_spectral_symmetry(trajectory: TimbralTrajectory) -> Dict[str, any]:
    """
    Analyze how palindromic a timbral trajectory is

    Args:
        trajectory: Timbral trajectory to analyze

    Returns:
        Dictionary with symmetry analysis
    """
    if len(trajectory.frames) < 2:
        return {
            'is_symmetric': True,
            'symmetry_score': 1.0,
            'midpoint_index': 0,
            'asymmetry_regions': []
        }

    n = len(trajectory.frames)
    midpoint = n // 2

    # Compare first half with reversed second half
    errors = []
    for i in range(midpoint):
        j = n - 1 - i  # Corresponding frame from end

        frame1 = trajectory.frames[i]
        frame2 = trajectory.frames[j]

        # Compare harmonic amplitudes
        min_len = min(len(frame1.harmonic_amplitudes), len(frame2.harmonic_amplitudes))
        if min_len == 0:
            continue

        # Mean squared error
        mse = sum(
            (frame1.harmonic_amplitudes[k] - frame2.harmonic_amplitudes[k]) ** 2
            for k in range(min_len)
        ) / min_len

        errors.append(mse)

    avg_error = sum(errors) / len(errors) if errors else 0.0
    symmetry_score = max(0.0, 1.0 - avg_error * 10)  # Scale error to 0-1

    # Find regions of high asymmetry
    asymmetry_regions = []
    threshold = 0.1
    for i, error in enumerate(errors):
        if error > threshold:
            asymmetry_regions.append({
                'frame_index': i,
                'error': error,
                'timestamp': i / len(errors) * trajectory.duration_seconds
            })

    return {
        'is_symmetric': symmetry_score > 0.9,
        'symmetry_score': symmetry_score,
        'midpoint_index': midpoint,
        'average_error': avg_error,
        'asymmetry_regions': asymmetry_regions
    }


def brightness_palindrome(
    notes: List[note.Note],
    brightness_curve: str = "triangle"
) -> List[Dict[str, any]]:
    """
    Create brightness envelope that is palindromic

    Args:
        notes: List of notes to apply brightness to
        brightness_curve: Curve shape ('triangle', 'arch', 'valley')

    Returns:
        List of dicts with note brightness values
    """
    n = len(notes)
    if n == 0:
        return []

    brightness_values = []

    for i in range(n):
        t = i / (n - 1) if n > 1 else 0

        if brightness_curve == "triangle":
            # Linear up then down
            brightness = 1.0 - 2.0 * abs(t - 0.5)
        elif brightness_curve == "arch":
            # Parabolic arch
            brightness = 1.0 - 4.0 * (t - 0.5) ** 2
        elif brightness_curve == "valley":
            # Inverted arch
            brightness = 4.0 * (t - 0.5) ** 2
        else:
            brightness = 0.5

        brightness = max(0.0, min(1.0, brightness))

        brightness_values.append({
            'note': notes[i],
            'brightness': brightness,
            'spectral_shape': SpectralShape.BRIGHT if brightness > 0.5 else SpectralShape.DARK
        })

    return brightness_values


def formant_trajectory(
    fundamental_hz: float,
    vowel_sequence: List[str],
    duration_seconds: float = 2.0,
    num_frames: int = 16
) -> TimbralTrajectory:
    """
    Create formant-based trajectory (vowel morphing)

    Args:
        fundamental_hz: Fundamental frequency
        vowel_sequence: Sequence of vowels ('a', 'e', 'i', 'o', 'u')
        duration_seconds: Total duration
        num_frames: Number of frames

    Returns:
        Timbral trajectory with formant evolution

    Note:
        Simplified formant approximation using peaked harmonics
    """
    # Approximate formant frequencies (Hz) for vowels
    formants = {
        'a': [730, 1090],   # "ah"
        'e': [530, 1840],   # "eh"
        'i': [270, 2290],   # "ee"
        'o': [570, 840],    # "oh"
        'u': [300, 870]     # "oo"
    }

    frames = []
    num_harmonics = 32

    for i in range(num_frames):
        # Which vowel(s) to interpolate between
        t = i / (num_frames - 1) if num_frames > 1 else 0
        vowel_pos = t * (len(vowel_sequence) - 1)
        idx = int(vowel_pos)
        frac = vowel_pos - idx

        if idx >= len(vowel_sequence) - 1:
            vowel1 = vowel_sequence[-1]
            vowel2 = vowel_sequence[-1]
            frac = 0
        else:
            vowel1 = vowel_sequence[idx]
            vowel2 = vowel_sequence[idx + 1]

        # Get formant frequencies
        f1_1, f2_1 = formants.get(vowel1, [500, 1500])
        f1_2, f2_2 = formants.get(vowel2, [500, 1500])

        # Interpolate formants
        f1 = f1_1 * (1 - frac) + f1_2 * frac
        f2 = f2_1 * (1 - frac) + f2_2 * frac

        # Create harmonic amplitudes with peaks near formants
        amplitudes = []
        for n in range(1, num_harmonics + 1):
            freq = n * fundamental_hz

            # Gaussian peaks at formant frequencies
            amp1 = math.exp(-((freq - f1) ** 2) / (2 * 200 ** 2))
            amp2 = math.exp(-((freq - f2) ** 2) / (2 * 300 ** 2))

            amp = (amp1 + amp2) * (1.0 / n)  # Also apply harmonic rolloff
            amplitudes.append(amp)

        # Normalize
        max_amp = max(amplitudes) if amplitudes else 1.0
        amplitudes = [a / max_amp for a in amplitudes]

        frame = SpectralFrame(
            fundamental_hz=fundamental_hz,
            harmonic_amplitudes=amplitudes
        )
        frames.append(frame)

    return TimbralTrajectory(
        frames=frames,
        duration_seconds=duration_seconds
    )


def spectral_inversion(frame: SpectralFrame) -> SpectralFrame:
    """
    Invert spectral content (reverse harmonic amplitudes)

    Args:
        frame: Input spectral frame

    Returns:
        Inverted spectral frame
    """
    inverted_amps = list(reversed(frame.harmonic_amplitudes))

    return SpectralFrame(
        fundamental_hz=frame.fundamental_hz,
        harmonic_amplitudes=inverted_amps
    )


def spectral_retrograde(trajectory: TimbralTrajectory) -> TimbralTrajectory:
    """
    Reverse spectral trajectory in time

    Args:
        trajectory: Input trajectory

    Returns:
        Time-reversed trajectory
    """
    reversed_frames = list(reversed(trajectory.frames))

    return TimbralTrajectory(
        frames=reversed_frames,
        duration_seconds=trajectory.duration_seconds,
        is_palindrome=trajectory.is_palindrome
    )


def create_harmonic_series_canon(
    fundamental_hz: float,
    num_harmonics: int = 16,
    decay_factor: float = 0.8
) -> List[SpectralFrame]:
    """
    Create series of frames representing harmonic series as canon

    Each frame emphasizes a different harmonic, creating a rising canon effect

    Args:
        fundamental_hz: Fundamental frequency
        num_harmonics: Number of harmonics
        decay_factor: How much each harmonic decays (0-1)

    Returns:
        List of spectral frames
    """
    frames = []

    for emphasized in range(1, num_harmonics + 1):
        amplitudes = []

        for n in range(1, num_harmonics + 1):
            if n == emphasized:
                # Emphasized harmonic
                amp = 1.0
            else:
                # Other harmonics decay based on distance
                distance = abs(n - emphasized)
                amp = decay_factor ** distance

            amplitudes.append(amp)

        # Normalize
        max_amp = max(amplitudes) if amplitudes else 1.0
        amplitudes = [a / max_amp for a in amplitudes]

        frame = SpectralFrame(
            fundamental_hz=fundamental_hz,
            harmonic_amplitudes=amplitudes
        )
        frames.append(frame)

    return frames


def spectral_distance(frame1: SpectralFrame, frame2: SpectralFrame) -> float:
    """
    Calculate distance between two spectral frames

    Args:
        frame1: First frame
        frame2: Second frame

    Returns:
        Distance metric (0 = identical)
    """
    min_len = min(len(frame1.harmonic_amplitudes), len(frame2.harmonic_amplitudes))

    if min_len == 0:
        return float('inf')

    # Euclidean distance in harmonic amplitude space
    squared_diffs = [
        (frame1.harmonic_amplitudes[i] - frame2.harmonic_amplitudes[i]) ** 2
        for i in range(min_len)
    ]

    return math.sqrt(sum(squared_diffs))


def apply_spectral_envelope_to_stream(
    s: stream.Stream,
    trajectory: TimbralTrajectory
) -> List[Dict[str, any]]:
    """
    Apply spectral trajectory to stream

    Args:
        s: Music21 stream
        trajectory: Timbral trajectory

    Returns:
        List of dicts with note and spectral data
    """
    notes = list(s.flatten().notes)
    if not notes:
        return []

    total_duration = s.highestTime
    if total_duration == 0:
        total_duration = 1.0

    result = []

    for n in notes:
        # Get time position of note
        time_ratio = n.offset / total_duration if total_duration > 0 else 0
        time_seconds = time_ratio * trajectory.duration_seconds

        # Get spectral frame at this time
        frame = trajectory.get_frame_at_time(time_seconds)

        result.append({
            'note': n,
            'offset': n.offset,
            'spectral_frame': frame,
            'brightness': frame.brightness,
            'spectral_centroid': frame.spectral_centroid,
            'harmonic_count': frame.harmonic_count
        })

    return result


def detect_timbral_palindrome(trajectory: TimbralTrajectory, tolerance: float = 0.1) -> bool:
    """
    Detect if trajectory is palindromic within tolerance

    Args:
        trajectory: Trajectory to check
        tolerance: Maximum allowed asymmetry (0-1)

    Returns:
        True if palindromic within tolerance
    """
    analysis = analyze_spectral_symmetry(trajectory)
    return analysis['symmetry_score'] >= (1.0 - tolerance)


def generate_spectral_canon_metadata(
    trajectory: TimbralTrajectory,
    title: str = "Spectral Canon"
) -> Dict[str, any]:
    """
    Generate metadata for spectral canon

    Args:
        trajectory: Timbral trajectory
        title: Canon title

    Returns:
        Metadata dictionary
    """
    symmetry = analyze_spectral_symmetry(trajectory)

    # Analyze brightness evolution
    brightnesses = [frame.brightness for frame in trajectory.frames]
    min_brightness = min(brightnesses) if brightnesses else 0
    max_brightness = max(brightnesses) if brightnesses else 0
    avg_brightness = sum(brightnesses) / len(brightnesses) if brightnesses else 0

    # Analyze spectral centroids
    centroids = [frame.spectral_centroid for frame in trajectory.frames]
    min_centroid = min(centroids) if centroids else 0
    max_centroid = max(centroids) if centroids else 0

    return {
        'title': title,
        'duration_seconds': trajectory.duration_seconds,
        'num_frames': len(trajectory.frames),
        'is_palindrome': trajectory.is_palindrome,
        'symmetry_score': symmetry['symmetry_score'],
        'brightness_range': (min_brightness, max_brightness),
        'average_brightness': avg_brightness,
        'spectral_centroid_range': (min_centroid, max_centroid),
        'timbral_complexity': symmetry['average_error'],
        'asymmetry_regions': len(symmetry['asymmetry_regions'])
    }
