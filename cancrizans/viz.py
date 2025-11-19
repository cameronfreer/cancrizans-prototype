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

try:
    from cancrizans.microtonal import MicrotonalScale
    from cancrizans.microtonal_utils import calculate_scale_tension
    MICROTONAL_AVAILABLE = True
except ImportError:
    MICROTONAL_AVAILABLE = False


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


# ============================================================================
# Phase 14: Advanced Visualization
# ============================================================================


def animate_transformation(
    original_score: stream.Score,
    transformed_score: stream.Score,
    path: Union[str, Path],
    num_frames: int = 30,
    duration: float = 3.0,
    dpi: int = 100
) -> Path:
    """
    Create an animated GIF showing gradual transformation between two scores.

    Interpolates between the original and transformed score, creating a
    smooth animation that visualizes the transformation process.

    Args:
        original_score: The starting Score
        transformed_score: The ending Score
        path: Destination file path for the GIF image
        num_frames: Number of frames in the animation (default 30)
        duration: Total duration in seconds (default 3.0)
        dpi: Resolution in dots per inch (default 100)

    Returns:
        Path to the saved animated GIF

    Example:
        >>> theme = stream.Score()
        >>> # ... populate theme ...
        >>> retrograde_theme = retrograde(theme)
        >>> animate_transformation(theme, retrograde_theme, "transform.gif")
    """
    try:
        from PIL import Image
    except ImportError:
        raise ImportError("PIL/Pillow is required for animation. Install with: pip install Pillow")

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Create temporary directory for frames
    import tempfile
    temp_dir = Path(tempfile.mkdtemp())

    frames = []
    for i in range(num_frames):
        # Calculate interpolation factor (0.0 to 1.0)
        t = i / (num_frames - 1) if num_frames > 1 else 0.0

        # Create frame filename
        frame_path = temp_dir / f"frame_{i:03d}.png"

        # For now, alternate between original and transformed
        # (true interpolation would require more complex music21 manipulation)
        if t < 0.5:
            score_to_show = original_score
            alpha = t * 2  # 0.0 to 1.0
        else:
            score_to_show = transformed_score
            alpha = (t - 0.5) * 2  # 0.0 to 1.0

        # Create piano roll for this frame
        fig, ax = plt.subplots(figsize=(12, 6))

        parts = list(score_to_show.parts)
        colors = plt.cm.tab10.colors

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
                    rect = patches.Rectangle(
                        (offset, pitch - 0.4),
                        duration,
                        0.8,
                        linewidth=1,
                        edgecolor='black',
                        facecolor=color,
                        alpha=0.3 + alpha * 0.4  # Fade in effect
                    )
                    ax.add_patch(rect)

        # Set consistent axis limits
        all_parts = list(original_score.parts) + list(transformed_score.parts)
        max_duration = max((p.duration.quarterLength for p in all_parts), default=10)

        ax.set_xlim(-1, max_duration + 1)
        ax.set_ylim(50, 80)
        ax.set_xlabel('Time (quarter notes)', fontsize=12)
        ax.set_ylabel('MIDI Pitch', fontsize=12)
        ax.set_title(f'Transformation Animation (frame {i+1}/{num_frames})',
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(frame_path, dpi=dpi, bbox_inches='tight')
        plt.close()

        frames.append(Image.open(frame_path))

    # Save as animated GIF
    frame_duration = int((duration / num_frames) * 1000)  # Convert to milliseconds
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=frame_duration,
        loop=0
    )

    # Clean up temporary files
    import shutil
    shutil.rmtree(temp_dir)

    return path


def visualize_3d_canon(
    score: stream.Score,
    path: Union[str, Path],
    rotation: Tuple[float, float] = (30, 45),
    dpi: int = 100
) -> Path:
    """
    Create a 3D visualization with time, pitch, and voice dimensions.

    Plots notes in 3D space where x=time, y=pitch, z=voice, allowing
    visualization of voice interactions and canon structure.

    Args:
        score: The Score to visualize
        path: Destination file path for the PNG image
        rotation: (elevation, azimuth) viewing angles in degrees
        dpi: Resolution in dots per inch (default 100)

    Returns:
        Path to the saved image

    Example:
        >>> canon = mirror_canon(theme)
        >>> visualize_3d_canon(canon, "canon_3d.png", rotation=(20, 60))
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    parts = list(score.parts)
    colors = plt.cm.tab10.colors

    for part_idx, part in enumerate(parts):
        color = colors[part_idx % len(colors)]
        voice_z = part_idx  # Z coordinate represents voice

        times = []
        pitches = []
        voices = []

        for el in part.flatten().notesAndRests:
            if isinstance(el, note.Rest):
                continue

            offset = float(el.offset)
            duration = float(el.quarterLength)

            if isinstance(el, note.Note):
                pitch_vals = [el.pitch.midi]
            elif isinstance(el, chord.Chord):
                pitch_vals = [p.midi for p in el.pitches]
            else:
                continue

            for pitch in pitch_vals:
                times.append(offset + duration / 2)
                pitches.append(pitch)
                voices.append(voice_z)

        # Plot notes as scatter points
        ax.scatter(times, pitches, voices,
                  c=[color] * len(times),
                  s=50,
                  alpha=0.6,
                  edgecolors='black',
                  linewidth=0.5,
                  label=f'Voice {part_idx + 1}')

    ax.set_xlabel('Time (quarter notes)', fontsize=11)
    ax.set_ylabel('MIDI Pitch', fontsize=11)
    ax.set_zlabel('Voice', fontsize=11)
    ax.set_title('3D Canon Visualization', fontsize=14, fontweight='bold')

    # Set viewing angle
    ax.view_init(elev=rotation[0], azim=rotation[1])

    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(path, dpi=dpi, bbox_inches='tight')
    plt.close()

    return path


def visualize_voice_graph(
    score: stream.Score,
    path: Union[str, Path],
    min_similarity: float = 0.7,
    dpi: int = 100
) -> Path:
    """
    Create a network graph showing voice imitation relationships.

    Analyzes voice pairs for imitation and creates a graph where nodes
    are voices and edges represent imitation relationships.

    Args:
        score: The Score to analyze
        path: Destination file path for the PNG image
        min_similarity: Minimum similarity threshold for edges (0.0-1.0)
        dpi: Resolution in dots per inch (default 100)

    Returns:
        Path to the saved image

    Example:
        >>> fugue = load_score("fugue.xml")
        >>> visualize_voice_graph(fugue, "voice_graph.png", min_similarity=0.6)
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        import networkx as nx
    except ImportError:
        # Fallback: create a simple matplotlib visualization
        fig, ax = plt.subplots(figsize=(10, 8))

        parts = list(score.parts)
        num_voices = len(parts)

        # Simple circular layout
        angles = np.linspace(0, 2 * np.pi, num_voices, endpoint=False)
        positions = {i: (np.cos(angle), np.sin(angle))
                    for i, angle in enumerate(angles)}

        # Draw nodes
        for i, pos in positions.items():
            circle = plt.Circle(pos, 0.15, color='lightblue',
                              edgecolor='black', linewidth=2, zorder=2)
            ax.add_patch(circle)
            ax.text(pos[0], pos[1], f'V{i+1}',
                   ha='center', va='center',
                   fontsize=12, fontweight='bold', zorder=3)

        # Draw edges (simplified - just show connections between consecutive voices)
        for i in range(num_voices - 1):
            pos1 = positions[i]
            pos2 = positions[i + 1]
            ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]],
                   'gray', linewidth=2, alpha=0.5, zorder=1)

        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Voice Relationship Graph (simplified)\nInstall networkx for full analysis',
                    fontsize=14, fontweight='bold')

        plt.tight_layout()
        plt.savefig(path, dpi=dpi, bbox_inches='tight')
        plt.close()

        return path

    # Full implementation with networkx
    G = nx.Graph()

    parts = list(score.parts)
    num_voices = len(parts)

    # Add nodes for each voice
    for i in range(num_voices):
        G.add_node(i, label=f'Voice {i+1}')

    # Analyze voice pairs for imitation
    for i in range(num_voices):
        for j in range(i + 1, num_voices):
            # Simple similarity metric: count matching pitches
            notes_i = [el.pitch.midi for el in parts[i].flatten().notes
                      if isinstance(el, note.Note)]
            notes_j = [el.pitch.midi for el in parts[j].flatten().notes
                      if isinstance(el, note.Note)]

            if not notes_i or not notes_j:
                continue

            # Calculate similarity as intersection ratio
            set_i = set(notes_i[:min(20, len(notes_i))])  # First 20 notes
            set_j = set(notes_j[:min(20, len(notes_j))])
            intersection = len(set_i & set_j)
            union = len(set_i | set_j)

            similarity = intersection / union if union > 0 else 0.0

            if similarity >= min_similarity:
                G.add_edge(i, j, weight=similarity)

    # Draw the graph
    fig, ax = plt.subplots(figsize=(10, 8))

    pos = nx.spring_layout(G, seed=42)

    # Draw edges with thickness based on weight
    edges = G.edges(data=True)
    for u, v, data in edges:
        weight = data.get('weight', 0.5)
        nx.draw_networkx_edges(G, pos, [(u, v)],
                              width=weight * 5,
                              alpha=0.6,
                              edge_color='gray',
                              ax=ax)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos,
                          node_color='lightblue',
                          node_size=1000,
                          edgecolors='black',
                          linewidths=2,
                          ax=ax)

    # Draw labels
    labels = {i: f'V{i+1}' for i in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels,
                           font_size=12,
                           font_weight='bold',
                           ax=ax)

    ax.set_title('Voice Imitation Network',
                fontsize=14, fontweight='bold')
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(path, dpi=dpi, bbox_inches='tight')
    plt.close()

    return path


def export_analysis_figure(
    score: stream.Score,
    analysis_type: str,
    path: Union[str, Path],
    formats: List[str] = None,
    dpi: int = 300,
    **kwargs
) -> List[Path]:
    """
    Export publication-ready analysis figures in multiple formats.

    Creates high-quality visualizations suitable for academic papers,
    presentations, and publications in various formats.

    Args:
        score: The Score to analyze and visualize
        analysis_type: Type of analysis ('piano_roll', 'symmetry', '3d', 'graph')
        path: Base destination file path (extension will be added)
        formats: List of output formats (e.g., ['png', 'pdf', 'svg', 'eps'])
                Default: ['png', 'pdf']
        dpi: Resolution for raster formats (default 300 for publication quality)
        **kwargs: Additional arguments passed to specific visualization functions

    Returns:
        List of Path objects for all generated files

    Example:
        >>> canon = mirror_canon(theme)
        >>> paths = export_analysis_figure(
        ...     canon, 'symmetry', 'output/figure',
        ...     formats=['png', 'pdf', 'svg'], dpi=600
        ... )
    """
    if formats is None:
        formats = ['png', 'pdf']

    path = Path(path)
    base_path = path.parent / path.stem  # Remove extension if present
    base_path.parent.mkdir(parents=True, exist_ok=True)

    output_paths = []

    for fmt in formats:
        output_path = Path(f"{base_path}.{fmt}")

        if analysis_type == 'piano_roll':
            piano_roll(score, output_path, dpi=dpi)
        elif analysis_type == 'symmetry':
            symmetry(score, output_path, dpi=dpi)
        elif analysis_type == '3d':
            rotation = kwargs.get('rotation', (30, 45))
            visualize_3d_canon(score, output_path, rotation=rotation, dpi=dpi)
        elif analysis_type == 'graph':
            min_similarity = kwargs.get('min_similarity', 0.7)
            visualize_voice_graph(score, output_path,
                                min_similarity=min_similarity, dpi=dpi)
        else:
            raise ValueError(f"Unknown analysis_type: {analysis_type}. "
                           f"Choose from: 'piano_roll', 'symmetry', '3d', 'graph'")

        output_paths.append(output_path)

    return output_paths


def visualize_microtonal_scale(
    scale: 'MicrotonalScale',
    path: Union[str, Path],
    show_cents: bool = True,
    show_ratios: bool = False,
    show_tension: bool = True,
    dpi: int = 100
) -> Path:
    """
    Visualize a microtonal scale showing intervals and characteristics.

    Creates a circular diagram showing scale degrees and their intervals,
    along with tension analysis and interval measurements.

    Args:
        scale: MicrotonalScale to visualize
        path: Destination file path for the image
        show_cents: Display cent values for each degree (default: True)
        show_ratios: Display frequency ratios if available (default: False)
        show_tension: Display harmonic tension analysis (default: True)
        dpi: Resolution in dots per inch (default 100)

    Returns:
        Path to the saved image

    Example:
        >>> from cancrizans.microtonal import create_tuning_system_scale, TuningSystem
        >>> scale = create_tuning_system_scale(TuningSystem.WERCKMEISTER_III, 60)
        >>> visualize_microtonal_scale(scale, 'werckmeister.png')
    """
    if not MICROTONAL_AVAILABLE:
        raise ImportError(
            "Microtonal visualization requires the microtonal module. "
            "Please install required dependencies."
        )

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fig, (ax_circle, ax_info) = plt.subplots(1, 2, figsize=(14, 7))

    # Left subplot: Circular scale visualization
    ax_circle.set_aspect('equal')
    ax_circle.set_xlim(-1.5, 1.5)
    ax_circle.set_ylim(-1.5, 1.5)
    ax_circle.axis('off')
    ax_circle.set_title(f'{scale.name}\nScale Diagram', fontsize=14, fontweight='bold')

    # Draw outer circle
    circle = plt.Circle((0, 0), 1.0, fill=False, color='black', linewidth=2)
    ax_circle.add_patch(circle)

    # Draw scale degrees
    intervals = scale.intervals_cents
    if not intervals:
        intervals = [0]  # Fallback

    # Normalize to octave (1200 cents)
    octave_cents = 1200.0

    for i, interval_cents in enumerate(intervals):
        # Calculate angle (0 degrees = top, clockwise)
        angle_deg = (interval_cents / octave_cents) * 360
        angle_rad = np.radians(90 - angle_deg)  # Convert to standard position

        # Position on circle
        x = np.cos(angle_rad)
        y = np.sin(angle_rad)

        # Draw degree marker
        marker_color = plt.cm.hsv(interval_cents / octave_cents)
        ax_circle.plot([0, x * 0.95], [0, y * 0.95],
                      color=marker_color, linewidth=1.5, alpha=0.6)

        # Draw degree point
        ax_circle.scatter([x], [y], s=200, c=[marker_color],
                         edgecolors='black', linewidths=2, zorder=5)

        # Label with degree number and cents
        label_x = x * 1.25
        label_y = y * 1.25

        if show_cents:
            label_text = f"{i}\n{interval_cents:.1f}¢"
        else:
            label_text = f"{i}"

        ax_circle.text(label_x, label_y, label_text,
                      ha='center', va='center', fontsize=9,
                      bbox=dict(boxstyle='round', facecolor='white',
                              alpha=0.8, edgecolor='gray'))

    # Draw center point
    ax_circle.scatter([0], [0], s=100, c='black', marker='o', zorder=10)
    ax_circle.text(0, 0, '0', ha='center', va='center',
                  color='white', fontsize=10, fontweight='bold')

    # Right subplot: Scale information
    ax_info.axis('off')

    info_text = []
    info_text.append(f"Scale: {scale.name}")
    info_text.append(f"Number of degrees: {len(intervals)}")
    info_text.append(f"Tonic MIDI: {scale.tonic_midi}")
    info_text.append("")

    # Interval information
    info_text.append("Intervals (cents):")
    for i, cents in enumerate(intervals[:12]):  # Show first 12
        info_text.append(f"  Degree {i}: {cents:.2f}¢")
    if len(intervals) > 12:
        info_text.append(f"  ... and {len(intervals) - 12} more")

    info_text.append("")

    # Step sizes
    if len(intervals) > 1:
        steps = [intervals[i+1] - intervals[i] for i in range(len(intervals)-1)]
        info_text.append("Step sizes:")
        info_text.append(f"  Min: {min(steps):.2f}¢")
        info_text.append(f"  Max: {max(steps):.2f}¢")
        info_text.append(f"  Avg: {np.mean(steps):.2f}¢")
        info_text.append("")

    # Tension analysis
    if show_tension:
        tension = calculate_scale_tension(scale)
        info_text.append(f"Harmonic Tension: {tension:.3f}")

        if tension < 0.3:
            tension_desc = "Low (consonant)"
        elif tension < 0.6:
            tension_desc = "Moderate"
        elif tension < 0.9:
            tension_desc = "High (dissonant)"
        else:
            tension_desc = "Very High"

        info_text.append(f"  ({tension_desc})")
        info_text.append("")

    # Draw tension visualization if enabled
    if show_tension:
        tension = calculate_scale_tension(scale)

        # Create a small tension bar
        bar_y = 0.15
        bar_width = 0.8
        bar_height = 0.05

        # Background bar
        rect_bg = patches.Rectangle((0.1, bar_y), bar_width, bar_height,
                                    linewidth=1, edgecolor='black',
                                    facecolor='lightgray')
        ax_info.add_patch(rect_bg)

        # Tension level bar
        tension_normalized = min(1.0, tension)
        tension_color = plt.cm.RdYlGn_r(tension_normalized)
        rect_tension = patches.Rectangle((0.1, bar_y),
                                        bar_width * tension_normalized,
                                        bar_height,
                                        linewidth=0, facecolor=tension_color,
                                        alpha=0.7)
        ax_info.add_patch(rect_tension)

        ax_info.text(0.5, bar_y - 0.05, 'Tension Level',
                    ha='center', va='top', fontsize=10, fontweight='bold')

    # Display info text
    text_y = 0.95
    for line in info_text:
        if line.startswith("Scale:") or line.startswith("Harmonic Tension:"):
            weight = 'bold'
            size = 11
        else:
            weight = 'normal'
            size = 9

        ax_info.text(0.05, text_y, line, transform=ax_info.transAxes,
                    fontsize=size, fontweight=weight, verticalalignment='top',
                    family='monospace')

        if line == "":
            text_y -= 0.03
        else:
            text_y -= 0.04

    ax_info.set_xlim(0, 1)
    ax_info.set_ylim(0, 1)

    plt.tight_layout()
    fig.savefig(path, dpi=dpi, bbox_inches='tight')
    plt.close(fig)

    return path


def compare_microtonal_scales(
    scales: List['MicrotonalScale'],
    path: Union[str, Path],
    dpi: int = 100
) -> Path:
    """
    Create a comparison visualization of multiple microtonal scales.

    Shows multiple scales side-by-side with their interval structures
    and tension characteristics.

    Args:
        scales: List of MicrotonalScale objects to compare
        path: Destination file path for the image
        dpi: Resolution in dots per inch (default 100)

    Returns:
        Path to the saved image

    Example:
        >>> from cancrizans.microtonal import create_tuning_system_scale, TuningSystem
        >>> scales = [
        ...     create_tuning_system_scale(TuningSystem.EQUAL_12, 60),
        ...     create_tuning_system_scale(TuningSystem.EQUAL_19, 60),
        ...     create_tuning_system_scale(TuningSystem.WERCKMEISTER_III, 60)
        ... ]
        >>> compare_microtonal_scales(scales, 'comparison.png')
    """
    if not MICROTONAL_AVAILABLE:
        raise ImportError(
            "Microtonal visualization requires the microtonal module. "
            "Please install required dependencies."
        )

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    n_scales = len(scales)
    fig, axes = plt.subplots(1, n_scales, figsize=(5 * n_scales, 5))

    if n_scales == 1:
        axes = [axes]

    for ax, scale in zip(axes, scales):
        ax.set_aspect('equal')
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.3, 1.3)
        ax.axis('off')

        # Title with scale name
        ax.set_title(f'{scale.name}\n({len(scale.intervals_cents)} degrees)',
                    fontsize=10, fontweight='bold')

        # Draw circle
        circle = plt.Circle((0, 0), 1.0, fill=False, color='black', linewidth=2)
        ax.add_patch(circle)

        # Draw scale degrees
        intervals = scale.intervals_cents if scale.intervals_cents else [0]
        octave_cents = 1200.0

        for i, interval_cents in enumerate(intervals):
            angle_deg = (interval_cents / octave_cents) * 360
            angle_rad = np.radians(90 - angle_deg)

            x = np.cos(angle_rad)
            y = np.sin(angle_rad)

            marker_color = plt.cm.hsv(interval_cents / octave_cents)
            ax.plot([0, x * 0.95], [0, y * 0.95],
                   color=marker_color, linewidth=1.5, alpha=0.6)
            ax.scatter([x], [y], s=150, c=[marker_color],
                      edgecolors='black', linewidths=1.5, zorder=5)

            # Only label every few degrees if many degrees
            if len(intervals) <= 19 or i % 2 == 0:
                label_x = x * 1.15
                label_y = y * 1.15
                ax.text(label_x, label_y, str(i),
                       ha='center', va='center', fontsize=7)

        # Center point
        ax.scatter([0], [0], s=80, c='black', marker='o', zorder=10)

        # Tension info at bottom
        tension = calculate_scale_tension(scale)
        ax.text(0, -1.25, f'Tension: {tension:.2f}',
               ha='center', va='top', fontsize=9,
               bbox=dict(boxstyle='round', facecolor='white',
                        alpha=0.8, edgecolor='gray'))

    plt.suptitle('Microtonal Scale Comparison',
                fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    fig.savefig(path, dpi=dpi, bbox_inches='tight')
    plt.close(fig)

    return path
