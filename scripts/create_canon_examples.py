"""
Create examples of different canon types: augmentation, diminution, mirror.
"""

from music21 import stream, note
from cancrizans import (
    retrograde,
    augmentation,
    diminution,
    mirror_canon,
    time_align,
    is_time_palindrome
)
from cancrizans.io import to_midi, to_musicxml
from cancrizans.viz import piano_roll, symmetry
from pathlib import Path

# Create examples directory
examples_dir = Path('examples')
examples_dir.mkdir(exist_ok=True)

print("Creating advanced canon examples...\n")

# Create a simple theme for all examples
theme = stream.Stream()
theme_notes = [
    ('C4', 1.0), ('D4', 1.0), ('E4', 1.0), ('F4', 1.0),
    ('G4', 0.5), ('A4', 0.5), ('G4', 0.5), ('F4', 0.5),
    ('E4', 1.0), ('D4', 1.0), ('C4', 2.0)
]

for pitch, dur in theme_notes:
    theme.append(note.Note(pitch, quarterLength=dur))

print("Base theme created with", len(theme_notes), "notes\n")

# 1. Augmentation Canon
print("1. Augmentation Canon (2x slower)")
theme_augmented = augmentation(theme, factor=2.0)
aug_canon = time_align(theme, theme_augmented, offset_quarters=0.0)

to_midi(aug_canon, examples_dir / '06_augmentation_canon.mid')
to_musicxml(aug_canon, examples_dir / '06_augmentation_canon.musicxml')
piano_roll(aug_canon, examples_dir / '06_augmentation_piano_roll.png')

print(f"   Theme duration: {theme.highestTime:.2f} quarters")
print(f"   Augmented duration: {theme_augmented.highestTime:.2f} quarters")
print(f"   Files created: 06_augmentation_canon.*\n")

# 2. Diminution Canon
print("2. Diminution Canon (2x faster)")
theme_diminished = diminution(theme, factor=2.0)
dim_canon = time_align(theme, theme_diminished, offset_quarters=0.0)

to_midi(dim_canon, examples_dir / '07_diminution_canon.mid')
to_musicxml(dim_canon, examples_dir / '07_diminution_canon.musicxml')
piano_roll(dim_canon, examples_dir / '07_diminution_piano_roll.png')

print(f"   Theme duration: {theme.highestTime:.2f} quarters")
print(f"   Diminished duration: {theme_diminished.highestTime:.2f} quarters")
print(f"   Files created: 07_diminution_canon.*\n")

# 3. Mirror Canon (retrograde + inversion)
print("3. Mirror Canon (retrograde + inversion)")
theme_mirrored = mirror_canon(theme, axis_pitch='E4')
mirror_can = time_align(theme, theme_mirrored, offset_quarters=0.0)

to_midi(mirror_can, examples_dir / '08_mirror_canon.mid')
to_musicxml(mirror_can, examples_dir / '08_mirror_canon.musicxml')
piano_roll(mirror_can, examples_dir / '08_mirror_piano_roll.png')
symmetry(mirror_can, examples_dir / '08_mirror_symmetry.png')

print(f"   Original first note: {list(theme.flatten().notes)[0].nameWithOctave}")
print(f"   Mirrored first note: {list(theme_mirrored.flatten().notes)[0].nameWithOctave}")
print(f"   Files created: 08_mirror_canon.*\n")

# 4. Combined: Crab Canon with Augmentation
print("4. Augmented Crab Canon (retrograde + augmentation)")
theme_retro_aug = augmentation(retrograde(theme), factor=1.5)
retro_aug_canon = time_align(theme, theme_retro_aug, offset_quarters=0.0)

to_midi(retro_aug_canon, examples_dir / '09_crab_augmentation_canon.mid')
piano_roll(retro_aug_canon, examples_dir / '09_crab_augmentation_piano_roll.png')

print(f"   Combines retrograde AND augmentation")
print(f"   Files created: 09_crab_augmentation_canon.*\n")

# 5. Triple Canon: Original, Retrograde, Augmented
print("5. Triple Canon (original + retrograde + augmented)")
theme_retro = retrograde(theme)
theme_aug = augmentation(theme, factor=1.5)

# Create a score with 3 parts
from music21 import stream
triple_score = stream.Score()

part1 = stream.Part()
part1.id = 'original'
for el in theme.flatten().notesAndRests:
    part1.insert(el.offset, el)

part2 = stream.Part()
part2.id = 'retrograde'
for el in theme_retro.flatten().notesAndRests:
    part2.insert(el.offset, el)

part3 = stream.Part()
part3.id = 'augmented'
for el in theme_aug.flatten().notesAndRests:
    part3.insert(el.offset, el)

triple_score.insert(0, part1)
triple_score.insert(0, part2)
triple_score.insert(0, part3)

to_midi(triple_score, examples_dir / '10_triple_canon.mid')
to_musicxml(triple_score, examples_dir / '10_triple_canon.musicxml')
piano_roll(triple_score, examples_dir / '10_triple_piano_roll.png')

print(f"   3 voices: original, retrograde, augmented")
print(f"   Files created: 10_triple_canon.*\n")

print("=" * 60)
print("✓ All advanced canon examples created!")
print(f"  Location: {examples_dir}/")
print(f"  Total: 5 new canon types")
print("\nCanon Types Created:")
print("  06 - Augmentation Canon (2x slower)")
print("  07 - Diminution Canon (2x faster)")
print("  08 - Mirror Canon (retrograde + inversion)")
print("  09 - Crab + Augmentation")
print("  10 - Triple Canon (original + retrograde + augmented)")
