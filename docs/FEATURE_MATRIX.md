# Feature Comparison Matrix

**Auto-generated**: 2025-11-12

This document provides a comprehensive comparison of features across Cancrizans components.

## Component Overview

| Component | Description | Languages | Status |
|-----------|-------------|-----------|--------|
| **Python Library** | Core analysis and transformation engine | Python 3.11+ | ✅ Stable |
| **CLI Tool** | Command-line interface | Python | ✅ Stable |
| **Web Interface** | Interactive PWA application | TypeScript, HTML, CSS | ✅ Stable |
| **Documentation** | Auto-generated docs & notebooks | Markdown, Jupyter | ✅ Stable |

---

## Feature Availability Matrix

### Core Transformations

| Feature | Python API | CLI | Web Interface | Notes |
|---------|-----------|-----|---------------|-------|
| Retrograde | ✅ | ✅ | ✅ | Time reversal |
| Inversion | ✅ | ✅ | ✅ | Pitch mirroring |
| Augmentation | ✅ | ✅ | ✅ | Tempo slowdown |
| Diminution | ✅ | ✅ | ✅ | Tempo speedup |
| Mirror Canon | ✅ | ✅ | ✅ | Retrograde + alignment |
| Transformation Chains | ✅ | ⚠️ | ✅ | CLI via scripting |

### Analysis Tools

| Feature | Python API | CLI | Web Interface | Notes |
|---------|-----------|-----|---------------|-------|
| Palindrome Detection | ✅ | ✅ | ✅ | Time palindrome |
| Symmetry Mapping | ✅ | ✅ | ⚠️ | Pairwise note mapping |
| Interval Analysis | ✅ | ✅ | ❌ | Melodic intervals |
| Harmonic Analysis | ✅ | ✅ | ❌ | Chord detection |
| Rhythm Analysis | ✅ | ✅ | ❌ | Duration patterns |
| Batch Analysis | ✅ | ✅ | ❌ | Research tool |
| Symmetry Scoring | ✅ | ❌ | ✅ | 0-100% score |

### Visualization

| Feature | Python API | CLI | Web Interface | Notes |
|---------|-----------|-----|---------------|-------|
| Piano Roll | ✅ | ✅ | ✅ | Note grid display |
| Symmetry Plot | ✅ | ✅ | ✅ | Palindrome connectors |
| Animated Roll | ❌ | ❌ | ✅ | Real-time playback |
| Color Schemes | ✅ | ⚠️ | ✅ | 4 schemes in web |
| Musical Notation | ❌ | ❌ | ✅ | VexFlow rendering |
| Waveform | ❌ | ❌ | ✅ | Audio visualization |

### I/O & Export

| Feature | Python API | CLI | Web Interface | Notes |
|---------|-----------|-----|---------------|-------|
| MIDI Import | ✅ | ✅ | ✅ | Read .mid files |
| MusicXML Import | ✅ | ✅ | ❌ | Read .xml files |
| MIDI Export | ✅ | ✅ | ✅ | Write .mid files |
| MusicXML Export | ✅ | ⚠️ | ❌ | Via Python |
| WAV Export | ⚠️ | ⚠️ | ❌ | Requires FluidSynth |
| JSON Export | ✅ | ✅ | ✅ | Analysis data |
| CSV Export | ✅ | ✅ | ❌ | Research data |
| LaTeX Export | ✅ | ✅ | ❌ | Tables |
| PNG Export | ✅ | ✅ | ✅ | Visualizations |
| URL Sharing | ❌ | ❌ | ✅ | Compressed links |

### Interactive Features

| Feature | Python API | CLI | Web Interface | Notes |
|---------|-----------|-----|---------------|-------|
| Audio Playback | ❌ | ❌ | ✅ | Tone.js synthesis |
| Interactive Composer | ❌ | ❌ | ✅ | Piano roll editor |
| MIDI Upload | ❌ | ❌ | ✅ | Drag & drop |
| Real-time Analysis | ❌ | ❌ | ✅ | Instant feedback |
| Tutorial System | ❌ | ❌ | ✅ | 11-step guide |
| LocalStorage | ❌ | ❌ | ✅ | Save/load |
| Offline Mode | ❌ | ❌ | ✅ | PWA caching |

### Documentation

| Feature | Python API | CLI | Web Interface | Notes |
|---------|-----------|-----|---------------|-------|
| API Reference | ✅ | ✅ | ❌ | Auto-generated |
| CLI Reference | ❌ | ✅ | ❌ | Complete guide |
| Jupyter Notebooks | ✅ | ❌ | ❌ | 3 notebooks |
| Lesson Plans | ✅ | ✅ | ⚠️ | 4 plans |
| Tutorial Guide | ✅ | ❌ | ✅ | Interactive |
| Examples Gallery | ✅ | ✅ | ⚠️ | 10+ examples |

---

## Legend

- ✅ **Fully Supported**: Feature is complete and tested
- ⚠️ **Partially Supported**: Feature exists but limited or requires dependencies
- ❌ **Not Supported**: Feature not available in this component

---

## Platform Requirements

### Python Library

- **Python**: 3.11+
- **Dependencies**: music21, mido, matplotlib, numpy
- **Optional**: scipy (for notebooks), midi2audio (for WAV export)
- **Platforms**: Linux, macOS, Windows

### CLI Tool

- **Inherits**: Python library requirements
- **Additional**: None (uses same dependencies)
- **Platforms**: Linux, macOS, Windows

### Web Interface

- **Browser**: Modern browser with ES2020 support
- **Requires**: JavaScript enabled
- **Recommended**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Platforms**: Any (cross-platform web app)

---

## Performance Comparison

| Operation | Python API | CLI | Web Interface |
|-----------|-----------|-----|---------------|
| Load MIDI (100 notes) | ~50ms | ~100ms | ~20ms |
| Retrograde | ~10ms | ~50ms | ~5ms |
| Palindrome Check | ~30ms | ~70ms | ~15ms |
| Render Piano Roll | ~500ms | ~600ms | ~100ms |
| Batch Analysis (10 files) | ~2s | ~3s | N/A |

**Note**: Times are approximate and depend on hardware.

---

## Feature Roadmap

### Planned Features

- [ ] Real-time MIDI input (Web)
- [ ] Advanced harmonic analysis (Python/CLI)
- [ ] Multi-language support (Web)
- [ ] Mobile app (React Native)
- [ ] Cloud storage integration (Web)
- [ ] Collaborative editing (Web)
- [ ] Machine learning canon generation (Python)

### Under Consideration

- WebAssembly Python bridge for advanced analysis in browser
- VST plugin for DAW integration
- Max/MSP external
- Ableton Live integration

---

## Use Case Recommendations

### For Researchers

**Recommended**: Python API + CLI + Jupyter Notebooks
- Batch processing capabilities
- Export to LaTeX for papers
- Reproducible analysis
- Statistical tools

### For Educators

**Recommended**: Web Interface + Lesson Plans
- Interactive tutorials
- No installation required
- Visual feedback
- Student-friendly

### For Composers

**Recommended**: Web Interface + Python API
- Interactive composition
- Quick prototyping (Web)
- Advanced transformations (Python)
- MIDI export

### For Students

**Recommended**: Web Interface + Jupyter Notebooks
- Learn by doing (Web tutorials)
- Explore concepts (Notebooks)
- Immediate feedback
- Examples gallery

---

## Integration Examples

### Python → CLI

```python
# Generate analysis
from cancrizans import load_bach_crab_canon
score = load_bach_crab_canon()
score.write('midi', 'output.mid')
```

```bash
# Analyze with CLI
cancrizans analyze output.mid --verbose
```

### CLI → Web

```bash
# Generate visualization
cancrizans render input.mid -t both

# Open in browser
# Upload PNGs to web interface for annotation
```

### Python → Web

```python
# Export for web
from cancrizans.io import to_midi
to_midi(score, 'for_web.mid')

# Upload to web interface for playback and sharing
```

---

## Contribution Guide

Want to add features? See:
- `CONTRIBUTING.md` for guidelines
- `docs/ARCHITECTURE.md` for system design
- `docs/API_REFERENCE.md` for API details

**Feature Requests**: Open an issue on GitHub with the `enhancement` label.
