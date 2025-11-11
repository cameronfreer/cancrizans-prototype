/**
 * Score loader - loads the embedded Bach Crab Canon data
 */

export interface Note {
  pitch: number; // MIDI pitch
  start: number; // Quarter note offset
  duration: number; // Quarter note duration
  name: string; // Note name (e.g., "C4")
}

export interface Voice {
  id: string;
  notes: Note[];
}

export interface Score {
  voices: Voice[];
  totalDuration: number;
  timeSignature: { beats: number; beatType: number };
  keySignature: number; // Fifths (-1 = F major)
}

/**
 * Parse a simplified version of Bach's Crab Canon.
 * This represents the same piece as the Python MusicXML.
 */
export function loadBachCrabCanon(): Score {
  // Voice 1 (Forward) - simplified representation
  const voice1Notes: Note[] = [
    // Measure 1
    { pitch: 72, start: 0, duration: 0.5, name: 'C5' },
    { pitch: 74, start: 0.5, duration: 0.5, name: 'D5' },
    { pitch: 75, start: 1, duration: 0.5, name: 'Eb5' },
    { pitch: 77, start: 1.5, duration: 0.5, name: 'F5' },
    { pitch: 79, start: 2, duration: 0.5, name: 'G5' },
    { pitch: 77, start: 2.5, duration: 0.5, name: 'F5' },
    { pitch: 75, start: 3, duration: 0.5, name: 'Eb5' },
    { pitch: 74, start: 3.5, duration: 0.5, name: 'D5' },
    // Measure 2
    { pitch: 72, start: 4, duration: 0.5, name: 'C5' },
    { pitch: 70, start: 4.5, duration: 0.5, name: 'Bb4' },
    { pitch: 68, start: 5, duration: 0.5, name: 'Ab4' },
    { pitch: 67, start: 5.5, duration: 0.5, name: 'G4' },
    { pitch: 65, start: 6, duration: 0.5, name: 'F4' },
    { pitch: 67, start: 6.5, duration: 0.5, name: 'G4' },
    { pitch: 68, start: 7, duration: 0.5, name: 'Ab4' },
    { pitch: 70, start: 7.5, duration: 0.5, name: 'Bb4' },
    // Measure 3
    { pitch: 72, start: 8, duration: 1, name: 'C5' },
    { pitch: 67, start: 9, duration: 1, name: 'G4' },
    { pitch: 75, start: 10, duration: 1, name: 'Eb5' },
    { pitch: 72, start: 11, duration: 1, name: 'C5' },
    // Measure 4
    { pitch: 74, start: 12, duration: 0.5, name: 'D5' },
    { pitch: 75, start: 12.5, duration: 0.5, name: 'Eb5' },
    { pitch: 77, start: 13, duration: 0.5, name: 'F5' },
    { pitch: 79, start: 13.5, duration: 0.5, name: 'G5' },
    { pitch: 80, start: 14, duration: 0.5, name: 'Ab5' },
    { pitch: 79, start: 14.5, duration: 0.5, name: 'G5' },
    { pitch: 77, start: 15, duration: 0.5, name: 'F5' },
    { pitch: 75, start: 15.5, duration: 0.5, name: 'Eb5' },
    // Measure 5
    { pitch: 74, start: 16, duration: 0.5, name: 'D5' },
    { pitch: 72, start: 16.5, duration: 0.5, name: 'C5' },
    { pitch: 70, start: 17, duration: 0.5, name: 'Bb4' },
    { pitch: 68, start: 17.5, duration: 0.5, name: 'Ab4' },
    { pitch: 67, start: 18, duration: 0.5, name: 'G4' },
    { pitch: 68, start: 18.5, duration: 0.5, name: 'Ab4' },
    { pitch: 70, start: 19, duration: 0.5, name: 'Bb4' },
    { pitch: 72, start: 19.5, duration: 0.5, name: 'C5' },
    // Measure 6
    { pitch: 74, start: 20, duration: 1, name: 'D5' },
    { pitch: 70, start: 21, duration: 1, name: 'Bb4' },
    { pitch: 67, start: 22, duration: 1, name: 'G4' },
    { pitch: 77, start: 23, duration: 1, name: 'F5' },
    // Measure 7
    { pitch: 75, start: 24, duration: 0.5, name: 'Eb5' },
    { pitch: 74, start: 24.5, duration: 0.5, name: 'D5' },
    { pitch: 72, start: 25, duration: 0.5, name: 'C5' },
    { pitch: 70, start: 25.5, duration: 0.5, name: 'Bb4' },
    { pitch: 68, start: 26, duration: 0.5, name: 'Ab4' },
    { pitch: 70, start: 26.5, duration: 0.5, name: 'Bb4' },
    { pitch: 72, start: 27, duration: 0.5, name: 'C5' },
    { pitch: 74, start: 27.5, duration: 0.5, name: 'D5' },
    // Measure 8
    { pitch: 75, start: 28, duration: 0.5, name: 'Eb5' },
    { pitch: 77, start: 28.5, duration: 0.5, name: 'F5' },
    { pitch: 79, start: 29, duration: 0.5, name: 'G5' },
    { pitch: 80, start: 29.5, duration: 0.5, name: 'Ab5' },
    { pitch: 82, start: 30, duration: 0.5, name: 'Bb5' },
    { pitch: 80, start: 30.5, duration: 0.5, name: 'Ab5' },
    { pitch: 79, start: 31, duration: 0.5, name: 'G5' },
    { pitch: 77, start: 31.5, duration: 0.5, name: 'F5' },
    // Measure 9
    { pitch: 75, start: 32, duration: 4, name: 'Eb5' },
  ];

  // Voice 2 (Retrograde) - starts with whole note Eb5, then retrograde pattern
  const voice2Notes: Note[] = [
    // Measure 1
    { pitch: 75, start: 0, duration: 4, name: 'Eb5' },
    // Measure 2
    { pitch: 77, start: 4, duration: 0.5, name: 'F5' },
    { pitch: 79, start: 4.5, duration: 0.5, name: 'G5' },
    { pitch: 80, start: 5, duration: 0.5, name: 'Ab5' },
    { pitch: 82, start: 5.5, duration: 0.5, name: 'Bb5' },
    { pitch: 80, start: 6, duration: 0.5, name: 'Ab5' },
    { pitch: 79, start: 6.5, duration: 0.5, name: 'G5' },
    { pitch: 77, start: 7, duration: 0.5, name: 'F5' },
    { pitch: 75, start: 7.5, duration: 0.5, name: 'Eb5' },
    // Measure 3
    { pitch: 74, start: 8, duration: 0.5, name: 'D5' },
    { pitch: 72, start: 8.5, duration: 0.5, name: 'C5' },
    { pitch: 70, start: 9, duration: 0.5, name: 'Bb4' },
    { pitch: 68, start: 9.5, duration: 0.5, name: 'Ab4' },
    { pitch: 70, start: 10, duration: 0.5, name: 'Bb4' },
    { pitch: 72, start: 10.5, duration: 0.5, name: 'C5' },
    { pitch: 74, start: 11, duration: 0.5, name: 'D5' },
    { pitch: 75, start: 11.5, duration: 0.5, name: 'Eb5' },
    // Measure 4
    { pitch: 77, start: 12, duration: 1, name: 'F5' },
    { pitch: 67, start: 13, duration: 1, name: 'G4' },
    { pitch: 70, start: 14, duration: 1, name: 'Bb4' },
    { pitch: 74, start: 15, duration: 1, name: 'D5' },
    // Measure 5
    { pitch: 72, start: 16, duration: 0.5, name: 'C5' },
    { pitch: 70, start: 16.5, duration: 0.5, name: 'Bb4' },
    { pitch: 68, start: 17, duration: 0.5, name: 'Ab4' },
    { pitch: 67, start: 17.5, duration: 0.5, name: 'G4' },
    { pitch: 68, start: 18, duration: 0.5, name: 'Ab4' },
    { pitch: 70, start: 18.5, duration: 0.5, name: 'Bb4' },
    { pitch: 72, start: 19, duration: 0.5, name: 'C5' },
    { pitch: 74, start: 19.5, duration: 0.5, name: 'D5' },
    // Measure 6
    { pitch: 72, start: 20, duration: 1, name: 'C5' },
    { pitch: 75, start: 21, duration: 1, name: 'Eb5' },
    { pitch: 67, start: 22, duration: 1, name: 'G4' },
    { pitch: 72, start: 23, duration: 1, name: 'C5' },
    // Measure 7
    { pitch: 70, start: 24, duration: 0.5, name: 'Bb4' },
    { pitch: 68, start: 24.5, duration: 0.5, name: 'Ab4' },
    { pitch: 67, start: 25, duration: 0.5, name: 'G4' },
    { pitch: 65, start: 25.5, duration: 0.5, name: 'F4' },
    { pitch: 67, start: 26, duration: 0.5, name: 'G4' },
    { pitch: 68, start: 26.5, duration: 0.5, name: 'Ab4' },
    { pitch: 70, start: 27, duration: 0.5, name: 'Bb4' },
    { pitch: 72, start: 27.5, duration: 0.5, name: 'C5' },
    // Measure 8
    { pitch: 74, start: 28, duration: 0.5, name: 'D5' },
    { pitch: 75, start: 28.5, duration: 0.5, name: 'Eb5' },
    { pitch: 77, start: 29, duration: 0.5, name: 'F5' },
    { pitch: 79, start: 29.5, duration: 0.5, name: 'G5' },
    { pitch: 77, start: 30, duration: 0.5, name: 'F5' },
    { pitch: 75, start: 30.5, duration: 0.5, name: 'Eb5' },
    { pitch: 74, start: 31, duration: 0.5, name: 'D5' },
    { pitch: 72, start: 31.5, duration: 0.5, name: 'C5' },
    // Measure 9
    { pitch: 72, start: 32, duration: 4, name: 'C5' },
  ];

  return {
    voices: [
      { id: 'voice1', notes: voice1Notes },
      { id: 'voice2', notes: voice2Notes },
    ],
    totalDuration: 36,
    timeSignature: { beats: 4, beatType: 4 },
    keySignature: -1, // F major
  };
}
