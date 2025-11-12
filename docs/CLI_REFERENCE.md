# CLI Reference

**Auto-generated**: 2025-11-12 01:02:19

This document provides comprehensive CLI documentation for the Cancrizans command-line interface.

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Commands](#commands)
   - [analyze](#analyze)
   - [render](#render)
   - [synthesize](#synthesize)
   - [research](#research)
4. [Examples](#examples)
5. [Tips & Tricks](#tips--tricks)

---

## Installation

```bash
# Install from source
pip install -e .

# Or install with audio support
pip install -e ".[audio]"
```

## Basic Usage

```bash
# Get help
cancrizans --help

# Get version
cancrizans --version

# Command-specific help
cancrizans analyze --help
```

## Commands

### `analyze`

Analyze a MIDI or MusicXML file for palindromic properties, intervals, harmony, and rhythm.

**Usage:**
```bash
cancrizans analyze [OPTIONS] INPUT_FILE
```

**Options:**
- `-o, --output PATH`: Output file for analysis results (JSON format)
- `--format [text|json]`: Output format (default: text)
- `--verbose`: Show detailed analysis

**Example:**
```bash
# Analyze Bach's Crab Canon
cancrizans analyze data/bach_crab_canon.mid

# Save analysis as JSON
cancrizans analyze data/bach_crab_canon.mid -o analysis.json --format json

# Verbose analysis
cancrizans analyze examples/01_scale_crab_canon.mid --verbose
```

**Sample Output:**
```
=== Palindrome Analysis ===
Is time palindrome: True
Symmetry pairs: 184

=== Interval Analysis ===
Most common interval: M2 (major second)
Interval diversity: 0.542
Average interval size: 1.85 semitones

=== Harmonic Analysis ===
Key: D minor
Most common chord: D minor triad

=== Rhythm Analysis ===
Total duration: 144.0 quarter notes
Most common duration: 1.0 quarters
Rhythm diversity: 0.312
```

---

### `render`

Render a MIDI file to various visual formats (piano roll, symmetry plot).

**Usage:**
```bash
cancrizans render [OPTIONS] INPUT_FILE
```

**Options:**
- `-o, --output PATH`: Output directory (default: current directory)
- `-t, --type [piano_roll|symmetry|both]`: Visualization type (default: both)
- `--dpi INTEGER`: Image resolution (default: 150)
- `--format [png|pdf|svg]`: Image format (default: png)

**Example:**
```bash
# Render piano roll
cancrizans render data/bach_crab_canon.mid -t piano_roll

# Render both visualizations
cancrizans render examples/bach_crab_canon.mid -t both

# High-resolution PDF
cancrizans render data/bach_crab_canon.mid --dpi 300 --format pdf

# Save to specific directory
cancrizans render examples/01_scale_crab_canon.mid -o ./visualizations/
```

**Generated Files:**
- `<input>_piano_roll.png`: Piano roll visualization
- `<input>_symmetry.png`: Symmetry visualization

---

### `synthesize`

Convert MIDI to audio (WAV format). Requires FluidSynth and soundfont file.

**Usage:**
```bash
cancrizans synthesize [OPTIONS] INPUT_FILE
```

**Options:**
- `-o, --output PATH`: Output WAV file
- `-s, --soundfont PATH`: Path to soundfont file (.sf2)
- `--sample-rate INTEGER`: Sample rate (default: 44100)

**Example:**
```bash
# Synthesize to WAV (requires FluidSynth)
cancrizans synthesize data/bach_crab_canon.mid -o bach.wav

# Custom soundfont
cancrizans synthesize data/bach_crab_canon.mid \
    -s /usr/share/sounds/sf2/FluidR3_GM.sf2 \
    -o output.wav

# High-quality audio
cancrizans synthesize examples/01_scale_crab_canon.mid \
    --sample-rate 48000 \
    -o scale_canon.wav
```

**Note:** Requires `midi2audio` and FluidSynth to be installed:
```bash
pip install "cancrizans[audio]"
# + FluidSynth system package
```

---

### `research`

Batch analyze multiple MIDI/MusicXML files and export comparative statistics.

**Usage:**
```bash
cancrizans research [OPTIONS] INPUT_DIR
```

**Options:**
- `-p, --pattern TEXT`: File pattern (default: *.mid)
- `-o, --output PATH`: Output directory (default: ./research_output)
- `--csv`: Export as CSV
- `--json`: Export as JSON
- `--latex`: Export as LaTeX table
- `--markdown`: Export as Markdown table

**Example:**
```bash
# Analyze all MIDI files in directory
cancrizans research examples/

# Analyze with custom pattern
cancrizans research examples/ -p "*.mid"

# Export all formats
cancrizans research examples/ --csv --json --latex --markdown

# Custom output directory
cancrizans research ~/my_canons/ -o ./analysis_results/
```

**Generated Files:**
- `analyses.csv`: Individual file analyses
- `analyses.json`: JSON format analyses
- `comparison.csv`: Comparative statistics
- `comparison_table.tex`: LaTeX table
- `comparison_table.md`: Markdown table

**Sample Output:**
```
Analyzing corpus: examples/
Pattern: *.mid
Found 10 files

Processing: 01_scale_crab_canon.mid ✓
Processing: 02_arpeggio_crab_canon.mid ✓
...

=== Comparative Statistics ===
Total files: 10
Average duration: 48.3 quarters
Average tempo: 84.2 BPM
Average interval diversity: 0.487

Exported:
  ✓ analyses.csv
  ✓ comparison.csv
  ✓ comparison_table.tex
  ✓ comparison_table.md
```

---

## Examples

### Complete Workflow

```bash
# 1. Analyze a canon
cancrizans analyze my_canon.mid --verbose

# 2. Generate visualizations
cancrizans render my_canon.mid -t both --dpi 200

# 3. Synthesize to audio
cancrizans synthesize my_canon.mid -o my_canon.wav

# 4. Batch analyze collection
cancrizans research ./my_canons/ --csv --json
```

### Pipeline with Scripts

```bash
# Analyze all canons and save results
for file in examples/*.mid; do
    cancrizans analyze "$file" -o "analysis_$(basename $file .mid).json"
done

# Generate all visualizations
for file in examples/*.mid; do
    cancrizans render "$file" -o ./visualizations/
done
```

### Research Workflow

```bash
# 1. Collect corpus
mkdir corpus
cp ~/music/canons/*.mid corpus/

# 2. Batch analyze
cancrizans research corpus/ --csv --json --latex

# 3. Visualize each
for file in corpus/*.mid; do
    cancrizans render "$file" -t symmetry -o ./corpus_viz/
done
```

---

## Tips & Tricks

### 1. Quick Analysis

For quick palindrome checking:
```bash
cancrizans analyze file.mid | grep "Is time palindrome"
```

### 2. Batch Processing

Process all MIDI files recursively:
```bash
find . -name "*.mid" -exec cancrizans analyze {} \;
```

### 3. Export All Formats

Generate comprehensive analysis:
```bash
cancrizans analyze file.mid --verbose > analysis.txt
cancrizans analyze file.mid --format json > analysis.json
cancrizans render file.mid -t both
```

### 4. Performance

For large corpora, use parallel processing:
```bash
find corpus/ -name "*.mid" | parallel cancrizans analyze {} -o {}.json
```

### 5. Integration with Other Tools

Pipe to other utilities:
```bash
# Count palindromes
cancrizans research examples/ --json | jq '.[] | select(.is_palindrome == true)' | wc -l

# Extract specific fields
cancrizans analyze file.mid --format json | jq '.interval_analysis.most_common_interval'
```

---

## Environment Variables

- `CANCRIZANS_SOUNDFONT`: Default soundfont path for synthesis
- `CANCRIZANS_OUTPUT_DIR`: Default output directory

Example:
```bash
export CANCRIZANS_SOUNDFONT="/usr/share/sounds/sf2/FluidR3_GM.sf2"
cancrizans synthesize file.mid -o output.wav
```

---

## Exit Codes

- `0`: Success
- `1`: General error
- `2`: File not found
- `3`: Invalid file format
- `4`: Missing dependencies (e.g., FluidSynth not installed)

---

## Getting Help

```bash
# General help
cancrizans --help

# Command help
cancrizans analyze --help
cancrizans render --help
cancrizans synthesize --help
cancrizans research --help
```

For more information, visit:
- Documentation: `docs/`
- Examples: `examples/`
- GitHub: https://github.com/yourusername/cancrizans
