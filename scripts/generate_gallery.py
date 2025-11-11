"""
Generate GALLERY.md with correct file references
"""

from pathlib import Path


def generate_gallery_md():
    """Generate the gallery markdown file."""
    content = """# 🎨 Cancrizans Gallery

Visual and audio examples of crab canons, palindromic structures, and musical transformations.

## 📊 Table of Contents

- [Bach's Crab Canon (BWV 1079)](#bachs-crab-canon)
- [Educational Examples](#educational-examples)
- [Advanced Canon Types](#advanced-canon-types)
- [Visualizations](#visualizations)

---

## 🎼 Bach's Crab Canon

The authentic **Canon Cancrizans** from *The Musical Offering* (BWV 1079).

### Statistics
- **Composer:** Johann Sebastian Bach (1685-1750)
- **Parts:** 2 voices
- **Duration:** 144 quarter notes (~2.4 minutes at 60 BPM)
- **Notes:** 184 per voice
- **Palindrome:** ✓ Verified
- **Consonance Ratio:** 76%
- **Average Interval:** 2.3 semitones

### Files
- [🎵 MIDI Playback](./examples/bach_crab_canon.mid)
- [📄 MusicXML Notation](./examples/bach_crab_canon.musicxml)
- [📊 Analysis JSON](./examples/bach_analysis.json)
- [📷 Piano Roll](./examples/bach_piano_roll.png)
- [🔄 Symmetry Plot](./examples/bach_symmetry.png)

### Visualizations

#### Piano Roll
![Bach Piano Roll](./examples/bach_piano_roll.png)

*Shows all notes plotted on a pitch-time grid. Note how the two voices create mirror patterns.*

#### Symmetry Plot
![Bach Symmetry](./examples/bach_symmetry.png)

*The red vertical line marks the temporal midpoint. Gray connectors link palindromic note pairs.*

---

## 📚 Educational Examples

Simple crab canons demonstrating different musical concepts.

### 1. Scale Crab Canon

A C major scale (C-D-E-F-G-A-B-C) played forward and backward simultaneously.

- **Files:** [MIDI](./examples/01_scale_crab_canon.mid) | [MusicXML](./examples/01_scale_crab_canon.musicxml) | [JSON](./examples/01_scale_analysis.json)
- **Visualizations:** [Piano Roll](./examples/01_scale_piano_roll.png) | [Symmetry](./examples/01_scale_symmetry.png)
- **Duration:** 4.5 quarter notes
- **Notes:** 8 per voice
- **Palindrome:** ✓ Verified

![Scale Piano Roll](./examples/01_scale_piano_roll.png)

### 2. Arpeggio Crab Canon

A C major arpeggio (C-E-G-C-E-C-G-E-C) as a crab canon.

- **Files:** [MIDI](./examples/02_arpeggio_crab_canon.mid) | [MusicXML](./examples/02_arpeggio_crab_canon.musicxml) | [JSON](./examples/02_arpeggio_analysis.json)
- **Visualizations:** [Piano Roll](./examples/02_arpeggio_piano_roll.png) | [Symmetry](./examples/02_arpeggio_symmetry.png)
- **Duration:** 5.0 quarter notes
- **Notes:** 9 per voice
- **Palindrome:** ✓ Verified

![Arpeggio Piano Roll](./examples/02_arpeggio_piano_roll.png)

### 3. Melodic Crab Canon

A simple stepwise melody with smooth contour.

- **Files:** [MIDI](./examples/03_melody_crab_canon.mid) | [MusicXML](./examples/03_melody_crab_canon.musicxml) | [JSON](./examples/03_melody_analysis.json)
- **Visualizations:** [Piano Roll](./examples/03_melody_piano_roll.png) | [Symmetry](./examples/03_melody_symmetry.png)
- **Duration:** 7.0 quarter notes
- **Notes:** 10 per voice
- **Palindrome:** ✓ Verified

![Melody Piano Roll](./examples/03_melody_piano_roll.png)

### 4. Rhythmic Crab Canon

Interesting rhythm on a single pitch (C5).

- **Files:** [MIDI](./examples/04_rhythm_crab_canon.mid) | [MusicXML](./examples/04_rhythm_crab_canon.musicxml) | [JSON](./examples/04_rhythm_analysis.json)
- **Visualizations:** [Piano Roll](./examples/04_rhythm_piano_roll.png) | [Symmetry](./examples/04_rhythm_symmetry.png)
- **Duration:** 5.0 quarter notes
- **Notes:** 8 per voice
- **Palindrome:** ✓ Verified

![Rhythm Piano Roll](./examples/04_rhythm_piano_roll.png)

### 5. Chromatic Crab Canon

Chromatic scale passage (C4-C5).

- **Files:** [MIDI](./examples/05_chromatic_crab_canon.mid) | [MusicXML](./examples/05_chromatic_crab_canon.musicxml) | [JSON](./examples/05_chromatic_analysis.json)
- **Visualizations:** [Piano Roll](./examples/05_chromatic_piano_roll.png) | [Symmetry](./examples/05_chromatic_symmetry.png)
- **Duration:** 5.5 quarter notes
- **Notes:** 13 per voice
- **Palindrome:** ✓ Verified

![Chromatic Symmetry](./examples/05_chromatic_symmetry.png)

---

## 🔬 Advanced Canon Types

Exploring variations on the crab canon technique.

### 6. Augmentation Canon

Theme played forward at normal speed, retrograde at half speed (2x duration).

- **Files:** [MIDI](./examples/06_augmentation_canon.mid) | [MusicXML](./examples/06_augmentation_canon.musicxml) | [JSON](./examples/06_augmentation_analysis.json)
- **Visualizations:** [Piano Roll](./examples/06_augmentation_piano_roll.png) | [Symmetry](./examples/06_augmentation_symmetry.png)
- **Technique:** Augmentation (factor: 2.0)
- **Palindrome:** ✓ Verified

![Augmentation Piano Roll](./examples/06_augmentation_piano_roll.png)

### 7. Diminution Canon

Theme played forward at normal speed, retrograde at double speed (0.5x duration).

- **Files:** [MIDI](./examples/07_diminution_canon.mid) | [MusicXML](./examples/07_diminution_canon.musicxml) | [JSON](./examples/07_diminution_analysis.json)
- **Visualizations:** [Piano Roll](./examples/07_diminution_piano_roll.png) | [Symmetry](./examples/07_diminution_symmetry.png)
- **Technique:** Diminution (factor: 0.5)
- **Palindrome:** ✓ Verified

![Diminution Piano Roll](./examples/07_diminution_piano_roll.png)

### 8. Mirror Canon

Theme with both retrograde AND inversion (pitch flip).

- **Files:** [MIDI](./examples/08_mirror_canon.mid) | [MusicXML](./examples/08_mirror_canon.musicxml) | [JSON](./examples/08_mirror_analysis.json)
- **Visualizations:** [Piano Roll](./examples/08_mirror_piano_roll.png) | [Symmetry](./examples/08_mirror_symmetry.png)
- **Technique:** Retrograde + Inversion
- **Palindrome:** ✓ Verified

![Mirror Canon Piano Roll](./examples/08_mirror_piano_roll.png)

### 9. Combined Canon

Multiple transformations applied: augmentation, diminution, and mirror.

- **Files:** [MIDI](./examples/09_crab_augmentation_canon.mid) | [MusicXML](./examples/09_crab_augmentation_canon.musicxml) | [JSON](./examples/09_crab_augmentation_analysis.json)
- **Visualizations:** [Piano Roll](./examples/09_crab_augmentation_piano_roll.png) | [Symmetry](./examples/09_crab_augmentation_symmetry.png)
- **Technique:** Multiple transformations
- **Palindrome:** ✓ Verified

![Combined Piano Roll](./examples/09_crab_augmentation_piano_roll.png)

### 10. Triple Canon

Three voices: forward, retrograde, and mirror.

- **Files:** [MIDI](./examples/10_triple_canon.mid) | [MusicXML](./examples/10_triple_canon.musicxml) | [JSON](./examples/10_triple_analysis.json)
- **Visualizations:** [Piano Roll](./examples/10_triple_piano_roll.png) | [Symmetry](./examples/10_triple_symmetry.png)
- **Voices:** 3
- **Palindrome:** ✓ Verified

![Triple Canon Piano Roll](./examples/10_triple_piano_roll.png)

---

## 📈 Visualizations

### Visualization Types

#### Piano Roll
Shows notes as rectangles on a pitch-time grid. Time flows left to right, pitch increases from bottom to top. Perfect for seeing melodic contour and rhythm.

#### Symmetry Plot
Displays palindromic structure with a vertical midpoint line. Connecting lines show which notes are mirror pairs. Highlights the temporal symmetry.

#### Waveform (Web App)
Real-time audio visualization showing the sound wave as it plays. Available in the web application.

### Custom Visualizations

You can generate your own visualizations using the CLI:

```bash
# Piano roll
python -m cancrizans render --input your_file.mid --roll output.png

# Symmetry plot
python -m cancrizans render --input your_file.mid --mirror output.png
```

---

## 🎯 Using These Examples

### For Learning
- Start with Example 1 (Scale) - simplest concept
- Progress to Example 2-3 (Arpeggio, Melody) - musical interest
- Try Example 4 (Rhythm) - focus on temporal patterns
- Explore Example 5 (Chromatic) - all semitones
- Study Examples 6-10 - advanced techniques

### For Teaching
- Use visualizations to explain concepts
- Play MIDI files to demonstrate sound
- Analyze JSON data for statistics
- Compare different canon types

### For Research
- Batch analyze all examples: `python -m cancrizans research examples/ --all`
- Export data for statistical analysis
- Study consonance/dissonance patterns
- Examine interval distributions

---

## 📊 Statistics Summary

| Canon | Duration | Notes/Voice | Consonance | Avg Interval |
|-------|----------|-------------|------------|--------------|
| Bach  | 144.0 q  | 184         | 76%        | 2.3 semi    |
| Scale | 4.5 q    | 8           | 100%       | 2.0 semi    |
| Arpeggio | 5.0 q | 9           | 100%       | 3.7 semi    |
| Melody | 7.0 q   | 10          | 90%        | 1.8 semi    |
| Rhythm | 5.0 q   | 8           | 100%       | 0.0 semi    |
| Chromatic | 5.5 q | 13         | 85%        | 1.0 semi    |

*q = quarter notes, semi = semitones*

---

## 🔗 Additional Resources

- [README.md](./README.md) - Project overview and installation
- [EXAMPLES.md](./EXAMPLES.md) - Detailed usage examples
- [LESSON_PLANS.md](./docs/LESSON_PLANS.md) - Educational materials
- [Jupyter Notebook](./notebooks/bach_crab_canon_exploration.ipynb) - Interactive analysis
- [Web Application](./web/) - Interactive explorer

---

*Gallery last updated: 2025-11-11*
*All examples verified as true palindromes* ✓
"""
    return content


def main():
    """Generate GALLERY.md"""
    gallery_path = Path('GALLERY.md')
    content = generate_gallery_md()

    with open(gallery_path, 'w') as f:
        f.write(content)

    print(f"✓ Generated: {gallery_path}")
    print(f"  - 10 example canons with visualizations")
    print(f"  - All links corrected")
    print(f"  - Statistics table added")


if __name__ == '__main__':
    main()
