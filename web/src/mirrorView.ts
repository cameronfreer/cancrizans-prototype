/**
 * Mirror view - visualizes the palindromic structure of the canon
 */

import { Score, Note } from './scoreLoader';

export class MirrorView {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private score: Score;
  private width: number = 0;
  private height: number = 0;
  private midpoint: number = 0;
  private highlightPairs: boolean = true;
  private activeNotes: Set<string> = new Set();

  constructor(canvas: HTMLCanvasElement, score: Score) {
    this.canvas = canvas;
    this.score = score;

    const ctx = canvas.getContext('2d');
    if (!ctx) throw new Error('Could not get canvas context');
    this.ctx = ctx;

    this.resize();
    this.midpoint = this.score.totalDuration / 2;
  }

  resize(): void {
    const container = this.canvas.parentElement;
    if (!container) return;

    this.width = container.clientWidth;
    this.height = 400;

    this.canvas.width = this.width;
    this.canvas.height = this.height;
  }

  render(currentTime?: number): void {
    this.ctx.clearRect(0, 0, this.width, this.height);

    // Draw background
    this.ctx.fillStyle = '#f9f9f9';
    this.ctx.fillRect(0, 0, this.width, this.height);

    // Calculate scales
    const xScale = (this.width - 80) / this.score.totalDuration;
    const yScale = this.height / 2 / 60; // 60 MIDI notes range
    const xOffset = 40;
    const yOffset = this.height / 4;

    // Draw midpoint axis
    const midX = xOffset + this.midpoint * xScale;
    this.ctx.strokeStyle = '#e74c3c';
    this.ctx.lineWidth = 2;
    this.ctx.setLineDash([5, 5]);
    this.ctx.beginPath();
    this.ctx.moveTo(midX, 0);
    this.ctx.lineTo(midX, this.height);
    this.ctx.stroke();
    this.ctx.setLineDash([]);

    // Draw label for midpoint
    this.ctx.fillStyle = '#e74c3c';
    this.ctx.font = 'bold 12px sans-serif';
    this.ctx.textAlign = 'center';
    this.ctx.fillText('Temporal Midpoint', midX, 15);

    // Draw time axis
    this.ctx.strokeStyle = '#34495e';
    this.ctx.lineWidth = 1;
    this.ctx.beginPath();
    this.ctx.moveTo(xOffset, this.height / 2);
    this.ctx.lineTo(this.width - 40, this.height / 2);
    this.ctx.stroke();

    // Draw time markers
    this.ctx.fillStyle = '#7f8c8d';
    this.ctx.font = '10px sans-serif';
    this.ctx.textAlign = 'center';

    for (let i = 0; i <= this.score.totalDuration; i += 4) {
      const x = xOffset + i * xScale;
      this.ctx.beginPath();
      this.ctx.moveTo(x, this.height / 2 - 5);
      this.ctx.lineTo(x, this.height / 2 + 5);
      this.ctx.stroke();

      this.ctx.fillText(`${i}`, x, this.height / 2 + 20);
    }

    // Draw notes for each voice
    const colors = ['#3498db', '#2ecc71'];
    const yOffsets = [yOffset, yOffset * 3];

    this.score.voices.forEach((voice, voiceIndex) => {
      voice.notes.forEach((note, noteIndex) => {
        const x = xOffset + (note.start + note.duration / 2) * xScale;
        const y = yOffsets[voiceIndex];
        const pitchOffset = (note.pitch - 72) * yScale; // Center around C5

        const noteKey = `${voiceIndex}-${noteIndex}`;
        const isActive = this.activeNotes.has(noteKey);

        // Draw note circle
        this.ctx.fillStyle = isActive ? '#f39c12' : colors[voiceIndex];
        this.ctx.strokeStyle = '#34495e';
        this.ctx.lineWidth = isActive ? 2 : 1;

        const radius = Math.max(3, note.duration * xScale * 0.3);

        this.ctx.beginPath();
        this.ctx.arc(x, y + pitchOffset, radius, 0, Math.PI * 2);
        this.ctx.fill();
        this.ctx.stroke();
      });
    });

    // Draw symmetry connectors if highlighting is enabled
    if (this.highlightPairs && this.score.voices.length === 2) {
      this.drawSymmetryConnectors(xOffset, yOffsets, xScale, yScale);
    }

    // Draw current time indicator
    if (currentTime !== undefined) {
      const timeX = xOffset + currentTime * xScale;
      this.ctx.strokeStyle = '#9b59b6';
      this.ctx.lineWidth = 2;
      this.ctx.beginPath();
      this.ctx.moveTo(timeX, 0);
      this.ctx.lineTo(timeX, this.height);
      this.ctx.stroke();
    }

    // Draw legend
    this.drawLegend();
  }

  private drawSymmetryConnectors(
    xOffset: number,
    yOffsets: number[],
    xScale: number,
    yScale: number
  ): void {
    const voice1 = this.score.voices[0].notes;
    const voice2 = this.score.voices[1].notes;

    this.ctx.strokeStyle = 'rgba(149, 165, 166, 0.15)';
    this.ctx.lineWidth = 0.5;

    // Match notes by finding retrograde pairs
    for (const note1 of voice1) {
      const expectedEnd = this.score.totalDuration - note1.start;
      const expectedStart = expectedEnd - note1.duration;

      // Find matching note in voice 2
      for (const note2 of voice2) {
        if (
          Math.abs(note2.start - expectedStart) < 0.2 &&
          Math.abs(note2.duration - note1.duration) < 0.2 &&
          note1.pitch === note2.pitch
        ) {
          // Draw connector
          const x1 = xOffset + (note1.start + note1.duration / 2) * xScale;
          const y1 = yOffsets[0] + (note1.pitch - 72) * yScale;

          const x2 = xOffset + (note2.start + note2.duration / 2) * xScale;
          const y2 = yOffsets[1] + (note2.pitch - 72) * yScale;

          // Draw quadratic curve
          const cpX = (x1 + x2) / 2;
          const cpY = this.height / 2;

          this.ctx.beginPath();
          this.ctx.moveTo(x1, y1);
          this.ctx.quadraticCurveTo(cpX, cpY, x2, y2);
          this.ctx.stroke();

          break;
        }
      }
    }
  }

  private drawLegend(): void {
    const legendX = 10;
    const legendY = this.height - 60;

    this.ctx.font = '11px sans-serif';
    this.ctx.textAlign = 'left';

    // Voice 1
    this.ctx.fillStyle = '#3498db';
    this.ctx.beginPath();
    this.ctx.arc(legendX + 5, legendY, 4, 0, Math.PI * 2);
    this.ctx.fill();
    this.ctx.fillStyle = '#34495e';
    this.ctx.fillText('Voice 1 (Forward)', legendX + 15, legendY + 4);

    // Voice 2
    this.ctx.fillStyle = '#2ecc71';
    this.ctx.beginPath();
    this.ctx.arc(legendX + 5, legendY + 20, 4, 0, Math.PI * 2);
    this.ctx.fill();
    this.ctx.fillStyle = '#34495e';
    this.ctx.fillText('Voice 2 (Retrograde)', legendX + 15, legendY + 24);

    // Active note
    this.ctx.fillStyle = '#f39c12';
    this.ctx.beginPath();
    this.ctx.arc(legendX + 5, legendY + 40, 4, 0, Math.PI * 2);
    this.ctx.fill();
    this.ctx.fillStyle = '#34495e';
    this.ctx.fillText('Active Note', legendX + 15, legendY + 44);
  }

  setHighlightPairs(enabled: boolean): void {
    this.highlightPairs = enabled;
    this.render();
  }

  highlightNote(voiceIndex: number, noteIndex: number): void {
    const key = `${voiceIndex}-${noteIndex}`;
    this.activeNotes.add(key);

    // Auto-remove after a short duration
    setTimeout(() => {
      this.activeNotes.delete(key);
      this.render();
    }, 300);

    this.render();
  }

  updateTime(currentTime: number): void {
    this.render(currentTime);
  }
}
