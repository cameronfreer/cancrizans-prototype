"""
Generate all missing PNG visualizations for examples.
"""

from pathlib import Path
from cancrizans.io import load_score
from cancrizans.viz import piano_roll, symmetry

def generate_missing_visualizations():
    """Generate all missing PNG files referenced in GALLERY.md"""
    examples_dir = Path('examples')

    # List of (midi_file, piano_roll_png, symmetry_png)
    visualizations = [
        ('01_scale_crab_canon.mid', '01_scale_piano_roll.png', '01_scale_symmetry.png'),
        ('02_arpeggio_crab_canon.mid', '02_arpeggio_piano_roll.png', '02_arpeggio_symmetry.png'),
        ('03_melody_crab_canon.mid', '03_melody_piano_roll.png', '03_melody_symmetry.png'),
        ('04_rhythm_crab_canon.mid', '04_rhythm_piano_roll.png', '04_rhythm_symmetry.png'),
        ('05_chromatic_crab_canon.mid', '05_chromatic_piano_roll.png', '05_chromatic_symmetry.png'),
        ('06_augmentation_canon.mid', '06_augmentation_piano_roll.png', '06_augmentation_symmetry.png'),
        ('07_diminution_canon.mid', '07_diminution_piano_roll.png', '07_diminution_symmetry.png'),
        ('08_mirror_canon.mid', '08_mirror_piano_roll.png', '08_mirror_symmetry.png'),
        ('09_crab_augmentation_canon.mid', '09_crab_augmentation_piano_roll.png', '09_crab_augmentation_symmetry.png'),
        ('10_triple_canon.mid', '10_triple_piano_roll.png', '10_triple_symmetry.png'),
    ]

    generated_count = 0

    for midi_file, piano_png, symmetry_png in visualizations:
        midi_path = examples_dir / midi_file

        if not midi_path.exists():
            print(f"⚠️  MIDI file not found: {midi_file}")
            continue

        # Load score
        try:
            score = load_score(midi_path)
        except Exception as e:
            print(f"⚠️  Could not load {midi_file}: {e}")
            continue

        # Generate piano roll if missing
        piano_path = examples_dir / piano_png
        if not piano_path.exists():
            try:
                piano_roll(score, piano_path)
                print(f"✓ Generated: {piano_png}")
                generated_count += 1
            except Exception as e:
                print(f"✗ Failed to generate {piano_png}: {e}")
        else:
            print(f"  Exists: {piano_png}")

        # Generate symmetry plot if missing
        sym_path = examples_dir / symmetry_png
        if not sym_path.exists():
            try:
                symmetry(score, sym_path)
                print(f"✓ Generated: {symmetry_png}")
                generated_count += 1
            except Exception as e:
                print(f"✗ Failed to generate {symmetry_png}: {e}")
        else:
            print(f"  Exists: {symmetry_png}")

    return generated_count


if __name__ == '__main__':
    print("=" * 60)
    print("Generating Missing Visualizations")
    print("=" * 60)
    print()

    count = generate_missing_visualizations()

    print()
    print("=" * 60)
    print(f"✓ Generated {count} new visualization(s)")
    print("=" * 60)
