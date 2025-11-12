/**
 * Export and Share System
 * Save compositions as JSON, encode in URLs, or export as files
 */

import type { ParsedNote } from './midi_import.js';
import type { TransformationChain } from './transformation_composer.js';

export interface Composition {
  version: string;
  name: string;
  description: string;
  notes: ParsedNote[];
  transformations?: TransformationChain[];
  metadata: {
    created: Date;
    modified: Date;
    author?: string;
    bpm?: number;
    key?: string;
  };
}

export class ExportShareSystem {
  private readonly VERSION = '1.0.0';

  /**
   * Export composition as JSON string
   */
  exportToJSON(composition: Composition): string {
    const exportData = {
      ...composition,
      version: this.VERSION,
      metadata: {
        ...composition.metadata,
        created: composition.metadata.created.toISOString(),
        modified: composition.metadata.modified.toISOString()
      }
    };

    return JSON.stringify(exportData, null, 2);
  }

  /**
   * Import composition from JSON string
   */
  importFromJSON(json: string): Composition {
    const data = JSON.parse(json);

    // Validate version
    if (!data.version || data.version !== this.VERSION) {
      console.warn(`Version mismatch: expected ${this.VERSION}, got ${data.version}`);
    }

    return {
      ...data,
      metadata: {
        ...data.metadata,
        created: new Date(data.metadata.created),
        modified: new Date(data.metadata.modified)
      }
    };
  }

  /**
   * Export composition as downloadable JSON file
   */
  downloadJSON(composition: Composition, filename?: string): void {
    const json = this.exportToJSON(composition);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = filename || `${this.sanitizeFilename(composition.name)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  /**
   * Encode composition in URL parameters
   */
  encodeToURL(composition: Composition, baseURL?: string): string {
    const compressed = this.compressComposition(composition);
    const encoded = encodeURIComponent(compressed);

    const url = new URL(baseURL || window.location.href);
    url.searchParams.set('c', encoded);

    return url.toString();
  }

  /**
   * Decode composition from URL parameters
   */
  decodeFromURL(url?: string): Composition | null {
    const urlObj = new URL(url || window.location.href);
    const encoded = urlObj.searchParams.get('c');

    if (!encoded) {
      return null;
    }

    try {
      const compressed = decodeURIComponent(encoded);
      return this.decompressComposition(compressed);
    } catch (error) {
      console.error('Error decoding composition from URL:', error);
      return null;
    }
  }

  /**
   * Copy shareable link to clipboard
   */
  async copyShareLink(composition: Composition): Promise<boolean> {
    try {
      const url = this.encodeToURL(composition);
      await navigator.clipboard.writeText(url);
      return true;
    } catch (error) {
      console.error('Error copying to clipboard:', error);
      return false;
    }
  }

  /**
   * Export notes as MIDI file
   */
  async exportToMIDI(
    notes: ParsedNote[],
    filename?: string,
    tempo: number = 120
  ): Promise<void> {
    const midiData = this.notesToMIDI(notes, tempo);
    const blob = new Blob([midiData], { type: 'audio/midi' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = filename || 'composition.mid';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  /**
   * Convert notes to MIDI file format
   */
  private notesToMIDI(notes: ParsedNote[], tempo: number): ArrayBuffer {
    // MIDI file structure
    const header = this.createMIDIHeader(1, 1, 480); // Format 1, 1 track, 480 ticks/quarter
    const track = this.createMIDITrack(notes, tempo, 480);

    const result = new Uint8Array(header.length + track.length);
    result.set(header, 0);
    result.set(track, header.length);

    return result.buffer;
  }

  /**
   * Create MIDI header chunk
   */
  private createMIDIHeader(format: number, tracks: number, division: number): Uint8Array {
    const header = new Uint8Array(14);
    const view = new DataView(header.buffer);

    // "MThd" chunk
    header[0] = 0x4D; // 'M'
    header[1] = 0x54; // 'T'
    header[2] = 0x68; // 'h'
    header[3] = 0x64; // 'd'

    // Chunk size (6 bytes)
    view.setUint32(4, 6);

    // Format
    view.setUint16(8, format);

    // Number of tracks
    view.setUint16(10, tracks);

    // Division (ticks per quarter note)
    view.setUint16(12, division);

    return header;
  }

  /**
   * Create MIDI track chunk
   */
  private createMIDITrack(notes: ParsedNote[], tempo: number, division: number): Uint8Array {
    const events: number[] = [];

    // Tempo event
    events.push(...this.writeVariableLength(0)); // Delta time 0
    events.push(0xFF, 0x51, 0x03); // Tempo meta event
    const microsecondsPerQuarter = Math.round(60000000 / tempo);
    events.push(
      (microsecondsPerQuarter >> 16) & 0xFF,
      (microsecondsPerQuarter >> 8) & 0xFF,
      microsecondsPerQuarter & 0xFF
    );

    // Sort notes by time
    const sortedNotes = [...notes].sort((a, b) => a.time - b.time);

    // Convert notes to MIDI events
    let lastTime = 0;

    for (const note of sortedNotes) {
      const startTicks = Math.round(note.time * division);
      const endTicks = Math.round((note.time + note.duration) * division);

      // Note On
      const deltaOn = startTicks - lastTime;
      events.push(...this.writeVariableLength(deltaOn));
      events.push(0x90, note.pitch, note.velocity); // Note On, channel 0

      lastTime = startTicks;

      // Note Off
      const deltaOff = endTicks - lastTime;
      events.push(...this.writeVariableLength(deltaOff));
      events.push(0x80, note.pitch, 0x00); // Note Off, channel 0

      lastTime = endTicks;
    }

    // End of track
    events.push(...this.writeVariableLength(0));
    events.push(0xFF, 0x2F, 0x00);

    // Create track chunk
    const track = new Uint8Array(8 + events.length);
    const view = new DataView(track.buffer);

    // "MTrk" chunk
    track[0] = 0x4D; // 'M'
    track[1] = 0x54; // 'T'
    track[2] = 0x72; // 'r'
    track[3] = 0x6B; // 'k'

    // Chunk size
    view.setUint32(4, events.length);

    // Events
    track.set(events, 8);

    return track;
  }

  /**
   * Write variable-length quantity (MIDI format)
   */
  private writeVariableLength(value: number): number[] {
    const bytes: number[] = [];
    bytes.push(value & 0x7F);

    value >>= 7;
    while (value > 0) {
      bytes.unshift((value & 0x7F) | 0x80);
      value >>= 7;
    }

    return bytes;
  }

  /**
   * Compress composition for URL encoding
   */
  private compressComposition(composition: Composition): string {
    // Simplified representation for URL encoding
    const simplified = {
      n: composition.name,
      d: composition.notes.map(note => [
        note.pitch,
        note.velocity,
        Math.round(note.time * 1000),
        Math.round(note.duration * 1000)
      ]),
      m: {
        b: composition.metadata.bpm,
        k: composition.metadata.key
      }
    };

    // Convert to JSON and compress
    const json = JSON.stringify(simplified);

    // Simple base64 encoding (could use LZW or similar for better compression)
    return btoa(json);
  }

  /**
   * Decompress composition from URL encoding
   */
  private decompressComposition(compressed: string): Composition {
    try {
      const json = atob(compressed);
      const simplified = JSON.parse(json);

      return {
        version: this.VERSION,
        name: simplified.n || 'Shared Composition',
        description: 'Loaded from shared link',
        notes: simplified.d.map((n: number[]) => ({
          pitch: n[0],
          velocity: n[1],
          time: n[2] / 1000,
          duration: n[3] / 1000
        })),
        metadata: {
          created: new Date(),
          modified: new Date(),
          bpm: simplified.m?.b,
          key: simplified.m?.k
        }
      };
    } catch (error) {
      throw new Error('Invalid composition data');
    }
  }

  /**
   * Sanitize filename
   */
  private sanitizeFilename(filename: string): string {
    return filename
      .replace(/[^a-z0-9_-]/gi, '_')
      .replace(/_{2,}/g, '_')
      .toLowerCase()
      .slice(0, 50);
  }

  /**
   * Generate QR code for sharing (returns data URL)
   */
  async generateQRCode(composition: Composition): Promise<string> {
    const url = this.encodeToURL(composition);

    // Simple QR code generation (in production, use a library like qrcode.js)
    // For now, return a placeholder or use an API
    const qrAPIUrl = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${encodeURIComponent(url)}`;

    return qrAPIUrl;
  }

  /**
   * Save to localStorage
   */
  saveToLocalStorage(key: string, composition: Composition): void {
    try {
      const json = this.exportToJSON(composition);
      localStorage.setItem(`cancrizans_${key}`, json);
    } catch (error) {
      console.error('Error saving to localStorage:', error);
      throw new Error('Failed to save composition');
    }
  }

  /**
   * Load from localStorage
   */
  loadFromLocalStorage(key: string): Composition | null {
    try {
      const json = localStorage.getItem(`cancrizans_${key}`);
      if (!json) return null;

      return this.importFromJSON(json);
    } catch (error) {
      console.error('Error loading from localStorage:', error);
      return null;
    }
  }

  /**
   * List all saved compositions in localStorage
   */
  listSavedCompositions(): Array<{ key: string; name: string; modified: Date }> {
    const compositions: Array<{ key: string; name: string; modified: Date }> = [];

    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith('cancrizans_')) {
        try {
          const json = localStorage.getItem(key);
          if (json) {
            const composition = this.importFromJSON(json);
            compositions.push({
              key: key.replace('cancrizans_', ''),
              name: composition.name,
              modified: composition.metadata.modified
            });
          }
        } catch (error) {
          console.error(`Error loading composition ${key}:`, error);
        }
      }
    }

    return compositions.sort((a, b) => b.modified.getTime() - a.modified.getTime());
  }

  /**
   * Delete from localStorage
   */
  deleteFromLocalStorage(key: string): void {
    localStorage.removeItem(`cancrizans_${key}`);
  }
}
