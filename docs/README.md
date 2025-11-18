# Cancrizans Documentation

> Advanced pattern analysis and microtonal canon generation for music21

[![Tests](https://github.com/cancrizans-project/cancrizans-prototype/workflows/CI/badge.svg)](https://github.com/cancrizans-project/cancrizans-prototype/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Cancrizans is a comprehensive Python library for analyzing and generating musical canons, with a focus on:
- **Pattern Analysis**: Detect motifs, sequences, imitation, and thematic development
- **Microtonal Music**: 40+ tuning systems and 36+ world music scales
- **Fugue Analysis**: Subject/answer detection, episodes, stretto sections
- **Voice Analysis**: Independence metrics, crossing detection, harmonic density
- **Canon Generation**: Retrograde, inversion, augmentation, and advanced transformations

## Quick Start

```python
from music21 import stream, note
from cancrizans import mirror_canon, detect_motifs

# Create a simple theme
theme = stream.Stream()
for pitch in [60, 62, 64, 65]:
    theme.append(note.Note(pitch, quarterLength=1))

# Generate a retrograde canon
canon = mirror_canon(theme)

# Detect recurring patterns
motifs = detect_motifs(canon, min_length=3)
print(f"Found {len(motifs)} motifs")
```

## Features

### Pattern Analysis (Phase 10)

**8 Advanced Analysis Functions:**

| Function | Description |
|----------|-------------|
| `detect_motifs()` | Find recurring melodic/rhythmic patterns with sliding window |
| `identify_melodic_sequences()` | Detect sequential patterns at different pitch levels |
| `detect_imitation_points()` | Find voice imitation with similarity scoring |
| `analyze_thematic_development()` | Track theme evolution and transformations |
| `find_contour_similarities()` | Match melodic shapes regardless of intervals |
| `analyze_fugue_structure()` | Complete fugue analysis (subject, answer, episodes, stretto) |
| `calculate_voice_independence()` | Polyphonic independence metrics |
| `calculate_pattern_complexity()` | Complexity scoring for musical patterns |

### Microtonal Features

**40+ Tuning Systems:**
- Equal temperaments: 12, 19, 24, 31, 53-TET
- Historical: Pythagorean, Werckmeister I-VI, Kirnberger I-III, Vallotti, Young
- Just intonation: 3-limit, 5-limit, 7-limit

**36+ World Music Scales:**
- **Arabic**: Hijaz, Rast, Bayati, Saba, Nahawand, Sikah, Kurd
- **Indian**: Bhairav, Bhairavi, Todi, Kafi, Yaman, Poorvi, Marwa
- **Indonesian**: Pelog, Slendro
- **East Asian**: In, Yo, Hirajoshi, Iwato, Kumoi

### Canon Transformations

- Retrograde (crab canon)
- Inversion
- Augmentation/Diminution
- Mirror canon
- Stretto
- Table canon
- Mensuration canon
- Spiral canon
- Canon per tonos

## Installation

```bash
pip install cancrizans

# With optional dependencies
pip install cancrizans[dev]      # Development tools
pip install cancrizans[audio]    # Audio synthesis
pip install cancrizans[notebooks] # Jupyter support
```

## Tutorials

We provide comprehensive Jupyter notebook tutorials:

### 1. [Pattern Analysis Tutorial](tutorials/pattern_analysis_tutorial.md)
- Motif detection examples
- Melodic sequence identification
- Imitation point detection
- Thematic development analysis
- Fugue structure analysis
- Voice independence metrics
- Pattern complexity measurement

### 2. [Microtonal Canon Tutorial](tutorials/microtonal_canon_tutorial.md)
- Historical temperaments
- World music scales
- Microtonal interval analysis
- Cross-cultural compatibility analysis
- Tuning system comparison

### 3. [Quick Start Guide](tutorials/quick_start.md)
- Basic canon creation
- Simple transformations
- Getting started quickly

## CLI Usage

```bash
# List available tuning systems
cancrizans scales --list-tunings

# Create a microtonal canon
cancrizans microtonal-canon --tuning WERCKMEISTER_III --canon-type retrograde

# Analyze patterns in a MIDI file
cancrizans analyze-patterns input.mid --output analysis.json

# Generate world music canon
cancrizans world-canon --scale MAQAM_HIJAZ --length 16
```

## API Reference

### Pattern Analysis

```python
from cancrizans import (
    detect_motifs,
    analyze_fugue_structure,
    calculate_voice_independence
)

# Detect motifs in a score
motifs = detect_motifs(score, min_length=4, min_occurrences=2)

# Analyze fugue structure
fugue_analysis = analyze_fugue_structure(fugue, subject_length=8)
print(f"Found {len(fugue_analysis['answers'])} answers")

# Calculate voice independence
metrics = calculate_voice_independence(polyphony)
print(f"Rhythmic independence: {metrics['rhythmic_independence']:.2f}")
```

### Microtonal Canons

```python
from cancrizans import create_microtonal_canon, generate_world_music_canon
from cancrizans.microtonal import TuningSystem, ScaleType

# Create canon with historical temperament
canon = create_microtonal_canon(
    theme,
    TuningSystem.WERCKMEISTER_III,
    canon_type='retrograde'
)

# Generate world music canon
arabic_canon = generate_world_music_canon(
    ScaleType.MAQAM_HIJAZ,
    length=16,
    canon_type='inversion'
)
```

### Voice Analysis

```python
from cancrizans import calculate_voice_independence, analyze_fugue_structure

# Analyze voice independence
independence = calculate_voice_independence(score)
print(f"Melodic independence: {independence['melodic_independence']:.2f}")
print(f"Voice crossings: {independence['voice_crossing_count']}")
print(f"Harmonic density: {independence['harmonic_density']:.2f}")

# Analyze fugue structure
fugue_data = analyze_fugue_structure(fugue, subject_length=6)
print(f"Subject intervals: {fugue_data['subject']['intervals']}")
print(f"Answers: {len(fugue_data['answers'])}")
print(f"Stretto sections: {len(fugue_data['stretto_sections'])}")
```

## Architecture

```
cancrizans/
├── canon.py              # Canon transformations and analysis
├── pattern.py            # Pattern detection and analysis (NEW)
├── microtonal.py         # Microtonal scales and tuning systems
├── generator.py          # Algorithmic canon generation
├── io.py                 # File I/O (MIDI, MusicXML, LilyPond)
├── viz.py                # Visualization tools
├── audio.py              # Audio synthesis
├── ml.py                 # Machine learning features
├── research.py           # Research and batch analysis
└── cli.py                # Command-line interface
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cancrizans --cov-report=html

# Run specific test file
pytest tests/test_pattern.py -v
```

**Test Coverage:** 793 tests, 100% passing

## Development

```bash
# Clone repository
git clone https://github.com/cancrizans-project/cancrizans-prototype
cd cancrizans-prototype

# Install development dependencies
pip install -e ".[dev]"

# Run code quality checks
ruff check cancrizans tests

# Run security scans
bandit -r cancrizans

# Format code
ruff format cancrizans tests
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Run the test suite and linters
5. Submit a pull request

## Performance

Cancrizans is optimized for performance:
- **Pattern Detection**: O(n²) sliding window with early termination
- **Fugue Analysis**: Efficient imitation detection algorithms
- **Voice Analysis**: Vectorized numpy operations
- **Caching**: LRU caching for expensive computations

## Research Applications

Cancrizans is designed for music research:
- Corpus analysis of canons and fugues
- Cross-cultural music comparison
- Algorithmic composition studies
- Pattern recognition in polyphony
- Historical temperament analysis
- Microtonality research

## Citation

If you use Cancrizans in your research, please cite:

```bibtex
@software{cancrizans2025,
  title={Cancrizans: Advanced Pattern Analysis and Microtonal Canon Generation},
  author={Cancrizans Project},
  year={2025},
  url={https://github.com/cancrizans-project/cancrizans-prototype}
}
```

## License

MIT License - see [LICENSE](../LICENSE) for details.

## Changelog

### v0.40.0 (Latest)
- ✨ Added comprehensive tutorial notebooks
- ✨ Created documentation infrastructure
- 📝 Added notebook execution scripts

### v0.39.0
- ✨ Added `analyze_fugue_structure()` for complete fugue analysis
- ✨ Added `calculate_voice_independence()` for polyphonic metrics
- ✨ Added `calculate_pattern_complexity()` for complexity scoring

### v0.38.0
- 🔧 Major CI/CD enhancements (code quality, security scanning)
- 🔧 Added ruff linter with comprehensive rules
- 🔧 Added bandit security scanner
- 🔧 Improved caching and artifact management

### v0.37.3
- ✨ Created pattern analysis module (`pattern.py`)
- ✨ Added 5 core pattern detection functions
- ✅ Added 32 comprehensive pattern tests

[View Full Changelog](CHANGELOG.md)

## Support

- 📖 [Documentation](https://cancrizans.readthedocs.io) (Coming soon)
- 💬 [Discussions](https://github.com/cancrizans-project/cancrizans-prototype/discussions)
- 🐛 [Issue Tracker](https://github.com/cancrizans-project/cancrizans-prototype/issues)

## Acknowledgments

- Built with [music21](http://web.mit.edu/music21/)
- Inspired by J.S. Bach's Crab Canon from The Musical Offering (BWV 1079)
- Microtonal scales based on ethnomusicological research

---

Made with ❤️ by the Cancrizans Project
