/**
 * Animated Visualization
 * Real-time visualization that highlights notes as they play
 */

import type { ParsedNote } from './midi_import.js';

export interface VisualizationConfig {
  width: number;
  height: number;
  colorScheme: 'default' | 'rainbow' | 'heatmap' | 'monochrome';
  showVelocity: boolean;
  showNoteNames: boolean;
  playheadColor: string;
}

export class AnimatedVisualization {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private config: VisualizationConfig;
  private notes: ParsedNote[] = [];
  private currentTime: number = 0;
  private isPlaying: boolean = false;
  private animationFrameId: number | null = null;
  private startTimestamp: number = 0;
  private pausedTime: number = 0;

  constructor(canvas: HTMLCanvasElement, config?: Partial<VisualizationConfig>) {
    this.canvas = canvas;
    const ctx = this.canvas.getContext('2d');
    if (!ctx) {
      throw new Error('Could not get 2D context');
    }
    this.ctx = ctx;

    this.config = {
      width: canvas.width,
      height: canvas.height,
      colorScheme: 'default',
      showVelocity: true,
      showNoteNames: false,
      playheadColor: '#ff0000',
      ...config
    };
  }

  /**
   * Set the notes to visualize
   */
  setNotes(notes: ParsedNote[]): void {
    this.notes = [...notes].sort((a, b) => a.time - b.time);
    this.currentTime = 0;
    this.render();
  }

  /**
   * Start animation
   */
  start(startTime: number = 0): void {
    this.isPlaying = true;
    this.currentTime = startTime;
    this.startTimestamp = performance.now() - startTime * 1000;
    this.animate();
  }

  /**
   * Pause animation
   */
  pause(): void {
    this.isPlaying = false;
    this.pausedTime = this.currentTime;
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
  }

  /**
   * Resume animation
   */
  resume(): void {
    if (this.isPlaying) return;
    this.start(this.pausedTime);
  }

  /**
   * Stop animation and reset
   */
  stop(): void {
    this.isPlaying = false;
    this.currentTime = 0;
    this.pausedTime = 0;
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
    this.render();
  }

  /**
   * Seek to a specific time
   */
  seek(time: number): void {
    this.currentTime = time;
    this.pausedTime = time;
    this.startTimestamp = performance.now() - time * 1000;
    this.render();
  }

  /**
   * Animation loop
   */
  private animate = (): void => {
    if (!this.isPlaying) return;

    const now = performance.now();
    this.currentTime = (now - this.startTimestamp) / 1000;

    this.render();

    // Check if we've reached the end
    const maxTime = Math.max(...this.notes.map(n => n.time + n.duration));
    if (this.currentTime >= maxTime) {
      this.stop();
      return;
    }

    this.animationFrameId = requestAnimationFrame(this.animate);
  };

  /**
   * Render the visualization
   */
  private render(): void {
    const { width, height } = this.config;
    const ctx = this.ctx;

    // Clear canvas
    ctx.fillStyle = '#1a1a1a';
    ctx.fillRect(0, 0, width, height);

    if (this.notes.length === 0) {
      this.drawEmptyState();
      return;
    }

    // Calculate dimensions
    const minPitch = Math.min(...this.notes.map(n => n.pitch));
    const maxPitch = Math.max(...this.notes.map(n => n.pitch));
    const maxTime = Math.max(...this.notes.map(n => n.time + n.duration));

    const pitchRange = maxPitch - minPitch + 1;
    const noteHeight = height / pitchRange;

    // Draw grid lines
    this.drawGrid(minPitch, maxPitch, maxTime);

    // Draw notes
    for (const note of this.notes) {
      const isActive = this.currentTime >= note.time &&
                       this.currentTime <= note.time + note.duration;
      const isPast = this.currentTime > note.time + note.duration;

      this.drawNote(note, minPitch, maxPitch, maxTime, isActive, isPast, noteHeight);
    }

    // Draw playhead
    this.drawPlayhead(maxTime);

    // Draw time indicator
    this.drawTimeIndicator();
  }

  /**
   * Draw a single note
   */
  private drawNote(
    note: ParsedNote,
    minPitch: number,
    _maxPitch: number,
    maxTime: number,
    isActive: boolean,
    isPast: boolean,
    noteHeight: number
  ): void {
    const ctx = this.ctx;
    const { width, height } = this.config;

    const x = (note.time / maxTime) * width;
    const noteWidth = (note.duration / maxTime) * width;
    const y = height - ((note.pitch - minPitch + 1) * noteHeight);

    // Determine color
    let color: string;
    if (isActive) {
      color = this.getActiveNoteColor(note);
    } else if (isPast) {
      color = this.getPastNoteColor(note);
    } else {
      color = this.getFutureNoteColor(note);
    }

    // Draw note rectangle
    ctx.fillStyle = color;
    ctx.fillRect(x, y, Math.max(2, noteWidth), noteHeight);

    // Draw border for active notes
    if (isActive) {
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.strokeRect(x, y, Math.max(2, noteWidth), noteHeight);

      // Glow effect
      ctx.shadowBlur = 10;
      ctx.shadowColor = color;
      ctx.fillRect(x, y, Math.max(2, noteWidth), noteHeight);
      ctx.shadowBlur = 0;
    }

    // Draw note name if enabled
    if (this.config.showNoteNames && noteWidth > 20) {
      ctx.fillStyle = isActive ? '#000000' : '#ffffff';
      ctx.font = `${Math.min(12, noteHeight * 0.8)}px monospace`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      const noteName = this.midiToNoteName(note.pitch);
      ctx.fillText(noteName, x + noteWidth / 2, y + noteHeight / 2);
    }
  }

  /**
   * Get color for active notes
   */
  private getActiveNoteColor(note: ParsedNote): string {
    switch (this.config.colorScheme) {
      case 'rainbow':
        return this.pitchToRainbow(note.pitch);
      case 'heatmap':
        return this.velocityToHeatmap(note.velocity);
      case 'monochrome':
        return '#ffffff';
      default:
        return this.config.showVelocity
          ? this.velocityToColor(note.velocity)
          : '#4CAF50';
    }
  }

  /**
   * Get color for past notes
   */
  private getPastNoteColor(note: ParsedNote): string {
    switch (this.config.colorScheme) {
      case 'rainbow':
        return this.adjustBrightness(this.pitchToRainbow(note.pitch), 0.3);
      case 'heatmap':
        return this.adjustBrightness(this.velocityToHeatmap(note.velocity), 0.3);
      case 'monochrome':
        return '#666666';
      default:
        return this.config.showVelocity
          ? this.adjustBrightness(this.velocityToColor(note.velocity), 0.3)
          : '#2E7D32';
    }
  }

  /**
   * Get color for future notes
   */
  private getFutureNoteColor(note: ParsedNote): string {
    switch (this.config.colorScheme) {
      case 'rainbow':
        return this.adjustBrightness(this.pitchToRainbow(note.pitch), 0.5);
      case 'heatmap':
        return this.adjustBrightness(this.velocityToHeatmap(note.velocity), 0.5);
      case 'monochrome':
        return '#999999';
      default:
        return this.config.showVelocity
          ? this.adjustBrightness(this.velocityToColor(note.velocity), 0.5)
          : '#66BB6A';
    }
  }

  /**
   * Draw grid lines for pitch
   */
  private drawGrid(minPitch: number, maxPitch: number, maxTime: number): void {
    const ctx = this.ctx;
    const { width, height } = this.config;

    ctx.strokeStyle = '#333333';
    ctx.lineWidth = 1;

    // Horizontal lines (for each pitch)
    const pitchRange = maxPitch - minPitch + 1;
    const noteHeight = height / pitchRange;

    for (let i = 0; i <= pitchRange; i++) {
      const y = i * noteHeight;
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }

    // Vertical lines (time markers)
    const timeInterval = this.getTimeInterval(maxTime);
    for (let t = 0; t <= maxTime; t += timeInterval) {
      const x = (t / maxTime) * width;
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }
  }

  /**
   * Draw playhead
   */
  private drawPlayhead(maxTime: number): void {
    const ctx = this.ctx;
    const { width, height } = this.config;

    const x = (this.currentTime / maxTime) * width;

    ctx.strokeStyle = this.config.playheadColor;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, height);
    ctx.stroke();

    // Playhead shadow for visibility
    ctx.shadowBlur = 5;
    ctx.shadowColor = this.config.playheadColor;
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, height);
    ctx.stroke();
    ctx.shadowBlur = 0;
  }

  /**
   * Draw time indicator
   */
  private drawTimeIndicator(): void {
    const ctx = this.ctx;

    ctx.fillStyle = '#ffffff';
    ctx.font = '14px monospace';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';

    const timeStr = this.formatTime(this.currentTime);
    ctx.fillText(timeStr, 10, 10);
  }

  /**
   * Draw empty state
   */
  private drawEmptyState(): void {
    const ctx = this.ctx;
    const { width, height } = this.config;

    ctx.fillStyle = '#666666';
    ctx.font = '16px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('No notes to display', width / 2, height / 2);
  }

  /**
   * Convert MIDI pitch to rainbow color
   */
  private pitchToRainbow(pitch: number): string {
    const hue = (pitch % 12) * 30; // 12 pitches, 360 degrees
    return `hsl(${hue}, 80%, 60%)`;
  }

  /**
   * Convert velocity to heatmap color
   */
  private velocityToHeatmap(velocity: number): string {
    const normalized = velocity / 127;
    const hue = (1 - normalized) * 240; // Blue (240) to Red (0)
    return `hsl(${hue}, 100%, 50%)`;
  }

  /**
   * Convert velocity to brightness
   */
  private velocityToColor(velocity: number): string {
    const brightness = Math.round((velocity / 127) * 100);
    return `hsl(120, 60%, ${brightness}%)`;
  }

  /**
   * Adjust color brightness
   */
  private adjustBrightness(color: string, factor: number): string {
    // Simple brightness adjustment for HSL colors
    const match = color.match(/hsl\((\d+),\s*(\d+)%,\s*(\d+)%\)/);
    if (match) {
      const [, h, s, l] = match;
      const newL = Math.round(parseInt(l) * factor);
      return `hsl(${h}, ${s}%, ${newL}%)`;
    }
    return color;
  }

  /**
   * Get appropriate time interval for grid
   */
  private getTimeInterval(maxTime: number): number {
    if (maxTime < 5) return 1;
    if (maxTime < 20) return 2;
    if (maxTime < 60) return 5;
    return 10;
  }

  /**
   * Format time as MM:SS
   */
  private formatTime(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }

  /**
   * Convert MIDI note to name
   */
  private midiToNoteName(midi: number): string {
    const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
    const octave = Math.floor(midi / 12) - 1;
    const note = noteNames[midi % 12];
    return `${note}${octave}`;
  }

  /**
   * Update configuration
   */
  updateConfig(config: Partial<VisualizationConfig>): void {
    this.config = { ...this.config, ...config };
    this.render();
  }

  /**
   * Get current time
   */
  getCurrentTime(): number {
    return this.currentTime;
  }

  /**
   * Check if playing
   */
  getIsPlaying(): boolean {
    return this.isPlaying;
  }
}
