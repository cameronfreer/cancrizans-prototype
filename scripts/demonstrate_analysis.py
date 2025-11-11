"""
Demonstrate the new analysis capabilities: interval, harmonic, and rhythm analysis.
"""

from music21 import converter
from cancrizans import interval_analysis, harmonic_analysis, rhythm_analysis
import json

print("=" * 70)
print("MUSICAL ANALYSIS DEMONSTRATION")
print("=" * 70)
print()

# Load Bach's Crab Canon
print("Loading Bach's Crab Canon...")
score = converter.parse('data/bach_crab_canon_original.mid')
print(f"✓ Loaded: {len(list(score.parts))} voices\n")

# 1. Interval Analysis
print("1. INTERVAL ANALYSIS")
print("-" * 70)

interval_stats = interval_analysis(score)

print(f"Total melodic intervals: {interval_stats['total_intervals']}")
print(f"Average interval size: {interval_stats['average']:.2f} semitones")
print(f"Largest leap: {interval_stats['largest_leap']} semitones")
print()

print("Distribution:")
print(f"  Ascending: {interval_stats['distribution']['ascending']} " +
      f"({interval_stats['distribution']['ascending']/interval_stats['total_intervals']*100:.1f}%)")
print(f"  Descending: {interval_stats['distribution']['descending']} " +
      f"({interval_stats['distribution']['descending']/interval_stats['total_intervals']*100:.1f}%)")
print(f"  Repeated: {interval_stats['distribution']['repeated']} " +
      f"({interval_stats['distribution']['repeated']/interval_stats['total_intervals']*100:.1f}%)")
print()

print("Most common intervals:")
for interval, count in interval_stats['most_common']:
    direction = "ascending" if interval > 0 else "descending" if interval < 0 else "repeated"
    print(f"  {abs(interval):2d} semitones ({direction}): {count} times")
print()

# 2. Harmonic Analysis
print("2. HARMONIC ANALYSIS")
print("-" * 70)

harmonic_stats = harmonic_analysis(score)

print(f"Total sonorities: {harmonic_stats['total_sonorities']}")
print(f"Consonances: {harmonic_stats['consonances']}")
print(f"Dissonances: {harmonic_stats['dissonances']}")
print(f"Consonance ratio: {harmonic_stats['consonance_ratio']:.2%}")
print()

print("Interval classes (vertical intervals):")
for interval_class, count in sorted(harmonic_stats['interval_classes'].items()):
    interval_names = {
        0: "Unison/Octave",
        1: "Minor 2nd",
        2: "Major 2nd",
        3: "Minor 3rd",
        4: "Major 3rd",
        5: "Perfect 4th",
        6: "Tritone",
        7: "Perfect 5th",
        8: "Minor 6th",
        9: "Major 6th",
        10: "Minor 7th",
        11: "Major 7th"
    }
    name = interval_names.get(interval_class, str(interval_class))
    print(f"  {name}: {count} times")
print()

# 3. Rhythm Analysis
print("3. RHYTHM ANALYSIS")
print("-" * 70)

rhythm_stats = rhythm_analysis(score)

print(f"Total events: {rhythm_stats['total_events']}")
print(f"Average duration: {rhythm_stats['average_duration']:.3f} quarter notes")
print(f"Shortest note: {rhythm_stats['shortest']:.3f} quarters")
print(f"Longest note: {rhythm_stats['longest']:.3f} quarters")
print(f"Unique durations: {rhythm_stats['unique_durations']}")
print()

print("Most common durations:")
for duration, count in rhythm_stats['most_common']:
    # Convert to note names
    note_type = {
        0.25: "16th note",
        0.5: "8th note",
        1.0: "quarter note",
        2.0: "half note",
        4.0: "whole note"
    }.get(duration, f"{duration} quarters")
    print(f"  {note_type}: {count} times ({count/rhythm_stats['total_events']*100:.1f}%)")
print()

# Save analysis results
print("=" * 70)
print("SAVING ANALYSIS RESULTS")
print("-" * 70)

analysis_results = {
    'interval_analysis': interval_stats,
    'harmonic_analysis': harmonic_stats,
    'rhythm_analysis': rhythm_stats
}

with open('examples/bach_analysis.json', 'w') as f:
    # Convert any non-serializable types
    def clean_for_json(obj):
        if isinstance(obj, dict):
            return {str(k): clean_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean_for_json(item) for item in obj]
        elif isinstance(obj, tuple):
            return list(obj)
        else:
            return obj

    json.dump(clean_for_json(analysis_results), f, indent=2)

print("✓ Analysis results saved to: examples/bach_analysis.json")
print()

print("=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
print()
print("Key Findings:")
print(f"  • Bach uses {rhythm_stats['unique_durations']} different note durations")
print(f"  • {harmonic_stats['consonance_ratio']:.0%} of vertical intervals are consonant")
print(f"  • Average melodic interval: {interval_stats['average']:.1f} semitones")
print(f"  • Most common interval: {abs(interval_stats['most_common'][0][0])} semitones")
print()
