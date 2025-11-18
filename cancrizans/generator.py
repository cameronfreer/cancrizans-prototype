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


    def generate_markov_canon(
        self,
        training_pitches: List[str],
        length: int = 16,
        order: int = 1
    ) -> stream.Score:
        """Generate canon using Markov chain trained on pitch sequence.

        Args:
            training_pitches: Sequence of pitches to learn from
            length: Number of notes to generate
            order: Markov chain order (1 = first-order, 2 = second-order)

        Returns:
            Complete palindromic canon

        Examples:
            >>> # Train on a scale and generate variations
            >>> training = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
            >>> canon = generator.generate_markov_canon(training, length=12)
        """
        if len(training_pitches) < order + 1:
            raise ValueError(f"Training sequence must have at least {order + 1} pitches")

        # Build transition probabilities
        transitions = {}
        for i in range(len(training_pitches) - order):
            # Create state from current note(s)
            if order == 1:
                state = training_pitches[i]
            else:
                state = tuple(training_pitches[i:i+order])

            next_pitch = training_pitches[i + order]

            if state not in transitions:
                transitions[state] = []
            transitions[state].append(next_pitch)

        # Generate sequence
        theme = stream.Part()

        # Start with first note(s) from training
        if order == 1:
            current_state = training_pitches[0]
            theme.append(note.Note(current_state, quarterLength=1.0))
        else:
            current_state = tuple(training_pitches[:order])
            for p in current_state:
                theme.append(note.Note(p, quarterLength=1.0))

        # Generate remaining notes
        generated_count = order
        while generated_count < length:
            if current_state in transitions:
                # Pick random next note from possibilities
                next_pitch = random.choice(transitions[current_state])
                theme.append(note.Note(next_pitch, quarterLength=1.0))

                # Update state
                if order == 1:
                    current_state = next_pitch
                else:
                    current_state = tuple(list(current_state)[1:] + [next_pitch])

                generated_count += 1
            else:
                # Restart from beginning if we hit a dead end
                if order == 1:
                    current_state = training_pitches[0]
                else:
                    current_state = tuple(training_pitches[:order])

        return assemble_crab_from_theme(theme)

    def generate_contour_canon(
        self,
        contour: List[int],
        root: str = 'C4',
        scale: List[int] = None
    ) -> stream.Score:
        """Generate canon following a melodic contour pattern.

        Args:
            contour: Melodic contour as relative steps (e.g., [0, 1, -1, 2, -2])
            root: Starting note
            scale: Scale intervals (default: chromatic)

        Returns:
            Complete palindromic canon

        Examples:
            >>> # Arch contour: up, peak, down
            >>> contour = [0, 1, 2, 3, 2, 1, 0]
            >>> canon = generator.generate_contour_canon(contour, root='D4')
        """
        if scale is None:
            scale = list(range(12))  # Chromatic

        theme = stream.Part()
        root_pitch = pitch.Pitch(root)
        current_midi = root_pitch.midi

        theme.append(note.Note(midi=current_midi, quarterLength=1.0))

        for step in contour:
            # Map step to scale degree
            scale_degree = abs(step) % len(scale)
            interval = scale[scale_degree]

            if step > 0:
                current_midi += interval
            elif step < 0:
                current_midi -= interval

            # Keep in range
            while current_midi > 84:
                current_midi -= 12
            while current_midi < 36:
                current_midi += 12

            theme.append(note.Note(midi=current_midi, quarterLength=1.0))

        return assemble_crab_from_theme(theme)

    def generate_motif_canon(
        self,
        motif: List[str],
        development_pattern: str = 'sequence',
        repetitions: int = 3,
        interval: int = 2
    ) -> stream.Score:
        """Generate canon by developing a musical motif.

        Args:
            motif: Initial pitch pattern
            development_pattern: How to develop the motif:
                'sequence' - repeat at different pitches
                'variation' - rhythmic variations
                'fragmentation' - use fragments of motif
            repetitions: Number of repetitions/variations
            interval: Interval for sequencing (semitones)

        Returns:
            Complete palindromic canon

        Examples:
            >>> # Sequence a motif upward
            >>> motif = ['C4', 'E4', 'G4']
            >>> canon = generator.generate_motif_canon(motif, 'sequence', 4, 2)
        """
        theme = stream.Part()

        if development_pattern == 'sequence':
            # Repeat motif at different pitch levels
            for rep in range(repetitions):
                transposition = rep * interval
                for p in motif:
                    p_obj = pitch.Pitch(p)
                    new_midi = p_obj.midi + transposition
                    theme.append(note.Note(midi=new_midi, quarterLength=1.0))

        elif development_pattern == 'variation':
            # Vary rhythm while keeping pitches
            durations = [1.0, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25]
            dur_idx = 0

            for rep in range(repetitions):
                for p in motif:
                    duration = durations[dur_idx % len(durations)]
                    theme.append(note.Note(p, quarterLength=duration))
                    dur_idx += 1

        elif development_pattern == 'fragmentation':
            # Use progressively smaller fragments
            for rep in range(repetitions):
                fragment_size = max(1, len(motif) - rep)
                fragment = motif[:fragment_size]
                for p in fragment:
                    theme.append(note.Note(p, quarterLength=1.0))

        return assemble_crab_from_theme(theme)

    def generate_template_canon(
        self,
        template: str = 'passacaglia',
        root: str = 'D3',
        length: int = 8
    ) -> stream.Score:
        """Generate canon using a classical template/ground bass pattern.

        Args:
            template: Template type:
                'passacaglia' - Descending tetrachord
                'chaconne' - Harmonic pattern
                'ostinato' - Repeated bass pattern
                'romanesca' - Renaissance pattern
            root: Root note
            length: Pattern length

        Returns:
            Complete palindromic canon

        Examples:
            >>> # Classic descending passacaglia bass
            >>> canon = generator.generate_template_canon('passacaglia', 'D3')
        """
        theme = stream.Part()
        root_pitch = pitch.Pitch(root)
        base_midi = root_pitch.midi

        if template == 'passacaglia':
            # Descending tetrachord: I - VII - VI - V in minor
            # Pattern: 0, -2, -3, -5 (approximately)
            pattern = [0, -1, -2, -3, -4, -5, -6, -7][:length]

        elif template == 'chaconne':
            # I - V - VI - V or I - IV - V - I
            pattern = [0, 7, 9, 7, 0, 5, 7, 0][:length]

        elif template == 'ostinato':
            # Repeated short pattern
            base_pattern = [0, 2, 4, 2]
            pattern = (base_pattern * (length // len(base_pattern) + 1))[:length]

        elif template == 'romanesca':
            # I - V - VI - III - IV - I - IV - V
            pattern = [0, 7, 9, 4, 5, 0, 5, 7][:length]

        else:
            # Default: simple ascending
            pattern = list(range(length))

        for interval in pattern:
            midi_num = base_midi + interval
            theme.append(note.Note(midi=midi_num, quarterLength=1.0))

        return assemble_crab_from_theme(theme)

    def generate_constrained_canon(
        self,
        length: int = 12,
        root: str = 'C4',
        constraints: dict = None
    ) -> stream.Score:
        """Generate canon with voice leading and harmonic constraints.

        Args:
            length: Number of notes
            root: Starting note
            constraints: Dictionary of constraints:
                'max_leap': Maximum interval leap (default: 7)
                'prefer_steps': Probability of stepwise motion (default: 0.7)
                'avoid_tritone': Avoid tritone intervals (default: True)
                'scale': Limit to scale degrees (default: None = chromatic)

        Returns:
            Complete palindromic canon

        Examples:
            >>> # Generate with smooth voice leading
            >>> constraints = {'max_leap': 5, 'prefer_steps': 0.8}
            >>> canon = generator.generate_constrained_canon(16, 'G4', constraints)
        """
        if constraints is None:
            constraints = {}

        max_leap = constraints.get('max_leap', 7)
        prefer_steps = constraints.get('prefer_steps', 0.7)
        avoid_tritone = constraints.get('avoid_tritone', True)
        scale = constraints.get('scale', None)

        theme = stream.Part()
        current_pitch = pitch.Pitch(root)
        theme.append(note.Note(current_pitch, quarterLength=1.0))

        for _ in range(length - 1):
            # Determine next pitch with constraints
            if random.random() < prefer_steps:
                # Prefer stepwise motion
                if scale:
                    step = random.choice([s for s in scale if abs(s) <= 2])
                else:
                    step = random.choice([-2, -1, 1, 2])
            else:
                # Allow larger intervals
                if scale:
                    step = random.choice([s for s in scale if abs(s) <= max_leap])
                else:
                    step = random.randint(-max_leap, max_leap)

            # Avoid tritone if requested
            if avoid_tritone and abs(step) == 6:
                step = 5 if step > 0 else -5

            new_midi = current_pitch.midi + step

            # Keep in range
            while new_midi > 84:
                new_midi -= 12
            while new_midi < 36:
                new_midi += 12

            current_pitch = pitch.Pitch(midi=new_midi)
            theme.append(note.Note(current_pitch, quarterLength=1.0))

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
