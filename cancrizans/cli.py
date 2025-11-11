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
        else:
            print(f"Unknown command: {args.command}")
            return 1

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
