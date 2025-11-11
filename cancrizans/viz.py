"""
Visualization utilities for musical analysis: piano rolls and symmetry plots.
"""

from pathlib import Path
from typing import Union, List, Tuple
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from music21 import stream, note, chord

from cancrizans.canon import pairwise_symmetry_map


def piano_roll(
    score: stream.Score,
    path: Union[str, Path],
    dpi: int = 100
) -> Path:
    """
    Generate a piano roll visualization of a score.

    Shows notes as horizontal bars on a pitch-time grid, with different
    colors for different voices.

    Args:
        score: The Score to visualize
        path: Destination file path for the PNG image
        dpi: Resolution in dots per inch (default 100)

    Returns:
        Path to the saved image
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 6))

    parts = list(score.parts)
    colors = plt.cm.tab10.colors

    min_pitch = 127
    max_pitch = 0

    # Collect all note data
    for part_idx, part in enumerate(parts):
        color = colors[part_idx % len(colors)]

        for el in part.flatten().notesAndRests:
            if isinstance(el, note.Rest):
                continue

            offset = float(el.offset)
            duration = float(el.quarterLength)

            if isinstance(el, note.Note):
                pitches = [el.pitch.midi]
            elif isinstance(el, chord.Chord):
                pitches = [p.midi for p in el.pitches]
            else:
                continue

            for pitch in pitches:
                min_pitch = min(min_pitch, pitch)
                max_pitch = max(max_pitch, pitch)

                # Draw note as rectangle
                rect = patches.Rectangle(
                    (offset, pitch - 0.4),
                    duration,
                    0.8,
                    linewidth=1,
                    edgecolor='black',
                    facecolor=color,
                    alpha=0.7
                )
                ax.add_patch(rect)

    # Set axis limits and labels
    ax.set_xlim(-1, max(p.duration.quarterLength for p in parts) + 1)
    ax.set_ylim(min_pitch - 2, max_pitch + 2)

    ax.set_xlabel('Time (quarter notes)', fontsize=12)
    ax.set_ylabel('MIDI Pitch', fontsize=12)
    ax.set_title('Piano Roll', fontsize=14, fontweight='bold')

    ax.grid(True, alpha=0.3)

    # Add legend for parts
    legend_elements = [
        patches.Patch(facecolor=colors[i % len(colors)], label=f'Voice {i+1}')
        for i in range(len(parts))
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.savefig(path, dpi=dpi, bbox_inches='tight')
    plt.close()

    return path


def symmetry(
    score: stream.Score,
    path: Union[str, Path],
    dpi: int = 100
) -> Path:
    """
    Generate a symmetry visualization showing palindromic structure.

    Displays notes on a horizontal time axis mirrored about the piece's
    midpoint, with connecting lines between symmetric pairs.

    Args:
        score: The Score to visualize
        path: Destination file path for the PNG image
        dpi: Resolution in dots per inch (default 100)

    Returns:
        Path to the saved image
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(14, 8))

    parts = list(score.parts)

    if len(parts) != 2:
        print(f"Warning: symmetry plot expects 2 voices, got {len(parts)}")

    # Calculate total duration
    total_duration = max(
        max((el.offset + el.quarterLength for el in part.flatten().notesAndRests),
            default=0)
        for part in parts
    )

    midpoint = total_duration / 2

    colors = plt.cm.tab10.colors

    # Extract events from both voices
    events_by_part: List[List[Tuple[float, float, int]]] = []

    for part in parts:
        events = []
        for el in part.flatten().notesAndRests:
            if isinstance(el, note.Rest):
                continue

            offset = float(el.offset)
            duration = float(el.quarterLength)

            if isinstance(el, note.Note):
                pitch = el.pitch.midi
            elif isinstance(el, chord.Chord):
                pitch = min(p.midi for p in el.pitches)
            else:
                continue

            events.append((offset, duration, pitch))

        events_by_part.append(sorted(events, key=lambda x: x[0]))

    # Draw central time axis (midpoint)
    ax.axvline(x=midpoint, color='red', linewidth=2, linestyle='--',
               label='Temporal midpoint', alpha=0.8)

    # Plot notes for each voice
    for part_idx, events in enumerate(events_by_part):
        color = colors[part_idx % len(colors)]
        y_offset = part_idx * 30  # Vertical separation between voices

        for offset, duration, pitch in events:
            # Normalize pitch to a reasonable range for visualization
            pitch_norm = (pitch - 60) * 2  # Center around middle C

            # Draw note as circle
            ax.scatter(offset + duration/2, y_offset + pitch_norm,
                      s=duration * 50, c=[color], alpha=0.6,
                      edgecolors='black', linewidth=1)

    # Draw symmetry connectors
    if len(events_by_part) == 2:
        events_a = events_by_part[0]
        events_b = events_by_part[1]

        # Match events by pitch and duration
        for offset_a, dur_a, pitch_a in events_a:
            # Look for corresponding retrograde event in voice B
            expected_end_b = total_duration - offset_a
            expected_start_b = expected_end_b - dur_a

            for offset_b, dur_b, pitch_b in events_b:
                # Check if this is a matching retrograde pair
                if (abs(offset_b - expected_start_b) < 0.1 and
                    abs(dur_b - dur_a) < 0.1 and
                    pitch_a == pitch_b):

                    # Draw connector line
                    x_a = offset_a + dur_a / 2
                    y_a = 0 + (pitch_a - 60) * 2

                    x_b = offset_b + dur_b / 2
                    y_b = 30 + (pitch_b - 60) * 2

                    # Draw arc connecting the symmetric pair
                    ax.plot([x_a, x_b], [y_a, y_b],
                           color='gray', alpha=0.2, linewidth=0.5)

                    break

    ax.set_xlim(-2, total_duration + 2)
    ax.set_xlabel('Time (quarter notes)', fontsize=12)
    ax.set_ylabel('Pitch (relative)', fontsize=12)
    ax.set_title('Palindromic Symmetry Visualization', fontsize=14, fontweight='bold')

    # Add legend
    legend_elements = [
        patches.Patch(facecolor=colors[i % len(colors)],
                     label=f'Voice {i+1}')
        for i in range(len(parts))
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.savefig(path, dpi=dpi, bbox_inches='tight')
    plt.close()

    return path
