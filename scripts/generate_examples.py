#!/usr/bin/env python3
"""
Generate Comprehensive Example Collection

Auto-generate a diverse collection of example canons.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cancrizans.generator import CanonGenerator
from cancrizans.validator import CanonValidator
from cancrizans.io import to_midi
from cancrizans.viz import piano_roll, symmetry


def generate_all_examples():
    """Generate complete example collection."""
    print("Generating comprehensive example collection...\n")

    output_dir = Path(__file__).parent.parent / 'examples' / 'generated'
    output_dir.mkdir(parents=True, exist_ok=True)

    generator = CanonGenerator(seed=42)
    validator = CanonValidator()

    examples = [
        # Scale canons
        ('11_c_major_scale', lambda: generator.generate_scale_canon('C', 'major', 4, 8)),
        ('12_d_minor_scale', lambda: generator.generate_scale_canon('D', 'minor', 4, 8)),
        ('13_g_major_scale', lambda: generator.generate_scale_canon('G', 'major', 3, 12)),
        ('14_a_minor_scale', lambda: generator.generate_scale_canon('A', 'minor', 3, 12)),

        # Arpeggio canons
        ('15_c_major_arp', lambda: generator.generate_arpeggio_canon('C4', 'major', 2)),
        ('16_a_minor_arp', lambda: generator.generate_arpeggio_canon('A3', 'minor', 2)),
        ('17_f_major_arp', lambda: generator.generate_arpeggio_canon('F4', 'major', 3)),
        ('18_e_minor_arp', lambda: generator.generate_arpeggio_canon('E3', 'minor', 3)),
        ('19_diminished_arp', lambda: generator.generate_arpeggio_canon('B3', 'diminished', 2)),
        ('20_augmented_arp', lambda: generator.generate_arpeggio_canon('C4', 'augmented', 2)),

        # Random walk canons
        ('21_random_walk_small', lambda: generator.generate_random_walk('C4', 12, 2)),
        ('22_random_walk_medium', lambda: generator.generate_random_walk('G4', 16, 3)),
        ('23_random_walk_large', lambda: generator.generate_random_walk('D4', 20, 4)),

        # Fibonacci canons
        ('24_fibonacci_short', lambda: generator.generate_fibonacci_canon('C4', 8)),
        ('25_fibonacci_long', lambda: generator.generate_fibonacci_canon('G4', 13)),

        # Modal canons
        ('26_dorian_canon', lambda: generator.generate_modal_canon('dorian', 'D4', 8)),
        ('27_phrygian_canon', lambda: generator.generate_modal_canon('phrygian', 'E4', 8)),
        ('28_lydian_canon', lambda: generator.generate_modal_canon('lydian', 'F4', 8)),
        ('29_mixolydian_canon', lambda: generator.generate_modal_canon('mixolydian', 'G4', 8)),
        ('30_aeolian_canon', lambda: generator.generate_modal_canon('aeolian', 'A4', 8)),
        ('31_locrian_canon', lambda: generator.generate_modal_canon('locrian', 'B3', 8)),

        # Golden ratio canons
        ('32_golden_ratio', lambda: generator.generate_golden_ratio_canon('D4', 13)),
        ('33_golden_ratio_alt', lambda: generator.generate_golden_ratio_canon('F#4', 13)),

        # Fractal canons
        ('34_fractal_simple', lambda: generator.generate_fractal_canon([1, 2], 2)),
        ('35_fractal_complex', lambda: generator.generate_fractal_canon([1, 2, -1], 2)),
        ('36_fractal_three', lambda: generator.generate_fractal_canon([1, -1, 2], 2)),

        # Polyrhythmic canons
        ('37_polyrhythm_3_2', lambda: generator.generate_polyrhythmic_canon(
            ['C4', 'E4', 'G4', 'C5', 'G4', 'E4'], (3, 2)
        )),
        ('38_polyrhythm_5_3', lambda: generator.generate_polyrhythmic_canon(
            ['D4', 'F#4', 'A4', 'D5', 'A4', 'F#4'], (5, 3)
        )),

        # Rhythmic canons
        ('39_rhythmic_varied', lambda: generator.generate_rhythmic_canon(
            ['C4', 'D4', 'E4', 'F4', 'G4'],
            [1.0, 0.5, 0.5, 1.5, 0.5]
        )),
        ('40_rhythmic_syncopated', lambda: generator.generate_rhythmic_canon(
            ['E4', 'G4', 'B4', 'E5'],
            [0.75, 0.25, 1.0, 0.5]
        )),
    ]

    total = len(examples)
    successful = 0
    failed = 0

    quality_scores = []

    for i, (name, gen_func) in enumerate(examples, 1):
        try:
            print(f"[{i}/{total}] Generating {name}...")

            # Generate canon
            canon = gen_func()

            # Validate
            validation = validator.validate(canon)
            quality = validation['overall_quality']
            grade = validator.get_quality_grade(quality)

            quality_scores.append((name, quality, grade))

            # Export MIDI
            midi_path = output_dir / f"{name}.mid"
            to_midi(canon, str(midi_path))

            # Generate visualizations
            try:
                piano_path = output_dir / f"{name}_piano_roll.png"
                piano_roll(canon, str(piano_path))

                sym_path = output_dir / f"{name}_symmetry.png"
                symmetry(canon, str(sym_path))

                print(f"  ✓ Generated (Quality: {quality:.2f}, Grade: {grade})")
                successful += 1

            except Exception as viz_err:
                print(f"  ⚠ Generated MIDI but visualization failed: {viz_err}")
                successful += 1

        except Exception as e:
            print(f"  ✗ Failed: {e}")
            failed += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"GENERATION SUMMARY")
    print(f"{'='*60}")
    print(f"Total: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Success rate: {(successful/total)*100:.1f}%")

    if quality_scores:
        print(f"\n{'='*60}")
        print(f"QUALITY REPORT")
        print(f"{'='*60}")

        avg_quality = sum(q for _, q, _ in quality_scores) / len(quality_scores)
        print(f"Average quality: {avg_quality:.3f}")

        # Grade distribution
        grade_counts = {}
        for _, _, grade in quality_scores:
            grade_counts[grade] = grade_counts.get(grade, 0) + 1

        print(f"\nGrade Distribution:")
        for grade in sorted(grade_counts.keys(), reverse=True):
            count = grade_counts[grade]
            bar = '█' * count
            print(f"  {grade}: {bar} ({count})")

        # Top 5 quality canons
        print(f"\nTop 5 Quality Canons:")
        top_5 = sorted(quality_scores, key=lambda x: x[1], reverse=True)[:5]
        for i, (name, quality, grade) in enumerate(top_5, 1):
            print(f"  {i}. {name}: {quality:.3f} ({grade})")

    print(f"\n✓ Examples saved to: {output_dir}")


def main():
    """Generate examples."""
    generate_all_examples()


if __name__ == '__main__':
    main()
