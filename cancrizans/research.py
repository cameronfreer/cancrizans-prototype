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
)


class CanonAnalyzer:
    """Analyzes a single crab canon with comprehensive metrics."""

    def __init__(self, score: stream.Score, name: str = "Untitled"):
        self.score = score
        self.name = name
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
