/**
 * Export functionality for the web UI
 */

import { Score } from './scoreLoader';

export class Exporter {
  private score: Score;

  constructor(score: Score) {
    this.score = score;
  }

  /**
   * Export score as MIDI file (simplified - uses Tone.js recording)
   */
  async exportMIDI(): Promise<void> {
    alert('MIDI export from browser is coming soon! For now, use the Python CLI:\n\n' +
          'python -m cancrizans render --midi output.mid');
  }

  /**
   * Export current view as PNG image
   */
  async exportPNG(canvas: HTMLCanvasElement, filename: string = 'cancrizans.png'): Promise<void> {
    const dataURL = canvas.toDataURL('image/png');
    const link = document.createElement('a');
    link.href = dataURL;
    link.download = filename;
    link.click();
  }

  /**
   * Export score data as JSON
   */
  exportJSON(filename: string = 'score.json'): void {
    const dataStr = JSON.stringify(this.score, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);

    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();

    URL.revokeObjectURL(url);
  }

  /**
   * Export analysis results
   */
  exportAnalysis(filename: string = 'analysis.json'): void {
    const analysis = this.analyzeScore();
    const dataStr = JSON.stringify(analysis, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);

    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();

    URL.revokeObjectURL(url);
  }

  private analyzeScore(): any {
    const voice1 = this.score.voices[0];
    const voice2 = this.score.voices[1];

    return {
      metadata: {
        title: "Bach's Crab Canon (BWV 1079)",
        voices: this.score.voices.length,
        totalDuration: this.score.totalDuration,
        timeSignature: this.score.timeSignature,
      },
      statistics: {
        voice1: {
          notes: voice1.notes.length,
          averagePitch: voice1.notes.reduce((sum, n) => sum + n.pitch, 0) / voice1.notes.length,
          pitchRange: {
            lowest: Math.min(...voice1.notes.map(n => n.pitch)),
            highest: Math.max(...voice1.notes.map(n => n.pitch)),
          },
        },
        voice2: {
          notes: voice2.notes.length,
          averagePitch: voice2.notes.reduce((sum, n) => sum + n.pitch, 0) / voice2.notes.length,
          pitchRange: {
            lowest: Math.min(...voice2.notes.map(n => n.pitch)),
            highest: Math.max(...voice2.notes.map(n => n.pitch)),
          },
        },
      },
    };
  }

  /**
   * Share via Web Share API (mobile)
   */
  async share(): Promise<void> {
    if (!navigator.share) {
      alert('Web Share API not supported on this browser');
      return;
    }

    try {
      await navigator.share({
        title: "Bach's Crab Canon",
        text: 'Check out this interactive palindromic canon explorer!',
        url: window.location.href,
      });
    } catch (err) {
      console.log('Share cancelled or failed:', err);
    }
  }
}
