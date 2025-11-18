"""
Command-line interface for the cancrizans package.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from cancrizans.bach_crab import load_bach_crab_canon, assemble_crab_from_theme, save_crab_canon_xml
from cancrizans.canon import is_time_palindrome, pairwise_symmetry_map, retrograde
from cancrizans.io import to_midi, to_musicxml, to_wav_via_sf2, load_score
from cancrizans.viz import piano_roll, symmetry
from cancrizans.research import analyze_corpus, BatchAnalyzer, ResearchExporter
from cancrizans.microtonal import (
    TuningSystem, ScaleType, create_equal_temperament, create_just_intonation_scale,
    create_pythagorean_scale, create_world_music_scale, create_meantone_scale,
    create_werckmeister_iii, bohlen_pierce_scale, gamma_scale, alpha_scale, beta_scale,
    export_scala_file, import_scala_file, compare_scales
)


def analyze_command(args: argparse.Namespace) -> int:
    """Execute the analyze subcommand."""
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        return 1

    print(f"Analyzing: {input_path}")
    print("-" * 60)

    # Load the score
    score = load_score(input_path)

    # Get parts
    parts = list(score.parts)
    print(f"Number of voices: {len(parts)}")

    # Calculate statistics
    total_duration = score.highestTime
    print(f"Total duration: {total_duration:.2f} quarter notes")

    for i, part in enumerate(parts, 1):
        notes = list(part.flatten().notesAndRests)
        note_count = sum(1 for n in notes if not n.isRest)
        rest_count = sum(1 for n in notes if n.isRest)
        print(f"  Voice {i}: {note_count} notes, {rest_count} rests")

    print()
    print("Palindrome Verification:")
    print("-" * 60)

    # Check if it's a time palindrome
    is_palindrome = is_time_palindrome(score)
    print(f"is_time_palindrome: {is_palindrome}")

    if is_palindrome:
        print("✓ This score is a valid crab canon (retrograde canon)")
    else:
        print("✗ This score is NOT a crab canon")

    # Count symmetric pairs
    if len(parts) >= 1:
        pairs = pairwise_symmetry_map(parts[0])
        total_events = len(list(parts[0].flatten().notesAndRests))
        print(f"Symmetric pairs in voice 1: {len(pairs)}")
        print(f"Total events in voice 1: {total_events}")

        if len(pairs) * 2 >= total_events:
            print("✓ All events participate in symmetric pairs")

    # Calculate structural checksum
    print()
    print("Structural Checksum:")
    print("-" * 60)

    pitch_histogram = {}
    total_intervals = []

    for part in parts:
        prev_pitch = None
        for el in part.flatten().notesAndRests:
            if el.isRest:
                continue

            if hasattr(el, 'pitch'):
                pitch = el.pitch.midi
                pitch_histogram[pitch] = pitch_histogram.get(pitch, 0) + 1

                if prev_pitch is not None:
                    interval = abs(pitch - prev_pitch)
                    total_intervals.append(interval)

                prev_pitch = pitch

    print(f"Unique pitches: {len(pitch_histogram)}")
    print(f"Total intervals: {len(total_intervals)}")
    print(f"Average interval: {sum(total_intervals) / len(total_intervals):.2f} semitones"
          if total_intervals else "N/A")

    return 0


def render_command(args: argparse.Namespace) -> int:
    """Execute the render subcommand."""
    input_path = Path(args.input) if args.input else None

    # Load or create the score
    if input_path and input_path.exists():
        print(f"Loading score from: {input_path}")
        score = load_score(input_path)
    else:
        print("Loading Bach Crab Canon...")
        score = load_bach_crab_canon()

    print("Rendering outputs...")
    print("-" * 60)

    # Export MIDI
    if args.midi:
        midi_path = to_midi(score, args.midi)
        print(f"✓ MIDI exported to: {midi_path}")

    # Export MusicXML
    if args.xml:
        xml_path = to_musicxml(score, args.xml)
        print(f"✓ MusicXML exported to: {xml_path}")

    # Export WAV (optional)
    if args.wav:
        if not args.midi:
            print("Error: WAV export requires MIDI file. Use --midi option first.")
            return 1

        if not args.soundfont:
            print("Error: WAV export requires a SoundFont file. Use --soundfont option.")
            return 1

        sf2_path = Path(args.soundfont)
        if not sf2_path.exists():
            print(f"Error: SoundFont file not found: {sf2_path}")
            return 1

        wav_path = to_wav_via_sf2(args.midi, sf2_path, args.wav)
        if wav_path:
            print(f"✓ WAV exported to: {wav_path}")
        else:
            print("✗ WAV export failed (see message above)")

    # Generate piano roll
    if args.roll:
        roll_path = piano_roll(score, args.roll)
        print(f"✓ Piano roll saved to: {roll_path}")

    # Generate symmetry plot
    if args.mirror:
        mirror_path = symmetry(score, args.mirror)
        print(f"✓ Symmetry plot saved to: {mirror_path}")

    return 0


def synthesize_command(args: argparse.Namespace) -> int:
    """Execute the synthesize subcommand."""
    print("Synthesizing crab canon from theme...")
    print("-" * 60)

    # Load the canonical Bach theme
    bach_score = load_bach_crab_canon()
    parts = list(bach_score.parts)

    if not parts:
        print("Error: Could not load Bach theme")
        return 1

    # Use the first part as the theme
    theme = parts[0]

    # Apply transposition if requested
    if args.transpose != 0:
        print(f"Transposing by {args.transpose} semitones...")
        theme = theme.transpose(args.transpose)

    # Assemble the crab canon
    print("Assembling crab canon (forward + retrograde)...")
    crab_canon = assemble_crab_from_theme(theme, offset_quarters=0.0)

    # Verify it's a palindrome
    is_palindrome = is_time_palindrome(crab_canon)
    print(f"Palindrome verification: {is_palindrome}")

    if is_palindrome:
        print("✓ Successfully created a valid crab canon")
    else:
        print("✗ Warning: Generated canon may not be a perfect palindrome")

    # Set tempo if specified
    if args.tempo:
        import music21 as m21
        crab_canon.insert(0, m21.tempo.MetronomeMark(number=args.tempo))
        print(f"Tempo set to: {args.tempo} BPM")

    # Export the synthesized canon
    output_dir = Path(args.output) if args.output else Path("out")
    output_dir.mkdir(exist_ok=True)

    midi_path = to_midi(crab_canon, output_dir / "synthesized_crab.mid")
    print(f"✓ Synthesized MIDI: {midi_path}")

    xml_path = to_musicxml(crab_canon, output_dir / "synthesized_crab.musicxml")
    print(f"✓ Synthesized MusicXML: {xml_path}")

    return 0


def research_command(args: argparse.Namespace) -> int:
    """Execute the research subcommand (batch analysis)."""
    input_dir = Path(args.directory)

    if not input_dir.exists() or not input_dir.is_dir():
        print(f"Error: Directory not found: {input_dir}")
        return 1

    print(f"Analyzing corpus in: {input_dir}")
    print(f"File pattern: {args.pattern}")
    print("-" * 60)

    # Analyze all files in the directory
    analyses, comparison = analyze_corpus(input_dir, args.pattern)

    if not analyses:
        print("No files found matching the pattern.")
        return 1

    print(f"✓ Analyzed {len(analyses)} canon(s)")
    print()

    # Display summary statistics
    print("Comparative Statistics:")
    print("-" * 60)
    print(f"Total canons: {comparison['total_canons']}")
    print(f"Valid palindromes: {comparison['palindrome_count']} ({comparison['palindrome_count']/comparison['total_canons']*100:.1f}%)")
    print(f"Average duration: {comparison['average_duration']:.1f} quarters")
    print(f"Consonance ratio: {comparison['consonance_stats']['mean']:.1%} (min: {comparison['consonance_stats']['min']:.1%}, max: {comparison['consonance_stats']['max']:.1%})")
    print(f"Average interval size: {comparison['interval_stats']['avg_size']:.2f} semitones")
    print()

    # Export results
    output_dir = Path(args.output) if args.output else Path("research_output")
    output_dir.mkdir(exist_ok=True)

    if args.csv:
        csv_path = output_dir / "analysis.csv"
        ResearchExporter.to_csv(analyses, csv_path)
        print(f"✓ CSV exported to: {csv_path}")

    if args.json:
        json_path = output_dir / "analysis.json"
        ResearchExporter.to_json(analyses, json_path)
        print(f"✓ JSON exported to: {json_path}")

    if args.latex:
        latex_path = output_dir / "analysis.tex"
        ResearchExporter.to_latex_table(analyses, latex_path)
        print(f"✓ LaTeX table exported to: {latex_path}")

    if args.markdown:
        md_path = output_dir / "analysis.md"
        ResearchExporter.to_markdown_table(analyses, md_path)
        print(f"✓ Markdown table exported to: {md_path}")

    # Export all formats if --all is specified
    if args.all:
        ResearchExporter.to_csv(analyses, output_dir / "analysis.csv")
        ResearchExporter.to_json(analyses, output_dir / "analysis.json")
        ResearchExporter.to_latex_table(analyses, output_dir / "analysis.tex")
        ResearchExporter.to_markdown_table(analyses, output_dir / "analysis.md")
        print(f"✓ All formats exported to: {output_dir}")

    return 0


def scales_command(args: argparse.Namespace) -> int:
    """Execute the scales subcommand."""

    if args.list_tunings:
        print("Available Tuning Systems:")
        print("=" * 60)
        for tuning in TuningSystem:
            print(f"  {tuning.name:30s} - {tuning.value}")
        return 0

    if args.list_scales:
        region = args.region.lower() if args.region else None

        print("Available World Music Scales:")
        print("=" * 60)

        # Group by region
        regions = {
            'arabic': [],
            'turkish': [],
            'persian': [],
            'indian': [],
            'indonesian': [],
            'japanese': [],
            'chinese': [],
            'thai': [],
            'african': [],
            'latin': [],
        }

        for scale_type in ScaleType:
            value_lower = scale_type.value.lower()
            if 'arabic' in value_lower:
                regions['arabic'].append(scale_type)
            elif 'turkish' in value_lower:
                regions['turkish'].append(scale_type)
            elif 'persian' in value_lower:
                regions['persian'].append(scale_type)
            elif 'hindustani' in value_lower or 'raga' in value_lower:
                regions['indian'].append(scale_type)
            elif 'javanese' in value_lower or 'pelog' in value_lower or 'slendro' in value_lower:
                regions['indonesian'].append(scale_type)
            elif 'japanese' in value_lower:
                regions['japanese'].append(scale_type)
            elif 'chinese' in value_lower:
                regions['chinese'].append(scale_type)
            elif 'thai' in value_lower:
                regions['thai'].append(scale_type)
            elif 'african' in value_lower or 'ethiopian' in value_lower:
                regions['african'].append(scale_type)
            elif 'escala' in value_lower or 'samba' in value_lower or 'brazilian' in value_lower:
                regions['latin'].append(scale_type)

        for region_name, scales in regions.items():
            if region and region != region_name:
                continue
            if scales:
                print(f"\n{region_name.capitalize()}:")
                for scale in scales:
                    print(f"  {scale.name:30s} - {scale.value}")

        return 0

    if args.export:
        # Create and export a scale
        if not args.scale_type and not args.tuning:
            print("Error: Must specify --scale-type or --tuning to export")
            return 1

        scale = None

        if args.tuning:
            tuning = args.tuning.upper()
            try:
                if tuning == 'PYTHAGOREAN':
                    scale = create_pythagorean_scale()
                elif tuning == 'MEANTONE':
                    scale = create_meantone_scale()
                elif tuning == 'WERCKMEISTER_III':
                    scale = create_werckmeister_iii()
                elif tuning == 'BOHLEN_PIERCE':
                    scale = bohlen_pierce_scale()
                elif tuning == 'ALPHA':
                    scale = alpha_scale()
                elif tuning == 'BETA':
                    scale = beta_scale()
                elif tuning == 'GAMMA':
                    scale = gamma_scale()
                elif tuning.startswith('EQUAL_'):
                    divisions = int(tuning.split('_')[1])
                    scale = create_equal_temperament(divisions)
                else:
                    print(f"Error: Unknown tuning system: {tuning}")
                    return 1
            except Exception as e:
                print(f"Error creating scale: {e}")
                return 1

        elif args.scale_type:
            try:
                scale_enum = ScaleType[args.scale_type.upper()]
                scale = create_world_music_scale(scale_enum)
            except KeyError:
                print(f"Error: Unknown scale type: {args.scale_type}")
                print("Use --list-scales to see available scales")
                return 1
            except Exception as e:
                print(f"Error creating scale: {e}")
                return 1

        if scale:
            output_path = Path(args.export)
            export_scala_file(scale, str(output_path))
            print(f"✓ Exported {scale.name} to: {output_path}")
            print(f"  Scale degrees: {len(scale.intervals_cents)}")
            print(f"  Intervals (cents): {', '.join(f'{c:.2f}' for c in scale.intervals_cents[:8])}" +
                  ("..." if len(scale.intervals_cents) > 8 else ""))

        return 0

    if args.info:
        # Show info about a tuning or scale
        if args.tuning:
            tuning_name = args.tuning.upper()
            try:
                tuning = TuningSystem[tuning_name]
                print(f"Tuning System: {tuning.value}")
                print("=" * 60)

                # Create and display the scale
                if tuning_name == 'PYTHAGOREAN':
                    scale = create_pythagorean_scale()
                elif tuning_name == 'MEANTONE':
                    scale = create_meantone_scale()
                elif tuning_name == 'WERCKMEISTER_III':
                    scale = create_werckmeister_iii()
                elif tuning_name == 'BOHLEN_PIERCE':
                    scale = bohlen_pierce_scale()
                elif tuning_name == 'ALPHA':
                    scale = alpha_scale()
                elif tuning_name == 'BETA':
                    scale = beta_scale()
                elif tuning_name == 'GAMMA':
                    scale = gamma_scale()
                else:
                    print(f"Info not available for {tuning.value}")
                    return 0

                print(f"Degrees: {len(scale.intervals_cents)}")
                print(f"\nIntervals (in cents from tonic):")
                for i, cents in enumerate(scale.intervals_cents):
                    print(f"  {i:2d}: {cents:8.3f} cents")

            except KeyError:
                print(f"Error: Unknown tuning: {tuning_name}")
                print("Use --list-tunings to see available tuning systems")
                return 1

        elif args.scale_type:
            try:
                scale_enum = ScaleType[args.scale_type.upper()]
                scale = create_world_music_scale(scale_enum)

                print(f"Scale: {scale.name}")
                print("=" * 60)
                print(f"Degrees: {len(scale.intervals_cents)}")
                print(f"\nIntervals (in cents from tonic):")
                for i, cents in enumerate(scale.intervals_cents):
                    print(f"  {i:2d}: {cents:8.3f} cents")

            except KeyError:
                print(f"Error: Unknown scale type: {args.scale_type}")
                print("Use --list-scales to see available scales")
                return 1

        else:
            print("Error: Must specify --tuning or --scale-type with --info")
            return 1

        return 0

    # Default: show help
    print("Use --list-tunings, --list-scales, --info, or --export")
    return 1


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="cancrizans",
        description="Explore and render J.S. Bach's Crab Canon as a strict palindrome"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a musical score for palindromic structure"
    )
    analyze_parser.add_argument(
        "input",
        help="Path to MusicXML or MIDI file to analyze"
    )

    # Render command
    render_parser = subparsers.add_parser(
        "render",
        help="Render a score to various output formats"
    )
    render_parser.add_argument(
        "--input",
        help="Path to input file (defaults to Bach Crab Canon)"
    )
    render_parser.add_argument(
        "--midi",
        help="Output path for MIDI file"
    )
    render_parser.add_argument(
        "--xml",
        help="Output path for MusicXML file"
    )
    render_parser.add_argument(
        "--wav",
        help="Output path for WAV file (requires --soundfont)"
    )
    render_parser.add_argument(
        "--soundfont",
        help="Path to SoundFont (.sf2) file for WAV rendering"
    )
    render_parser.add_argument(
        "--roll",
        help="Output path for piano roll PNG"
    )
    render_parser.add_argument(
        "--mirror",
        help="Output path for symmetry/mirror plot PNG"
    )

    # Synthesize command
    synthesize_parser = subparsers.add_parser(
        "synthesize",
        help="Synthesize a crab canon from a theme"
    )
    synthesize_parser.add_argument(
        "--tempo",
        type=int,
        default=84,
        help="Tempo in BPM (default: 84)"
    )
    synthesize_parser.add_argument(
        "--transpose",
        type=int,
        default=0,
        help="Transpose by semitones (default: 0)"
    )
    synthesize_parser.add_argument(
        "--output",
        default="out",
        help="Output directory (default: out)"
    )

    # Research command
    research_parser = subparsers.add_parser(
        "research",
        help="Batch analyze multiple canons for research"
    )
    research_parser.add_argument(
        "directory",
        help="Directory containing MIDI/MusicXML files"
    )
    research_parser.add_argument(
        "--pattern",
        default="*.mid",
        help="File pattern to match (default: *.mid)"
    )
    research_parser.add_argument(
        "--output",
        help="Output directory (default: research_output)"
    )
    research_parser.add_argument(
        "--csv",
        action="store_true",
        help="Export to CSV format"
    )
    research_parser.add_argument(
        "--json",
        action="store_true",
        help="Export to JSON format"
    )
    research_parser.add_argument(
        "--latex",
        action="store_true",
        help="Export to LaTeX table format"
    )
    research_parser.add_argument(
        "--markdown",
        action="store_true",
        help="Export to Markdown table format"
    )
    research_parser.add_argument(
        "--all",
        action="store_true",
        help="Export to all formats"
    )

    # Generate command
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate algorithmic canons"
    )
    generate_parser.add_argument(
        "algorithm",
        choices=['scale', 'arpeggio', 'random', 'fibonacci', 'modal', 'golden'],
        help="Generation algorithm"
    )
    generate_parser.add_argument(
        "--output", "-o",
        help="Output MIDI file path"
    )
    generate_parser.add_argument(
        "--key", default="C",
        help="Key for scale/arpeggio (default: C)"
    )
    generate_parser.add_argument(
        "--root", default="C4",
        help="Root note (default: C4)"
    )
    generate_parser.add_argument(
        "--mode", default="major",
        help="Mode: major, minor, dorian, etc."
    )
    generate_parser.add_argument(
        "--length", "-l", type=int, default=8,
        help="Number of notes (default: 8)"
    )
    generate_parser.add_argument(
        "--seed", type=int,
        help="Random seed for reproducibility"
    )
    generate_parser.add_argument(
        "--validate", action="store_true",
        help="Validate generated canon"
    )
    generate_parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Verbose output"
    )

    # Validate command
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate canon quality"
    )
    validate_parser.add_argument(
        "input",
        help="Path to MIDI/MusicXML file to validate"
    )
    validate_parser.add_argument(
        "--output", "-o",
        help="Output JSON file for validation results"
    )
    validate_parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Show detailed recommendations"
    )

    # Scales command
    scales_parser = subparsers.add_parser(
        "scales",
        help="Explore microtonal scales and tuning systems"
    )
    scales_parser.add_argument(
        "--list-tunings", action="store_true",
        help="List all available tuning systems"
    )
    scales_parser.add_argument(
        "--list-scales", action="store_true",
        help="List all available world music scales"
    )
    scales_parser.add_argument(
        "--region",
        help="Filter scales by region (arabic, turkish, persian, indian, etc.)"
    )
    scales_parser.add_argument(
        "--info", action="store_true",
        help="Show detailed information about a scale or tuning"
    )
    scales_parser.add_argument(
        "--tuning",
        help="Tuning system name (e.g., PYTHAGOREAN, MEANTONE, WERCKMEISTER_III, EQUAL_19)"
    )
    scales_parser.add_argument(
        "--scale-type",
        help="World music scale type (e.g., MAQAM_RAST, RAGA_BHAIRAV, PELOG)"
    )
    scales_parser.add_argument(
        "--export",
        help="Export scale to Scala (.scl) file format"
    )

    # Microtonal canon subcommand
    microtonal_parser = subparsers.add_parser(
        "microtonal-canon",
        help="Create or analyze microtonal canons"
    )
    microtonal_parser.add_argument(
        "--input", "-i",
        help="Input MusicXML/MIDI file (theme for canon generation)"
    )
    microtonal_parser.add_argument(
        "--world-scale",
        help="Generate canon using world music scale (e.g., MAQAM_HIJAZ, RAGA_BHAIRAV, PELOG)"
    )
    microtonal_parser.add_argument(
        "--tuning",
        default="JUST_INTONATION_5",
        help="Tuning system (default: JUST_INTONATION_5)"
    )
    microtonal_parser.add_argument(
        "--canon-type",
        default="retrograde",
        choices=['retrograde', 'inversion', 'augmentation', 'stretto'],
        help="Type of canon transformation (default: retrograde)"
    )
    microtonal_parser.add_argument(
        "--tonic",
        type=int,
        default=60,
        help="MIDI note for tonic (default: 60 = C4)"
    )
    microtonal_parser.add_argument(
        "--length",
        type=int,
        default=16,
        help="Number of notes for generated melody (default: 16)"
    )
    microtonal_parser.add_argument(
        "--octave-range",
        type=int,
        default=2,
        help="Octave range for melody generation (default: 2)"
    )
    microtonal_parser.add_argument(
        "--no-pitch-bend",
        action="store_true",
        help="Disable pitch bend MIDI data"
    )
    microtonal_parser.add_argument(
        "--analyze",
        action="store_true",
        help="Analyze existing canon for cross-cultural compatibility"
    )
    microtonal_parser.add_argument(
        "--output", "-o",
        help="Output file for analysis results (JSON)"
    )
    microtonal_parser.add_argument(
        "--output-dir",
        help="Output directory for generated files (default: out/)"
    )

    # Pattern analysis command
    pattern_parser = subparsers.add_parser(
        "analyze-patterns",
        help="Analyze musical patterns (motifs, sequences, imitation)"
    )
    pattern_parser.add_argument(
        "input",
        help="Path to MIDI/MusicXML file to analyze"
    )
    pattern_parser.add_argument(
        "--output", "-o",
        help="Output JSON file for analysis results"
    )
    pattern_parser.add_argument(
        "--min-length",
        type=int,
        default=3,
        help="Minimum motif length (default: 3)"
    )
    pattern_parser.add_argument(
        "--min-occurrences",
        type=int,
        default=2,
        help="Minimum motif occurrences (default: 2)"
    )
    pattern_parser.add_argument(
        "--detect-fugue",
        action="store_true",
        help="Analyze fugue structure (subject, answer, episodes)"
    )
    pattern_parser.add_argument(
        "--voice-independence",
        action="store_true",
        help="Calculate voice independence metrics"
    )
    pattern_parser.add_argument(
        "--complexity",
        action="store_true",
        help="Calculate pattern complexity"
    )
    pattern_parser.add_argument(
        "--sequences",
        action="store_true",
        help="Identify melodic sequences"
    )
    pattern_parser.add_argument(
        "--imitation",
        action="store_true",
        help="Detect imitation points between voices"
    )
    pattern_parser.add_argument(
        "--all",
        action="store_true",
        help="Run all pattern analysis functions"
    )
    pattern_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output with details"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == "analyze":
            return analyze_command(args)
        elif args.command == "render":
            return render_command(args)
        elif args.command == "synthesize":
            return synthesize_command(args)
        elif args.command == "research":
            return research_command(args)
        elif args.command == "generate":
            return generate_command(args)
        elif args.command == "validate":
            return validate_command(args)
        elif args.command == "scales":
            return scales_command(args)
        elif args.command == "microtonal-canon":
            return microtonal_canon_command(args)
        elif args.command == "analyze-patterns":
            return analyze_patterns_command(args)
        else:
            print(f"Unknown command: {args.command}")
            return 1

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def analyze_patterns_command(args: argparse.Namespace) -> int:
    """Execute the analyze-patterns subcommand."""
    import json
    from cancrizans import (
        detect_motifs,
        identify_melodic_sequences,
        detect_imitation_points,
        analyze_thematic_development,
        find_contour_similarities,
        analyze_fugue_structure,
        calculate_voice_independence,
        calculate_pattern_complexity
    )

    input_path = Path(args.input)

    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        return 1

    print(f"Analyzing patterns in: {input_path}")
    print("=" * 70)

    # Load the score
    score = load_score(input_path)

    results = {
        'file': str(input_path),
        'parts': len(score.parts) if hasattr(score, 'parts') else 1
    }

    # Detect motifs (always run unless only specific analyses requested)
    run_all = args.all or not any([
        args.detect_fugue, args.voice_independence,
        args.complexity, args.sequences, args.imitation
    ])

    if run_all or True:  # Always detect motifs
        print("\n🎵 Detecting Motifs...")
        print("-" * 70)
        motif_result = detect_motifs(
            score,
            min_length=args.min_length,
            min_occurrences=args.min_occurrences
        )

        motifs_list = motif_result['motifs']
        print(f"Found {len(motifs_list)} recurring motifs")

        if motifs_list and args.verbose:
            for i, motif in enumerate(motifs_list[:5], 1):
                print(f"\n  Motif {i}:")
                print(f"    Intervals: {motif['intervals']}")
                print(f"    Rhythms: {motif['rhythms']}")
                print(f"    Occurrences: {motif['num_occurrences']} times")
                print(f"    Positions: {[occ['offset'] for occ in motif['occurrences'][:5]]}")

        results['motifs'] = {
            'count': len(motifs_list),
            'details': motifs_list[:10]  # Top 10 motifs
        }

    # Melodic sequences
    if run_all or args.sequences:
        print("\n📈 Identifying Melodic Sequences...")
        print("-" * 70)
        seq_result = identify_melodic_sequences(score)

        sequences_list = seq_result['sequences']
        print(f"Found {len(sequences_list)} sequential patterns")

        if sequences_list and args.verbose:
            for i, seq in enumerate(sequences_list[:3], 1):
                print(f"\n  Sequence {i}:")
                print(f"    Type: {seq['type']}")
                print(f"    Transpositions: {seq['transpositions']}")
                print(f"    Repetitions: {seq['num_repetitions']}")
                print(f"    Segment length: {seq['segment_length']}")

        results['sequences'] = {
            'count': len(sequences_list),
            'types': seq_result['types'],
            'details': sequences_list[:5]  # Top 5 sequences
        }

    # Imitation points
    if (run_all or args.imitation) and hasattr(score, 'parts') and len(score.parts) >= 2:
        print("\n🔄 Detecting Imitation Points...")
        print("-" * 70)
        imitation_result = detect_imitation_points(score)

        imitations_list = imitation_result['imitation_points']
        print(f"Found {len(imitations_list)} imitation points")

        if imitations_list and args.verbose:
            for i, im in enumerate(imitations_list[:5], 1):
                print(f"\n  Imitation {i}:")
                print(f"    Subject voice: {im['subject_part']}")
                print(f"    Answer voice: {im['answer_part']}")
                print(f"    Delay: {im['delay']:.2f} quarter notes")
                print(f"    Similarity: {im['similarity']:.2f}")
                print(f"    Type: {im['type']}")

        results['imitations'] = {
            'count': len(imitations_list),
            'types': imitation_result['imitation_types'],
            'details': imitations_list[:10]  # Top 10 imitations
        }

    # Fugue structure
    if args.detect_fugue and hasattr(score, 'parts') and len(score.parts) >= 2:
        print("\n🎼 Analyzing Fugue Structure...")
        print("-" * 70)
        fugue_analysis = analyze_fugue_structure(score)

        if fugue_analysis['subject']:
            print(f"Subject detected:")
            print(f"  Intervals: {fugue_analysis['subject']['intervals']}")
            print(f"  Length: {fugue_analysis['subject']['length']} notes")

        print(f"\nAnswers: {len(fugue_analysis['answers'])}")
        if fugue_analysis['answers'] and args.verbose:
            for ans in fugue_analysis['answers']:
                print(f"  Voice {ans['voice']}, offset {ans['offset']:.2f}, "
                      f"type: {ans['type']}, similarity: {ans['similarity']:.2f}")

        print(f"Counter-subjects: {len(fugue_analysis['counter_subjects'])}")
        print(f"Episodes: {len(fugue_analysis['episodes'])}")
        print(f"Stretto sections: {len(fugue_analysis['stretto_sections'])}")
        print(f"Exposition ends at: {fugue_analysis['exposition_end']:.2f}")

        results['fugue'] = {
            'subject': fugue_analysis['subject'],
            'answer_count': len(fugue_analysis['answers']),
            'counter_subject_count': len(fugue_analysis['counter_subjects']),
            'episode_count': len(fugue_analysis['episodes']),
            'stretto_count': len(fugue_analysis['stretto_sections']),
            'exposition_end': fugue_analysis['exposition_end']
        }

    # Voice independence
    if args.voice_independence and hasattr(score, 'parts') and len(score.parts) >= 2:
        print("\n👥 Calculating Voice Independence...")
        print("-" * 70)
        independence = calculate_voice_independence(score)

        print(f"Number of voices: {independence['num_voices']}")
        print(f"Rhythmic independence: {independence['rhythmic_independence']:.3f}")
        print(f"Melodic independence: {independence['melodic_independence']:.3f}")
        print(f"Contour independence: {independence['contour_independence']:.3f}")
        print(f"Harmonic density: {independence['harmonic_density']:.2f} voices")
        print(f"Voice crossings: {independence['voice_crossing_count']}")

        if args.verbose:
            print(f"\nPer-voice activity:")
            for i, activity in enumerate(independence['per_voice_activity'], 1):
                print(f"  Voice {i}: {activity:.3f}")

        results['voice_independence'] = independence

    # Pattern complexity
    if run_all or args.complexity:
        print("\n📊 Calculating Pattern Complexity...")
        print("-" * 70)
        complexity = calculate_pattern_complexity(score)

        print(f"Interval complexity: {complexity['interval_complexity']:.3f}")
        print(f"Rhythmic complexity: {complexity['rhythmic_complexity']:.3f}")
        print(f"Range complexity: {complexity['range_complexity']:.3f}")
        print(f"Direction changes: {complexity['direction_changes']}")
        print(f"Overall complexity: {complexity['overall_complexity']:.3f}")

        results['complexity'] = complexity

    # Thematic development (skip for now - different API)
    # if run_all:
    #     print("\n🎭 Analyzing Thematic Development...")
    #     print("-" * 70)
    #     development = analyze_thematic_development(score)
    #     # ... implementation details

    # Contour similarities (skip for now - different API)
    # if run_all:
    #     print("\n🌊 Finding Contour Similarities...")
    #     print("-" * 70)
    #     contours = find_contour_similarities(score)
    #     print(f"Found {len(contours)} matching contours")

    # Save results if output specified
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n✓ Results saved to: {output_path}")

    print("\n" + "=" * 70)
    print("✓ Pattern analysis complete!")

    return 0


if __name__ == "__main__":
    sys.exit(main())


def generate_command(args: argparse.Namespace) -> int:
    """Execute the generate subcommand."""
    from cancrizans.generator import CanonGenerator
    from cancrizans.validator import CanonValidator

    generator = CanonGenerator(seed=args.seed if args.seed else None)
    validator = CanonValidator()

    print(f"Generating {args.algorithm} canon...")

    # Generate based on algorithm
    if args.algorithm == 'scale':
        canon = generator.generate_scale_canon(
            key=args.key,
            mode=args.mode,
            length=args.length
        )
    elif args.algorithm == 'arpeggio':
        canon = generator.generate_arpeggio_canon(
            root=args.root,
            chord_type=args.mode
        )
    elif args.algorithm == 'random':
        canon = generator.generate_random_walk(
            length=args.length,
            max_interval=3
        )
    elif args.algorithm == 'fibonacci':
        canon = generator.generate_fibonacci_canon(
            length=args.length
        )
    elif args.algorithm == 'modal':
        canon = generator.generate_modal_canon(
            mode=args.mode,
            length=args.length
        )
    elif args.algorithm == 'golden':
        canon = generator.generate_golden_ratio_canon(
            length=args.length
        )
    else:
        print(f"Unknown algorithm: {args.algorithm}")
        return 1

    print("✓ Canon generated")

    # Validate if requested
    if args.validate:
        print("\nValidating...")
        validation = validator.validate(canon)
        quality = validation['overall_quality']
        grade = validator.get_quality_grade(quality)

        print(f"Quality Score: {quality:.3f} ({grade})")

        if validation['errors']:
            print("\nErrors:")
            for error in validation['errors']:
                print(f"  • {error}")

        if validation['warnings'] and args.verbose:
            print("\nWarnings:")
            for warning in validation['warnings']:
                print(f"  • {warning}")

    # Save output
    if args.output:
        output_path = Path(args.output)
        to_midi(canon, str(output_path))
        print(f"✓ Saved to: {output_path}")

    return 0


def validate_command(args: argparse.Namespace) -> int:
    """Execute the validate subcommand."""
    from cancrizans.validator import CanonValidator
    from cancrizans.io import load_score

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        return 1

    print(f"Validating: {input_path}")
    print("-" * 60)

    # Load score
    score = load_score(input_path)

    # Validate
    validator = CanonValidator()
    validation = validator.validate(score)

    # Display results
    print(f"\nValid Canon: {validation['is_valid_canon']}")

    if validation['errors']:
        print("\n❌ Errors:")
        for error in validation['errors']:
            print(f"  • {error}")

    if validation['warnings']:
        print("\n⚠ Warnings:")
        for warning in validation['warnings']:
            print(f"  • {warning}")

    # Quality scores
    print(f"\n{'='*60}")
    print("QUALITY SCORES")
    print(f"{'='*60}")

    scores = validation['quality_scores']
    for key, value in sorted(scores.items()):
        bar_len = int(value * 20)
        bar = '█' * bar_len + '░' * (20 - bar_len)
        print(f"{key.capitalize():15s} [{bar}] {value:.3f}")

    overall = validation['overall_quality']
    grade = validator.get_quality_grade(overall)
    print(f"\n{'Overall Quality':15s} {overall:.3f} ({grade})")

    # Recommendations
    if args.verbose:
        recommendations = validator.get_recommendations(validation)
        print(f"\n{'='*60}")
        print("RECOMMENDATIONS")
        print(f"{'='*60}")
        for rec in recommendations:
            print(f"  • {rec}")

    # Export if requested
    if args.output:
        import json
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            # Convert to JSON-serializable format
            export_data = {
                'is_valid_canon': validation['is_valid_canon'],
                'errors': validation['errors'],
                'warnings': validation['warnings'],
                'quality_scores': validation['quality_scores'],
                'metrics': validation['metrics'],
                'overall_quality': validation['overall_quality'],
                'grade': grade
            }
            json.dump(export_data, f, indent=2)
        print(f"\n✓ Exported to: {output_path}")

    return 0 if validation['is_valid_canon'] else 1


def microtonal_canon_command(args: argparse.Namespace) -> int:
    """Execute the microtonal-canon subcommand."""
    from cancrizans.canon import create_microtonal_canon, generate_world_music_canon, cross_cultural_canon_analysis
    from cancrizans.microtonal import TuningSystem, ScaleType
    from cancrizans.io import to_midi, to_musicxml
    from music21 import stream, note, converter

    # Handle generation vs analysis mode
    if args.analyze:
        # Analyze existing file for cross-cultural compatibility
        if not args.input:
            print("Error: --input required for --analyze mode")
            return 1

        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: File not found: {input_path}")
            return 1

        print(f"Loading: {input_path}")
        score = converter.parse(str(input_path))

        print("\nAnalyzing cross-cultural compatibility...")
        print("=" * 60)

        analysis = cross_cultural_canon_analysis(score)

        # Display results sorted by compatibility
        sorted_results = sorted(
            analysis.items(),
            key=lambda x: x[1]['compatibility'],
            reverse=True
        )

        print(f"\n{'Scale':40s} {'Compat':>8s} {'Deviation':>10s} {'Ratios':>7s}")
        print("-" * 70)

        for scale_name, metrics in sorted_results[:10]:  # Top 10
            compat = metrics['compatibility']
            deviation = metrics['tuning_deviation']
            ratios = metrics['just_ratios_found']
            print(f"{scale_name:40s} {compat:8.3f} {deviation:10.2f}¢ {ratios:7d}")

        # Export results if requested
        if args.output:
            import json
            output_path = Path(args.output)
            with open(output_path, 'w') as f:
                json.dump(analysis, f, indent=2)
            print(f"\n✓ Exported analysis to: {output_path}")

        return 0

    # Generation mode
    if args.world_scale:
        # Generate canon using world music scale
        try:
            scale_type = ScaleType[args.world_scale]
        except KeyError:
            print(f"Error: Unknown scale type: {args.world_scale}")
            print("\nAvailable scales:")
            for st in ScaleType:
                print(f"  {st.name}")
            return 1

        print(f"Generating {args.canon_type} canon using {scale_type.value}...")
        canon = generate_world_music_canon(
            scale_type,
            length=args.length,
            canon_type=args.canon_type,
            octave_range=args.octave_range
        )

    elif args.input:
        # Apply microtonal tuning to existing theme
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: File not found: {input_path}")
            return 1

        print(f"Loading theme: {input_path}")
        theme_score = converter.parse(str(input_path))

        # Extract first part as theme
        if len(theme_score.parts) > 0:
            theme = theme_score.parts[0]
        else:
            theme = theme_score.flatten()

        # Get tuning system
        try:
            tuning_system = TuningSystem[args.tuning]
        except KeyError:
            print(f"Error: Unknown tuning system: {args.tuning}")
            print("\nAvailable tuning systems:")
            for ts in TuningSystem:
                print(f"  {ts.name}")
            return 1

        print(f"Creating {args.canon_type} canon in {tuning_system.value}...")
        canon = create_microtonal_canon(
            theme,
            tuning_system,
            canon_type=args.canon_type,
            tonic_midi=args.tonic,
            apply_pitch_bends=not args.no_pitch_bend
        )

    else:
        print("Error: Either --input or --world-scale must be specified")
        return 1

    # Export the canon
    output_dir = Path(args.output_dir) if args.output_dir else Path("out")
    output_dir.mkdir(exist_ok=True)

    midi_path = to_midi(canon, output_dir / "microtonal_canon.mid")
    print(f"✓ MIDI: {midi_path}")

    xml_path = to_musicxml(canon, output_dir / "microtonal_canon.musicxml")
    print(f"✓ MusicXML: {xml_path}")

    # Display info
    print(f"\n{'='*60}")
    print("CANON INFO")
    print(f"{'='*60}")
    print(f"Type: {args.canon_type.title()} Canon")
    if args.world_scale:
        print(f"Scale: {scale_type.value}")
    elif args.tuning:
        print(f"Tuning: {tuning_system.value}")
    print(f"Parts: {len(canon.parts)}")
    print(f"Duration: {canon.duration.quarterLength} beats")

    return 0
