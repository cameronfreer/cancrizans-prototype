# Contributing to Cancrizans

Thank you for your interest in contributing to Cancrizans! This document provides guidelines and instructions for contributing to the project.

## 🚀 Quick Start

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/cancrizans-prototype
   cd cancrizans-prototype
   ```

2. **Set up development environment**
   ```bash
   # Install development dependencies
   pip install -e ".[dev]"

   # Verify installation
   pytest tests/ -v
   cancrizans --help
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📋 Development Workflow

### 1. Code Style

We use **ruff** for linting and formatting:

```bash
# Check code quality
ruff check cancrizans tests

# Auto-fix issues
ruff check --fix cancrizans tests

# Format code
ruff format cancrizans tests
```

**Code Style Guidelines:**
- Follow PEP 8 conventions
- Use type hints for function signatures
- Write docstrings for all public functions and classes
- Keep functions focused and under 50 lines when possible
- Use descriptive variable names

### 2. Testing

We maintain **100% test pass rate** with comprehensive coverage:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=cancrizans --cov-report=term-missing

# Run specific test file
pytest tests/test_pattern.py -v

# Run specific test
pytest tests/test_pattern.py::TestMotifDetection::test_detect_simple_motif -v

# Run tests in parallel (faster)
pytest tests/ -n auto
```

**Testing Guidelines:**
- Write tests for all new features
- Maintain or improve code coverage
- Use descriptive test names: `test_<what>_<condition>_<expected_result>`
- Use fixtures for common test setup
- Test edge cases and error conditions

### 3. Type Checking

We use **mypy** for type checking:

```bash
# Run type checker
mypy cancrizans --ignore-missing-imports
```

**Type Hints:**
- Add type hints to all function signatures
- Use `from typing import ...` for complex types
- Document types in docstrings when helpful

### 4. Documentation

Update documentation for any user-facing changes:

```bash
# Documentation files to update:
# - README.md - Main project documentation
# - docs/README.md - API reference
# - CHANGELOG.md - Version history
# - Docstrings - Inline code documentation
```

**Documentation Guidelines:**
- Use clear, concise language
- Include code examples in docstrings
- Update API reference for new functions
- Add entries to CHANGELOG.md

## 🎯 Types of Contributions

### Bug Fixes

1. **Report the bug** in GitHub Issues with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and OS

2. **Create a test** that reproduces the bug

3. **Fix the bug** and ensure the test passes

4. **Submit a PR** with the fix and test

### New Features

1. **Discuss first** - Open an issue to discuss large features

2. **Design carefully** - Consider:
   - API design and naming
   - Integration with existing code
   - Performance implications
   - Test coverage

3. **Implement incrementally**:
   - Core functionality first
   - Tests alongside implementation
   - Documentation updates
   - Examples and tutorials

4. **Submit PR** with:
   - Comprehensive tests
   - Documentation
   - Usage examples
   - Changelog entry

### Documentation

Documentation improvements are always welcome:
- Fix typos and grammar
- Clarify confusing sections
- Add examples
- Improve API references
- Create tutorials

## 📦 Pull Request Process

### Before Submitting

```bash
# 1. Update from main
git fetch upstream
git rebase upstream/main

# 2. Run full test suite
pytest tests/ -v --cov=cancrizans

# 3. Check code quality
ruff check cancrizans tests
ruff format cancrizans tests

# 4. Run type checker
mypy cancrizans --ignore-missing-imports

# 5. Update documentation
# - Add/update docstrings
# - Update CHANGELOG.md
# - Update relevant docs
```

### Submitting

1. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request** on GitHub
   - Use the PR template
   - Fill out all sections
   - Link related issues
   - Add screenshots if UI changes

3. **Address review feedback**
   - Respond to comments
   - Make requested changes
   - Push updates to the same branch

### PR Review Criteria

Your PR will be reviewed for:
- ✅ **Tests pass** - All 811+ tests must pass
- ✅ **Code quality** - Passes ruff checks
- ✅ **Type safety** - Passes mypy checks
- ✅ **Test coverage** - Maintains or improves coverage
- ✅ **Documentation** - Includes necessary docs
- ✅ **Performance** - No significant regressions
- ✅ **Design** - Follows project patterns

## 🏗️ Project Structure

```
cancrizans-prototype/
├── cancrizans/          # Main package
│   ├── __init__.py     # Package exports
│   ├── canon.py        # Canon transformations
│   ├── pattern.py      # Pattern analysis
│   ├── microtonal.py   # Microtonal features
│   ├── cli.py          # Command-line interface
│   ├── generator.py    # Canon generation
│   ├── io.py           # File I/O
│   ├── viz.py          # Visualizations
│   └── ...
├── tests/              # Test suite
│   ├── test_canon.py
│   ├── test_pattern.py
│   └── ...
├── docs/               # Documentation
├── scripts/            # Utility scripts
├── notebooks/          # Jupyter tutorials
└── .github/            # GitHub config
    └── workflows/      # CI/CD workflows
```

## 🎨 Code Examples

### Adding a New Function

```python
def analyze_harmonic_rhythm(
    score: stream.Score,
    beat_strength_threshold: float = 0.5
) -> Dict[str, any]:
    """
    Analyze the harmonic rhythm of a score.

    Identifies the rate at which harmonies change, a key element
    of musical analysis and composition.

    Args:
        score: The score to analyze
        beat_strength_threshold: Minimum beat strength to consider (0-1)

    Returns:
        Dictionary containing:
        - 'changes_per_measure': Average harmony changes per measure
        - 'change_points': List of offsets where harmonies change
        - 'regularity_score': Measure of rhythmic regularity (0-1)

    Example:
        >>> from cancrizans import analyze_harmonic_rhythm
        >>> from music21 import corpus
        >>> bach = corpus.parse('bach/bwv66.6')
        >>> result = analyze_harmonic_rhythm(bach)
        >>> print(f"Changes per measure: {result['changes_per_measure']:.2f}")

    Raises:
        ValueError: If score is empty or invalid
    """
    # Implementation here
    pass
```

### Adding Tests

```python
class TestHarmonicRhythm:
    """Test harmonic rhythm analysis."""

    @pytest.fixture
    def simple_progression(self):
        """Create a simple chord progression for testing."""
        from music21 import stream, chord
        s = stream.Stream()
        # Add test chords
        s.append(chord.Chord(['C4', 'E4', 'G4'], quarterLength=2))
        s.append(chord.Chord(['F4', 'A4', 'C5'], quarterLength=2))
        return s

    def test_simple_progression(self, simple_progression):
        """Test analysis of simple progression."""
        result = analyze_harmonic_rhythm(simple_progression)

        assert 'changes_per_measure' in result
        assert 'change_points' in result
        assert result['changes_per_measure'] > 0
```

## 🐛 Debugging Tips

```bash
# Run single test with verbose output
pytest tests/test_pattern.py::test_detect_motifs -vvs

# Drop into debugger on failure
pytest tests/ --pdb

# See print statements
pytest tests/ -s

# Run only failed tests from last run
pytest tests/ --lf

# Run with detailed traceback
pytest tests/ --tb=long
```

## 📊 Performance Guidelines

- Avoid O(n³) or worse algorithms for large inputs
- Use caching decorators for expensive computations
- Profile code with cProfile for bottlenecks
- Test with realistic data sizes

```python
from cancrizans.cache import memoize

@memoize
def expensive_analysis(score: stream.Score) -> Dict:
    """Cache expensive computations."""
    # ... implementation
    pass
```

## 🔍 Security Guidelines

- Never commit secrets, tokens, or credentials
- Validate all user input
- Use safe file operations (check paths, permissions)
- Follow OWASP guidelines for music file parsing
- Run `bandit` security scanner: `bandit -r cancrizans`

## 💬 Communication

- **Issues**: Bug reports, feature requests, questions
- **Pull Requests**: Code contributions
- **Discussions**: Design discussions, ideas, help

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors are recognized in:
- `CHANGELOG.md` for their contributions
- GitHub contributors page
- Release notes for significant features

Thank you for contributing to Cancrizans! 🎵
