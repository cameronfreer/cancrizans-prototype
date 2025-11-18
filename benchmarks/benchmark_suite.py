"""
Comprehensive performance benchmarks for Cancrizans.

This module provides benchmarks for key operations to detect
performance regressions over time.
"""

import time
from pathlib import Path
from typing import Dict, List, Callable, Any
import json
from datetime import datetime

from music21 import stream, note, chord, corpus

# Import Cancrizans modules
from cancrizans import (
    CanonGenerator,
    is_time_palindrome,
    retrograde,
    table_canon,
    advanced_crab_canon,
    detect_motifs,
    identify_melodic_sequences,
    detect_imitation_points,
    analyze_fugue_structure,
    calculate_voice_independence,
    to_midi,
    load_score,
)


class BenchmarkResult:
    """Container for benchmark results."""

    def __init__(self, name: str, duration: float, iterations: int = 1):
        self.name = name
        self.duration = duration
        self.iterations = iterations
        self.avg_duration = duration / iterations if iterations > 0 else duration

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'total_duration': self.duration,
            'iterations': self.iterations,
            'avg_duration': self.avg_duration,
        }


class BenchmarkSuite:
    """Suite of performance benchmarks."""

    def __init__(self):
        self.results: List[BenchmarkResult] = []

    def benchmark(
        self,
        name: str,
        func: Callable,
        iterations: int = 10,
        setup: Callable = None,
    ) -> BenchmarkResult:
        """
        Run a benchmark and record results.

        Args:
            name: Name of the benchmark
            func: Function to benchmark
            iterations: Number of iterations to run
            setup: Optional setup function run before each iteration

        Returns:
            BenchmarkResult with timing information
        """
        times = []

        for _ in range(iterations):
            if setup:
                setup()

            start = time.perf_counter()
            func()
            end = time.perf_counter()

            times.append(end - start)

        total_duration = sum(times)
        result = BenchmarkResult(name, total_duration, iterations)
        self.results.append(result)

        return result

    def print_results(self):
        """Print benchmark results in a formatted table."""
        print("\n" + "=" * 70)
        print("BENCHMARK RESULTS")
        print("=" * 70)
        print(f"{'Benchmark':<40} {'Avg Time':<15} {'Iterations':<10}")
        print("-" * 70)

        for result in self.results:
            print(
                f"{result.name:<40} {result.avg_duration*1000:>10.3f} ms {result.iterations:>10}"
            )

        print("=" * 70)

    def save_results(self, output_path: Path):
        """Save results to JSON file."""
        data = {
            'timestamp': datetime.now().isoformat(),
            'benchmarks': [r.to_dict() for r in self.results],
        }

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)


def run_benchmarks() -> BenchmarkSuite:
    """Run all performance benchmarks."""
    suite = BenchmarkSuite()

    # Setup: Create test data
    print("Setting up test data...")
    gen = CanonGenerator(seed=42)

    # Generate test canons of various sizes
    small_canon = gen.generate_scale_canon('C', 'major', length=8)
    medium_canon = gen.generate_scale_canon('C', 'major', length=16)
    large_canon = gen.generate_scale_canon('C', 'major', length=32)

    # Create polyphonic test score
    polyphonic_score = stream.Score()
    for i in range(4):
        part = stream.Part()
        for j in range(20):
            n = note.Note(60 + i * 5 + j % 12, quarterLength=1.0)
            part.append(n)
        polyphonic_score.append(part)

    print("\nRunning benchmarks...\n")

    # ===================================================================
    # CANON GENERATION BENCHMARKS
    # ===================================================================

    suite.benchmark(
        "Generate small scale canon (8 notes)",
        lambda: gen.generate_scale_canon('C', 'major', length=8),
        iterations=100,
    )

    suite.benchmark(
        "Generate medium scale canon (16 notes)",
        lambda: gen.generate_scale_canon('C', 'major', length=16),
        iterations=50,
    )

    suite.benchmark(
        "Generate large scale canon (32 notes)",
        lambda: gen.generate_scale_canon('C', 'major', length=32),
        iterations=20,
    )

    suite.benchmark(
        "Generate fibonacci canon",
        lambda: gen.generate_fibonacci_canon(length=10),
        iterations=50,
    )

    suite.benchmark(
        "Generate golden ratio canon",
        lambda: gen.generate_golden_ratio_canon(length=12),
        iterations=50,
    )

    # ===================================================================
    # CANON DETECTION BENCHMARKS
    # ===================================================================

    suite.benchmark(
        "Check palindrome symmetry (small)",
        lambda: is_time_palindrome(small_canon),
        iterations=100,
    )

    suite.benchmark(
        "Check palindrome symmetry (medium)",
        lambda: is_time_palindrome(medium_canon),
        iterations=50,
    )

    suite.benchmark(
        "Check palindrome symmetry (large)",
        lambda: is_time_palindrome(large_canon),
        iterations=20,
    )

    # ===================================================================
    # CANON TRANSFORMATION BENCHMARKS
    # ===================================================================

    suite.benchmark(
        "Apply retrograde transformation",
        lambda: retrograde(small_canon),
        iterations=100,
    )

    suite.benchmark(
        "Apply table canon transformation",
        lambda: table_canon(small_canon),
        iterations=100,
    )

    suite.benchmark(
        "Apply advanced crab canon",
        lambda: advanced_crab_canon(small_canon),
        iterations=50,
    )

    # ===================================================================
    # PATTERN ANALYSIS BENCHMARKS
    # ===================================================================

    suite.benchmark(
        "Detect motifs (polyphonic)",
        lambda: detect_motifs(polyphonic_score, min_length=3, max_length=6),
        iterations=20,
    )

    suite.benchmark(
        "Identify melodic sequences",
        lambda: identify_melodic_sequences(polyphonic_score),
        iterations=20,
    )

    suite.benchmark(
        "Detect imitation points",
        lambda: detect_imitation_points(polyphonic_score),
        iterations=20,
    )

    suite.benchmark(
        "Analyze fugue structure",
        lambda: analyze_fugue_structure(polyphonic_score),
        iterations=10,
    )

    suite.benchmark(
        "Calculate voice independence",
        lambda: calculate_voice_independence(polyphonic_score),
        iterations=20,
    )

    # ===================================================================
    # I/O BENCHMARKS
    # ===================================================================

    import tempfile

    def benchmark_midi_export():
        with tempfile.NamedTemporaryFile(suffix='.mid', delete=True) as tmp:
            to_midi(small_canon, Path(tmp.name))

    suite.benchmark("Export to MIDI", benchmark_midi_export, iterations=50)

    def benchmark_midi_import():
        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as tmp:
            tmp_path = Path(tmp.name)
            to_midi(small_canon, tmp_path)
            try:
                load_score(tmp_path)
            finally:
                tmp_path.unlink()

    suite.benchmark("Import from MIDI", benchmark_midi_import, iterations=50)

    return suite


def main():
    """Run benchmarks and save results."""
    suite = run_benchmarks()
    suite.print_results()

    # Save results
    output_path = Path(__file__).parent / 'results' / 'benchmark_results.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    suite.save_results(output_path)

    print(f"\nResults saved to: {output_path}")


if __name__ == '__main__':
    main()
