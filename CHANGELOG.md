# Changelog

All notable changes to the Cancrizans project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.16.0] - 2025-11-13

### 🎯 Phase 20: Coverage Excellence - 97% Maintained + Enhanced Edge Case Testing

#### Added
- **Validator Edge Case Tests** (`tests/test_validator.py`)
  - 2 new tests for defensive code paths
  - Direct testing of `_assess_harmonic_quality()` with single-part scores (lines 144-145)
  - Direct testing of `_assess_rhythmic_quality()` with empty durations (lines 188-189)
  - Coverage: validator.py increased from 94% to **96%** (+2pp, 12 → 8 lines missing)

- **Generator Extreme Pitch Clamping Tests** (`tests/test_generator.py`)
  - 3 new tests for pitch boundary handling
  - Random walk extreme high pitch clamping at MIDI 84 (line 137)
  - Fibonacci canon extreme high pitch clamping (line 177)
  - Fractal canon extreme low pitch octave adjustment (line 251)
  - Coverage: generator.py improved to **98%** (3 → 2 lines missing)

- **Cache Exception Handling Tests** (`tests/test_cache.py`)
  - 3 new tests for error resilience
  - Pickle error handling during cache save (lines 117-118)
  - IO error handling during cache write
  - OS error handling during cache file deletion (lines 169-170)
  - Coverage: cache.py increased from 95% to **98%** (+3pp, 4 → 2 lines missing)

#### Test Improvements
- **Total test count**: **285 tests** (up from 277, **+8 new tests**)
- **Overall coverage**: **97%** maintained (39 lines missing, down from 46) 🎯
- **Module improvements**:
  - cache.py: 95% → **98%** (+3pp) - only 2 lines missing!
  - validator.py: 94% → **96%** (+2pp)
  - generator.py: **98%** (improved from 3 → 2 lines missing)
  - All other modules: maintained at excellent levels

#### Quality Milestones
- ✅ **97% overall coverage maintained** - rock solid! 🎯
- ✅ All 285 tests passing (100% success rate)
- ✅ Comprehensive edge case coverage across all major modules
- ✅ Enhanced error resilience testing for cache operations
- ✅ Better coverage of defensive programming paths

#### Test Strategy
- **Defensive Code Testing**: Direct testing of private methods to cover safety checks
- **Extreme Value Testing**: Boundary conditions for pitch clamping
- **Exception Resilience**: Comprehensive error handling validation
- **Mock-Based Testing**: Sophisticated mocking for filesystem errors

#### Test Categories
- Unit tests: 206 tests (includes 84 edge case tests)
- Edge case tests: 84 tests across all modules (+8 from Phase 19)
- CLI command tests: 52 tests
- Integration, visualization, and research tests: maintained
- Transformation chain tests: 19 tests

#### Focus Areas
- **Edge Case Excellence**: Pushed coverage of edge cases across validator, generator, and cache
- **Error Resilience**: Tested graceful degradation when filesystem operations fail
- **Defensive Programming**: Validated safety checks in critical code paths
- **Boundary Conditions**: Comprehensive testing of pitch/value limits

## [0.15.0] - 2025-11-13

### 🚀 Phase 19: 97% Coverage Milestone + Transformation Chains (TDD)

#### Added
- **NEW FEATURE: TransformationChain** (`cancrizans/transformation_chain.py`)
  - **Developed using strict Test-Driven Development (TDD)**
  - Compose multiple musical transformations with fluent builder pattern
  - Chain transformations like retrograde, inversion, augmentation sequentially
  - 19 comprehensive tests written BEFORE implementation
  - Preset chains: `crab_canon()`, `mirror_canon()`, `table_canon()`
  - Named transformations for better debugging and documentation
  - Exception handling and edge case coverage
  - Example usage:
    ```python
    from cancrizans import TransformationChain, retrograde, invert

    chain = (TransformationChain()
             .add(retrograde)
             .add(lambda s: invert(s, axis_pitch='C4'))
             .apply(theme))
    ```

- **CLI Coverage Enhancement Tests** (`tests/test_cli_commands.py`)
  - 4 new tests targeting uncovered CLI paths
  - WAV export success path with mocked FluidSynth
  - WAV export failure path testing
  - Research command LaTeX export (lines 259-261)
  - Research command Markdown export (lines 264-266)
  - Coverage: cli.py increased from 91% to **94%** (+3pp)

- **I/O Coverage Enhancement Tests** (`tests/test_io.py`)
  - 5 new tests targeting uncovered I/O paths
  - Complex ABC rest duration formatting (line 227)
  - Successful WAV conversion with mocked FluidSynth (lines 270-273)
  - Generic exception handling in WAV export (lines 285-287)
  - `load_score()` wrapping Part objects in Score (lines 310-314)
  - `load_score()` wrapping generic Stream types (lines 316-319)
  - Coverage: io.py increased from 89% to **99%** (+10pp!) - Only 1 line missing!

#### Test Improvements
- **Total test count**: **277 tests** (up from 249, **+28 new tests**)
  - 19 new transformation chain tests (TDD)
  - 4 new CLI enhancement tests
  - 5 new I/O enhancement tests
- **Overall coverage**: **97%** (up from 95%, **+2 percentage points**) 🎯
- **Module improvements**:
  - io.py: 89% → **99%** (+10pp) - MASSIVE improvement! ⭐
  - cli.py: 91% → **94%** (+3pp)
  - transformation_chain.py: **98%** (new module)
  - All other modules: maintained or improved

#### Quality Milestones
- ✅ **97% overall coverage achieved** - major milestone! 🎯
- ✅ All 277 tests passing (100% success rate)
- ✅ Pure Test-Driven Development for TransformationChain feature
- ✅ I/O module nearly perfect at 99% coverage
- ✅ CLI module significantly improved
- ✅ New composable transformation system adds powerful functionality

#### Test-Driven Development Workflow
- **Red Phase**: Wrote 19 comprehensive tests that initially failed
- **Green Phase**: Implemented `TransformationChain` class to pass all tests
- **Refactor Phase**: Clean, well-documented code with type hints
- **Result**: 100% test pass rate, 98% coverage on new feature

#### Test Categories
- Unit tests: 198 tests (includes transformation chain tests)
- Edge case tests: 76 tests across all modules
- CLI command tests: 52 tests
- Integration, visualization, and research tests: maintained
- Transformation chain tests: 19 tests (new)

#### Focus Areas
- **Test-Driven Development**: Strict TDD for new transformation chain feature
- **Coverage Excellence**: Pushed I/O module to 99%, overall to 97%
- **Composability**: New transformation chain system enables complex workflows
- **CLI Robustness**: Enhanced testing of WAV export and research export paths
- **I/O Reliability**: Comprehensive testing of edge cases and error paths

## [0.14.0] - 2025-11-13

### 🎯 Phase 18: I/O & Caching Edge Case Testing - 92% Coverage Milestone

#### Added
- **I/O Edge Case Tests** (`tests/test_io.py`)
  - 13 comprehensive edge case tests for file I/O operations
  - Nested directory creation for all export functions (MIDI, MusicXML, LilyPond, ABC)
  - LilyPond high octave handling
  - ABC non-standard duration edge cases
  - WAV export error handling:
    - Missing MIDI file validation
    - Missing SoundFont file validation
    - ImportError handling when midi2audio unavailable
  - LilyPond zero/small duration handling
  - ABC rest with various durations
  - String path handling (vs Path objects)
  - Coverage: io.py increased from 78% to **85%** (+7pp)

- **Cache Edge Case Tests** (`tests/test_cache.py`)
  - 10 comprehensive edge case tests for caching mechanisms
  - Memoize with keyword arguments
  - Memoize with unhashable arguments (lists, dicts)
  - Disk cache LRU eviction when maxsize exceeded
  - Disk cache handling corrupted cache files (pickle errors)
  - Disk cache handling empty/truncated files (EOFError)
  - cache_info with corrupted cache files
  - clear_all_caches with permission errors
  - get_cache_stats with corrupted files
  - Multiple disk cache instances non-interference
  - Coverage: cache.py increased from 80% to **88%** (+8pp)

#### Test Improvements
- **Total test count**: 249 tests (up from 226, **+23 new tests**)
- **Overall coverage**: **92%** (up from 90%, +2 percentage points) 🎯
- **Module improvements**:
  - cache.py: 80% → **88%** (+8pp) - largest improvement!
  - io.py: 78% → **85%** (+7pp) - second largest improvement!
  - validator.py: **92%** (maintained)
  - canon.py: **89%** (maintained)
  - cli.py: **87%** (maintained)

#### Quality Milestones
- ✅ **92% overall coverage achieved** - continuing upward trajectory!
- ✅ All 249 tests passing (100% success rate)
- ✅ Robust error handling for file I/O operations
- ✅ Comprehensive caching edge case coverage
- ✅ Better handling of corrupted/missing files
- ✅ Improved resilience of caching mechanisms

#### Test Categories Expansion
- Unit tests: 179 tests (includes 67 edge case tests across all modules)
- Edge case tests: 67 tests across validator, CLI, canon, I/O, and cache
- CLI command tests: 48 tests
- Integration, visualization, and research tests: maintained

#### Focus Areas
- **I/O Robustness**: Tested all export formats (MIDI, MusicXML, LilyPond, ABC, WAV)
- **Error Handling**: Comprehensive testing of file not found, corruption, and permission scenarios
- **Caching Reliability**: Tested cache corruption, eviction, and multi-instance scenarios
- **Path Handling**: Ensured both string and Path object compatibility

## [0.13.0] - 2025-11-13

### 🚀 Phase 17: Comprehensive Edge Case Testing & 90% Coverage Milestone

#### Added
- **Validator Edge Case Tests** (`tests/test_validator.py`)
  - 16 comprehensive edge case tests for boundary conditions
  - Zero-duration parts validation
  - Single-note parts handling
  - Extreme pitch ranges (low and high)
  - Narrow and wide range canons
  - All identical rhythms detection
  - Non-palindrome penalty verification
  - All quality grade boundaries (A+ through F)
  - Individual recommendation tests for each quality metric
  - Coverage: validator.py increased from 89% to **92%** (+3pp)

- **CLI Edge Case Tests** (`tests/test_cli_commands.py`)
  - 9 new integration tests for error paths and edge cases
  - Research with non-existent directory
  - Render WAV with missing soundfont
  - Main function with no command
  - Generate with validation warnings
  - Validate with JSON export
  - Research with no matching files
  - Analyze with rests
  - Synthesize with transposition and tempo
  - Coverage: cli.py increased from 85% to **87%** (+2pp)

- **Canon Edge Case Tests** (`tests/test_canon.py`)
  - 19 comprehensive edge case tests for transformations
  - Retrograde with empty streams, chords, rests, and sequences
  - Inversion with chords, rests, and pitch sequences
  - Augmentation and diminution with chords
  - is_time_palindrome with wrong part counts and different lengths
  - Empty parts palindrome verification
  - _extract_events with chords
  - Interval, harmonic, and rhythm analysis with empty/single-note streams
  - Pairwise symmetry with empty streams and single notes
  - Coverage: canon.py increased from 85% to **89%** (+4pp)

#### Test Improvements
- **Total test count**: 226 tests (up from 182, **+44 new tests**)
- **Overall coverage**: **90%** (up from 88%, +2 percentage points) 🎯
- **Module improvements**:
  - validator.py: 89% → **92%** (+3pp)
  - canon.py: 85% → **89%** (+4pp)
  - cli.py: 85% → **87%** (+2pp)
  - generator.py: 95% → **98%** (maintained)
  - __main__.py: **100%** (maintained)

#### Quality Milestones
- ✅ **90% overall coverage achieved** - major project milestone!
- ✅ All 226 tests passing (100% success rate)
- ✅ Comprehensive edge case coverage across all major modules
- ✅ Improved error handling validation
- ✅ Better boundary condition testing
- ✅ Enhanced musical transformation robustness

#### Test Categories Expansion
- Unit tests: 156 tests (includes 44 new edge case tests)
- CLI command tests: 48 tests (up from 39)
- Edge case tests: 44 new tests strategically distributed
- Integration, visualization, and research tests: maintained

## [0.12.0] - 2025-11-12

### 🎯 Phase 16: Coverage Excellence & Edge Case Testing

#### Added
- **__main__ Module Tests** (`tests/test_cli_commands.py`)
  - 2 new tests for module entry point
  - Tests module import and CLI execution via `python -m cancrizans`
  - Coverage: __main__.py increased from 0% to 100% ✅

- **Generator Edge Case Tests** (`tests/test_generator.py`)
  - 4 comprehensive edge case tests
  - Descending scale generation
  - Random walk extreme pitch boundaries (MIDI range 36-84)
  - Fibonacci canon octave adjustments
  - Golden ratio canon octave boundary handling
  - Coverage: generator.py increased from 95% to 98%

#### Test Improvements
- **Total test count**: 182 tests (up from 176, +6 new tests)
- **Overall coverage**: 88% maintained with higher quality
- **Module improvements**:
  - __main__.py: 0% → **100%** (+100pp)
  - generator.py: 95% → **98%** (+3pp)
  - All edge cases now properly tested

#### Quality Assurance
- All 182 tests passing (100% success rate)
- Coverage quality improved through boundary testing
- Better handling of extreme musical ranges
- Comprehensive module entry point validation

## [0.11.0] - 2025-11-12

### 🖥️ Phase 14: CLI Module Testing & Validation

#### Added
- **Comprehensive CLI Tests** (`tests/test_cli_commands.py`)
  - 37 extensive tests covering all CLI commands
  - **analyze command**: 5 tests (file handling, voice count, palindrome status, duration)
  - **render command**: 7 tests (MIDI, MusicXML, piano roll, symmetry, multi-format, WAV validation)
  - **synthesize command**: 4 tests (default, transpose, tempo, palindrome verification)
  - **generate command**: 6 tests (scale, arpeggio, random, fibonacci, validation, error handling)
  - **validate command**: 3 tests (basic validation, verbose mode, error handling)
  - **research command**: 4 tests (batch processing, CSV/JSON export, empty directory)
  - **main() entry point**: 4 tests (help, no args, subcommands)
  - **Integration workflows**: 3 tests (generate→validate, generate→analyze, full workflow)
  - Coverage: cli.py increased from 0% to 85%

#### Test Coverage Improvements
- **Total test count**: 176 tests (up from 139, +37 new tests)
- **Overall coverage**: 88% (up from 66%, +22 percentage points!)
- **Modules with major improvements**:
  - cli.py: 0% → **85%** (+85pp) 🎯
  - bach_crab.py: 73% → **98%** (+25pp)
  - validator.py: 86% → **89%** (+3pp)
  - canon.py: 84% → **85%** (+1pp)

#### All Modules Coverage Summary
- bach_crab.py: **98%**
- research.py: **99%**
- viz.py: **98%**
- generator.py: **95%**
- validator.py: **89%**
- cli.py: **85%** (was 0%)
- canon.py: **85%**
- cache.py: **80%**
- io.py: **78%**

#### Testing Infrastructure
- Mock-based CLI testing with argparse.Namespace
- Temporary file handling for all I/O operations
- stdout/stderr capture for output validation
- Integration tests covering real-world workflows
- Error path testing (nonexistent files, invalid arguments)

## [0.10.0] - 2025-11-12

### 🧪 Phase 13: Comprehensive Testing & Coverage Expansion

#### Added
- **Visualization Tests** (`tests/test_viz.py`)
  - 19 comprehensive tests for `viz.py` module
  - Piano roll visualization tests with multiple scenarios
  - Symmetry plot tests with edge cases
  - Tests for chords, rests, custom DPI, multi-voice handling
  - Image validation with PIL/Pillow
  - Coverage: viz.py increased from 0% to 98%

- **Research Module Tests** (`tests/test_research.py`)
  - 31 comprehensive tests for `research.py` module
  - CanonAnalyzer tests (caching, structure, properties)
  - BatchAnalyzer tests (multi-file processing)
  - ResearchExporter tests (CSV, JSON, LaTeX, Markdown)
  - Corpus analysis integration tests
  - Coverage: research.py increased from 0% to 99%

- **Extended I/O Tests** (`tests/test_io.py`)
  - 9 additional tests for export edge cases
  - LilyPond accidentals (sharps, flats), octaves, rests
  - ABC notation accidentals, octaves, durations, rests
  - load_score() edge case handling
  - Coverage: io.py increased from 60% to 78%

#### Testing Improvements
- **Total test count**: 139 tests (up from 80, +59 new tests)
- **Overall coverage**: 66% (up from 48%, +18 percentage points)
- **100% pass rate** across all test suites
- **Modules with excellent coverage**:
  - research.py: 99% (was 0%)
  - viz.py: 98% (was 0%)
  - generator.py: 95%
  - validator.py: 86%
  - canon.py: 84%
  - cache.py: 80%
  - io.py: 78% (was 60%)

#### Changed
- Expanded test fixtures for edge case validation
- Improved test organization with focused test classes
- Enhanced assertions for better failure messages

## [0.9.0] - 2025-11-12

### ⚡ Phase 12: Performance Optimization & Caching

#### Added
- **Caching Infrastructure** (`cancrizans/cache.py`)
  - `@memoize` decorator - In-memory function result caching
  - `@lru_cache` wrapper - Bounded memory cache with LRU eviction
  - `@disk_cache` decorator - Persistent disk-based caching
  - `clear_all_caches()` - Clear all registered caches
  - `get_cache_stats()` - Retrieve cache statistics
  - Cache utilities for optimizing expensive operations

- **Performance Benchmarking** (`scripts/benchmark.py`)
  - Comprehensive performance profiling of all operations
  - Statistical analysis (mean, median, stdev, min, max)
  - Benchmark results documented in `docs/performance.md`
  - Key metrics:
    - Retrograde (40 notes): 0.719ms mean
    - Inversion (40 notes): 2.329ms mean
    - Palindrome verification: 0.483ms mean
    - Full validation: 34.488ms mean
    - Scale canon generation: 1.611ms mean
    - Bach canon loading: 83.775ms mean

- **Cache Tests** (`tests/test_cache.py`)
  - 11 comprehensive caching tests
  - Memoization functionality tests
  - LRU cache behavior validation
  - Disk cache persistence tests
  - Performance improvement verification
  - Cache clearing and statistics tests

#### Performance Improvements
- Caching infrastructure allows users to optimize expensive operations
- Disk cache enables persistent results across program runs
- LRU cache prevents unbounded memory growth
- Benchmarks establish performance baselines for future optimization

#### Changed
- Test suite expanded to 80 tests (up from 69)
- All tests passing with 100% success rate
- Documentation updated with caching examples

## [0.8.0] - 2025-11-12

### 📤 Phase 11: Advanced Export Formats & Integration Tests

#### Added
- **LilyPond Export** (`cancrizans/io.py:to_lilypond()`)
  - Professional music engraving format (.ly files)
  - Custom content generator (no external dependencies)
  - Proper octave and accidental handling
  - Multi-staff support for canons
  - Ready to compile: `lilypond output.ly` → PDF/PNG

- **ABC Notation Export** (`cancrizans/io.py:to_abc()`)
  - Text-based compact notation (.abc files)
  - Folk music standard format
  - Multi-voice support with voice markers
  - Easy to read and edit
  - Compatible with ABC viewers and players

- **CLI Integration Tests** (`tests/test_cli_integration.py`)
  - 10 end-to-end workflow tests
  - Generate command tests (all 6 algorithms)
  - Validate command tests
  - Analyze command tests
  - Multi-canon generation tests

- **Generator Tutorial Notebook** (`notebooks/generator_tutorial.ipynb`)
  - Comprehensive tutorial for all 11 algorithms
  - Quality validation examples
  - Export format demonstrations
  - Ready to run examples

- **Export Format Tests** (7 new tests in `tests/test_io.py`)
  - LilyPond file creation and structure tests
  - ABC notation content validation
  - Multi-voice handling tests

#### Fixed
- Export functions now handle all duration types correctly
- LilyPond octave notation matches standard (c' = middle C)
- ABC notation properly handles accidentals and octaves

#### Changed
- `io.py` module documentation expanded for new exports
- Test suite expanded to 69 tests (up from 52)
- Code coverage improved to 46% (up from 44%)
- io.py coverage: 60% (up from 49%)

## [0.7.0] - 2025-11-12

### 🧪 Phase 10: Testing & Quality Assurance

#### Added
- **Comprehensive Test Suite** (`tests/`)
  - 52 unit tests with 100% pass rate
  - Test coverage: 44% overall, 95% on generator module
  - Tests for canon transformations, generator, validator, and I/O
  - Automated testing with pytest
  - Coverage reporting with pytest-cov

- **Test Configuration**
  - `pytest.ini` - Pytest configuration with markers
  - `.coveragerc` - Coverage reporting configuration
  - HTML coverage reports in `htmlcov/`

- **Pre-executed Jupyter Notebook**
  - `transformation_techniques.ipynb` - Now fully executed with outputs
  - Interactive examples of retrograde, inversion, augmentation
  - Visualization of transformations

- **Notebook Fixing Scripts**
  - `scripts/fix_notebooks.py` - Updates notebooks to use correct API
  - `scripts/update_notebook_cells.py` - Fixes interval analysis cells

#### Fixed
- Notebooks now use `assemble_crab_from_theme()` instead of `mirror_canon()`
- Interval analysis cells updated to use correct API keys
- All test assertions aligned with actual implementation

#### Changed
- Improved code quality with comprehensive test coverage
- Better documentation of expected behavior through tests

## [0.6.0] - 2025-11-12

### 🔧 Phase 9: Advanced Tools & Examples

#### Added
- **Algorithmic Canon Generator** (`cancrizans/generator.py`)
  - 11 different generation algorithms
  - Scale canons (major/minor)
  - Arpeggio canons (major/minor/diminished/augmented)
  - Random walk canons
  - Fibonacci sequence canons
  - Golden ratio canons
  - Modal canons (all 6 modes: dorian, phrygian, lydian, mixolydian, aeolian, locrian)
  - Fractal canons with self-similar patterns
  - Polyrhythmic canons
  - Custom rhythmic patterns

- **Canon Quality Validator** (`cancrizans/validator.py`)
  - Complete validation with error/warning detection
  - Multi-dimensional quality scoring:
    - Melodic quality (repetition, leaps, stepwise motion)
    - Harmonic quality (consonance/dissonance)
    - Rhythmic quality (variety and patterns)
    - Range quality (ideal 12-24 semitones)
    - Intervallic quality (diversity)
  - Overall quality score (0-1) with letter grades (A+ to F)
  - Actionable recommendations for improvement

- **Performance Benchmark Suite** (`scripts/benchmark.py`)
  - Benchmarks for transformations, analysis, generation, validation
  - Scalability tests with varying input sizes
  - Statistical reporting (mean, median, stdev, min, max)

- **Example Canon Collection** (`scripts/generate_examples.py`)
  - Generates 30 different algorithmic canons
  - Validates each with quality scores
  - Exports MIDI and visualizations
  - Quality report with grade distribution
  - 100% generation success rate
  - Average quality: 0.657 (C+ to B- range)

- **Extended CLI Commands**
  - `cancrizans generate` - Generate algorithmic canons
    - Supports all 11 algorithms
    - Optional quality validation
    - MIDI export
  - `cancrizans validate` - Validate canon quality
    - Comprehensive quality analysis
    - Visual quality bars
    - Detailed recommendations

#### Fixed
- Generator functions now properly return Score objects (not Part)
- Fixed duration calculations for Fibonacci, Golden Ratio, and Polyrhythmic generators
- Validator now uses `flatten().notes` to handle MIDI files with measures
- All quality assessment methods now work with loaded MIDI files

#### Changed
- Validator quality metrics now properly handle various score formats
- Generator uses clean fractions for note durations to avoid music21 format errors

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
