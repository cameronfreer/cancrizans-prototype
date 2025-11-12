#!/usr/bin/env python3
"""
Auto-generate API reference documentation from docstrings
"""

import inspect
import importlib
import sys
from pathlib import Path
from typing import Any, Callable
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import cancrizans
from cancrizans import canon, bach_crab, viz, research, io


def get_function_signature(func: Callable) -> str:
    """Get formatted function signature."""
    try:
        sig = inspect.signature(func)
        return f"{func.__name__}{sig}"
    except (ValueError, TypeError):
        return f"{func.__name__}(...)"


def get_docstring(obj: Any) -> str:
    """Get and format docstring."""
    doc = inspect.getdoc(obj)
    if doc:
        # Indent docstring
        lines = doc.split('\n')
        return '\n'.join(f"  {line}" if line.strip() else "" for line in lines)
    return "  No documentation available."


def generate_module_docs(module: Any, module_name: str) -> str:
    """Generate documentation for a module."""
    output = [f"### `{module_name}`\n"]

    # Get module docstring
    if module.__doc__:
        output.append(f"{module.__doc__.strip()}\n")

    # Get all public functions and classes
    members = inspect.getmembers(module)
    functions = [(name, obj) for name, obj in members
                 if inspect.isfunction(obj) and not name.startswith('_')]
    classes = [(name, obj) for name, obj in members
               if inspect.isclass(obj) and not name.startswith('_')]

    # Document functions
    if functions:
        output.append("\n#### Functions\n")
        for name, func in sorted(functions):
            sig = get_function_signature(func)
            output.append(f"##### `{sig}`\n")
            output.append(get_docstring(func))
            output.append("\n")

    # Document classes
    if classes:
        output.append("\n#### Classes\n")
        for name, cls in sorted(classes):
            output.append(f"##### `class {name}`\n")
            output.append(get_docstring(cls))

            # Document class methods
            methods = inspect.getmembers(cls, predicate=inspect.isfunction)
            public_methods = [(n, m) for n, m in methods
                             if not n.startswith('_') or n == '__init__']

            if public_methods:
                output.append("\n  **Methods:**\n")
                for method_name, method in sorted(public_methods):
                    sig = get_function_signature(method)
                    output.append(f"  - `{sig}`")

                    # Get brief description (first line of docstring)
                    doc = inspect.getdoc(method)
                    if doc:
                        first_line = doc.split('\n')[0].strip()
                        output.append(f": {first_line}")
                    output.append("\n")

            output.append("\n")

    return '\n'.join(output)


def generate_examples() -> str:
    """Generate usage examples."""
    examples = """## Usage Examples

### Basic Retrograde

```python
from cancrizans import retrograde, load_bach_crab_canon

# Load Bach's Crab Canon
score = load_bach_crab_canon()

# Get the first part
theme = score.parts[0]

# Apply retrograde transformation
retrograded = retrograde(theme)

print(f"Original duration: {theme.duration.quarterLength} quarters")
print(f"Retrograded duration: {retrograded.duration.quarterLength} quarters")
```

### Palindrome Verification

```python
from cancrizans import is_time_palindrome, load_bach_crab_canon

# Load Bach's Crab Canon
score = load_bach_crab_canon()

# Verify it's a perfect palindrome
is_palindrome, details = is_time_palindrome(score, details=True)

print(f"Is palindrome: {is_palindrome}")
print(f"Symmetry pairs: {len(details['pairs'])}")
```

### Creating a Mirror Canon

```python
from cancrizans import mirror_canon
from music21 import note, stream

# Create a simple melody
melody = stream.Part()
for pitch in ['C4', 'D4', 'E4', 'F4', 'G4']:
    melody.append(note.Note(pitch, quarterLength=1.0))

# Create mirror canon (retrograde + alignment)
canon = mirror_canon(melody)

print(f"Mirror canon has {len(canon.parts)} parts")
print(f"Duration: {canon.duration.quarterLength} quarters")
```

### Interval Analysis

```python
from cancrizans import interval_analysis, load_bach_crab_canon

# Analyze Bach's Crab Canon
score = load_bach_crab_canon()
analysis = interval_analysis(score)

print(f"Most common interval: {analysis['most_common_interval']}")
print(f"Interval diversity: {analysis['interval_diversity']:.2f}")
print(f"Average interval size: {analysis['average_interval_size']:.2f}")
```

### Batch Research

```python
from cancrizans.research import analyze_corpus

# Analyze all MIDI files in examples directory
analyses, comparison = analyze_corpus(
    input_dir='./examples',
    pattern='*.mid'
)

print(f"Analyzed {len(analyses)} canons")
print(f"Average duration: {comparison['avg_duration']:.2f} quarters")
print(f"Average tempo: {comparison['avg_tempo']:.1f} BPM")
```

### Visualization

```python
from cancrizans import load_bach_crab_canon
from cancrizans.viz import piano_roll, symmetry

# Load and visualize
score = load_bach_crab_canon()

# Create piano roll visualization
piano_roll(score, 'bach_piano_roll.png')

# Create symmetry visualization
symmetry(score, 'bach_symmetry.png')

print("Visualizations saved!")
```

### Transformation Chain

```python
from cancrizans import retrograde, invert, augmentation
from music21 import note, stream

# Create melody
melody = stream.Part()
for pitch in ['C4', 'E4', 'G4', 'C5']:
    melody.append(note.Note(pitch, quarterLength=1.0))

# Apply transformation chain
result = melody
result = augmentation(result, factor=2)  # Slower
result = invert(result, axis=65)         # Invert around F4
result = retrograde(result)              # Reverse

print(f"Original: {melody.duration.quarterLength}q")
print(f"Transformed: {result.duration.quarterLength}q")
```
"""
    return examples


def generate_api_reference() -> str:
    """Generate complete API reference documentation."""

    header = f"""# API Reference

**Auto-generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Version**: {cancrizans.__version__}

This document provides comprehensive API documentation for the Cancrizans library.

## Table of Contents

1. [Core Functions (`cancrizans.canon`)](#canrizanscanon)
2. [Bach Utilities (`cancrizans.bach_crab`)](#canrizansbach_crab)
3. [Visualization (`cancrizans.viz`)](#cancrizansviz)
4. [Research Tools (`cancrizans.research`)](#canrizansresearch)
5. [I/O Functions (`cancrizans.io`)](#canrizansio)
6. [Usage Examples](#usage-examples)

---

"""

    # Generate module documentation
    modules = [
        (canon, 'cancrizans.canon'),
        (bach_crab, 'cancrizans.bach_crab'),
        (viz, 'cancrizans.viz'),
        (research, 'cancrizans.research'),
        (io, 'cancrizans.io'),
    ]

    module_docs = []
    for module, name in modules:
        module_docs.append(generate_module_docs(module, name))

    # Combine all parts
    full_doc = header + '\n'.join(module_docs) + '\n' + generate_examples()

    return full_doc


def main():
    """Generate API documentation."""
    print("Generating API reference documentation...")

    # Generate documentation
    api_docs = generate_api_reference()

    # Write to file
    output_path = Path(__file__).parent.parent / 'docs' / 'API_REFERENCE.md'
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(api_docs)

    print(f"✓ Generated: {output_path}")
    print(f"  Size: {len(api_docs)} characters")
    print(f"  Lines: {len(api_docs.splitlines())}")


if __name__ == '__main__':
    main()
