# 🦀 Cancrizans

**Explore and render J.S. Bach's Crab Canon as a strict musical palindrome**

Cancrizans is a comprehensive toolkit for analyzing, verifying, and rendering palindromic musical structures, with a focus on Bach's *Canon Cancrizans* from *The Musical Offering* (BWV 1079).

## What is a Crab Canon?

A **Crab Canon** (Latin: *Canon Cancrizans*) is a musical composition technique where a melody plays forward while simultaneously playing backward (retrograde). Bach's Crab Canon from *The Musical Offering* is one of the most famous examples in Western music.

In this canon:
- **Voice 1** plays the melody forward
- **Voice 2** plays the exact same melody backward (retrograde)
- When played together, they create a perfect **musical palindrome**

The name comes from the sideways movement of crabs, referencing the backward motion of the retrograde voice. In Bach's original manuscript, the piece was notated as a puzzle: a single staff that could be read from either end, with one performer reading normally and another reading the page upside down.

## Features

### Python Library & CLI
- **Core transformations**: retrograde, inversion, time alignment
- **Palindrome verification**: automated structural analysis
- **Export formats**: MIDI, MusicXML, WAV (optional)
- **Visualizations**: piano roll and symmetry plots
- **CLI interface**: analyze, render, and synthesize canons

### Web Interface
- **Interactive notation** rendered with VexFlow
- **Audio playback** with Tone.js (adjustable tempo, pan, mute)
- **Mirror view**: visual palindrome structure with symmetry connectors
- **Playback modes**: normal, first/second half, from-middle-outward
- **Keyboard shortcuts**: Space (play/pause), H (highlight), M (metronome)
- **Fully offline**: no external dependencies at runtime

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
```

### Python API

```python
from cancrizans import (
    load_bach_crab_canon,
    retrograde,
    is_time_palindrome,
    assemble_crab_from_theme
)
from cancrizans.io import to_midi, to_musicxml
from cancrizans.viz import piano_roll, symmetry

# Load Bach's Crab Canon
score = load_bach_crab_canon()

# Verify it's a palindrome
print(is_time_palindrome(score))  # True

# Export
to_midi(score, "output.mid")
to_musicxml(score, "output.musicxml")

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
```

### Web Interface

1. Open `web/index.html` in a browser (after running `npm run dev`)
2. Use the playback controls to explore the canon
3. Toggle "Highlight Symmetry" to see palindromic pairs
4. Try different playback modes and tempos
5. Use keyboard shortcuts for quick control

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
