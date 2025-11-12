/**
 * MIDI File Import System
 * Allows users to upload and analyze their own MIDI files
 */

export interface ParsedNote {
  pitch: number;
  velocity: number;
  time: number;
  duration: number;
}

export interface MidiFileInfo {
  name: string;
  notes: ParsedNote[];
  tempo: number;
  timeSignature: { numerator: number; denominator: number };
  duration: number;
  trackCount: number;
}

export class MidiImporter {
  private fileInput: HTMLInputElement;
  private dropZone: HTMLElement;
  private onImportCallback?: (info: MidiFileInfo) => void;

  constructor() {
    this.fileInput = document.getElementById('midi-upload') as HTMLInputElement;
    this.dropZone = document.getElementById('midi-drop-zone') as HTMLElement;

    this.setupEventListeners();
  }

  private setupEventListeners(): void {
    // File input change
    this.fileInput?.addEventListener('change', (e) => {
      const target = e.target as HTMLInputElement;
      if (target.files && target.files.length > 0) {
        this.handleFile(target.files[0]);
      }
    });

    // Drag and drop
    if (this.dropZone) {
      this.dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        this.dropZone.classList.add('drag-over');
      });

      this.dropZone.addEventListener('dragleave', () => {
        this.dropZone.classList.remove('drag-over');
      });

      this.dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        this.dropZone.classList.remove('drag-over');

        if (e.dataTransfer?.files && e.dataTransfer.files.length > 0) {
          this.handleFile(e.dataTransfer.files[0]);
        }
      });
    }
  }

  onImport(callback: (info: MidiFileInfo) => void): void {
    this.onImportCallback = callback;
  }

  private async handleFile(file: File): Promise<void> {
    if (!file.name.endsWith('.mid') && !file.name.endsWith('.midi')) {
      alert('Please upload a MIDI file (.mid or .midi)');
      return;
    }

    try {
      const arrayBuffer = await file.arrayBuffer();
      const midiData = this.parseMidiFile(arrayBuffer);

      if (this.onImportCallback) {
        this.onImportCallback(midiData);
      }
    } catch (error) {
      console.error('Error parsing MIDI file:', error);
      alert('Error parsing MIDI file. Please ensure it is a valid MIDI file.');
    }
  }

  private parseMidiFile(arrayBuffer: ArrayBuffer): MidiFileInfo {
    const view = new DataView(arrayBuffer);
    let offset = 0;

    // Parse MIDI header
    const headerChunk = this.readString(view, offset, 4);
    if (headerChunk !== 'MThd') {
      throw new Error('Invalid MIDI file: Missing MThd header');
    }
    offset += 4;

    // Skip header length and format
    offset += 4; // header length
    offset += 2; // format

    const trackCount = view.getUint16(offset);
    offset += 2;

    const division = view.getUint16(offset);
    offset += 2;

    // Parse tracks
    const notes: ParsedNote[] = [];
    let tempo = 120; // Default tempo
    const timeSignature = { numerator: 4, denominator: 4 };
    let maxTime = 0;

    for (let i = 0; i < trackCount; i++) {
      const trackResult = this.parseTrack(view, offset, division, tempo);
      notes.push(...trackResult.notes);
      offset = trackResult.nextOffset;

      if (trackResult.tempo) {
        tempo = trackResult.tempo;
      }

      for (const note of trackResult.notes) {
        maxTime = Math.max(maxTime, note.time + note.duration);
      }
    }

    return {
      name: 'Uploaded MIDI',
      notes,
      tempo,
      timeSignature,
      duration: maxTime,
      trackCount
    };
  }

  private parseTrack(
    view: DataView,
    startOffset: number,
    division: number,
    _baseTempo: number
  ): { notes: ParsedNote[]; nextOffset: number; tempo?: number } {
    let offset = startOffset;

    // Read track header
    const trackHeader = this.readString(view, offset, 4);
    if (trackHeader !== 'MTrk') {
      throw new Error('Invalid MIDI track: Missing MTrk header');
    }
    offset += 4;

    const trackLength = view.getUint32(offset);
    offset += 4;

    const trackEnd = offset + trackLength;
    const notes: ParsedNote[] = [];
    const activeNotes = new Map<number, { time: number; velocity: number }>();

    let currentTime = 0;
    let runningStatus = 0;
    let tempo: number | undefined = undefined;

    while (offset < trackEnd) {
      // Read delta time
      const { value: deltaTime, bytesRead } = this.readVariableLength(view, offset);
      offset += bytesRead;
      currentTime += deltaTime;

      // Read status byte
      let statusByte = view.getUint8(offset);

      // Handle running status
      if ((statusByte & 0x80) === 0) {
        statusByte = runningStatus;
      } else {
        offset++;
        runningStatus = statusByte;
      }

      const messageType = statusByte & 0xF0;
      // Channel info not needed for basic note parsing

      // Note On
      if (messageType === 0x90) {
        const pitch = view.getUint8(offset++);
        const velocity = view.getUint8(offset++);

        if (velocity > 0) {
          activeNotes.set(pitch, {
            time: currentTime / division,
            velocity
          });
        } else {
          // Velocity 0 = Note Off
          const noteStart = activeNotes.get(pitch);
          if (noteStart) {
            notes.push({
              pitch,
              velocity: noteStart.velocity,
              time: noteStart.time,
              duration: (currentTime / division) - noteStart.time
            });
            activeNotes.delete(pitch);
          }
        }
      }
      // Note Off
      else if (messageType === 0x80) {
        const pitch = view.getUint8(offset++);
        offset++; // skip velocity

        const noteStart = activeNotes.get(pitch);
        if (noteStart) {
          notes.push({
            pitch,
            velocity: noteStart.velocity,
            time: noteStart.time,
            duration: (currentTime / division) - noteStart.time
          });
          activeNotes.delete(pitch);
        }
      }
      // Meta Event
      else if (statusByte === 0xFF) {
        const metaType = view.getUint8(offset++);
        const { value: metaLength, bytesRead: metaBytesRead } = this.readVariableLength(view, offset);
        offset += metaBytesRead;

        // Tempo change
        if (metaType === 0x51 && metaLength === 3) {
          const microsecondsPerQuarter =
            (view.getUint8(offset) << 16) |
            (view.getUint8(offset + 1) << 8) |
            view.getUint8(offset + 2);
          tempo = Math.round(60000000 / microsecondsPerQuarter);
        }

        offset += metaLength;
      }
      // Other events (skip)
      else {
        // Control Change, Program Change, etc.
        const paramCount = this.getMessageParameterCount(messageType);
        offset += paramCount;
      }
    }

    return { notes, nextOffset: offset, tempo };
  }

  private getMessageParameterCount(messageType: number): number {
    switch (messageType) {
      case 0x80: // Note Off
      case 0x90: // Note On
      case 0xA0: // Aftertouch
      case 0xB0: // Control Change
      case 0xE0: // Pitch Bend
        return 2;
      case 0xC0: // Program Change
      case 0xD0: // Channel Pressure
        return 1;
      default:
        return 0;
    }
  }

  private readVariableLength(view: DataView, offset: number): { value: number; bytesRead: number } {
    let value = 0;
    let bytesRead = 0;
    let byte: number;

    do {
      byte = view.getUint8(offset + bytesRead);
      value = (value << 7) | (byte & 0x7F);
      bytesRead++;
    } while ((byte & 0x80) !== 0 && bytesRead < 4);

    return { value, bytesRead };
  }

  private readString(view: DataView, offset: number, length: number): string {
    let result = '';
    for (let i = 0; i < length; i++) {
      result += String.fromCharCode(view.getUint8(offset + i));
    }
    return result;
  }

  triggerFileSelect(): void {
    this.fileInput?.click();
  }
}
