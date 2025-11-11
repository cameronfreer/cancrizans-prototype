"""
Analyze and convert the real Bach Crab Canon MIDI file.
"""

from pathlib import Path
import music21 as m21
from music21 import converter, stream, note, midi
from cancrizans.io import to_midi, to_musicxml

# Load the original MIDI
original_midi = Path('data/bach_crab_canon_original.mid')
score = converter.parse(str(original_midi))

print("=== Bach Crab Canon Analysis ===\n")
print(f"Parts: {len(score.parts)}")
print(f"Total duration: {score.highestTime:.2f} quarter notes")

# Analyze each part
for i, part in enumerate(score.parts):
    notes_list = list(part.flatten().notesAndRests)
    note_count = sum(1 for n in notes_list if not n.isRest)
    rest_count = sum(1 for n in notes_list if n.isRest)

    print(f"\nPart {i+1}:")
    print(f"  Total elements: {len(notes_list)}")
    print(f"  Notes: {note_count}")
    print(f"  Rests: {rest_count}")

    if note_count > 0:
        first_notes = [n for n in notes_list if not n.isRest][:5]
        print(f"  First 5 notes: {[n.nameWithOctave for n in first_notes]}")

# Check if it's a palindrome
from cancrizans.canon import is_time_palindrome

print(f"\nis_time_palindrome: {is_time_palindrome(score)}")

# Export cleaned version
print("\nExporting cleaned version...")
to_musicxml(score, 'data/bach_crab_canon_real.musicxml')
print("✓ Saved to data/bach_crab_canon_real.musicxml")
