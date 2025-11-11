/**
 * Interactive Canon Composer
 * Click-to-add notes with real-time retrograde generation
 */

export interface ComposerNote {
  pitch: number; // MIDI note number
  time: number; // Time in quarter notes from start
  duration: number; // Duration in quarter notes
  id: string;
}

export interface Template {
  name: string;
  description: string;
  notes: Omit<ComposerNote, 'id'>[];
}

export class CanonComposer {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private notes: ComposerNote[] = [];
  private selectedNote: ComposerNote | null = null;
  private isDragging: boolean = false;

  // Grid settings
  private readonly gridWidth: number = 32; // Pixels per quarter note
  private readonly noteHeight: number = 8; // Pixels per semitone
  private readonly minPitch: number = 48; // C3
  private readonly maxPitch: number = 84; // C6
  private readonly maxTime: number = 32; // 32 quarter notes max

  // Current edit mode
  private snapToGrid: boolean = true;
  private currentDuration: number = 1.0; // quarter note

  // Callbacks
  private onNotesChange?: (notes: ComposerNote[]) => void;

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;
    const ctx = canvas.getContext('2d');
    if (!ctx) throw new Error('Could not get canvas context');
    this.ctx = ctx;

    this.resize();
    this.setupEventListeners();
    this.draw();
  }

  resize(): void {
    const container = this.canvas.parentElement;
    if (!container) return;

    this.canvas.width = this.maxTime * this.gridWidth;
    this.canvas.height = (this.maxPitch - this.minPitch + 1) * this.noteHeight;
  }

  private setupEventListeners(): void {
    this.canvas.addEventListener('mousedown', this.handleMouseDown.bind(this));
    this.canvas.addEventListener('mousemove', this.handleMouseMove.bind(this));
    this.canvas.addEventListener('mouseup', this.handleMouseUp.bind(this));
    this.canvas.addEventListener('mouseleave', this.handleMouseUp.bind(this));
  }

  private handleMouseDown(e: MouseEvent): void {
    const rect = this.canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Check if clicking existing note
    const clickedNote = this.findNoteAtPosition(x, y);

    if (clickedNote) {
      if (e.shiftKey) {
        // Delete note with shift+click
        this.removeNote(clickedNote.id);
      } else {
        // Select note for dragging
        this.selectedNote = clickedNote;
        this.isDragging = true;
      }
    } else {
      // Add new note
      const time = this.snapToGrid
        ? Math.round(x / this.gridWidth * 4) / 4
        : x / this.gridWidth;
      const pitch = this.maxPitch - Math.round(y / this.noteHeight);

      if (pitch >= this.minPitch && pitch <= this.maxPitch && time >= 0 && time < this.maxTime) {
        this.addNote(pitch, time, this.currentDuration);
      }
    }

    this.draw();
  }

  private handleMouseMove(e: MouseEvent): void {
    if (!this.isDragging || !this.selectedNote) return;

    const rect = this.canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const time = this.snapToGrid
      ? Math.round(x / this.gridWidth * 4) / 4
      : x / this.gridWidth;
    const pitch = this.maxPitch - Math.round(y / this.noteHeight);

    if (pitch >= this.minPitch && pitch <= this.maxPitch && time >= 0 && time < this.maxTime) {
      this.selectedNote.pitch = pitch;
      this.selectedNote.time = time;
      this.notifyChange();
    }

    this.draw();
  }

  private handleMouseUp(): void {
    this.isDragging = false;
    this.selectedNote = null;
  }

  private findNoteAtPosition(x: number, y: number): ComposerNote | null {
    for (const note of this.notes) {
      const noteX = note.time * this.gridWidth;
      const noteY = (this.maxPitch - note.pitch) * this.noteHeight;
      const noteWidth = note.duration * this.gridWidth;

      if (x >= noteX && x <= noteX + noteWidth &&
          y >= noteY && y <= noteY + this.noteHeight) {
        return note;
      }
    }

    return null;
  }

  addNote(pitch: number, time: number, duration: number): void {
    const note: ComposerNote = {
      pitch,
      time,
      duration,
      id: `note-${Date.now()}-${Math.random()}`,
    };
    this.notes.push(note);
    this.notifyChange();
    this.draw();
  }

  removeNote(id: string): void {
    this.notes = this.notes.filter(n => n.id !== id);
    this.notifyChange();
    this.draw();
  }

  clearAll(): void {
    this.notes = [];
    this.notifyChange();
    this.draw();
  }

  getNotes(): ComposerNote[] {
    return [...this.notes];
  }

  setNotes(notes: ComposerNote[]): void {
    this.notes = [...notes];
    this.draw();
    this.notifyChange();
  }

  loadTemplate(template: Template): void {
    this.notes = template.notes.map(n => ({
      ...n,
      id: `note-${Date.now()}-${Math.random()}`,
    }));
    this.notifyChange();
    this.draw();
  }

  getRetrogradeNotes(): ComposerNote[] {
    if (this.notes.length === 0) return [];

    // Find total duration
    const maxEnd = Math.max(...this.notes.map(n => n.time + n.duration));

    // Create retrograde
    return this.notes.map(n => ({
      ...n,
      time: maxEnd - (n.time + n.duration),
      id: `retro-${n.id}`,
    }));
  }

  getSuggestedNotes(): number[] {
    // Constraint solver: suggest pitches that work well
    // For now, suggest notes from same scale as existing notes
    if (this.notes.length === 0) {
      // Default to C major scale
      return [60, 62, 64, 65, 67, 69, 71, 72]; // C4-C5
    }

    // Extract unique pitches and suggest nearby scale degrees
    const pitches = new Set(this.notes.map(n => n.pitch));
    const suggestions = new Set<number>();

    for (const pitch of pitches) {
      // Add steps and leaps within scale
      suggestions.add(pitch);
      suggestions.add(pitch + 2); // whole step
      suggestions.add(pitch - 2);
      suggestions.add(pitch + 4); // third
      suggestions.add(pitch - 4);
      suggestions.add(pitch + 7); // fifth
      suggestions.add(pitch - 7);
    }

    return Array.from(suggestions)
      .filter(p => p >= this.minPitch && p <= this.maxPitch)
      .sort((a, b) => a - b);
  }

  setSnapToGrid(snap: boolean): void {
    this.snapToGrid = snap;
  }

  setDuration(duration: number): void {
    this.currentDuration = duration;
  }

  onUpdate(callback: (notes: ComposerNote[]) => void): void {
    this.onNotesChange = callback;
  }

  private notifyChange(): void {
    if (this.onNotesChange) {
      this.onNotesChange(this.getNotes());
    }
  }

  private draw(): void {
    // Clear
    this.ctx.fillStyle = '#1a1a1a';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Draw grid
    this.drawGrid();

    // Draw notes
    this.drawNotes(this.notes, '#3498db', 0.8);

    // Draw retrograde preview (lighter)
    const retroNotes = this.getRetrogradeNotes();
    this.drawNotes(retroNotes, '#e74c3c', 0.3);
  }

  private drawGrid(): void {
    this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
    this.ctx.lineWidth = 1;

    // Vertical lines (time)
    for (let t = 0; t <= this.maxTime; t++) {
      const x = t * this.gridWidth;
      this.ctx.globalAlpha = t % 4 === 0 ? 0.3 : 0.1;
      this.ctx.beginPath();
      this.ctx.moveTo(x, 0);
      this.ctx.lineTo(x, this.canvas.height);
      this.ctx.stroke();
    }

    // Horizontal lines (pitch)
    const pitchNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
    for (let p = this.minPitch; p <= this.maxPitch; p++) {
      const y = (this.maxPitch - p) * this.noteHeight;
      const isWhiteKey = ![1, 3, 6, 8, 10].includes(p % 12);
      this.ctx.globalAlpha = isWhiteKey ? 0.2 : 0.1;
      this.ctx.beginPath();
      this.ctx.moveTo(0, y);
      this.ctx.lineTo(this.canvas.width, y);
      this.ctx.stroke();

      // Draw pitch labels on C notes
      if (p % 12 === 0) {
        this.ctx.globalAlpha = 0.5;
        this.ctx.fillStyle = '#fff';
        this.ctx.font = '10px monospace';
        const octave = Math.floor(p / 12) - 1;
        this.ctx.fillText(`${pitchNames[p % 12]}${octave}`, 2, y + 10);
      }
    }

    this.ctx.globalAlpha = 1.0;
  }

  private drawNotes(notes: ComposerNote[], color: string, alpha: number): void {
    this.ctx.globalAlpha = alpha;
    this.ctx.fillStyle = color;

    for (const note of notes) {
      const x = note.time * this.gridWidth;
      const y = (this.maxPitch - note.pitch) * this.noteHeight;
      const width = note.duration * this.gridWidth;
      const height = this.noteHeight;

      this.ctx.fillRect(x, y, width, height);

      // Draw border
      this.ctx.strokeStyle = color;
      this.ctx.lineWidth = 1;
      this.ctx.strokeRect(x, y, width, height);
    }

    this.ctx.globalAlpha = 1.0;
  }

  dispose(): void {
    // Clean up event listeners if needed
  }
}

// Template library
export const TEMPLATES: Template[] = [
  {
    name: 'C Major Scale',
    description: 'Simple ascending C major scale',
    notes: [
      { pitch: 60, time: 0, duration: 0.5 },   // C4
      { pitch: 62, time: 0.5, duration: 0.5 }, // D4
      { pitch: 64, time: 1, duration: 0.5 },   // E4
      { pitch: 65, time: 1.5, duration: 0.5 }, // F4
      { pitch: 67, time: 2, duration: 0.5 },   // G4
      { pitch: 69, time: 2.5, duration: 0.5 }, // A4
      { pitch: 71, time: 3, duration: 0.5 },   // B4
      { pitch: 72, time: 3.5, duration: 1.0 }, // C5
    ],
  },
  {
    name: 'Arpeggio',
    description: 'C major arpeggio pattern',
    notes: [
      { pitch: 60, time: 0, duration: 0.5 },    // C4
      { pitch: 64, time: 0.5, duration: 0.5 },  // E4
      { pitch: 67, time: 1, duration: 0.5 },    // G4
      { pitch: 72, time: 1.5, duration: 0.5 },  // C5
      { pitch: 76, time: 2, duration: 0.5 },    // E5
      { pitch: 72, time: 2.5, duration: 0.5 },  // C5
      { pitch: 67, time: 3, duration: 0.5 },    // G4
      { pitch: 64, time: 3.5, duration: 0.5 },  // E4
      { pitch: 60, time: 4, duration: 1.0 },    // C4
    ],
  },
  {
    name: 'Stepwise Melody',
    description: 'Smooth melodic motion',
    notes: [
      { pitch: 67, time: 0, duration: 0.5 },    // G4
      { pitch: 69, time: 0.5, duration: 0.5 },  // A4
      { pitch: 71, time: 1, duration: 0.5 },    // B4
      { pitch: 72, time: 1.5, duration: 0.5 },  // C5
      { pitch: 74, time: 2, duration: 1.0 },    // D5
      { pitch: 72, time: 3, duration: 0.5 },    // C5
      { pitch: 71, time: 3.5, duration: 0.5 },  // B4
      { pitch: 69, time: 4, duration: 0.5 },    // A4
      { pitch: 67, time: 4.5, duration: 0.5 },  // G4
      { pitch: 66, time: 5, duration: 0.5 },    // F#4
      { pitch: 67, time: 5.5, duration: 1.5 },  // G4
    ],
  },
  {
    name: 'Rhythmic Pattern',
    description: 'Interesting rhythm on single pitch',
    notes: [
      { pitch: 72, time: 0, duration: 0.25 },
      { pitch: 72, time: 0.25, duration: 0.25 },
      { pitch: 72, time: 0.5, duration: 0.5 },
      { pitch: 72, time: 1, duration: 1.0 },
      { pitch: 72, time: 2, duration: 0.5 },
      { pitch: 72, time: 2.5, duration: 0.25 },
      { pitch: 72, time: 2.75, duration: 0.25 },
      { pitch: 72, time: 3, duration: 2.0 },
    ],
  },
  {
    name: 'Chromatic Run',
    description: 'Chromatic scale passage',
    notes: [
      { pitch: 60, time: 0, duration: 0.375 },
      { pitch: 61, time: 0.375, duration: 0.375 },
      { pitch: 62, time: 0.75, duration: 0.375 },
      { pitch: 63, time: 1.125, duration: 0.375 },
      { pitch: 64, time: 1.5, duration: 0.375 },
      { pitch: 65, time: 1.875, duration: 0.375 },
      { pitch: 66, time: 2.25, duration: 0.375 },
      { pitch: 67, time: 2.625, duration: 0.375 },
      { pitch: 68, time: 3, duration: 0.375 },
      { pitch: 69, time: 3.375, duration: 0.375 },
      { pitch: 70, time: 3.75, duration: 0.375 },
      { pitch: 71, time: 4.125, duration: 0.375 },
      { pitch: 72, time: 4.5, duration: 1.0 },
    ],
  },
  {
    name: 'Bach-style Fragment',
    description: 'Baroque melodic phrase',
    notes: [
      { pitch: 65, time: 0, duration: 0.5 },    // F4
      { pitch: 67, time: 0.5, duration: 0.5 },  // G4
      { pitch: 69, time: 1, duration: 0.5 },    // A4
      { pitch: 71, time: 1.5, duration: 0.25 }, // B4
      { pitch: 72, time: 1.75, duration: 0.25 },// C5
      { pitch: 74, time: 2, duration: 1.0 },    // D5
      { pitch: 72, time: 3, duration: 0.5 },    // C5
      { pitch: 71, time: 3.5, duration: 0.5 },  // B4
      { pitch: 69, time: 4, duration: 0.5 },    // A4
      { pitch: 67, time: 4.5, duration: 0.5 },  // G4
      { pitch: 69, time: 5, duration: 0.5 },    // A4
      { pitch: 65, time: 5.5, duration: 1.5 },  // F4
    ],
  },
];
