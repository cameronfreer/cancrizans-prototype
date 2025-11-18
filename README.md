# 🦀 Cancrizans

**Explore and render J.S. Bach's Crab Canon as a strict musical palindrome**

Cancrizans is a comprehensive toolkit for analyzing, verifying, and rendering palindromic musical structures, with a focus on Bach's *Canon Cancrizans* from *The Musical Offering* (BWV 1079).

[![CI](https://github.com/cancrizans-project/cancrizans-prototype/workflows/CI/badge.svg)](https://github.com/cancrizans-project/cancrizans-prototype/actions)
[![codecov](https://codecov.io/gh/cancrizans-project/cancrizans-prototype/branch/main/graph/badge.svg)](https://codecov.io/gh/cancrizans-project/cancrizans-prototype)
[![Python](https://img.shields.io/badge/python-3.11%2B%20%7C%203.12-blue)](https://www.python.org)
[![Tests](https://img.shields.io/badge/tests-811%20passed-brightgreen)](tests/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Code Quality](https://img.shields.io/badge/code%20quality-ruff-purple)](https://github.com/astral-sh/ruff)

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
- **Advanced canon types**: table canon, mensuration canon, spiral canon, puzzle canon solver
- **Pattern analysis** (NEW!): 8 advanced analysis functions
  - Motif detection with transposition tracking
  - Melodic sequence identification
  - Imitation point detection (fugal entries)
  - Fugue structure analysis (subject, answer, episodes, stretto)
  - Voice independence metrics
  - Pattern complexity scoring
  - Thematic development tracking
  - Contour similarity matching
- **Microtonal music** (NEW!): 40+ tuning systems, 36+ world music scales
  - Historical temperaments (Werckmeister, Kirnberger, Vallotti, etc.)
  - Just intonation (3-limit, 5-limit, 7-limit)
  - Equal temperaments (12, 19, 24, 31, 53-TET)
  - World music scales (Arabic maqamat, Indian ragas, Indonesian gamelan)
- **Analysis tools**: interval, harmonic, rhythm, and counterpoint analysis
- **Music theory analysis**: voice leading, cadence detection, modulation detection, species counterpoint
- **Palindrome verification**: automated structural analysis with pairwise mapping
- **Export formats**: MIDI, MusicXML, LilyPond (.ly), ABC notation (.abc), WAV (optional)
- **Visualizations**: piano roll and symmetry plots with matplotlib
- **CLI interface**: analyze, render, synthesize, validate, generate, **analyze-patterns**, and research
- **Algorithmic generation**: 11 algorithms (scale, arpeggio, fibonacci, golden ratio, modal, etc.)
- **Quality validation**: Automated scoring and recommendations for generated canons
- **Research tools**: Batch processing, multi-format export (CSV/JSON/LaTeX/Markdown)
- **Performance optimization**: Caching decorators (@memoize, @lru_cache, @disk_cache)
- **Transformation chains**: Compose multiple transformations with fluent builder pattern
- **Advanced MIDI features**: Velocity curves, tempo curves, multi-instrument export, MIDI analysis
- **World-class testing**: 811 tests, comprehensive coverage, 100% pass rate

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

# Install with uv (recommended)
uv sync

# Install with optional audio support
uv sync --extra audio

# Install development dependencies
uv sync --extra dev

# Or install all optional dependencies
uv sync --all-extras
```

### Web Interface

```bash
cd web

# Using pnpm (recommended)
pnpm install
pnpm dev  # Development server at http://localhost:3000
pnpm build  # Build for production

# Or using npm
npm install
npm run dev
npm run build
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

# NEW: Compose transformations with TransformationChain
from cancrizans import TransformationChain

# Build transformation chains with fluent API
result = (TransformationChain()
          .add(retrograde)
          .add(lambda s: invert(s, axis_pitch='C4'))
          .add(lambda s: augmentation(s, factor=2.0))
          .apply(theme))

# Or use preset chains
crab_chain = TransformationChain.crab_canon()
mirror_chain = TransformationChain.mirror_canon(axis_pitch='G4')
table_chain = TransformationChain.table_canon()  # retrograde + inversion
```

### Web Interface

1. Open `web/index.html` in a browser (after running `npm run dev`)
2. Use the playback controls to explore the canon
3. Toggle "Highlight Symmetry" to see palindromic pairs
4. Try different playback modes and tempos
5. Use keyboard shortcuts for quick control

## Testing

The project includes a comprehensive test suite with 455 tests (100% pass rate, 97% coverage) covering core functionality:

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=cancrizans --cov-report=html

# Run specific test file
uv run pytest tests/test_generator.py

# Run CLI integration tests
uv run pytest tests/test_cli_integration.py

# Run tests in verbose mode
uv run pytest -v
```

**Test Coverage:**
- Overall: 97% (rock solid! Only 39 lines missing) 🎯
- __main__ module: 100%
- Research tools: 99%
- I/O module: 99%
- Canon transformations: 99%
- Cache module: 98% (was 95% in Phase 19, +3pp!) ⭐
- Generator module: 98%
- Bach Crab Canon: 98%
- Transformation chains: 98%
- Visualization: 98%
- Validator module: 96% (was 94% in Phase 19, +2pp!)
- CLI module: 94%

**Test Categories:**
- Unit tests: 206 tests (includes 84 edge case tests across all modules)
- Integration tests: 11 tests
- Visualization tests: 19 tests
- Research tests: 31 tests
- CLI command tests: 52 tests (includes 2 __main__ module tests)
- Transformation chain tests: 19 tests
- Edge case tests: 84 tests across validator, CLI, canon, I/O, cache, and generator

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
uv sync --extra dev

# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=cancrizans --cov-report=html

# Run specific test file
uv run pytest cancrizans/tests/test_palindrome.py -v
```

All tests run offline and require no external resources.

## CI/CD Infrastructure

Cancrizans maintains a comprehensive CI/CD pipeline with multiple automated workflows:

### 🔄 Continuous Integration
- **Main CI Pipeline** (`.github/workflows/ci.yml`)
  - Parallel test execution with pytest-xdist
  - Code coverage tracking with Codecov
  - Code quality checks with ruff
  - Type checking with mypy
  - Test result parsing and summaries
  - Full CLI workflow validation
  - Matrix testing (Python 3.11, 3.12)

### 🔒 Security Scanning
- **CodeQL Analysis** (`.github/workflows/codeql.yml`)
  - Semantic code analysis
  - Security and quality query sets
  - Weekly scheduled scans
  - SARIF result uploads

- **Dependency & Code Security** (`.github/workflows/security-scan.yml`)
  - Dependency vulnerability scanning (Safety)
  - Python security linting (Bandit)
  - Daily automated scans
  - JSON report generation

### ⚡ Performance Monitoring
- **Benchmark Suite** (`.github/workflows/benchmark.yml`)
  - 20+ performance benchmarks
  - Historical comparison tracking
  - Regression detection (>10% threshold)
  - Weekly scheduled runs
  - PR-level performance feedback
  - See [benchmarks/README.md](benchmarks/README.md) for details

### 📝 Documentation Quality
- **Documentation Checks** (`.github/workflows/docs-check.yml`)
  - Markdown linting
  - Link validation
  - Spell checking
  - Notebook validation
  - Docstring coverage analysis

- **Documentation Deployment** (`.github/workflows/docs-deploy.yml`)
  - Automatic Sphinx documentation generation
  - GitHub Pages deployment
  - API reference generation
  - Notebook HTML conversion
  - Custom landing page

### 📊 Quality Assurance
- **Coverage Enforcement** (`.github/workflows/coverage-check.yml`)
  - Minimum 80% coverage threshold
  - Per-module coverage tracking
  - PR coverage comments
  - Detailed coverage reports
  - Identifies low-coverage files

- **Nightly Comprehensive Tests** (`.github/workflows/nightly.yml`)
  - Full test matrix (Python 3.11, 3.12, 3.13 × Ubuntu, macOS, Windows)
  - Extended integration tests
  - Memory profiling
  - Notebook execution validation
  - Benchmark regression detection
  - Automatic issue creation on failure

- **Dependency Review** (`.github/workflows/dependency-review.yml`)
  - Outdated package detection
  - Security vulnerability audits
  - License compatibility checks
  - Dependency tree analysis
  - Installation size tracking

### 🤖 Automation
- **Dependabot** (`.github/dependabot.yml`)
  - Weekly dependency updates
  - Grouped minor/patch updates
  - Separate Python and GitHub Actions updates

- **Stale Issue Management** (`.github/workflows/stale.yml`)
  - Auto-mark stale issues (60 days)
  - Auto-close after 7 days (issues) or 14 days (PRs)
  - Customizable exemptions

- **Auto-labeling** (`.github/workflows/labeler.yml`)
  - Automatic PR labels based on changed files
  - PR size labeling (xs/s/m/l/xl)
  - First-time contributor greetings

- **Commit Linting** (`.github/workflows/commit-lint.yml`)
  - Commit message validation
  - Style guidelines enforcement

- **Label Management** (`.github/workflows/labels-sync.yml`)
  - Automatic GitHub label synchronization
  - Consistent labeling across PRs and issues
  - 50+ predefined labels (priority, type, component, status)

- **Cleanup** (`.github/workflows/cleanup.yml`)
  - Weekly artifact cleanup (>30 days old)
  - Cache cleanup to free storage
  - Old workflow run removal (>90 days)

- **Pre-commit Hooks** (`.pre-commit-config.yaml`)
  - Ruff formatting and linting
  - Markdown, YAML, and notebook formatting
  - Security checks with Bandit
  - Type checking with mypy
  - Shell script validation
  - 10+ pre-commit hooks for code quality

- **Issue Management** (`.github/workflows/issue-management.yml`)
  - Automatic issue triaging and labeling
  - Duplicate issue detection
  - Auto-assignment to milestones by priority
  - Answered question auto-closing
  - First-time contributor welcome messages

- **Contributor Recognition** (`.github/workflows/contributors.yml`)
  - Automatic CONTRIBUTORS.md generation
  - Contribution statistics tracking
  - Thank you messages for first-time contributors
  - Weekly contribution reports

- **Metrics Collection** (`.github/workflows/metrics.yml`)
  - Repository statistics tracking
  - Code and git metrics
  - CI/CD infrastructure metrics
  - JSON and markdown reports

- **Cache Optimization** (`.github/workflows/cache-optimization.yml`)
  - Daily cache warming for faster CI
  - Multi-platform pip/uv cache pre-population
  - Docker layer cache optimization
  - Test cache warming (pytest, mypy, ruff)

- **Link Checker** (`.github/workflows/link-checker.yml`)
  - Weekly external link validation
  - Broken link detection and reporting
  - Internal file reference validation
  - API endpoint health checks
  - Automatic issue creation for broken links

- **Auto-Merge** (`.github/workflows/auto-merge.yml`)
  - Automatic Dependabot PR merging
  - Smart policy (patch/minor dev deps, patch prod deps)
  - CI check waiting and validation
  - Auto-approval for safe updates

- **Notifications** (`.github/workflows/notifications.yml`)
  - Workflow failure alerts
  - Security issue notifications
  - Release announcements
  - Weekly activity digests
  - Status page updates on GitHub Pages

- **Smart Testing** (`.github/workflows/smart-testing.yml`)
  - Intelligent test selection based on changed files
  - Component-based test matrix
  - Time savings estimation and reporting
  - PR comments with test strategy

### 📊 Analytics & Monitoring
- **Test Analytics** (`.github/workflows/test-analytics.yml`)
  - Detailed test result analysis
  - Slowest test tracking
  - Coverage trend analysis
  - Flaky test detection (nightly)
  - Mutation testing for test quality

- **Performance Tracking** (`.github/workflows/performance-tracking.yml`)
  - Historical performance data collection
  - Performance trend visualization
  - GitHub Pages dashboard deployment
  - PR-level performance impact analysis
  - Automated regression alerts

### 📦 Release Automation
- **Release Workflow** (`.github/workflows/release.yml`)
  - Version validation across files
  - Full test suite on multiple Python versions
  - Distribution building (wheel + source)
  - Automatic changelog generation
  - GitHub release creation
  - Asset uploading
  - PyPI publishing (ready to enable)

- **Release Drafter** (`.github/workflows/release-drafter.yml`)
  - Automatic release notes from PR labels
  - Semantic version resolution (major/minor/patch)
  - Categorized changelog (features, bugs, security, etc.)
  - Auto-labeling based on file changes
  - Draft releases for review before publishing

### 📊 Quality Metrics
- **811+ tests** with 100% pass rate
- **80%+ code coverage** enforced with automated checks
- **Zero security vulnerabilities** (daily scans with CodeQL, Safety, Bandit)
- **18 performance benchmarks** with regression detection (<10% threshold)
- **29 automated workflows** covering all aspects of development
- **50+ GitHub labels** for organized issue/PR management
- **10+ pre-commit hooks** for local code quality enforcement
- **Nightly comprehensive tests** across 3 Python versions and 3 OS platforms
- **Automated documentation deployment** to GitHub Pages
- **Docker support** with multi-architecture builds (amd64, arm64)
- **VS Code dev container** for instant development setup
- **Automated code review** with complexity, security, and quality checks
- **Automatic changelog generation** from PR labels
- **Test analytics** with flaky test detection and mutation testing
- **Performance tracking dashboard** with historical trends
- **Automated issue management** with smart triaging
- **Contributor recognition** with automatic acknowledgments
- **Metrics collection** tracking code, git, and CI/CD statistics
- **Cache optimization** with daily warming for faster builds
- **Link validation** with weekly checks and auto-issue creation
- **Auto-merge** for safe Dependabot updates
- **Smart testing** saving CI time with targeted test selection
- **Notification system** for failures, security, and releases
- **Professional contribution infrastructure** (templates, guides, automation)

All workflows include automated summaries in GitHub Actions for easy monitoring. See `.github/workflows/` for complete configurations.

### 🛠️ Development Tools
- **Pre-commit**: `pre-commit install` to enable local code quality checks
- **Benchmarks**: `python benchmarks/benchmark_suite.py` for performance testing
- **Coverage**: `pytest --cov=cancrizans --cov-report=html` for detailed coverage reports
- **Docs**: Build documentation locally with Sphinx (see `.github/workflows/docs-deploy.yml`)
- **Docker**: `docker-compose up dev` for containerized development
- **VS Code**: Dev container configuration in `.devcontainer/` for seamless setup
- **Code Quality**: `radon cc cancrizans/ -a` for complexity analysis

### 🐳 Docker Support

Cancrizans includes comprehensive Docker support for consistent development and deployment:

```bash
# Build the Docker image
docker build -t cancrizans .

# Run a command
docker run -v $(pwd)/output:/output cancrizans \
  cancrizans generate scale --output /output/canon.mid

# Development with docker-compose
docker-compose run --rm dev /bin/bash

# Run tests in container
docker-compose --profile testing run --rm test

# Run benchmarks
docker-compose --profile benchmark run --rm benchmark

# Start Jupyter notebook
docker-compose --profile jupyter up jupyter
```

**Pre-built images** are available on GitHub Container Registry:
```bash
docker pull ghcr.io/cancrizans-project/cancrizans-prototype:latest
```

**VS Code Dev Container**: Open the project in VS Code and select "Reopen in Container" for a fully configured development environment with all tools pre-installed.

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
