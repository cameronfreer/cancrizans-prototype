/**
 * Transformation Composer
 * Chain multiple transformations to create complex musical patterns
 */

import type { ParsedNote } from './midi_import.js';

export type TransformationType =
  | 'retrograde'
  | 'inversion'
  | 'augmentation'
  | 'diminution'
  | 'transpose'
  | 'reflect'
  | 'repeat'
  | 'interleave';

export interface Transformation {
  type: TransformationType;
  parameters: Record<string, number>;
  description: string;
}

export interface TransformationChain {
  id: string;
  name: string;
  transformations: Transformation[];
  created: Date;
}

export class TransformationComposer {
  private chains: Map<string, TransformationChain> = new Map();
  private nextId = 1;

  /**
   * Create a new transformation chain
   */
  createChain(name: string): string {
    const id = `chain-${this.nextId++}`;
    this.chains.set(id, {
      id,
      name,
      transformations: [],
      created: new Date()
    });
    return id;
  }

  /**
   * Add a transformation to a chain
   */
  addTransformation(
    chainId: string,
    type: TransformationType,
    parameters: Record<string, number> = {}
  ): void {
    const chain = this.chains.get(chainId);
    if (!chain) {
      throw new Error(`Chain ${chainId} not found`);
    }

    chain.transformations.push({
      type,
      parameters,
      description: this.getTransformationDescription(type, parameters)
    });
  }

  /**
   * Apply a transformation chain to notes
   */
  applyChain(chainId: string, notes: ParsedNote[]): ParsedNote[] {
    const chain = this.chains.get(chainId);
    if (!chain) {
      throw new Error(`Chain ${chainId} not found`);
    }

    let result = [...notes];

    for (const transformation of chain.transformations) {
      result = this.applyTransformation(result, transformation);
    }

    return result;
  }

  /**
   * Apply a single transformation
   */
  private applyTransformation(
    notes: ParsedNote[],
    transformation: Transformation
  ): ParsedNote[] {
    switch (transformation.type) {
      case 'retrograde':
        return this.retrograde(notes);

      case 'inversion':
        return this.inversion(notes, transformation.parameters.axis || 60);

      case 'augmentation':
        return this.augmentation(notes, transformation.parameters.factor || 2);

      case 'diminution':
        return this.diminution(notes, transformation.parameters.factor || 2);

      case 'transpose':
        return this.transpose(notes, transformation.parameters.semitones || 0);

      case 'reflect':
        return this.reflect(notes, transformation.parameters.axis || 60);

      case 'repeat':
        return this.repeat(notes, transformation.parameters.times || 2);

      case 'interleave':
        return this.interleave(notes, this.retrograde(notes));

      default:
        return notes;
    }
  }

  /**
   * Retrograde: reverse the order of notes
   */
  private retrograde(notes: ParsedNote[]): ParsedNote[] {
    if (notes.length === 0) return [];

    const maxTime = Math.max(...notes.map(n => n.time + n.duration));
    const reversed = [...notes].reverse();

    return reversed.map((note) => ({
      ...note,
      time: maxTime - (note.time + note.duration)
    }));
  }

  /**
   * Inversion: flip pitches around an axis
   */
  private inversion(notes: ParsedNote[], axis: number): ParsedNote[] {
    return notes.map(note => ({
      ...note,
      pitch: Math.max(0, Math.min(127, 2 * axis - note.pitch))
    }));
  }

  /**
   * Augmentation: stretch time by a factor
   */
  private augmentation(notes: ParsedNote[], factor: number): ParsedNote[] {
    return notes.map(note => ({
      ...note,
      time: note.time * factor,
      duration: note.duration * factor
    }));
  }

  /**
   * Diminution: compress time by a factor
   */
  private diminution(notes: ParsedNote[], factor: number): ParsedNote[] {
    return notes.map(note => ({
      ...note,
      time: note.time / factor,
      duration: note.duration / factor
    }));
  }

  /**
   * Transpose: shift all pitches by semitones
   */
  private transpose(notes: ParsedNote[], semitones: number): ParsedNote[] {
    return notes.map(note => ({
      ...note,
      pitch: Math.max(0, Math.min(127, note.pitch + semitones))
    }));
  }

  /**
   * Reflect: mirror both time and pitch
   */
  private reflect(notes: ParsedNote[], pitchAxis: number): ParsedNote[] {
    const retrograded = this.retrograde(notes);
    return this.inversion(retrograded, pitchAxis);
  }

  /**
   * Repeat: repeat the sequence multiple times
   */
  private repeat(notes: ParsedNote[], times: number): ParsedNote[] {
    if (notes.length === 0) return [];

    const duration = Math.max(...notes.map(n => n.time + n.duration));
    const result: ParsedNote[] = [];

    for (let repeatIndex = 0; repeatIndex < times; repeatIndex++) {
      result.push(
        ...notes.map(note => ({
          ...note,
          time: note.time + (duration * repeatIndex)
        }))
      );
    }

    return result;
  }

  /**
   * Interleave: alternate between two sequences
   */
  private interleave(notes1: ParsedNote[], notes2: ParsedNote[]): ParsedNote[] {
    const result: ParsedNote[] = [];
    const maxLength = Math.max(notes1.length, notes2.length);

    for (let i = 0; i < maxLength; i++) {
      if (i < notes1.length) {
        result.push(notes1[i]);
      }
      if (i < notes2.length) {
        result.push(notes2[i]);
      }
    }

    // Re-sort by time
    return result.sort((a, b) => a.time - b.time);
  }

  /**
   * Get human-readable description of transformation
   */
  private getTransformationDescription(
    type: TransformationType,
    parameters: Record<string, number>
  ): string {
    switch (type) {
      case 'retrograde':
        return 'Reverse note order (play backwards)';

      case 'inversion':
        return `Invert pitches around ${parameters.axis || 60} (${this.midiToNoteName(parameters.axis || 60)})`;

      case 'augmentation':
        return `Stretch time by ${parameters.factor || 2}x`;

      case 'diminution':
        return `Compress time by ${parameters.factor || 2}x`;

      case 'transpose':
        const direction = (parameters.semitones || 0) > 0 ? 'up' : 'down';
        return `Transpose ${Math.abs(parameters.semitones || 0)} semitones ${direction}`;

      case 'reflect':
        return `Reflect both time and pitch (crab + inversion)`;

      case 'repeat':
        return `Repeat ${parameters.times || 2} times`;

      case 'interleave':
        return 'Interleave with retrograde';

      default:
        return type;
    }
  }

  /**
   * Get all chains
   */
  getAllChains(): TransformationChain[] {
    return Array.from(this.chains.values());
  }

  /**
   * Get a specific chain
   */
  getChain(chainId: string): TransformationChain | undefined {
    return this.chains.get(chainId);
  }

  /**
   * Delete a chain
   */
  deleteChain(chainId: string): void {
    this.chains.delete(chainId);
  }

  /**
   * Export chain as JSON
   */
  exportChain(chainId: string): string {
    const chain = this.chains.get(chainId);
    if (!chain) {
      throw new Error(`Chain ${chainId} not found`);
    }
    return JSON.stringify(chain, null, 2);
  }

  /**
   * Import chain from JSON
   */
  importChain(json: string): string {
    const chain = JSON.parse(json) as TransformationChain;
    chain.id = `chain-${this.nextId++}`; // Assign new ID
    chain.created = new Date(chain.created); // Parse date
    this.chains.set(chain.id, chain);
    return chain.id;
  }

  /**
   * Create a classic crab canon (retrograde)
   */
  createCrabCanon(): string {
    const chainId = this.createChain('Crab Canon');
    this.addTransformation(chainId, 'retrograde');
    return chainId;
  }

  /**
   * Create a table canon (mirror + inversion)
   */
  createTableCanon(): string {
    const chainId = this.createChain('Table Canon');
    this.addTransformation(chainId, 'reflect', { axis: 60 });
    return chainId;
  }

  /**
   * Create a complex transformation example
   */
  createComplexExample(): string {
    const chainId = this.createChain('Complex Transformation');
    this.addTransformation(chainId, 'transpose', { semitones: 7 }); // Up a fifth
    this.addTransformation(chainId, 'augmentation', { factor: 1.5 }); // Slower
    this.addTransformation(chainId, 'retrograde'); // Reverse
    this.addTransformation(chainId, 'inversion', { axis: 65 }); // Invert
    return chainId;
  }

  /**
   * Convert MIDI note number to note name
   */
  private midiToNoteName(midi: number): string {
    const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
    const octave = Math.floor(midi / 12) - 1;
    const note = noteNames[midi % 12];
    return `${note}${octave}`;
  }
}
