"""
Research tools for batch analysis, data export, and comparative studies.

This module provides utilities for musicological research:
- Batch processing of multiple canons
- Statistical analysis and comparison
- Export to research data formats (CSV, JSON, LaTeX tables)
- Corpus analysis helpers
"""

from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import json
import csv
from datetime import datetime

from music21 import stream, converter
from cancrizans import (
    is_time_palindrome,
    interval_analysis,
    harmonic_analysis,
    rhythm_analysis,
    spectral_analysis,
    symmetry_metrics,
    chord_progression_analysis,
    compare_canons,
)


class CanonAnalyzer:
    """Analyzes a single crab canon with comprehensive metrics."""

    def __init__(self, score: stream.Score, name: str = "Untitled", advanced: bool = True):
        self.score = score
        self.name = name
        self.advanced = advanced
        self._analysis_cache: Optional[Dict[str, Any]] = None

    def analyze(self) -> Dict[str, Any]:
        """Perform comprehensive analysis and cache results."""
        if self._analysis_cache is not None:
            return self._analysis_cache

        analysis = {
            'name': self.name,
            'timestamp': datetime.now().isoformat(),
            'is_palindrome': is_time_palindrome(self.score),
            'basic_properties': self._analyze_basic_properties(),
            'intervals': interval_analysis(self.score),
            'harmony': harmonic_analysis(self.score),
            'rhythm': rhythm_analysis(self.score),
            'structure': self._analyze_structure(),
        }

        # Add advanced analysis if enabled
        if self.advanced:
            analysis['spectral'] = spectral_analysis(self.score)
            if len(list(self.score.parts)) == 2:
                analysis['symmetry'] = symmetry_metrics(self.score)
                analysis['chord_progression'] = chord_progression_analysis(self.score)

        self._analysis_cache = analysis
        return analysis

    def _analyze_basic_properties(self) -> Dict[str, Any]:
        """Extract basic properties of the score."""
        parts = list(self.score.parts)

        # Count total notes
        total_notes = sum(len(list(part.flatten().notesAndRests)) for part in parts)

        # Get duration
        duration = self.score.quarterLength if hasattr(self.score, 'quarterLength') else 0

        # Get key signature (if present)
        key_sig = None
        for part in parts:
            ks = part.flatten().getElementsByClass('KeySignature')
            if ks:
                key_sig = str(ks[0])
                break

        return {
            'num_voices': len(parts),
            'total_notes': total_notes,
            'duration_quarters': duration,
            'key_signature': key_sig,
        }

    def _analyze_structure(self) -> Dict[str, Any]:
        """Analyze structural properties."""
        parts = list(self.score.parts)

        # Pitch range for each voice
        pitch_ranges = []
        for part in parts:
            notes = [n for n in part.flatten().notes if hasattr(n, 'pitch')]
            if notes:
                pitches = [n.pitch.midi for n in notes]
                pitch_ranges.append({
                    'min': min(pitches),
                    'max': max(pitches),
                    'span': max(pitches) - min(pitches),
                })

        # Melodic contour correlation (if 2 voices)
        contour_correlation = None
        if len(parts) == 2:
            # Calculate correlation between pitch movements
            contour_correlation = self._calculate_contour_correlation(parts[0], parts[1])

        return {
            'pitch_ranges': pitch_ranges,
            'contour_correlation': contour_correlation,
        }

    def _calculate_contour_correlation(self, voice1: stream.Part, voice2: stream.Part) -> float:
        """Calculate correlation between melodic contours."""
        # Simplified correlation: -1 (perfect mirror) to +1 (perfect parallel)
        notes1 = [n.pitch.midi for n in voice1.flatten().notes if hasattr(n, 'pitch')]
        notes2 = [n.pitch.midi for n in voice2.flatten().notes if hasattr(n, 'pitch')]

        if len(notes1) < 2 or len(notes2) < 2:
            return 0.0

        # Calculate direction changes
        dirs1 = [1 if notes1[i+1] > notes1[i] else -1 if notes1[i+1] < notes1[i] else 0
                 for i in range(min(len(notes1)-1, len(notes2)-1))]
        dirs2 = [1 if notes2[i+1] > notes2[i] else -1 if notes2[i+1] < notes2[i] else 0
                 for i in range(min(len(notes1)-1, len(notes2)-1))]

        # Correlation: percentage of matching directions
        matches = sum(1 for d1, d2 in zip(dirs1, dirs2) if d1 == d2)
        return (2.0 * matches / len(dirs1)) - 1.0 if dirs1 else 0.0


class BatchAnalyzer:
    """Batch process multiple canons for comparative analysis."""

    def __init__(self):
        self.canons: List[CanonAnalyzer] = []

    def add_canon(self, score: stream.Score, name: str):
        """Add a canon to the batch."""
        self.canons.append(CanonAnalyzer(score, name))

    def add_from_file(self, filepath: Path, name: Optional[str] = None):
        """Load and add a canon from a file."""
        score = converter.parse(str(filepath))
        name = name or filepath.stem
        self.add_canon(score, name)

    def analyze_all(self) -> List[Dict[str, Any]]:
        """Analyze all canons in the batch."""
        return [canon.analyze() for canon in self.canons]

    def compare(self) -> Dict[str, Any]:
        """Generate comparative statistics across all canons."""
        analyses = self.analyze_all()

        if not analyses:
            return {}

        return {
            'total_canons': len(analyses),
            'palindrome_count': sum(1 for a in analyses if a['is_palindrome']),
            'average_duration': sum(a['basic_properties']['duration_quarters'] for a in analyses) / len(analyses),
            'consonance_stats': {
                'mean': sum(a['harmony']['consonance_ratio'] for a in analyses) / len(analyses),
                'min': min(a['harmony']['consonance_ratio'] for a in analyses),
                'max': max(a['harmony']['consonance_ratio'] for a in analyses),
            },
            'interval_stats': {
                'avg_size': sum(a['intervals']['average'] for a in analyses) / len(analyses),
            },
        }


class ResearchExporter:
    """Export analysis results to various research formats."""

    @staticmethod
    def to_csv(analyses: List[Dict[str, Any]], output_path: Path):
        """Export analyses to CSV format."""
        if not analyses:
            return

        # Flatten nested dictionaries for CSV
        rows = []
        for a in analyses:
            row = {
                'name': a['name'],
                'is_palindrome': a['is_palindrome'],
                'num_voices': a['basic_properties']['num_voices'],
                'total_notes': a['basic_properties']['total_notes'],
                'duration_quarters': a['basic_properties']['duration_quarters'],
                'consonance_ratio': a['harmony']['consonance_ratio'],
                'avg_interval': a['intervals']['average'],
                'largest_leap': a['intervals']['largest_leap'],
                'unique_durations': a['rhythm']['unique_durations'],
            }
            rows.append(row)

        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    @staticmethod
    def to_json(analyses: List[Dict[str, Any]], output_path: Path):
        """Export analyses to JSON format."""
        with open(output_path, 'w') as f:
            json.dump(analyses, f, indent=2)

    @staticmethod
    def to_latex_table(analyses: List[Dict[str, Any]], output_path: Path):
        """Export analyses to LaTeX table format."""
        lines = [
            r'\begin{table}[h]',
            r'\centering',
            r'\caption{Crab Canon Analysis Results}',
            r'\begin{tabular}{lcccc}',
            r'\toprule',
            r'Canon & Palindrome & Consonance & Avg. Interval & Duration \\',
            r'\midrule',
        ]

        for a in analyses:
            name = a['name'].replace('_', r'\_')
            palindrome = r'\checkmark' if a['is_palindrome'] else ''
            consonance = f"{a['harmony']['consonance_ratio']:.2%}"
            interval = f"{a['intervals']['average']:.1f}"
            duration = f"{a['basic_properties']['duration_quarters']:.0f}"

            lines.append(f"{name} & {palindrome} & {consonance} & {interval} & {duration} \\\\")

        lines.extend([
            r'\bottomrule',
            r'\end{tabular}',
            r'\end{table}',
        ])

        with open(output_path, 'w') as f:
            f.write('\n'.join(lines))

    @staticmethod
    def to_markdown_table(analyses: List[Dict[str, Any]], output_path: Path):
        """Export analyses to Markdown table format."""
        lines = [
            '| Canon | Palindrome | Voices | Duration | Consonance | Avg Interval |',
            '|-------|:----------:|:------:|---------:|-----------:|-------------:|',
        ]

        for a in analyses:
            name = a['name']
            palindrome = '✓' if a['is_palindrome'] else '✗'
            voices = a['basic_properties']['num_voices']
            duration = f"{a['basic_properties']['duration_quarters']:.0f}"
            consonance = f"{a['harmony']['consonance_ratio']:.1%}"
            interval = f"{a['intervals']['average']:.2f}"

            lines.append(f"| {name} | {palindrome} | {voices} | {duration} | {consonance} | {interval} |")

        with open(output_path, 'w') as f:
            f.write('\n'.join(lines))


def analyze_corpus(directory: Path, pattern: str = "*.mid") -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Analyze all canons in a directory.

    Args:
        directory: Path to directory containing MIDI/MusicXML files
        pattern: Glob pattern for file matching

    Returns:
        Tuple of (individual analyses, comparative statistics)
    """
    batch = BatchAnalyzer()

    for filepath in directory.glob(pattern):
        batch.add_from_file(filepath)

    analyses = batch.analyze_all()
    comparison = batch.compare()

    return analyses, comparison


def batch_visualize(directory: Path, output_dir: Path, pattern: str = "*.mid",
                   vis_types: Optional[List[str]] = None):
    """
    Generate visualizations for all canons in a directory.

    Args:
        directory: Path to directory containing MIDI/MusicXML files
        output_dir: Directory to save visualizations
        pattern: Glob pattern for file matching
        vis_types: List of visualization types ('piano_roll', 'symmetry')
                  Defaults to both.

    Example:
        >>> batch_visualize(Path('corpus'), Path('visualizations'))
    """
    from cancrizans.viz import piano_roll, symmetry
    from cancrizans.io import load_score

    if vis_types is None:
        vis_types = ['piano_roll', 'symmetry']

    output_dir.mkdir(parents=True, exist_ok=True)

    for filepath in directory.glob(pattern):
        score = load_score(filepath)
        base_name = filepath.stem

        if 'piano_roll' in vis_types:
            output_path = output_dir / f"{base_name}_piano_roll.png"
            piano_roll(score, str(output_path))

        if 'symmetry' in vis_types:
            output_path = output_dir / f"{base_name}_symmetry.png"
            symmetry(score, str(output_path))


def generate_educational_examples(output_dir: Path, seed: Optional[int] = 42):
    """
    Generate a set of educational canon examples with varying properties.

    Creates canons demonstrating different techniques:
    - Simple scale canon (for beginners)
    - Arpeggio canon (harmonic structure)
    - Modal canon (modes beyond major/minor)
    - Markov-generated canon (algorithmic composition)
    - Contour-based canon (melodic shape)
    - Motif development canon (thematic variation)

    Args:
        output_dir: Directory to save example files
        seed: Random seed for reproducibility

    Example:
        >>> generate_educational_examples(Path('examples'))
    """
    from cancrizans.generator import CanonGenerator
    from cancrizans.io import to_midi, to_musicxml, set_metadata

    output_dir.mkdir(parents=True, exist_ok=True)
    gen = CanonGenerator(seed=seed)

    examples = {
        'educational_scale_canon': ('Scale Canon', 'Simple ascending scale'),
        'educational_arpeggio_canon': ('Arpeggio Canon', 'Harmonic arpeggio'),
        'educational_modal_canon': ('Modal Canon', 'Dorian mode'),
        'educational_markov_canon': ('Markov Canon', 'Algorithmic generation'),
        'educational_contour_canon': ('Contour Canon', 'Arch-shaped melody'),
        'educational_motif_canon': ('Motif Canon', 'Thematic development'),
    }

    # Generate each type
    scores = {
        'educational_scale_canon': gen.generate_scale_canon('C', 'major', length=8),
        'educational_arpeggio_canon': gen.generate_arpeggio_canon('G', 'major'),
        'educational_modal_canon': gen.generate_modal_canon('dorian', 'D4', length=12),
        'educational_markov_canon': gen.generate_markov_canon(
            ['C4', 'D4', 'E4', 'F4', 'G4', 'F4', 'E4', 'D4'], length=16
        ),
        'educational_contour_canon': gen.generate_contour_canon(
            [0, 1, 2, 3, 2, 1, 0], root='C4'
        ),
        'educational_motif_canon': gen.generate_motif_canon(
            ['C4', 'E4', 'G4'], development_pattern='sequence', repetitions=3
        ),
    }

    for key, (title, description) in examples.items():
        score = scores[key]
        set_metadata(score, title=title, composer="Cancrizans Educational")

        # Export to MIDI and MusicXML
        to_midi(score, output_dir / f"{key}.mid")
        to_musicxml(score, output_dir / f"{key}.musicxml")


def generate_research_report(
    analyses: List[Dict[str, Any]],
    output_path: Path,
    include_plots: bool = True
):
    """
    Generate a comprehensive research report with statistics and visualizations.

    Args:
        analyses: List of canon analyses from BatchAnalyzer
        output_path: Path for the output Markdown report
        include_plots: Whether to include statistical plots

    Example:
        >>> batch = BatchAnalyzer()
        >>> batch.add_from_file(Path('canon1.mid'))
        >>> batch.add_from_file(Path('canon2.mid'))
        >>> analyses = batch.analyze_all()
        >>> generate_research_report(analyses, Path('report.md'))
    """
    lines = [
        '# Crab Canon Research Report',
        f'\nGenerated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        f'\n## Corpus Overview',
        f'\nTotal canons analyzed: {len(analyses)}',
        f'Palindromic canons: {sum(1 for a in analyses if a["is_palindrome"])}',
        '\n## Summary Statistics',
        '\n### Basic Properties',
    ]

    if analyses:
        avg_duration = sum(a['basic_properties']['duration_quarters'] for a in analyses) / len(analyses)
        avg_notes = sum(a['basic_properties']['total_notes'] for a in analyses) / len(analyses)

        lines.extend([
            f'- Average duration: {avg_duration:.1f} quarter notes',
            f'- Average total notes: {avg_notes:.1f}',
        ])

        # Harmonic stats
        lines.append('\n### Harmonic Analysis')
        avg_consonance = sum(a['harmony']['consonance_ratio'] for a in analyses) / len(analyses)
        lines.append(f'- Average consonance ratio: {avg_consonance:.2%}')

        # Interval stats
        lines.append('\n### Intervallic Analysis')
        avg_interval = sum(a['intervals']['average'] for a in analyses) / len(analyses)
        lines.append(f'- Average interval size: {avg_interval:.2f} semitones')

        # Spectral stats (if advanced analysis enabled)
        if 'spectral' in analyses[0]:
            lines.append('\n### Spectral Analysis')
            avg_tessitura = sum(a['spectral']['tessitura'] for a in analyses) / len(analyses)
            lines.append(f'- Average tessitura (median pitch): {avg_tessitura:.1f} MIDI')

        # Symmetry stats (if available)
        palindrome_analyses = [a for a in analyses if 'symmetry' in a]
        if palindrome_analyses:
            lines.append('\n### Symmetry Metrics (Palindromic Canons)')
            avg_pitch_sym = sum(a['symmetry']['pitch_symmetry'] for a in palindrome_analyses) / len(palindrome_analyses)
            avg_rhythm_sym = sum(a['symmetry']['rhythmic_symmetry'] for a in palindrome_analyses) / len(palindrome_analyses)
            lines.extend([
                f'- Average pitch symmetry: {avg_pitch_sym:.2%}',
                f'- Average rhythmic symmetry: {avg_rhythm_sym:.2%}',
            ])

        # Individual canon table
        lines.extend([
            '\n## Individual Canon Details',
            '\n| Canon | Palindrome | Duration | Consonance | Avg Interval |',
            '|-------|:----------:|---------:|-----------:|-------------:|',
        ])

        for a in analyses:
            name = a['name']
            palindrome = '✓' if a['is_palindrome'] else '✗'
            duration = f"{a['basic_properties']['duration_quarters']:.0f}"
            consonance = f"{a['harmony']['consonance_ratio']:.1%}"
            interval = f"{a['intervals']['average']:.2f}"
            lines.append(f"| {name} | {palindrome} | {duration} | {consonance} | {interval} |")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text('\n'.join(lines))


def compare_corpus_canons(
    canons: List[Tuple[str, stream.Score]],
    output_path: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Perform pairwise comparisons between all canons in a corpus.

    Args:
        canons: List of (name, score) tuples
        output_path: Optional path to save comparison matrix as JSON

    Returns:
        Dictionary with comparison matrix and summary statistics

    Example:
        >>> canons = [
        >>>     ('Bach', load_score('bach.mid')),
        >>>     ('Example', load_score('example.mid')),
        >>> ]
        >>> results = compare_corpus_canons(canons)
    """
    n = len(canons)
    comparison_matrix = [[{} for _ in range(n)] for _ in range(n)]

    # Perform pairwise comparisons
    for i in range(n):
        for j in range(i + 1, n):
            name1, score1 = canons[i]
            name2, score2 = canons[j]

            comparison = compare_canons(score1, score2)

            comparison_matrix[i][j] = {
                'canons': (name1, name2),
                **comparison
            }
            comparison_matrix[j][i] = comparison_matrix[i][j]

    # Calculate summary statistics
    all_similarities = []
    for i in range(n):
        for j in range(i + 1, n):
            all_similarities.append(comparison_matrix[i][j]['overall_similarity'])

    summary = {
        'num_canons': n,
        'num_comparisons': n * (n - 1) // 2,
        'avg_similarity': sum(all_similarities) / len(all_similarities) if all_similarities else 0.0,
        'min_similarity': min(all_similarities) if all_similarities else 0.0,
        'max_similarity': max(all_similarities) if all_similarities else 0.0,
        'comparison_matrix': comparison_matrix,
    }

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            # Convert to serializable format
            serializable = {
                'num_canons': summary['num_canons'],
                'num_comparisons': summary['num_comparisons'],
                'avg_similarity': summary['avg_similarity'],
                'min_similarity': summary['min_similarity'],
                'max_similarity': summary['max_similarity'],
                'comparisons': [
                    {
                        'canon1': canons[i][0],
                        'canon2': canons[j][0],
                        **comparison_matrix[i][j]
                    }
                    for i in range(n) for j in range(i + 1, n)
                ]
            }
            json.dump(serializable, f, indent=2)

    return summary
