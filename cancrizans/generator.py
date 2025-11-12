"""
Algorithmic Canon Generator

Generate palindromic canons using various compositional rules and algorithms.
"""

import random
from typing import List, Tuple, Optional
from fractions import Fraction
from music21 import note, stream, pitch
from cancrizans.bach_crab import assemble_crab_from_theme


class CanonGenerator:
    """Generate palindromic canons algorithmically."""

    def __init__(self, seed: Optional[int] = None):
        """Initialize generator with optional random seed."""
        if seed is not None:
            random.seed(seed)

    def generate_scale_canon(
        self,
        key: str = 'C',
        mode: str = 'major',
        octave: int = 4,
        length: int = 8,
        ascending: bool = True
    ) -> stream.Score:
        """Generate a canon based on a scale.

        Args:
            key: Root note (e.g., 'C', 'D')
            mode: 'major' or 'minor'
            octave: Starting octave
            length: Number of notes
            ascending: True for ascending, False for descending

        Returns:
            Complete palindromic canon
        """
        theme = stream.Part()

        # Define scale degrees
        if mode == 'major':
            intervals = [0, 2, 4, 5, 7, 9, 11, 12]  # Major scale
        else:  # minor
            intervals = [0, 2, 3, 5, 7, 8, 10, 12]  # Natural minor

        # Calculate starting MIDI number
        root_pitch = pitch.Pitch(f"{key}{octave}")
        base_midi = root_pitch.midi

        # Generate melody
        for i in range(length):
            degree = i % len(intervals)
            if not ascending:
                degree = (len(intervals) - 1 - degree) % len(intervals)

            midi_num = base_midi + intervals[degree]
            theme.append(note.Note(midi=midi_num, quarterLength=1.0))

        return assemble_crab_from_theme(theme)

    def generate_arpeggio_canon(
        self,
        root: str = 'C4',
        chord_type: str = 'major',
        inversions: int = 2,
        duration: float = 1.0
    ) -> stream.Score:
        """Generate a canon based on arpeggiated chords.

        Args:
            root: Root note
            chord_type: 'major', 'minor', 'diminished', 'augmented'
            inversions: Number of inversions to include
            duration: Note duration

        Returns:
            Complete palindromic canon
        """
        theme = stream.Part()

        # Define chord intervals
        chord_intervals = {
            'major': [0, 4, 7],
            'minor': [0, 3, 7],
            'diminished': [0, 3, 6],
            'augmented': [0, 4, 8]
        }

        intervals = chord_intervals.get(chord_type, chord_intervals['major'])
        root_pitch = pitch.Pitch(root)
        base_midi = root_pitch.midi

        # Generate arpeggio with inversions
        for inversion in range(inversions + 1):
            for interval in intervals:
                midi_num = base_midi + interval + (12 * inversion)
                theme.append(note.Note(midi=midi_num, quarterLength=duration))

        return assemble_crab_from_theme(theme)

    def generate_random_walk(
        self,
        start: str = 'C4',
        length: int = 16,
        max_interval: int = 3,
        duration: float = 1.0
    ) -> stream.Score:
        """Generate a canon using random walk algorithm.

        Args:
            start: Starting note
            length: Number of notes
            max_interval: Maximum interval size (semitones)
            duration: Note duration

        Returns:
            Complete palindromic canon
        """
        theme = stream.Part()

        current_pitch = pitch.Pitch(start)
        theme.append(note.Note(current_pitch, quarterLength=duration))

        for _ in range(length - 1):
            # Random step within max_interval
            step = random.randint(-max_interval, max_interval)
            current_pitch = pitch.Pitch(midi=current_pitch.midi + step)

            # Keep within reasonable range (C2 to C6)
            if current_pitch.midi < 36:
                current_pitch = pitch.Pitch(midi=36)
            elif current_pitch.midi > 84:
                current_pitch = pitch.Pitch(midi=84)

            theme.append(note.Note(current_pitch, quarterLength=duration))

        return assemble_crab_from_theme(theme)

    def generate_fibonacci_canon(
        self,
        root: str = 'C4',
        length: int = 8
    ) -> stream.Score:
        """Generate canon using Fibonacci sequence for intervals.

        Args:
            root: Root note
            length: Number of notes

        Returns:
            Complete palindromic canon
        """
        theme = stream.Part()

        # Generate Fibonacci sequence
        fib = [1, 1]
        for i in range(length - 2):
            fib.append(fib[-1] + fib[-2])

        root_pitch = pitch.Pitch(root)
        current_midi = root_pitch.midi
        theme.append(note.Note(midi=current_midi, quarterLength=1.0))

        # Use Fibonacci numbers as intervals (mod 12 for scale)
        for i in range(1, length):
            interval = fib[i] % 12
            current_midi = root_pitch.midi + interval

            # Keep in range
            while current_midi > 84:
                current_midi -= 12
            while current_midi < 36:
                current_midi += 12

            # Use clean duration values based on Fibonacci
            duration_map = {0: 1.0, 1: 1.0, 2: 0.5, 3: 0.25}
            duration = duration_map.get(fib[i] % 4, 1.0)
            theme.append(note.Note(midi=current_midi, quarterLength=duration))

        return assemble_crab_from_theme(theme)

    def generate_rhythmic_canon(
        self,
        pitch_pattern: List[str],
        rhythm_pattern: List[float]
    ) -> stream.Score:
        """Generate canon with specific pitch and rhythm patterns.

        Args:
            pitch_pattern: List of pitch names (e.g., ['C4', 'D4', 'E4'])
            rhythm_pattern: List of durations (e.g., [1.0, 0.5, 0.5])

        Returns:
            Complete palindromic canon
        """
        theme = stream.Part()

        # Cycle through patterns
        max_length = max(len(pitch_pattern), len(rhythm_pattern))

        for i in range(max_length):
            p = pitch_pattern[i % len(pitch_pattern)]
            r = rhythm_pattern[i % len(rhythm_pattern)]
            theme.append(note.Note(p, quarterLength=r))

        return assemble_crab_from_theme(theme)

    def generate_fractal_canon(
        self,
        seed_pattern: List[int],
        iterations: int = 2,
        root: str = 'C4'
    ) -> stream.Score:
        """Generate canon using self-similar fractal patterns.

        Args:
            seed_pattern: Initial interval pattern (semitones)
            iterations: Number of fractal iterations
            root: Root note

        Returns:
            Complete palindromic canon
        """
        theme = stream.Part()

        # Expand pattern fractally
        pattern = seed_pattern.copy()
        for _ in range(iterations):
            new_pattern = []
            for interval in pattern:
                # Each interval becomes a mini-version of the pattern
                new_pattern.extend([interval + p for p in seed_pattern])
            pattern = new_pattern

        # Convert to notes
        root_pitch = pitch.Pitch(root)
        current_midi = root_pitch.midi
        theme.append(note.Note(midi=current_midi, quarterLength=1.0))

        for interval in pattern[:16]:  # Limit length
            current_midi += interval

            # Keep in range
            while current_midi > 84:
                current_midi -= 12
            while current_midi < 36:
                current_midi += 12

            theme.append(note.Note(midi=current_midi, quarterLength=1.0))

        return assemble_crab_from_theme(theme)

    def generate_golden_ratio_canon(
        self,
        root: str = 'C4',
        length: int = 13
    ) -> stream.Score:
        """Generate canon using golden ratio proportions.

        Args:
            root: Root note
            length: Number of notes (Fibonacci number recommended)

        Returns:
            Complete palindromic canon
        """
        theme = stream.Part()

        phi = 1.618033988749895  # Golden ratio

        root_pitch = pitch.Pitch(root)
        base_midi = root_pitch.midi

        for i in range(length):
            # Use golden ratio to determine pitch
            midi_num = int(base_midi + (i * phi) % 12)

            # Use golden ratio for rhythm (approximate with clean fractions)
            duration = 1.0 if (i % 2 == 0) else 0.625  # 5/8 approximates 1/phi

            theme.append(note.Note(midi=midi_num, quarterLength=duration))

        return assemble_crab_from_theme(theme)

    def generate_modal_canon(
        self,
        mode: str = 'dorian',
        root: str = 'D4',
        length: int = 8
    ) -> stream.Score:
        """Generate canon in a specific mode.

        Args:
            mode: Mode name (dorian, phrygian, lydian, mixolydian, aeolian, locrian)
            root: Root note
            length: Number of notes

        Returns:
            Complete palindromic canon
        """
        # Modal interval patterns
        modes = {
            'dorian':     [0, 2, 3, 5, 7, 9, 10, 12],
            'phrygian':   [0, 1, 3, 5, 7, 8, 10, 12],
            'lydian':     [0, 2, 4, 6, 7, 9, 11, 12],
            'mixolydian': [0, 2, 4, 5, 7, 9, 10, 12],
            'aeolian':    [0, 2, 3, 5, 7, 8, 10, 12],
            'locrian':    [0, 1, 3, 5, 6, 8, 10, 12]
        }

        intervals = modes.get(mode, modes['dorian'])

        theme = stream.Part()
        root_pitch = pitch.Pitch(root)
        base_midi = root_pitch.midi

        for i in range(length):
            degree = i % len(intervals)
            midi_num = base_midi + intervals[degree]
            theme.append(note.Note(midi=midi_num, quarterLength=1.0))

        return assemble_crab_from_theme(theme)

    def generate_polyrhythmic_canon(
        self,
        pitches: List[str],
        rhythm_ratio: Tuple[int, int] = (3, 2)
    ) -> stream.Score:
        """Generate canon with polyrhythmic patterns.

        Args:
            pitches: Pitch sequence
            rhythm_ratio: Tuple of (numerator, denominator) for polyrhythm

        Returns:
            Complete palindromic canon
        """
        theme = stream.Part()

        num, den = rhythm_ratio
        # Use simple duration values based on the ratio
        duration1 = 1.0 if num >= den else 0.5
        duration2 = 1.0 if den >= num else 0.5

        for i, p in enumerate(pitches):
            # Alternate between two rhythmic values
            duration = duration1 if (i % 2 == 0) else duration2
            theme.append(note.Note(p, quarterLength=duration))

        return assemble_crab_from_theme(theme)


def generate_example_canons() -> dict:
    """Generate a collection of example canons using different algorithms.

    Returns:
        Dictionary mapping names to canons
    """
    generator = CanonGenerator(seed=42)  # Fixed seed for reproducibility

    examples = {
        'scale_major': generator.generate_scale_canon(key='C', mode='major'),
        'scale_minor': generator.generate_scale_canon(key='A', mode='minor'),
        'arpeggio_major': generator.generate_arpeggio_canon(root='C4', chord_type='major'),
        'arpeggio_minor': generator.generate_arpeggio_canon(root='A3', chord_type='minor'),
        'random_walk': generator.generate_random_walk(length=12, max_interval=2),
        'fibonacci': generator.generate_fibonacci_canon(root='G4', length=8),
        'golden_ratio': generator.generate_golden_ratio_canon(root='D4', length=13),
        'dorian_mode': generator.generate_modal_canon(mode='dorian', root='D4'),
        'lydian_mode': generator.generate_modal_canon(mode='lydian', root='F4'),
        'fractal': generator.generate_fractal_canon(seed_pattern=[1, 2, -1], iterations=2),
        'polyrhythmic': generator.generate_polyrhythmic_canon(
            pitches=['C4', 'E4', 'G4', 'C5', 'G4', 'E4'],
            rhythm_ratio=(3, 2)
        )
    }

    return examples
