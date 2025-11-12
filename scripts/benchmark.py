#!/usr/bin/env python3
"""
Performance Benchmark Suite

Measure performance of various Cancrizans operations.
"""

import time
import sys
from pathlib import Path
from typing import Callable, Any, Dict
import statistics

sys.path.insert(0, str(Path(__file__).parent.parent))

from cancrizans import (
    load_bach_crab_canon,
    retrograde,
    invert,
    augmentation,
    is_time_palindrome,
    pairwise_symmetry_map,
    interval_analysis,
    harmonic_analysis,
    rhythm_analysis
)
from cancrizans.generator import CanonGenerator
from cancrizans.validator import CanonValidator
from music21 import note, stream


def benchmark(func: Callable, *args, iterations: int = 100, **kwargs) -> Dict[str, float]:
    """Benchmark a function.

    Args:
        func: Function to benchmark
        iterations: Number of iterations
        *args, **kwargs: Arguments to pass to function

    Returns:
        Dictionary with timing statistics
    """
    times = []

    # Warmup
    for _ in range(min(10, iterations // 10)):
        func(*args, **kwargs)

    # Actual benchmark
    for _ in range(iterations):
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to ms

    return {
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'stdev': statistics.stdev(times) if len(times) > 1 else 0,
        'min': min(times),
        'max': max(times),
        'iterations': iterations
    }


def benchmark_transformations():
    """Benchmark transformation operations."""
    print("=== Transformation Benchmarks ===\n")

    # Create test melody
    melody = stream.Part()
    for p in ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5'] * 5:
        melody.append(note.Note(p, quarterLength=1.0))

    # Retrograde
    stats = benchmark(retrograde, melody, iterations=100)
    print(f"Retrograde (40 notes):")
    print(f"  Mean: {stats['mean']:.3f}ms")
    print(f"  Median: {stats['median']:.3f}ms")
    print(f"  Std Dev: {stats['stdev']:.3f}ms\n")

    # Inversion
    stats = benchmark(invert, melody, iterations=100)
    print(f"Inversion (40 notes):")
    print(f"  Mean: {stats['mean']:.3f}ms")
    print(f"  Median: {stats['median']:.3f}ms")
    print(f"  Std Dev: {stats['stdev']:.3f}ms\n")

    # Augmentation
    stats = benchmark(augmentation, melody, iterations=100)
    print(f"Augmentation (40 notes):")
    print(f"  Mean: {stats['mean']:.3f}ms")
    print(f"  Median: {stats['median']:.3f}ms")
    print(f"  Std Dev: {stats['stdev']:.3f}ms\n")


def benchmark_analysis():
    """Benchmark analysis operations."""
    print("=== Analysis Benchmarks ===\n")

    # Load Bach's canon
    score = load_bach_crab_canon()

    # Palindrome check
    stats = benchmark(is_time_palindrome, score, iterations=50)
    print(f"Palindrome Check (184 notes/part):")
    print(f"  Mean: {stats['mean']:.3f}ms")
    print(f"  Median: {stats['median']:.3f}ms")
    print(f"  Std Dev: {stats['stdev']:.3f}ms\n")

    # Symmetry mapping
    stats = benchmark(pairwise_symmetry_map, score, iterations=50)
    print(f"Symmetry Mapping (184 pairs):")
    print(f"  Mean: {stats['mean']:.3f}ms")
    print(f"  Median: {stats['median']:.3f}ms")
    print(f"  Std Dev: {stats['stdev']:.3f}ms\n")

    # Interval analysis
    stats = benchmark(interval_analysis, score, iterations=50)
    print(f"Interval Analysis:")
    print(f"  Mean: {stats['mean']:.3f}ms")
    print(f"  Median: {stats['median']:.3f}ms")
    print(f"  Std Dev: {stats['stdev']:.3f}ms\n")

    # Harmonic analysis
    stats = benchmark(harmonic_analysis, score, iterations=20)
    print(f"Harmonic Analysis:")
    print(f"  Mean: {stats['mean']:.3f}ms")
    print(f"  Median: {stats['median']:.3f}ms")
    print(f"  Std Dev: {stats['stdev']:.3f}ms\n")

    # Rhythm analysis
    stats = benchmark(rhythm_analysis, score, iterations=50)
    print(f"Rhythm Analysis:")
    print(f"  Mean: {stats['mean']:.3f}ms")
    print(f"  Median: {stats['median']:.3f}ms")
    print(f"  Std Dev: {stats['stdev']:.3f}ms\n")


def benchmark_generation():
    """Benchmark canon generation."""
    print("=== Generation Benchmarks ===\n")

    generator = CanonGenerator(seed=42)

    # Scale canon
    stats = benchmark(generator.generate_scale_canon, iterations=50)
    print(f"Scale Canon Generation:")
    print(f"  Mean: {stats['mean']:.3f}ms")
    print(f"  Median: {stats['median']:.3f}ms")
    print(f"  Std Dev: {stats['stdev']:.3f}ms\n")

    # Random walk
    stats = benchmark(generator.generate_random_walk, length=16, iterations=50)
    print(f"Random Walk Canon (16 notes):")
    print(f"  Mean: {stats['mean']:.3f}ms")
    print(f"  Median: {stats['median']:.3f}ms")
    print(f"  Std Dev: {stats['stdev']:.3f}ms\n")

    # Fibonacci
    stats = benchmark(generator.generate_fibonacci_canon, iterations=50)
    print(f"Fibonacci Canon:")
    print(f"  Mean: {stats['mean']:.3f}ms")
    print(f"  Median: {stats['median']:.3f}ms")
    print(f"  Std Dev: {stats['stdev']:.3f}ms\n")


def benchmark_validation():
    """Benchmark validation operations."""
    print("=== Validation Benchmarks ===\n")

    validator = CanonValidator()
    score = load_bach_crab_canon()

    # Full validation
    stats = benchmark(validator.validate, score, iterations=20)
    print(f"Full Canon Validation:")
    print(f"  Mean: {stats['mean']:.3f}ms")
    print(f"  Median: {stats['median']:.3f}ms")
    print(f"  Std Dev: {stats['stdev']:.3f}ms\n")


def benchmark_scale():
    """Benchmark with varying input sizes."""
    print("=== Scalability Benchmarks ===\n")

    sizes = [10, 25, 50, 100, 200]

    print("Retrograde Performance vs. Size:")
    print("Size (notes) | Mean (ms) | Median (ms)")
    print("-" * 45)

    for size in sizes:
        melody = stream.Part()
        for i in range(size):
            melody.append(note.Note('C4', quarterLength=1.0))

        stats = benchmark(retrograde, melody, iterations=50)
        print(f"{size:12d} | {stats['mean']:9.3f} | {stats['median']:11.3f}")

    print("\n")


def run_full_benchmark():
    """Run complete benchmark suite."""
    print("=" * 60)
    print("CANCRIZANS PERFORMANCE BENCHMARK SUITE")
    print("=" * 60)
    print()

    start_time = time.time()

    benchmark_transformations()
    benchmark_analysis()
    benchmark_generation()
    benchmark_validation()
    benchmark_scale()

    end_time = time.time()
    total_time = end_time - start_time

    print("=" * 60)
    print(f"Total benchmark time: {total_time:.2f}s")
    print("=" * 60)


def main():
    """Run benchmarks."""
    import argparse

    parser = argparse.ArgumentParser(description='Benchmark Cancrizans performance')
    parser.add_argument(
        '--suite',
        choices=['all', 'transform', 'analysis', 'generate', 'validate', 'scale'],
        default='all',
        help='Benchmark suite to run'
    )

    args = parser.parse_args()

    if args.suite == 'all':
        run_full_benchmark()
    elif args.suite == 'transform':
        benchmark_transformations()
    elif args.suite == 'analysis':
        benchmark_analysis()
    elif args.suite == 'generate':
        benchmark_generation()
    elif args.suite == 'validate':
        benchmark_validation()
    elif args.suite == 'scale':
        benchmark_scale()


if __name__ == '__main__':
    main()
