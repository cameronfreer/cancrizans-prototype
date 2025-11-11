/**
 * Musical notation rendering using VexFlow
 */

import { Factory, Stave, StaveNote, Voice, Formatter, Renderer } from 'vexflow';
import { Score, Note } from './scoreLoader';

export class NotationRenderer {
  private container: HTMLElement;
  private score: Score;
  private renderer?: Renderer;
  private context?: any;

  constructor(container: HTMLElement, score: Score) {
    this.container = container;
    this.score = score;
  }

  render(): void {
    // Clear container
    this.container.innerHTML = '';

    const width = this.container.clientWidth || 1000;
    const height = 600;

    // Create VexFlow renderer
    this.renderer = new Renderer(this.container, Renderer.Backends.SVG);
    this.renderer.resize(width, height);
    this.context = this.renderer.getContext();

    // Render both voices on separate staves
    const staveHeight = 120;
    const staveWidth = width - 40;
    const margin = 20;

    // Group notes by measures (4 quarter notes per measure)
    const measuresPerLine = 3;
    const measureWidth = staveWidth / measuresPerLine;

    // Voice 1 (top staff)
    this.renderVoice(
      this.score.voices[0].notes,
      margin,
      margin,
      measureWidth,
      measuresPerLine,
      'Voice 1 (Forward)'
    );

    // Voice 2 (bottom staff)
    this.renderVoice(
      this.score.voices[1].notes,
      margin,
      margin + staveHeight + 80,
      measureWidth,
      measuresPerLine,
      'Voice 2 (Retrograde)'
    );
  }

  private renderVoice(
    notes: Note[],
    x: number,
    y: number,
    measureWidth: number,
    measuresPerLine: number,
    label: string
  ): void {
    if (!this.context) return;

    // Group notes into measures (4 beats each)
    const measures: Note[][] = [];
    let currentMeasure: Note[] = [];
    let currentBeat = 0;

    for (const note of notes) {
      const measureStart = Math.floor(note.start / 4) * 4;
      const measureBeat = note.start - measureStart;

      if (measureBeat < currentBeat || currentBeat === 0) {
        if (currentMeasure.length > 0) {
          measures.push([...currentMeasure]);
        }
        currentMeasure = [];
        currentBeat = 0;
      }

      currentMeasure.push(note);
      currentBeat = measureBeat + note.duration;
    }

    if (currentMeasure.length > 0) {
      measures.push(currentMeasure);
    }

    // Render measures
    let currentX = x;
    let currentY = y;
    let measureIndex = 0;

    for (const measure of measures) {
      // Create stave
      const stave = new Stave(currentX, currentY, measureWidth);

      // Add clef and time signature to first measure
      if (measureIndex === 0) {
        stave.addClef('treble');
        stave.addTimeSignature('4/4');
        stave.addKeySignature('Bb'); // F major (1 flat)
        stave.setText(label, 3);
      }

      stave.setContext(this.context).draw();

      // Convert notes to VexFlow format
      try {
        const vfNotes = this.convertToVexFlowNotes(measure);

        if (vfNotes.length > 0) {
          const voice = new Voice({ num_beats: 4, beat_value: 4 });
          voice.addTickables(vfNotes);

          new Formatter()
            .joinVoices([voice])
            .format([voice], measureWidth - 50);

          voice.draw(this.context, stave);
        }
      } catch (error) {
        console.warn('Error rendering measure:', error);
      }

      // Move to next measure position
      currentX += measureWidth;
      measureIndex++;

      if (measureIndex % measuresPerLine === 0) {
        currentX = x;
        currentY += 120;
      }
    }
  }

  private convertToVexFlowNotes(notes: Note[]): StaveNote[] {
    const vfNotes: StaveNote[] = [];

    for (const note of notes) {
      try {
        // Convert MIDI to note name
        const noteName = this.midiToVexFlow(note.pitch);

        // Convert duration to VexFlow duration
        const duration = this.durationToVexFlow(note.duration);

        const staveNote = new StaveNote({
          keys: [noteName],
          duration: duration,
        });

        // Add accidentals if needed
        if (noteName.includes('b') || noteName.includes('#')) {
          const accidental = noteName.includes('b') ? 'b' : '#';
          staveNote.addModifier(0, new (VexFlow as any).Accidental(accidental));
        }

        vfNotes.push(staveNote);
      } catch (error) {
        console.warn('Error converting note:', note, error);
      }
    }

    return vfNotes;
  }

  private midiToVexFlow(midi: number): string {
    const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
    const octave = Math.floor(midi / 12) - 1;
    const noteName = notes[midi % 12];

    // Convert sharps to flats for F major context
    let adjustedNote = noteName;
    if (noteName === 'G#') adjustedNote = 'Ab';
    if (noteName === 'A#') adjustedNote = 'Bb';
    if (noteName === 'D#') adjustedNote = 'Eb';

    return `${adjustedNote}/${octave}`;
  }

  private durationToVexFlow(quarterLength: number): string {
    // VexFlow durations: w (whole), h (half), q (quarter), 8 (eighth), etc.
    if (quarterLength >= 4) return 'w';
    if (quarterLength >= 2) return 'h';
    if (quarterLength >= 1) return 'q';
    if (quarterLength >= 0.5) return '8';
    if (quarterLength >= 0.25) return '16';
    return '32';
  }

  highlightNote(voiceIndex: number, noteIndex: number): void {
    // TODO: Implement note highlighting
    // This would require tracking rendered notes and applying CSS classes
  }
}

// Polyfill for VexFlow if needed
declare global {
  interface Window {
    VexFlow: any;
  }
}

const VexFlow = window.VexFlow || {
  Accidental: class {
    constructor(type: string) {}
  },
};
