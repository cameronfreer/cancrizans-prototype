# Changelog

All notable changes to the Cancrizans project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2025-11-12

### 📚 Phase 8: Documentation & Interactive Demos

#### Added
- **Auto-Generated API Reference** (`docs/API_REFERENCE.md`)
  - Complete Python API documentation (1,541 lines)
  - Function signatures and usage examples
  - All modules: canon, bach_crab, viz, research, io

- **CLI Reference Guide** (`docs/CLI_REFERENCE.md`)
  - Complete command-line documentation (367 lines)
  - All commands with examples
  - Workflows and pipeline integration

- **Feature Comparison Matrix** (`docs/FEATURE_MATRIX.md`)
  - Complete feature availability matrix
  - Performance benchmarks
  - Use case recommendations

- **Interactive Jupyter Notebooks** (2 new)
  - `transformation_techniques.ipynb`: Advanced transformations
  - `symmetry_analysis.ipynb`: Deep-dive into palindromes

- **Documentation Scripts**
  - `generate_api_docs.py`: Auto-generate API reference
  - `generate_cli_reference.py`: Auto-generate CLI guide

#### Enhanced
- **README**: Added links to new documentation
- **Notebooks**: Total of 3 comprehensive tutorials

## [0.4.0] - 2025-11-12

### 🚀 Phase 7: Advanced Features & Analysis

#### Added
- **MIDI File Import System** (`web/src/midi_import.ts`, 320+ lines)
  - Drag-and-drop file upload interface
  - Complete MIDI parser implementation
  - Handles multiple tracks and tempo changes
  - Extracts notes with pitch, velocity, time, and duration
  - Real-time file validation and error handling

- **Palindrome Detector** (`web/src/palindrome_detector.ts`, 400+ lines)
  - Comprehensive symmetry analysis system
  - Multiple metrics: pitch, rhythm, velocity, and interval symmetry
  - Overall palindrome score (0-100%)
  - Automatic palindromic segment detection
  - Smart recommendations for improving symmetry
  - Visual score displays with progress bars

- **Transformation Composer** (`web/src/transformation_composer.ts`, 300+ lines)
  - Chain multiple musical transformations
  - 8 transformation types: retrograde, inversion, augmentation, diminution, transpose, reflect, repeat, interleave
  - Parameter controls for each transformation
  - Preset chains: Crab Canon, Table Canon, Complex Example
  - Export/import transformation chains as JSON
  - Visual step-by-step chain display

- **Animated Piano Roll Visualization** (`web/src/animated_visualization.ts`, 450+ lines)
  - Real-time note highlighting during playback
  - 4 color schemes: default (velocity), rainbow (pitch), heatmap, monochrome
  - Adjustable playhead and time display
  - Note name overlay option
  - Smooth animations with canvas rendering
  - Configurable visualization parameters

- **Export & Share System** (`web/src/export_share.ts`, 450+ lines)
  - Export compositions as MIDI files
  - Export as JSON for backup/sharing
  - URL-based sharing with compressed composition data
  - LocalStorage persistence
  - List and load saved compositions
  - Copy shareable links to clipboard
  - Status messages for user feedback

- **Phase 7 Integration Module** (`web/src/phase7_integration.ts`, 600+ lines)
  - Unified manager for all Phase 7 features
  - Automatic URL composition loading on startup
  - Coordinated updates across all visualizations
  - Status message system
  - Complete UI event handling

#### Enhanced
- **Web UI** (`web/index.html`)
  - New sections for MIDI import, palindrome analysis, transformation composer
  - Animated visualization canvas
  - Enhanced export/share controls
  - Improved button organization

- **Styles** (`web/src/styles.css`, +300 lines)
  - Drop zone styling with drag-over effects
  - Symmetry score visualizations
  - Transformation chain step displays
  - Status message styling
  - Responsive design for new features

- **Main Application** (`web/src/main.ts`)
  - Phase7Manager initialization
  - Integrated all new features seamlessly

#### Technical Improvements
- Complete TypeScript type safety across all new modules
- Efficient MIDI binary parsing
- Canvas-based high-performance visualizations
- LRU caching for analysis results
- Modular architecture for easy extension

## [0.3.0] - 2025-11-11

### 🎓 Phase 5: Educational Features

#### Added
- **Interactive Tutorial System** (`web/src/tutorial.ts`)
  - 11-step guided tutorial through crab canon concepts
  - Element highlighting and positioning
  - Progress tracking with prev/next navigation
  - Accessible with screen reader support
  - Tutorial button in main UI

- **Auto-Generated Educational Documentation**
  - `docs/LESSON_PLANS.md`: 4 complete lesson plans (30-45 min each)
  - `docs/TUTORIAL_GUIDE.md`: Interactive tutorial instructions
  - `docs/QUIZ_BANK.md`: 15+ assessment questions with answer keys
  - Standards-aligned curricula (National Core Arts, Common Core, ISTE)
  - Cross-curricular connections (math, CS, language arts)

- **Document Generation Script** (`scripts/generate_educational_docs.py`)
  - Programmatically generates all educational markdown files
  - Timestamps and versioning
  - 427 lines of educational content generation

#### Enhanced
- Web UI CSS (+154 lines for tutorial system)
- Tutorial integration in `main.ts`
- Accessibility manager integration with tutorials

### 📊 Phase 4: Research Tools

#### Added
- **Research Module** (`cancrizans/research.py`, 288 lines)
  - `CanonAnalyzer`: Comprehensive single-canon analysis with caching
  - `BatchAnalyzer`: Corpus-wide batch processing
  - `ResearchExporter`: Export to CSV, JSON, LaTeX, Markdown
  - Comparative statistics across multiple canons

- **New CLI Command**: `cancrizans research`
  - Batch analyze directories of MIDI/MusicXML files
  - Pattern matching for file selection
  - Multi-format export options
  - Comparative statistics display

#### Enhanced
- CLI (`cancrizans/cli.py`) with research subcommand (+60 lines)
- Analysis capabilities for musicological research

### 🎨 Phase 3: Polish & Production Ready

#### Added
- **Progressive Web App (PWA)**
  - `web/public/manifest.json`: App manifest with metadata
  - `web/public/sw.js`: Service worker for offline functionality
  - Caching strategy for app shell and assets
  - Installable on mobile and desktop

- **Accessibility Features** (`web/src/accessibility.ts`, 145 lines)
  - `AccessibilityManager`: ARIA live regions, screen reader support
  - `FocusTrap`: Modal focus management
  - Keyboard navigation enhancements
  - Focus visible indicators (keyboard vs mouse)

- **Loading & Error Handling** (`web/src/loading.ts`, 132 lines)
  - `LoadingManager`: Elegant spinner overlay
  - `ErrorHandler`: Toast-style error notifications
  - Global error boundary
  - Auto-dismissing errors (10s timeout)

#### Enhanced
- `web/index.html`: PWA meta tags
- `web/src/main.ts`: Integrated managers, error handling
- `web/src/styles.css`: +138 lines for loading/errors
- Service worker registration for offline mode

#### Changed
- Version bumped: Python 0.2.0 → 0.3.0
- Version bumped: Web 0.1.0 → 0.3.0

### ✏️ Phase 2: Interactive Canon Builder

#### Added
- **Interactive Composer** (`web/src/composer.ts`, 471 lines)
  - Piano roll editor with click-to-add notes
  - Drag to move, shift+click to delete
  - Real-time retrograde generation and preview
  - Snap-to-grid functionality
  - Adjustable note durations

- **Template Library** (6 pre-made patterns)
  - C Major Scale
  - Arpeggio
  - Stepwise Melody
  - Rhythmic Pattern
  - Chromatic Run
  - Bach-style Fragment

- **Composer UI Components**
  - Template selector dropdown
  - Clear and Play buttons
  - Duration selector (16th to whole notes)
  - Live statistics (note count, duration)
  - Visual feedback with red retrograde preview

#### Enhanced
- `web/index.html`: New composer section with controls
- `web/src/main.ts`: Composer initialization and playback
- `web/src/styles.css`: Composer-specific styling (+60 lines)

### 🎵 Phase 1: Go Wide

#### Added
- **New Canon Transformations** (`cancrizans/canon.py`)
  - `augmentation()`: Multiply note durations (temporal stretching)
  - `diminution()`: Divide note durations (temporal compression)
  - `mirror_canon()`: Combined retrograde + inversion

- **Analysis Functions** (`cancrizans/canon.py`)
  - `interval_analysis()`: Melodic interval statistics
  - `harmonic_analysis()`: Vertical sonority analysis
  - `rhythm_analysis()`: Duration pattern statistics

- **Advanced Examples** (5 new canons, examples 06-10)
  - Augmentation canon
  - Diminution canon
  - Mirror canon
  - Combined transformations
  - Triple voice canon

- **Web Enhancements**
  - `web/src/instruments.ts`: 5 instrument presets (synth, piano, harpsichord, strings, organ)
  - `web/src/waveform.ts`: Real-time waveform visualization
  - `web/src/exporter.ts`: Export JSON, analysis, PNG, Web Share API

- **Demo Scripts**
  - `scripts/create_canon_examples.py`: Generate examples 06-10
  - `scripts/demonstrate_analysis.py`: Bach analysis demonstration

#### Enhanced
- `web/index.html`: Instrument selector, export buttons, waveform canvas
- `web/src/styles.css`: Mobile optimization
- `cancrizans/__init__.py`: Version 0.1.0 → 0.2.0, new exports

---

## [0.1.0] - 2025-11-10

### Initial Release

#### Added
- **Core Python Library** (`cancrizans/`)
  - `canon.py`: Core transformations (retrograde, invert, time_align)
  - `bach_crab.py`: Embedded Bach Crab Canon (BWV 1079)
  - `io.py`: Export to MIDI, MusicXML, WAV
  - `viz.py`: Piano roll and symmetry visualizations
  - `cli.py`: Command-line interface with 3 subcommands

- **Web Application** (`web/`)
  - Interactive VexFlow notation renderer
  - Tone.js audio playback with tempo control
  - Mirror view (palindrome visualization)
  - Playback controls (play, pause, stop, mute)
  - Multiple playback modes

- **Real Bach MIDI Integration**
  - Downloaded from jsbach.net (184 notes/voice)
  - Verified as true palindrome
  - Extracted to JSON for web UI

- **Example Canons** (examples 01-05)
  - Scale, arpeggio, melody, rhythm, chromatic
  - Each with MIDI, MusicXML, PNG visualizations
  - JSON analysis data

- **Comprehensive Documentation**
  - `README.md`: Project overview, installation, usage
  - `EXAMPLES.md`: Detailed code examples
  - `GALLERY.md`: Visual catalog of canons
  - `notebooks/bach_crab_canon_exploration.ipynb`: Pre-run Jupyter notebook (843KB)

- **Tests** (26 tests, all passing)
  - `test_retrograde.py`: Retrograde and inversion tests
  - `test_palindrome.py`: Palindrome verification tests
  - `test_exports.py`: File export tests

- **Scripts**
  - `analyze_real_midi.py`: MIDI analysis
  - `extract_midi_to_js.py`: MIDI to JSON conversion
  - `create_additional_examples.py`: Generate examples 01-05
  - `generate_docs.py`: Auto-documentation generation

#### Configuration
- `pyproject.toml`: Python package configuration
- `web/package.json`: Web application dependencies
- `web/tsconfig.json`: TypeScript configuration
- `web/vite.config.ts`: Vite build configuration

---

## Project Statistics

### Current Totals (v0.3.0)

**Code:**
- Python: ~2,000 lines (8 modules)
- TypeScript: ~3,500 lines (13 modules)
- Tests: 26 (all passing ✓)

**Documentation:**
- Markdown files: 8 (README, EXAMPLES, GALLERY, LESSON_PLANS, TUTORIAL_GUIDE, QUIZ_BANK, CHANGELOG, PROJECT_SUMMARY)
- Jupyter notebooks: 2 (bach exploration, waveform palindrome)
- Auto-generated docs: 3

**Examples:**
- Canon files: 10 complete canons
- Visualizations: 40+ PNG images
- Data files: JSON analysis for each canon

**Web Application:**
- Build size: 1.27 MB (optimized)
- PWA-ready: ✓
- Offline-capable: ✓
- Accessible: ✓ (WCAG AA)

---

## Development Phases

This project was developed in 6 phases:

1. **Initial Implementation** (v0.1.0): Core library, web app, Bach integration
2. **Phase 1 - Go Wide** (v0.2.0): Canon types, analysis, web enhancements
3. **Phase 2 - Interactive Builder** (v0.2.0): Composer tool, templates
4. **Phase 3 - Polish** (v0.3.0): PWA, accessibility, error handling
5. **Phase 4 - Research** (v0.3.0): Batch analysis, multi-format export
6. **Phase 5 - Educational** (v0.3.0): Tutorial system, lesson plans, assessments
7. **Phase 6 - Final** (v0.3.0): Documentation, fixes, optimizations

---

## Links

- **Repository**: https://github.com/cancrizans-prototype
- **License**: MIT
- **Python Package**: `pip install -e .`
- **Web App**: `cd web && npm install && npm run dev`

---

## Contributors

- Initial development: Claude (Anthropic)
- Project spec: Cameron Freer

---

*This changelog is maintained automatically with each phase completion.*
