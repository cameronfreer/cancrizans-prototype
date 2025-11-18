# 🦀 Cancrizans: Complete Bach Crab Canon Explorer

## Summary

This project provides a comprehensive toolkit for exploring J.S. Bach's **Crab Canon** (Canon Cancrizans) from *The Musical Offering* (BWV 1079) as a strict musical palindrome.

## Features

### 🐍 Python Library & CLI

**Core Functionality:**
- **Retrograde transformation**: Time-reversal of musical sequences
- **Inversion**: Pitch reflection around an axis
- **Palindrome verification**: Automated structural analysis
- **Canon assembly**: Programmatic construction of crab canons

**I/O:**
- Export: MIDI, MusicXML, WAV (optional)
- Import: MIDI, MusicXML

**Visualizations:**
- Piano roll: Notes on pitch-time grid
- Symmetry plot: Palindromic structure with central axis and connectors

**CLI:**
```bash
python -m cancrizans analyze <file>      # Verify palindrome property
python -m cancrizans render <options>    # Export all formats
python -m cancrizans synthesize <opts>   # Create canons from themes
```

**Test Coverage:**
- 26 tests, all passing
- 100% offline execution
- Tests: retrograde, inversion, palindrome, exports

### 🌐 Web Interface (TypeScript + Vite)

**Features:**
- **VexFlow notation**: Two-staff rendering with proper music notation
- **Tone.js playback**: Adjustable tempo (40-160 BPM), pan, mute, metronome
- **Mirror view**: Real-time palindrome visualization with symmetry connectors
- **Playback modes**: Normal, first/second half, from-middle-outward
- **Keyboard shortcuts**: Space (play/pause), H (highlight), M (metronome)
- **Fully offline**: No external dependencies

**Tech Stack:**
- TypeScript (strict mode)
- Vite (fast bundler)
- VexFlow 4.x (notation)
- Tone.js 15.x (audio)

### 📓 Jupyter Notebook

**Interactive Tutorial:**
- Step-by-step exploration of Bach's canon
- Palindrome verification with examples
- Custom canon creation
- Transformation exploration (retrograde, inversion)
- Visualization generation
- Pre-executed with all outputs

### 📊 Documentation

**Comprehensive Docs:**
- **README.md**: Project overview, installation, quick start
- **EXAMPLES.md**: Auto-generated from real code execution
- **GALLERY.md**: Visual catalog of all examples with images
- **Jupyter Notebook**: Interactive tutorial

**Examples:**
- Bach's authentic Crab Canon (184 notes per voice)
- 5 educational examples (scale, arpeggio, melody, rhythm, chromatic)
- Custom user-created canons
- All verified as true palindromes

## 📁 Project Structure

```
cancrizans/
├── cancrizans/               # Python package
│   ├── canon.py              # Core transformations
│   ├── bach_crab.py          # Bach canon data
│   ├── io.py                 # I/O utilities
│   ├── viz.py                # Visualizations
│   ├── cli.py                # CLI interface
│   └── tests/                # 26 tests
├── web/                      # TypeScript web app
│   ├── src/
│   │   ├── player.ts         # Tone.js audio
│   │   ├── notation.ts       # VexFlow rendering
│   │   ├── mirrorView.ts     # Palindrome viz
│   │   ├── ui.ts             # Controls
│   │   └── scoreLoader.ts    # Real Bach data
│   └── index.html
├── notebooks/
│   └── bach_crab_canon_exploration.ipynb
├── scripts/
│   ├── analyze_real_midi.py
│   ├── extract_midi_to_js.py
│   ├── create_additional_examples.py
│   └── generate_docs.py     # Auto-documentation
├── examples/                 # 20+ example files
│   ├── bach_*.{mid,xml,png}
│   ├── 01-05_*.{mid,png}
│   └── my_*.{mid,png}
├── data/
│   ├── bach_crab_canon_original.mid  # Authentic Bach
│   └── bach_crab_canon_real.musicxml
├── README.md
├── EXAMPLES.md              # Auto-generated
├── GALLERY.md               # Visual catalog
├── LICENSE                  # MIT
└── pyproject.toml
```

## 🎯 Acceptance Criteria

All criteria met and verified:

### ✅ 1. Analyze Command
```bash
$ python -m cancrizans analyze data/bach_crab_canon_real.musicxml
```
**Output:**
```
is_time_palindrome: True ✓
Symmetric pairs: 93
Total events: 186
✓ All events participate in symmetric pairs
```

### ✅ 2. Render Command
```bash
$ python -m cancrizans render --midi out.mid --xml out.xml --roll roll.png --mirror mirror.png
```
**Produces:**
- Valid MIDI file (playable)
- Valid MusicXML (importable)
- Piano roll PNG (clear visualization)
- Symmetry plot PNG (with midpoint and connectors)

### ✅ 3. Web UI
- Loads completely offline
- Renders musical notation with VexFlow
- Plays audio with Tone.js
- Displays mirror view with symmetry highlighting
- Supports all playback modes
- Responds to keyboard shortcuts

### ✅ 4. Tests
```bash
$ uv run pytest cancrizans/tests/ -v
```
**Result:** 26 passed in 1.00s

## 📊 Statistics

**Python Package:**
- 1,200+ lines of Python code
- 600+ lines of test code
- 5 modules (canon, bach_crab, io, viz, cli)
- 26 tests (retrograde, palindrome, exports)
- Type hints throughout

**Web App:**
- 800+ lines of TypeScript
- 5 modules (player, notation, mirrorView, ui, scoreLoader)
- Fully typed with strict mode
- Responsive design

**Documentation:**
- 400+ lines README
- 200+ lines auto-generated examples
- 300+ lines gallery
- Pre-executed Jupyter notebook

**Examples:**
- 1 authentic Bach canon (184 notes × 2)
- 5 educational canons
- 3 custom canons
- 20+ visualization files
- All verified as true palindromes

## 🎨 Visual Examples

### Bach's Crab Canon - Piano Roll
*Shows notes as horizontal bars on pitch-time grid*

### Bach's Crab Canon - Symmetry Plot
*Central red line marks temporal midpoint, gray connectors link palindromic pairs*

### Educational Examples
- Scale canon: Basic retrograde
- Arpeggio canon: Harmonic palindrome
- Melody canon: Phrase-level structure
- Rhythm canon: Temporal palindrome
- Chromatic canon: All 12 semitones

## 🧪 Testing

**Local Testing:**
```bash
# Install
uv sync --extra dev

# Run tests
uv run pytest

# Try CLI
uv run python -m cancrizans analyze data/bach_crab_canon_real.musicxml
uv run python -m cancrizans render --midi out.mid --roll roll.png
uv run python -m cancrizans synthesize --tempo 84

# Run Jupyter notebook
cd notebooks
uv run jupyter notebook bach_crab_canon_exploration.ipynb

# Launch web UI
cd web
npm install
npm run dev  # http://localhost:3000
```

## 📚 Dependencies

**Python:**
- music21 >= 9.1.0
- matplotlib >= 3.8.0
- mido >= 1.3.0
- numpy >= 1.26.0
- Optional: midi2audio (for WAV export)

**Web:**
- tone >= 15.0.4
- vexflow >= 4.2.4
- vite >= 5.0.0
- typescript >= 5.3.0

## 🎓 Educational Value

This project demonstrates:
- Musical palindromes and retrograde motion
- Canonical composition techniques
- Music information retrieval
- Audio synthesis and visualization
- Interactive web audio
- Test-driven development
- Type-safe TypeScript
- Auto-generated documentation

## 🔗 References

- Bach, J.S. *Das Musikalische Opfer* (The Musical Offering), BWV 1079 (1747)
- Hofstadter, D. *Gödel, Escher, Bach: An Eternal Golden Braid* (1979)
- [music21](http://web.mit.edu/music21/) documentation
- [VexFlow](https://www.vexflow.com/) notation library
- [Tone.js](https://tonejs.github.io/) audio framework

## 📝 License

**Code:** MIT License
**Musical Score:** Public Domain (Bach, 1747)
**Generated Examples:** CC0 Public Domain

## 🙏 Acknowledgments

- **music21** for powerful music analysis tools
- **VexFlow** for beautiful notation rendering
- **Tone.js** for web audio synthesis
- **J.S. Bach** for the incredible music
- **Douglas Hofstadter** for GEB inspiration

---

**"Going backwards, like a crab" 🦀**
