"""
Create additional musical examples: simple canons, educational demos.
"""

from music21 import stream, note, chord, meter, key, clef
from cancrizans import assemble_crab_from_theme, is_time_palindrome
from cancrizans.io import to_midi, to_musicxml
from cancrizans.viz import piano_roll, symmetry
from pathlib import Path

# Create examples directory
examples_dir = Path('examples')
examples_dir.mkdir(exist_ok=True)

print("Creating additional musical examples...\n")

# Example 1: Simple ascending scale crab canon
print("1. Simple Scale Crab Canon")
scale_theme = stream.Stream()
for pitch in ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']:
    scale_theme.append(note.Note(pitch, quarterLength=0.5))

scale_crab = assemble_crab_from_theme(scale_theme)
to_midi(scale_crab, examples_dir / '01_scale_crab_canon.mid')
piano_roll(scale_crab, examples_dir / '01_scale_piano_roll.png')
print(f"   ✓ is_palindrome: {is_time_palindrome(scale_crab)}")
print(f"   ✓ Files: 01_scale_crab_canon.mid, 01_scale_piano_roll.png\n")

# Example 2: Arpeggio crab canon
print("2. Arpeggio Crab Canon")
arp_theme = stream.Stream()
arp_notes = [
    ('C4', 0.5), ('E4', 0.5), ('G4', 0.5), ('C5', 0.5),
    ('E5', 0.5), ('C5', 0.5), ('G4', 0.5), ('E4', 0.5),
    ('C4', 1.0)
]
for pitch, dur in arp_notes:
    arp_theme.append(note.Note(pitch, quarterLength=dur))

arp_crab = assemble_crab_from_theme(arp_theme)
to_midi(arp_crab, examples_dir / '02_arpeggio_crab_canon.mid')
symmetry(arp_crab, examples_dir / '02_arpeggio_symmetry.png')
print(f"   ✓ is_palindrome: {is_time_palindrome(arp_crab)}")
print(f"   ✓ Files: 02_arpeggio_crab_canon.mid, 02_arpeggio_symmetry.png\n")

# Example 3: Melodic phrase crab canon
print("3. Melodic Phrase Crab Canon")
melody_theme = stream.Stream()
melody_notes = [
    ('G4', 0.5), ('A4', 0.5), ('B4', 0.5), ('C5', 0.5),
    ('D5', 1.0), ('C5', 0.5), ('B4', 0.5),
    ('A4', 0.5), ('G4', 0.5), ('F#4', 0.5), ('G4', 1.5),
]
for pitch, dur in melody_notes:
    melody_theme.append(note.Note(pitch, quarterLength=dur))

melody_crab = assemble_crab_from_theme(melody_theme)
to_midi(melody_crab, examples_dir / '03_melody_crab_canon.mid')
to_musicxml(melody_crab, examples_dir / '03_melody_crab_canon.musicxml')
piano_roll(melody_crab, examples_dir / '03_melody_piano_roll.png')
symmetry(melody_crab, examples_dir / '03_melody_symmetry.png')
print(f"   ✓ is_palindrome: {is_time_palindrome(melody_crab)}")
print(f"   ✓ Files: 03_melody_crab_canon.mid/.xml, visualizations\n")

# Example 4: Rhythmic crab canon (same pitch, different rhythms)
print("4. Rhythmic Crab Canon")
rhythm_theme = stream.Stream()
rhythm_pattern = [
    ('C5', 0.25), ('C5', 0.25), ('C5', 0.5),
    ('C5', 1.0), ('C5', 0.5), ('C5', 0.25), ('C5', 0.25),
    ('C5', 2.0),
]
for pitch, dur in rhythm_pattern:
    rhythm_theme.append(note.Note(pitch, quarterLength=dur))

rhythm_crab = assemble_crab_from_theme(rhythm_theme)
to_midi(rhythm_crab, examples_dir / '04_rhythm_crab_canon.mid')
piano_roll(rhythm_crab, examples_dir / '04_rhythm_piano_roll.png')
print(f"   ✓ is_palindrome: {is_time_palindrome(rhythm_crab)}")
print(f"   ✓ Files: 04_rhythm_crab_canon.mid, 04_rhythm_piano_roll.png\n")

# Example 5: Chromatic crab canon
print("5. Chromatic Crab Canon")
chromatic_theme = stream.Stream()
chromatic_notes = ['C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4', 'C5']
for pitch in chromatic_notes:
    chromatic_theme.append(note.Note(pitch, quarterLength=0.375))

chromatic_crab = assemble_crab_from_theme(chromatic_theme)
to_midi(chromatic_crab, examples_dir / '05_chromatic_crab_canon.mid')
symmetry(chromatic_crab, examples_dir / '05_chromatic_symmetry.png')
print(f"   ✓ is_palindrome: {is_time_palindrome(chromatic_crab)}")
print(f"   ✓ Files: 05_chromatic_crab_canon.mid, 05_chromatic_symmetry.png\n")

print("=" * 60)
print("✓ All examples created successfully!")
print(f"  Total: 5 crab canons with visualizations")
print(f"  Location: {examples_dir}/")
