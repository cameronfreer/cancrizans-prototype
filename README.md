# 🦀 Cancrizans

**Explore and render J.S. Bach's Crab Canon as a strict musical palindrome**

Cancrizans is a comprehensive toolkit for analyzing, verifying, and rendering palindromic musical structures, with a focus on Bach's *Canon Cancrizans* from *The Musical Offering* (BWV 1079).

[![Python Tests](https://img.shields.io/badge/tests-26%20passed-brightgreen)](cancrizans/tests/)
[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Music](https://img.shields.io/badge/music-Public%20Domain-green)](data/)

## 🚀 Quick Links

- **[📚 Examples & Usage →](EXAMPLES.md)** - Auto-generated examples with real outputs
- **[🎨 Visual Gallery →](GALLERY.md)** - Browse all examples with images
- **[📓 Jupyter Notebooks →](notebooks/)** - 3 interactive tutorials (Bach, transformations, symmetry)
- **[🌐 Web Interface →](web/)** - Live palindrome visualization
- **[📖 API Reference →](docs/API_REFERENCE.md)** - Complete API documentation (auto-generated)
- **[⌨️ CLI Reference →](docs/CLI_REFERENCE.md)** - Command-line guide with examples
- **[📊 Feature Matrix →](docs/FEATURE_MATRIX.md)** - Feature comparison across components

## What is a Crab Canon?

A **Crab Canon** (Latin: *Canon Cancrizans*) is a musical composition technique where a melody plays forward while simultaneously playing backward (retrograde). Bach's Crab Canon from *The Musical Offering* is one of the most famous examples in Western music.

In this canon:
- **Voice 1** plays the melody forward →
- **Voice 2** plays the exact same melody backward ←
- When played together, they create a perfect **musical palindrome** ↔

The name comes from the sideways movement of crabs, referencing the backward motion of the retrograde voice. In Bach's original manuscript, the piece was notated as a puzzle: a single staff that could be read from either end, with one performer reading normally and another reading the page upside down.

### By the Numbers

**Authentic Bach Crab Canon (BWV 1079):**
- **184 notes** per voice (368 total)
- **144 quarter notes** duration (~2.4 minutes at 60 BPM)
- **100% palindromic** - verified with `is_time_palindrome()`
- **2 voices** in perfect retrograde

## ✨ Features

### 🐍 Python Library & CLI
- **Core transformations**: retrograde, inversion, augmentation, diminution, mirror canon
- **Analysis tools**: interval, harmonic, and rhythm analysis
- **Palindrome verification**: automated structural analysis with pairwise mapping
- **Export formats**: MIDI, MusicXML, LilyPond (.ly), ABC notation (.abc), WAV (optional)
- **Visualizations**: piano roll and symmetry plots with matplotlib
- **CLI interface**: analyze, render, synthesize, and **research** (batch analysis)
- **Research tools**: Batch processing, multi-format export (CSV/JSON/LaTeX/Markdown)
- **Performance optimization**: Caching decorators (@memoize, @lru_cache, @disk_cache)
- **Comprehensive tests**: 80 tests, 100% offline, all passing

### 🌐 Web Interface (PWA)
- **✏️ Interactive Composer**: Create your own crab canons!
  - Click-to-add piano roll editor
  - Drag to move, shift+click to delete
  - Real-time retrograde preview (red notes)
  - 6 pre-made templates
  - Live playback with dual-voice synthesis
- **📁 MIDI Import**: Upload and analyze your own MIDI files
  - Drag-and-drop interface
  - Multi-track support
  - Automatic tempo and time signature detection
- **🔍 Palindrome Analyzer**: Comprehensive symmetry analysis
  - Overall symmetry score (0-100%)
  - Pitch, rhythm, velocity, and interval metrics
  - Automatic palindromic segment detection
  - Actionable recommendations
- **🔄 Transformation Chain Builder**: Create complex transformations
  - 8 transformation types (retrograde, inversion, augmentation, etc.)
  - Chain multiple operations
  - Preset patterns (Crab Canon, Table Canon)
  - Export/import transformation chains
- **🎬 Animated Piano Roll**: Real-time visualization
  - Note highlighting during playback
  - 4 color schemes (velocity, pitch, heatmap, monochrome)
  - Configurable note names display
  - Smooth canvas-based rendering
- **💾 Export & Share**: Multiple sharing options
  - Export as MIDI, JSON
  - URL-based sharing with compressed data
  - LocalStorage persistence
  - Copy shareable links
- **📚 Interactive Tutorial**: 11-step guided learning experience
- **Interactive notation** rendered with VexFlow (two-staff layout)
- **Audio playback** with Tone.js (5 instruments, adjustable tempo)
- **Mirror view**: visual palindrome structure with symmetry connectors
- **Real-time waveform visualization**
- **Playback modes**: normal, first/second half, from-middle-outward
- **Keyboard shortcuts**: Space (play/pause), H (highlight), M (metronome)
- **Progressive Web App**: Installable, works offline
- **Fully accessible**: WCAG AA compliant, screen reader support

### 🎓 Educational Materials
- **4 Complete Lesson Plans** (30-45 min each, standards-aligned)
- **Interactive Tutorial System** (built into web app)
- **Quiz Bank**: 15+ questions with answer keys
- **Tutorial Guide**: Step-by-step teaching instructions
- **2 Jupyter Notebooks**: Bach exploration + waveform palindromes
- **Pre-executed outputs**: All notebooks run with visualizations

### 📊 Research Tools
- **Batch Analysis**: Analyze entire directories of canons
- **Comparative Statistics**: Cross-corpus analysis
- **Export Formats**: CSV, JSON, LaTeX tables, Markdown
- **CanonAnalyzer**: Deep single-file analysis with caching
- **BatchAnalyzer**: Multi-file processing pipeline
- **ResearchExporter**: Academic-ready data formats

### 📓 Jupyter Notebooks
- **Bach Crab Canon Exploration**: step-by-step analysis (843KB, pre-executed)
- **Waveform Palindromes**: Symmetric envelope visualization (NEW!)
- **Interactive tutorials**: covers retrograde, inversion, custom canons
- **Visual outputs**: generates piano rolls, symmetry plots, spectrograms

### 📚 Documentation
- **Auto-generated examples** with real code execution
- **Visual gallery** with 40+ images (10 complete canons)
- **Complete API docs** with type hints
- **CHANGELOG**: Full version history
- **Lesson plans, quizzes, tutorial guides**

## Installation

### Python Package

```bash
# Clone the repository
git clone https://github.com/yourusername/cancrizans.git
cd cancrizans

# Install with pip (development mode)
pip install -e .

# Install with optional audio support
pip install -e ".[audio]"

# Install development dependencies
pip install -e ".[dev]"
```

### Web Interface

```bash
cd web
npm install
npm run dev  # Development server at http://localhost:3000
npm run build  # Build for production
```

## Quick Start

### Python CLI

```bash
# Analyze Bach's Crab Canon
python -m cancrizans analyze data/crab_canon.musicxml

# Render to various formats
python -m cancrizans render \
  --midi out/crab.mid \
  --xml out/crab.musicxml \
  --roll out/piano_roll.png \
  --mirror out/symmetry.png

# Synthesize a new crab canon from the theme
python -m cancrizans synthesize --tempo 84 --transpose 0

# Research: batch analyze multiple canons
python -m cancrizans research examples/ --pattern "*.mid" --all

# Generate algorithmic canons
python -m cancrizans generate scale --output canon.mid --validate
python -m cancrizans generate fibonacci --length 13 --output fib.mid

# Validate canon quality
python -m cancrizans validate my_canon.mid --verbose
```

### Python API

```python
from cancrizans import (
    load_bach_crab_canon,
    retrograde,
    is_time_palindrome,
    assemble_crab_from_theme
)
from cancrizans.io import to_midi, to_musicxml, to_lilypond, to_abc
from cancrizans.viz import piano_roll, symmetry

# Load Bach's Crab Canon
score = load_bach_crab_canon()

# Verify it's a palindrome
print(is_time_palindrome(score))  # True

# Export to multiple formats
to_midi(score, "output.mid")
to_musicxml(score, "output.musicxml")
to_lilypond(score, "output.ly")  # Professional engraving
to_abc(score, "output.abc")  # Text-based notation

# Visualize
piano_roll(score, "piano_roll.png")
symmetry(score, "symmetry.png")

# Create your own crab canon
from music21 import stream, note

theme = stream.Stream()
theme.append(note.Note('C4', quarterLength=1.0))
theme.append(note.Note('D4', quarterLength=1.0))
theme.append(note.Note('E4', quarterLength=1.0))

crab = assemble_crab_from_theme(theme)
print(is_time_palindrome(crab))  # True

# Generate algorithmic canons
from cancrizans.generator import CanonGenerator

gen = CanonGenerator(seed=42)
canon = gen.generate_fibonacci_canon(root='G4', length=13)
to_midi(canon, "fibonacci_canon.mid")

# Validate canon quality
from cancrizans.validator import CanonValidator

validator = CanonValidator()
results = validator.validate(canon)
print(f"Quality: {results['overall_quality']:.3f}")
print(f"Grade: {validator.get_quality_grade(results['overall_quality'])}")

# Performance optimization with caching
from cancrizans.cache import memoize, disk_cache, clear_all_caches

# Cache expensive computations in memory
@memoize
def expensive_analysis(score_data):
    # Your expensive analysis here
    return results

# Or use disk cache for persistent results
@disk_cache(maxsize=100)
def batch_process(file_path):
    # Processing that should persist across runs
    return results

# Clear all caches when needed
clear_all_caches()
```

### Web Interface

1. Open `web/index.html` in a browser (after running `npm run dev`)
2. Use the playback controls to explore the canon
3. Toggle "Highlight Symmetry" to see palindromic pairs
4. Try different playback modes and tempos
5. Use keyboard shortcuts for quick control

## Testing

The project includes a comprehensive test suite with 176 tests (100% pass rate, 88% coverage) covering core functionality:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=cancrizans --cov-report=html

# Run specific test file
pytest tests/test_generator.py

# Run CLI integration tests
pytest tests/test_cli_integration.py

# Run tests in verbose mode
pytest -v
```

**Test Coverage:**
- Overall: 88% (+22 percentage points from Phase 13!)
- CLI module: 85% (was 0%)
- Bach Crab Canon: 98% (+25pp)
- Research tools: 99%
- Visualization: 98%
- Generator module: 95%
- Validator module: 89%
- Canon transformations: 85%
- Cache module: 80%
- I/O module: 78%

**Test Categories:**
- Unit tests: 122 tests
- Integration tests: 11 tests
- Visualization tests: 19 tests
- Research tests: 31 tests
- CLI command tests: 37 tests (new)

Coverage reports are generated in `htmlcov/` directory.

## Project Structure

```
cancrizans/
├── README.md
├── LICENSE
├── pyproject.toml
├── cancrizans/
│   ├── __init__.py
│   ├── canon.py           # Core transformations
│   ├── bach_crab.py       # Bach's Crab Canon data
│   ├── io.py              # MIDI/MusicXML/WAV export
│   ├── viz.py             # Visualization
│   ├── cli.py             # Command-line interface
│   └── tests/
│       ├── test_retrograde.py
│       ├── test_palindrome.py
│       └── test_exports.py
├── data/
│   └── crab_canon.musicxml  # Public domain transcription
└── web/
    ├── index.html
    ├── package.json
    ├── vite.config.ts
    ├── tsconfig.json
    └── src/
        ├── main.ts
        ├── scoreLoader.ts  # Embedded score data
        ├── player.ts       # Tone.js audio
        ├── notation.ts     # VexFlow rendering
        ├── mirrorView.ts   # Palindrome visualization
        ├── ui.ts           # Controls
        └── styles.css
```

## CLI Commands

### `analyze`

Analyze a musical score for palindromic structure:

```bash
python -m cancrizans analyze data/crab_canon.musicxml
```

Output:
```
Analyzing: data/crab_canon.musicxml
------------------------------------------------------------
Number of voices: 2
Total duration: 36.00 quarter notes
  Voice 1: 52 notes, 0 rests
  Voice 2: 52 notes, 0 rests

Palindrome Verification:
------------------------------------------------------------
is_time_palindrome: True
✓ This score is a valid crab canon (retrograde canon)
Symmetric pairs in voice 1: 26
Total events in voice 1: 52
✓ All events participate in symmetric pairs
```

### `render`

Render a score to various output formats:

```bash
python -m cancrizans render \
  --input data/crab_canon.musicxml \
  --midi out/crab.mid \
  --xml out/crab.musicxml \
  --roll out/piano_roll.png \
  --mirror out/symmetry.png
```

For WAV export (requires FluidSynth):
```bash
python -m cancrizans render \
  --midi out/crab.mid \
  --wav out/crab.wav \
  --soundfont /path/to/soundfont.sf2
```

### `synthesize`

Create a crab canon from the embedded theme:

```bash
python -m cancrizans synthesize --tempo 84 --transpose 2 --output out/
```

## Visualizations

### Piano Roll

Shows notes as horizontal bars on a pitch-time grid:

```python
from cancrizans import load_bach_crab_canon
from cancrizans.viz import piano_roll

score = load_bach_crab_canon()
piano_roll(score, "piano_roll.png", dpi=150)
```

### Symmetry Plot

Displays the palindromic structure with a central time axis and symmetry connectors:

```python
from cancrizans.viz import symmetry

symmetry(score, "symmetry.png", dpi=150)
```

## Web Interface Features

### Playback Controls

- **Play/Pause/Stop**: Standard playback controls
- **Tempo**: Adjustable from 40-160 BPM
- **Mode**: Normal, First Half, Second Half, From Middle
- **Mute**: Toggle individual voices on/off
- **Metronome**: Audible beat reference

### Visualizations

1. **Musical Notation** (VexFlow)
   - Two-staff rendering of both voices
   - Proper clefs, key signature, time signature
   - Measure-by-measure layout

2. **Mirror View** (Canvas)
   - Horizontal time axis with central midpoint
   - Notes plotted by pitch and time
   - Symmetry connectors between palindromic pairs
   - Real-time playback cursor
   - Active note highlighting

### Keyboard Shortcuts

- **Space**: Play/Pause
- **H**: Toggle symmetry highlighting
- **M**: Toggle metronome

## Explore Further

### Transformations

Try different transformations to understand canonical techniques:

```python
from cancrizans import retrograde, invert

# Retrograde (time reversal)
backward_theme = retrograde(theme)

# Inversion (pitch reflection)
inverted_theme = invert(theme, axis_pitch='C4')

# Retrograde-inversion (both transformations)
retro_inverted = invert(retrograde(theme), axis_pitch='C4')
```

### Custom Canons

Create your own crab canon:

```python
from music21 import stream, note
from cancrizans import assemble_crab_from_theme, is_time_palindrome

# Define your theme
theme = stream.Stream()
theme.append(note.Note('G4', quarterLength=1.0))
theme.append(note.Note('A4', quarterLength=0.5))
theme.append(note.Note('B4', quarterLength=0.5))
theme.append(note.Note('C5', quarterLength=2.0))

# Assemble canon
canon = assemble_crab_from_theme(theme)

# Verify palindrome property
assert is_time_palindrome(canon)

# Export
to_midi(canon, "my_crab_canon.mid")
```

## Testing

Run the test suite:

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=cancrizans --cov-report=html

# Run specific test file
pytest cancrizans/tests/test_palindrome.py -v
```

All tests run offline and require no external resources.

## Requirements

### Python
- Python 3.11+
- music21 >= 9.1.0
- matplotlib >= 3.8.0
- mido >= 1.3.0
- numpy >= 1.26.0

### Optional (for WAV export)
- midi2audio >= 0.1.1
- FluidSynth (system dependency)

### Web
- Node.js 18+
- vite >= 5.0.0
- typescript >= 5.3.0
- tone >= 15.0.4
- vexflow >= 4.2.4

## About the Score

The embedded MusicXML represents a faithful, public-domain transcription of Bach's Crab Canon from *The Musical Offering* (BWV 1079). This transcription:

- Preserves the original two-voice structure
- Uses F major (B♭) key signature
- Includes all original pitches and rhythms
- Normalizes notation for modern readers (no upside-down puzzles)

Editorial choices prioritize clarity and accessibility while maintaining the essential palindromic structure.

## License

**Code**: MIT License (see LICENSE file)

**Musical Score**: Public Domain (Bach's *Canon Cancrizans*, BWV 1079)

## Contributing

Contributions welcome! Areas of interest:

- Additional canonical forms (augmentation, diminution, inversion canons)
- More historical examples (Machaut, Ockeghem, Webern)
- Enhanced visualizations (animated score following, 3D symmetry plots)
- Performance optimizations
- Alternative notation systems (tablature, graphic notation)

## References

- Bach, J.S. *Das Musikalische Opfer* (The Musical Offering), BWV 1079 (1747)
- Hofstadter, D. *Gödel, Escher, Bach: An Eternal Golden Braid* (1979)
- Lewin, D. *Musical Form and Transformation* (1993)

## Acknowledgments

Built with:
- [music21](http://web.mit.edu/music21/) - Python toolkit for music analysis
- [VexFlow](https://www.vexflow.com/) - JavaScript music notation rendering
- [Tone.js](https://tonejs.github.io/) - Web audio framework
- [Vite](https://vitejs.dev/) - Modern frontend build tool

---

**Cancrizans** - *"Going backwards, like a crab"* 🦀
