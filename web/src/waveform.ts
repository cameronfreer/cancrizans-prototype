/**
 * Waveform visualization using Web Audio API
 */

import * as Tone from 'tone';

export class WaveformVisualizer {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private analyzer: Tone.Analyser;
  private animationId?: number;
  private width: number = 0;
  private height: number = 0;

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;

    const ctx = canvas.getContext('2d');
    if (!ctx) throw new Error('Could not get canvas context');
    this.ctx = ctx;

    // Create analyzer
    this.analyzer = new Tone.Analyser('waveform', 1024);
    Tone.getDestination().connect(this.analyzer);

    this.resize();
    this.startAnimation();
  }

  resize(): void {
    const container = this.canvas.parentElement;
    if (!container) return;

    this.width = container.clientWidth;
    this.height = 100; // Fixed height

    this.canvas.width = this.width;
    this.canvas.height = this.height;
  }

  private startAnimation(): void {
    const draw = () => {
      const values = this.analyzer.getValue() as Float32Array;

      // Clear canvas
      this.ctx.fillStyle = '#1a1a1a';
      this.ctx.fillRect(0, 0, this.width, this.height);

      // Draw waveform
      this.ctx.lineWidth = 2;
      this.ctx.strokeStyle = '#3498db';
      this.ctx.beginPath();

      const sliceWidth = this.width / values.length;
      let x = 0;

      for (let i = 0; i < values.length; i++) {
        const v = values[i];
        const y = (v + 1) * this.height / 2;

        if (i === 0) {
          this.ctx.moveTo(x, y);
        } else {
          this.ctx.lineTo(x, y);
        }

        x += sliceWidth;
      }

      this.ctx.lineTo(this.width, this.height / 2);
      this.ctx.stroke();

      // Draw center line
      this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
      this.ctx.lineWidth = 1;
      this.ctx.beginPath();
      this.ctx.moveTo(0, this.height / 2);
      this.ctx.lineTo(this.width, this.height / 2);
      this.ctx.stroke();

      this.animationId = requestAnimationFrame(draw);
    };

    draw();
  }

  stop(): void {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }
  }

  dispose(): void {
    this.stop();
    this.analyzer.dispose();
  }
}
