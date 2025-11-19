"""
Microtonal Examples - Practical Usage Demonstrations

This script demonstrates the comprehensive microtonal features of Cancrizans,
including scale generation, canon composition, visualization, and file I/O.

Run this script to see the microtonal capabilities in action.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from cancrizans import CanonGenerator
from cancrizans.microtonal import (
    create_tuning_system_scale,
    create_world_music_scale,
    TuningSystem,
    ScaleType
)
from cancrizans.microtonal_utils import (
    recommend_scale_for_style,
    blend_scales,
    find_modulation_path,
    calculate_scale_tension,
    create_scale_catalog,
    analyze_scale_family,
    calculate_scale_compatibility,
    export_scala_file,
    import_scala_file
)
from cancrizans.viz import visualize_microtonal_scale, compare_microtonal_scales
from cancrizans.io import to_midi, to_musicxml


def example_1_baroque_canon():
    """Example 1: Generate a baroque canon in Werckmeister III tuning"""
    print("\n" + "="*70)
    print("Example 1: Baroque Canon in Werckmeister III")
    print("="*70)

    # Create generator
    gen = CanonGenerator(seed=42)

    # Generate baroque canon using style-based recommendation
    print("Generating baroque canon...")
    canon = gen.generate_microtonal_canon('baroque', 'D4', 16)

    # Export to MIDI
    output_dir = Path("output/microtonal_examples")
    output_dir.mkdir(parents=True, exist_ok=True)

    midi_path = output_dir / "baroque_werckmeister.mid"
    to_midi(canon, midi_path)
    print(f"✓ Saved MIDI: {midi_path}")

    # Get and visualize the scale
    scale = create_tuning_system_scale(TuningSystem.WERCKMEISTER_III, 60)
    viz_path = output_dir / "werckmeister_scale.png"
    visualize_microtonal_scale(scale, viz_path, dpi=150)
    print(f"✓ Saved visualization: {viz_path}")

    # Analyze the scale
    tension = calculate_scale_tension(scale)
    family = analyze_scale_family(scale)
    print(f"\nScale Analysis:")
    print(f"  Name: {scale.name}")
    print(f"  Degrees: {len(scale.intervals_cents)}")
    print(f"  Tension: {tension:.3f} (Low/consonant)")
    print(f"  Family: {family['possible_families']}")


def example_2_arabic_maqam():
    """Example 2: Generate an Arabic maqam canon"""
    print("\n" + "="*70)
    print("Example 2: Arabic Maqam Canon")
    print("="*70)

    # Get recommendations for Arabic style
    print("Getting scale recommendations for 'arabic' style...")
    recommendations = recommend_scale_for_style('arabic')

    print(f"Top 3 recommendations:")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"  {i}. {rec.world_scale_type} - {rec.confidence:.0%} confidence")
        print(f"     Reason: {rec.reason}")

    # Generate canon with top recommendation
    gen = CanonGenerator(seed=42)
    canon = gen.generate_microtonal_canon('arabic', 'E4', 12)

    output_dir = Path("output/microtonal_examples")
    midi_path = output_dir / "arabic_maqam.mid"
    to_midi(canon, midi_path)
    print(f"\n✓ Saved MIDI: {midi_path}")

    # Create and visualize the scale
    scale = create_world_music_scale(ScaleType.MAQAM_RAST, 60)
    viz_path = output_dir / "maqam_rast_scale.png"
    visualize_microtonal_scale(scale, viz_path, dpi=150)
    print(f"✓ Saved visualization: {viz_path}")


def example_3_scale_blending():
    """Example 3: Blend two scales to create a hybrid"""
    print("\n" + "="*70)
    print("Example 3: Scale Blending")
    print("="*70)

    # Create two different scales
    scale1 = create_tuning_system_scale(TuningSystem.WERCKMEISTER_III, 60)
    scale2 = create_tuning_system_scale(TuningSystem.MEANTONE, 60)

    print(f"Blending {scale1.name} with {scale2.name}...")

    # Create blends at different weights
    blend_25 = blend_scales(scale1, scale2, weight=0.25)
    blend_50 = blend_scales(scale1, scale2, weight=0.50)
    blend_75 = blend_scales(scale1, scale2, weight=0.75)

    print(f"✓ Created 3 hybrid scales")

    # Visualize comparison
    output_dir = Path("output/microtonal_examples")
    scales = [scale1, blend_25, blend_50, blend_75, scale2]

    viz_path = output_dir / "scale_blending_comparison.png"
    compare_microtonal_scales(scales, viz_path, dpi=150)
    print(f"✓ Saved comparison: {viz_path}")

    # Analyze compatibility
    compat = calculate_scale_compatibility(scale1, scale2)
    print(f"\nCompatibility between original scales: {compat:.2f}")


def example_4_modulation_canon():
    """Example 4: Create a canon that modulates between scales"""
    print("\n" + "="*70)
    print("Example 4: Modulating Canon")
    print("="*70)

    # Create source and target scales
    source = create_tuning_system_scale(TuningSystem.EQUAL_12, 60)
    target = create_tuning_system_scale(TuningSystem.EQUAL_19, 60)

    print(f"Finding modulation path from {source.name} to {target.name}...")

    # Find modulation path
    path = find_modulation_path(source, target, max_steps=4)
    print(f"✓ Created modulation path with {len(path)} steps")

    # Generate canon with modulation
    gen = CanonGenerator(seed=42)
    canon = gen.generate_microtonal_canon('experimental', 'C4', 32, modulation=True)

    output_dir = Path("output/microtonal_examples")
    midi_path = output_dir / "modulating_canon.mid"
    to_midi(canon, midi_path)
    print(f"✓ Saved MIDI: {midi_path}")

    # Visualize the modulation path
    viz_path = output_dir / "modulation_path.png"
    compare_microtonal_scales(path, viz_path, dpi=150)
    print(f"✓ Saved modulation path visualization: {viz_path}")


def example_5_world_music_comparison():
    """Example 5: Compare scales from different musical traditions"""
    print("\n" + "="*70)
    print("Example 5: World Music Scale Comparison")
    print("="*70)

    # Create scales from different traditions
    scales = [
        create_world_music_scale(ScaleType.MAQAM_HIJAZ, 60),  # Arabic
        create_world_music_scale(ScaleType.RAGA_BHAIRAV, 60),  # Indian
        create_world_music_scale(ScaleType.PELOG, 60),  # Indonesian
        create_world_music_scale(ScaleType.HIRAJOSHI, 60),  # Japanese
    ]

    print("Comparing 4 world music scales:")
    for scale in scales:
        tension = calculate_scale_tension(scale)
        family = analyze_scale_family(scale)
        print(f"\n  {scale.name}")
        print(f"    Degrees: {len(scale.intervals_cents)}")
        print(f"    Tension: {tension:.3f}")
        print(f"    Characteristics: {', '.join(family['characteristics'])}")

    # Visualize comparison
    output_dir = Path("output/microtonal_examples")
    viz_path = output_dir / "world_music_comparison.png"
    compare_microtonal_scales(scales, viz_path, dpi=150)
    print(f"\n✓ Saved comparison: {viz_path}")


def example_6_scala_file_workflow():
    """Example 6: Import/Export Scala files"""
    print("\n" + "="*70)
    print("Example 6: Scala File Format Workflow")
    print("="*70)

    output_dir = Path("output/microtonal_examples")

    # Export several scales to Scala format
    scales_to_export = [
        (TuningSystem.WERCKMEISTER_III, "Werckmeister III - Well temperament"),
        (TuningSystem.EQUAL_19, "19-TET - Equal temperament with 19 divisions"),
        (TuningSystem.BOHLEN_PIERCE, "Bohlen-Pierce - Non-octave scale"),
    ]

    print("Exporting scales to Scala format...")
    exported_files = []
    for tuning, description in scales_to_export:
        scale = create_tuning_system_scale(tuning, 60)
        filename = scale.name.lower().replace(' ', '_').replace('-', '_') + '.scl'
        scl_path = output_dir / filename
        export_scala_file(scale, scl_path, description=description)
        exported_files.append(scl_path)
        print(f"  ✓ {scl_path.name}")

    # Import one back and verify
    print("\nRe-importing first scale to verify roundtrip...")
    imported_scale = import_scala_file(exported_files[0], tonic_midi=60)
    print(f"  ✓ Imported: {imported_scale.name}")
    print(f"  ✓ Degrees: {len(imported_scale.intervals_cents)}")


def example_7_comprehensive_catalog():
    """Example 7: Browse the complete scale catalog"""
    print("\n" + "="*70)
    print("Example 7: Complete Scale Catalog")
    print("="*70)

    catalog = create_scale_catalog()

    print(f"Total categories: {len(catalog)}")
    print(f"Total scales: {sum(len(scales) for scales in catalog.values())}")

    print("\nCatalog breakdown:")
    for category, scales in catalog.items():
        print(f"\n  {category} ({len(scales)} scales)")
        # Show first 3 scales in each category
        for scale_name in scales[:3]:
            print(f"    • {scale_name}")
        if len(scales) > 3:
            print(f"    ... and {len(scales) - 3} more")


def example_8_style_specific_canons():
    """Example 8: Generate canons for different musical styles"""
    print("\n" + "="*70)
    print("Example 8: Style-Specific Canon Generation")
    print("="*70)

    styles = [
        ('baroque', 'D4', 16),
        ('indian', 'C4', 14),
        ('gamelan', 'G4', 10),
        ('experimental', 'A4', 18),
    ]

    gen = CanonGenerator(seed=42)
    output_dir = Path("output/microtonal_examples")

    print("Generating canons for different styles...")
    for style, root, length in styles:
        print(f"\n  {style.capitalize()} style:")

        # Get recommendation
        recs = recommend_scale_for_style(style)
        print(f"    Scale: {recs[0].scale_type}")

        # Generate canon
        canon = gen.generate_microtonal_canon(style, root, length)

        # Export
        midi_path = output_dir / f"canon_{style}.mid"
        to_midi(canon, midi_path)
        print(f"    ✓ Saved: {midi_path.name}")


def run_all_examples():
    """Run all examples"""
    print("\n" + "="*70)
    print("MICROTONAL FEATURES - COMPREHENSIVE EXAMPLES")
    print("="*70)
    print("\nThis script demonstrates the microtonal capabilities of Cancrizans.")
    print("All outputs will be saved to: output/microtonal_examples/")

    try:
        example_1_baroque_canon()
        example_2_arabic_maqam()
        example_3_scale_blending()
        example_4_modulation_canon()
        example_5_world_music_comparison()
        example_6_scala_file_workflow()
        example_7_comprehensive_catalog()
        example_8_style_specific_canons()

        print("\n" + "="*70)
        print("All examples completed successfully!")
        print("="*70)
        print("\nGenerated files:")
        output_dir = Path("output/microtonal_examples")
        if output_dir.exists():
            for file in sorted(output_dir.iterdir()):
                print(f"  • {file.name}")

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(run_all_examples())
