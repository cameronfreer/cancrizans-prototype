# Performance Benchmarks

This directory contains performance benchmarks for Cancrizans to track and prevent performance regressions.

## Running Benchmarks Locally

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run the benchmark suite
python benchmarks/benchmark_suite.py
```

This will:
1. Run all performance benchmarks
2. Print results to the console
3. Save results to `benchmarks/results/benchmark_results.json`

## Benchmark Categories

### Canon Generation
- Small scale canon (8 notes)
- Medium scale canon (16 notes)
- Large scale canon (32 notes)
- Fibonacci canon
- Golden ratio canon

### Canon Detection
- Crab canon detection (various sizes)
- Table canon detection (various sizes)

### Canon Transformations
- Crab canon application
- Table canon application

### Pattern Analysis
- Motif detection
- Melodic sequence identification
- Imitation point detection
- Fugue structure analysis
- Voice independence calculation

### I/O Operations
- MIDI export
- MIDI import

## Continuous Integration

Benchmarks run automatically:
- On every push to `main` and `develop` branches
- On every pull request
- Weekly on Sunday at 3:00 UTC

Results are:
- Displayed in GitHub Actions summary
- Uploaded as artifacts (retained for 90 days)
- Compared with previous runs to detect regressions

## Interpreting Results

### Performance Changes
- ✅ **Stable** (< 5% change): Normal variation
- 🚀 **Improved** (faster): Performance optimization
- ⚠️ **Regression** (> 10% slower): Investigate potential issue

### What Counts as a Regression?

A performance regression is defined as:
- Any benchmark that is **> 10% slower** than the previous run
- Consistent slowdowns across multiple benchmarks
- New operations that are significantly slower than similar existing ones

### When to Investigate

Investigate performance changes when:
1. A benchmark shows > 10% regression
2. Multiple benchmarks show consistent slowdowns
3. Core operations (generation, detection) are affected
4. The change affects user-facing features

## Adding New Benchmarks

To add a new benchmark:

1. **Edit `benchmark_suite.py`**:

```python
suite.benchmark(
    "Your benchmark name",
    lambda: your_function_to_benchmark(),
    iterations=50,  # Adjust as needed
)
```

2. **Run locally to verify**:
```bash
python benchmarks/benchmark_suite.py
```

3. **Commit and push** - CI will automatically run the new benchmark

## Benchmark Guidelines

### Good Benchmark Practices

✅ **Do:**
- Test realistic workloads
- Use consistent input sizes
- Run enough iterations for stable results
- Test both fast and slow operations
- Cover core functionality

❌ **Don't:**
- Test trivial operations (< 0.1ms)
- Use random inputs that vary between runs
- Run too many iterations for slow operations
- Include I/O in timing (unless testing I/O)
- Test implementation details

### Iteration Counts

Choose iterations based on operation speed:
- **Very fast** (< 1ms): 100-1000 iterations
- **Fast** (1-10ms): 50-100 iterations
- **Medium** (10-100ms): 20-50 iterations
- **Slow** (> 100ms): 5-20 iterations

## Benchmark Results Structure

Results are saved as JSON:

```json
{
  "timestamp": "2025-01-18T12:00:00",
  "benchmarks": [
    {
      "name": "Generate small scale canon (8 notes)",
      "total_duration": 0.523,
      "iterations": 100,
      "avg_duration": 0.00523
    }
  ]
}
```

## Performance Targets

Target performance metrics (as of v0.40.0):

| Operation | Target Time | Current Avg |
|-----------|-------------|-------------|
| Generate small canon (8 notes) | < 10ms | ~5ms |
| Generate medium canon (16 notes) | < 20ms | ~12ms |
| Detect crab canon (small) | < 5ms | ~2ms |
| Detect motifs (polyphonic) | < 50ms | ~35ms |
| Analyze fugue structure | < 100ms | ~75ms |

*Note: Times are approximate and depend on hardware*

## Troubleshooting

### Benchmarks Fail to Run

```bash
# Ensure all dependencies are installed
pip install -e ".[dev]"

# Check for import errors
python -c "from cancrizans import *"

# Run with verbose output
python -v benchmarks/benchmark_suite.py
```

### Inconsistent Results

- **Run multiple times**: Performance can vary due to system load
- **Close other programs**: Reduce background interference
- **Use consistent hardware**: CI runs on Ubuntu latest
- **Check for thermal throttling**: Long benchmarks may heat up CPU

### High Variance

If results show high variance:
1. Increase iteration count
2. Add warmup iterations (not currently implemented)
3. Pin CPU frequency (advanced, system-dependent)
4. Run on dedicated CI runners

## Future Enhancements

Planned improvements:
- [ ] Memory profiling alongside timing
- [ ] Automatic regression detection and alerts
- [ ] Historical performance graphs
- [ ] Benchmark comparison tool
- [ ] Warmup iterations before timing
- [ ] Statistical analysis (mean, median, std dev)
- [ ] Profiling integration (cProfile, line_profiler)

## Resources

- [Python Performance Tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)
- [timeit Module](https://docs.python.org/3/library/timeit.html)
- [Continuous Benchmarking](https://github.com/benchmark-action/github-action-benchmark)
