"""
Extract MIDI note data and convert to JavaScript format for the web UI.
"""

from music21 import converter
import json

# Load the real Bach MIDI
score = converter.parse('data/bach_crab_canon_original.mid')
parts = list(score.parts)

# Extract notes from both parts
voices_data = []

for part_idx, part in enumerate(parts):
    notes_list = []

    for element in part.flatten().notesAndRests:
        if element.isRest:
            continue

        if hasattr(element, 'pitch'):
            # Single note
            note_data = {
                'pitch': element.pitch.midi,
                'start': float(element.offset),
                'duration': float(element.quarterLength),
                'name': element.nameWithOctave
            }
            notes_list.append(note_data)
        elif hasattr(element, 'pitches'):
            # Chord - use lowest pitch
            pitches = list(element.pitches)
            lowest = min(pitches, key=lambda p: p.midi)
            note_data = {
                'pitch': lowest.midi,
                'start': float(element.offset),
                'duration': float(element.quarterLength),
                'name': lowest.nameWithOctave
            }
            notes_list.append(note_data)

    voices_data.append({
        'id': f'voice{part_idx + 1}',
        'notes': notes_list
    })

# Create output
output = {
    'voices': voices_data,
    'totalDuration': float(score.highestTime),
    'timeSignature': {'beats': 4, 'beatType': 4},
    'keySignature': -1  # F major
}

# Write as JSON
with open('web/src/bach_crab_canon_data.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"✓ Extracted {len(voices_data)} voices")
print(f"  Voice 1: {len(voices_data[0]['notes'])} notes")
print(f"  Voice 2: {len(voices_data[1]['notes'])} notes")
print(f"  Total duration: {output['totalDuration']:.2f} quarter notes")
print(f"✓ Saved to web/src/bach_crab_canon_data.json")
