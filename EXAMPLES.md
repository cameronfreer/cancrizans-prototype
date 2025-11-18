# 📚 Cancrizans: Examples and Usage

*Auto-generated on 2025-11-11 02:48:19*

This document contains real, executable examples with actual outputs from the Cancrizans toolkit.

## 📊 Bach Crab Canon Statistics

The authentic Bach Crab Canon (BWV 1079) analyzed:

- **Parts:** 2
- **Duration:** 144.00 quarter notes
- **Is Palindrome:** True ✓
- **Notes per part:** 184, 184

## 🖥️ Command Line Interface (CLI)

### Installation

```bash
uv sync
```

### Examples


#### Analyze a Score

```bash
python -m cancrizans analyze data/bach_crab_canon_real.musicxml
```

**Output:**
```
Analyzing: data/bach_crab_canon_real.musicxml
------------------------------------------------------------
Number of voices: 2
Total duration: 144.00 quarter notes
  Voice 1: 184 notes, 2 rests
  Voice 2: 184 notes, 2 rests

Palindrome Verification:
------------------------------------------------------------
is_time_palindrome: True
✓ This score is a valid crab canon (retrograde canon)
Symmetric pairs in voice 1: 93
Total events in voice 1: 186
✓ All events participate in symmetric pairs

Struc...
```


#### Render Outputs

```bash
python -m cancrizans render --midi out.mid --xml out.xml --roll roll.png --mirror mirror.png
```

**Output:**
```
Loading Bach Crab Canon...
Rendering outputs...
------------------------------------------------------------
✓ MIDI exported to: examples/cli_demo.mid
✓ MusicXML exported to: examples/cli_demo.xml
✓ Piano roll saved to: examples/cli_demo_roll.png
✓ Symmetry plot saved to: examples/cli_demo_mirror.pn
```


#### Synthesize a Crab Canon

```bash
python -m cancrizans synthesize --tempo 90 --output examples/
```

**Output:**
```
Synthesizing crab canon from theme...
------------------------------------------------------------
Assembling crab canon (forward + retrograde)...
Palindrome verification: True
✓ Successfully created a valid crab canon
Tempo set to: 90 BPM
✓ Synthesized MIDI: examples/synthesized_crab.mid
✓ Synthesi
```


## 🐍 Python API

### Quick Start

```python

# Example 1: Load and verify Bach's Crab Canon
from cancrizans import load_bach_crab_canon, is_time_palindrome

score = load_bach_crab_canon()
print(f"Is palindrome: {is_time_palindrome(score)}")  # True

# Example 2: Create your own crab canon
from music21 import stream, note
from cancrizans import assemble_crab_from_theme

theme = stream.Stream()
theme.append(note.Note('C4', quarterLength=1.0))
theme.append(note.Note('E4', quarterLength=1.0))
theme.append(note.Note('G4', quarterLength=2.0))

crab_canon = assemble_crab_from_theme(theme)
print(f"Is palindrome: {is_time_palindrome(crab_canon)}")  # True

# Example 3: Export to MIDI
from cancrizans.io import to_midi

to_midi(crab_canon, "my_canon.mid")

# Example 4: Visualize
from cancrizans.viz import piano_roll, symmetry

piano_roll(crab_canon, "piano_roll.png")
symmetry(crab_canon, "symmetry.png")

# Example 5: Retrograde transformation
from cancrizans import retrograde

backward_theme = retrograde(theme)

```

## 📓 Jupyter Notebook

See `notebooks/bach_crab_canon_exploration.ipynb` for an interactive tutorial with:

- Step-by-step analysis of Bach's Crab Canon
- Palindrome verification
- Visualization generation
- Creating custom crab canons
- Exploring musical transformations

To run:

```bash
cd notebooks
jupyter notebook bach_crab_canon_exploration.ipynb
```

## 🎵 Generated Files

This documentation run created the following example files:

```
examples/
├── bach_crab_canon.mid         # Bach's canon in MIDI
├── bach_crab_canon.musicxml    # Bach's canon in MusicXML
├── bach_piano_roll.png         # Piano roll visualization
├── bach_symmetry.png           # Symmetry plot
├── my_crab_canon.mid           # Custom crab canon
├── my_crab_piano_roll.png      # Custom canon visualization
└── my_crab_symmetry.png        # Custom symmetry plot
```

## 🔍 Advanced Topics

### Retrograde Transformation

A retrograde reverses the time order of notes while preserving pitches and durations:

```python
from cancrizans import retrograde
from music21 import stream, note

# Original: C-D-E-F
theme = stream.Stream()
for pitch in ['C4', 'D4', 'E4', 'F4']:
    theme.append(note.Note(pitch, quarterLength=1.0))

# Retrograde: F-E-D-C
backward = retrograde(theme)
```

### Inversion

Inversion reflects pitches around an axis:

```python
from cancrizans import invert

# Invert around G4
inverted = invert(theme, axis_pitch='G4')
```

### Palindrome Verification

Check if two voices form a crab canon:

```python
from cancrizans import is_time_palindrome, time_align

# Align two voices
score = time_align(voice1, voice2, offset_quarters=0.0)

# Verify
if is_time_palindrome(score):
    print("This is a crab canon!")
```

## 🎨 Visualizations

### Piano Roll

Shows notes as colored bars on a pitch-time grid:

```python
from cancrizans.viz import piano_roll

piano_roll(score, "output.png", dpi=150)
```

### Symmetry Plot

Displays the temporal midpoint and symmetric note pairs:

```python
from cancrizans.viz import symmetry

symmetry(score, "symmetry.png", dpi=150)
```

## 🌐 Web Interface

The web interface provides:

- Interactive VexFlow notation
- Real-time Tone.js playback
- Palindrome visualization
- Playback controls (tempo, mode, mute)

To run:

```bash
cd web
npm install
npm run dev
```

Then open http://localhost:3000

## 📖 Further Reading

- [README.md](../README.md) - Project overview
- [Jupyter Notebook](../notebooks/bach_crab_canon_exploration.ipynb) - Interactive tutorial
- Bach, J.S. *The Musical Offering*, BWV 1079 (1747)
- Hofstadter, D. *Gödel, Escher, Bach* (1979)

---

**Generated by:** `scripts/generate_docs.py`
**Source:** Real analysis of Bach's Crab Canon
**License:** MIT (Code) / Public Domain (Score)
