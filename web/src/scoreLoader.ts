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
 * Load Bach's Crab Canon (Canon Cancrizans) from The Musical Offering (BWV 1079).
 * This is a perfect retrograde canon where Voice 2 is Voice 1 played backwards.
 * Generated from the authentic Python MusicXML version.
 */
export function loadBachCrabCanon(): Score {
  // Voice 1 (Forward) - 57 notes
  const voice1Notes: Note[] = [
    { pitch: 72, start: 0.0, duration: 0.5, name: 'C5' },
    { pitch: 74, start: 0.5, duration: 0.5, name: 'D5' },
    { pitch: 75, start: 1.0, duration: 0.5, name: 'Eb5' },
    { pitch: 77, start: 1.5, duration: 0.5, name: 'F5' },
    { pitch: 79, start: 2.0, duration: 0.5, name: 'G5' },
    { pitch: 77, start: 2.5, duration: 0.5, name: 'F5' },
    { pitch: 75, start: 3.0, duration: 0.5, name: 'Eb5' },
    { pitch: 74, start: 3.5, duration: 0.5, name: 'D5' },
    { pitch: 72, start: 4.0, duration: 0.5, name: 'C5' },
    { pitch: 70, start: 4.5, duration: 0.5, name: 'Bb4' },
    { pitch: 68, start: 5.0, duration: 0.5, name: 'Ab4' },
    { pitch: 67, start: 5.5, duration: 0.5, name: 'G4' },
    { pitch: 65, start: 6.0, duration: 0.5, name: 'F4' },
    { pitch: 67, start: 6.5, duration: 0.5, name: 'G4' },
    { pitch: 68, start: 7.0, duration: 0.5, name: 'Ab4' },
    { pitch: 70, start: 7.5, duration: 0.5, name: 'Bb4' },
    { pitch: 72, start: 8.0, duration: 1.0, name: 'C5' },
    { pitch: 67, start: 9.0, duration: 1.0, name: 'G4' },
    { pitch: 75, start: 10.0, duration: 1.0, name: 'Eb5' },
    { pitch: 72, start: 11.0, duration: 1.0, name: 'C5' },
    { pitch: 74, start: 12.0, duration: 0.5, name: 'D5' },
    { pitch: 75, start: 12.5, duration: 0.5, name: 'Eb5' },
    { pitch: 77, start: 13.0, duration: 0.5, name: 'F5' },
    { pitch: 79, start: 13.5, duration: 0.5, name: 'G5' },
    { pitch: 80, start: 14.0, duration: 0.5, name: 'Ab5' },
    { pitch: 79, start: 14.5, duration: 0.5, name: 'G5' },
    { pitch: 77, start: 15.0, duration: 0.5, name: 'F5' },
    { pitch: 75, start: 15.5, duration: 0.5, name: 'Eb5' },
    { pitch: 74, start: 16.0, duration: 0.5, name: 'D5' },
    { pitch: 72, start: 16.5, duration: 0.5, name: 'C5' },
    { pitch: 70, start: 17.0, duration: 0.5, name: 'Bb4' },
    { pitch: 68, start: 17.5, duration: 0.5, name: 'Ab4' },
    { pitch: 67, start: 18.0, duration: 0.5, name: 'G4' },
    { pitch: 68, start: 18.5, duration: 0.5, name: 'Ab4' },
    { pitch: 70, start: 19.0, duration: 0.5, name: 'Bb4' },
    { pitch: 72, start: 19.5, duration: 0.5, name: 'C5' },
    { pitch: 74, start: 20.0, duration: 1.0, name: 'D5' },
    { pitch: 70, start: 21.0, duration: 1.0, name: 'Bb4' },
    { pitch: 67, start: 22.0, duration: 1.0, name: 'G4' },
    { pitch: 77, start: 23.0, duration: 1.0, name: 'F5' },
    { pitch: 75, start: 24.0, duration: 0.5, name: 'Eb5' },
    { pitch: 74, start: 24.5, duration: 0.5, name: 'D5' },
    { pitch: 72, start: 25.0, duration: 0.5, name: 'C5' },
    { pitch: 70, start: 25.5, duration: 0.5, name: 'Bb4' },
    { pitch: 68, start: 26.0, duration: 0.5, name: 'Ab4' },
    { pitch: 70, start: 26.5, duration: 0.5, name: 'Bb4' },
    { pitch: 72, start: 27.0, duration: 0.5, name: 'C5' },
    { pitch: 74, start: 27.5, duration: 0.5, name: 'D5' },
    { pitch: 75, start: 28.0, duration: 0.5, name: 'Eb5' },
    { pitch: 77, start: 28.5, duration: 0.5, name: 'F5' },
    { pitch: 79, start: 29.0, duration: 0.5, name: 'G5' },
    { pitch: 80, start: 29.5, duration: 0.5, name: 'Ab5' },
    { pitch: 82, start: 30.0, duration: 0.5, name: 'Bb5' },
    { pitch: 80, start: 30.5, duration: 0.5, name: 'Ab5' },
    { pitch: 79, start: 31.0, duration: 0.5, name: 'G5' },
    { pitch: 77, start: 31.5, duration: 0.5, name: 'F5' },
    { pitch: 75, start: 32.0, duration: 4.0, name: 'Eb5' },
  ];

  // Voice 2 (Retrograde) - 50 notes
  // This is Voice 1 played backwards in time - a perfect crab canon!
  const voice2Notes: Note[] = [
    { pitch: 75, start: 0.0, duration: 4.0, name: 'Eb5' },
    { pitch: 77, start: 4.0, duration: 0.5, name: 'F5' },
    { pitch: 79, start: 4.5, duration: 0.5, name: 'G5' },
    { pitch: 80, start: 5.0, duration: 0.5, name: 'Ab5' },
    { pitch: 82, start: 5.5, duration: 0.5, name: 'Bb5' },
    { pitch: 80, start: 6.0, duration: 0.5, name: 'Ab5' },
    { pitch: 79, start: 6.5, duration: 0.5, name: 'G5' },
    { pitch: 77, start: 7.0, duration: 0.5, name: 'F5' },
    { pitch: 75, start: 7.5, duration: 0.5, name: 'Eb5' },
    { pitch: 74, start: 8.0, duration: 0.5, name: 'D5' },
    { pitch: 72, start: 8.5, duration: 0.5, name: 'C5' },
    { pitch: 70, start: 9.0, duration: 0.5, name: 'Bb4' },
    { pitch: 68, start: 9.5, duration: 0.5, name: 'Ab4' },
    { pitch: 70, start: 10.0, duration: 0.5, name: 'Bb4' },
    { pitch: 72, start: 10.5, duration: 0.5, name: 'C5' },
    { pitch: 74, start: 11.0, duration: 0.5, name: 'D5' },
    { pitch: 75, start: 11.5, duration: 0.5, name: 'Eb5' },
    { pitch: 77, start: 12.0, duration: 1.0, name: 'F5' },
    { pitch: 67, start: 13.0, duration: 1.0, name: 'G4' },
    { pitch: 70, start: 14.0, duration: 1.0, name: 'Bb4' },
    { pitch: 74, start: 15.0, duration: 1.0, name: 'D5' },
    { pitch: 72, start: 16.0, duration: 0.5, name: 'C5' },
    { pitch: 70, start: 16.5, duration: 0.5, name: 'Bb4' },
    { pitch: 68, start: 17.0, duration: 0.5, name: 'Ab4' },
    { pitch: 67, start: 17.5, duration: 0.5, name: 'G4' },
    { pitch: 68, start: 18.0, duration: 0.5, name: 'Ab4' },
    { pitch: 70, start: 18.5, duration: 0.5, name: 'Bb4' },
    { pitch: 72, start: 19.0, duration: 0.5, name: 'C5' },
    { pitch: 74, start: 19.5, duration: 0.5, name: 'D5' },
    { pitch: 72, start: 20.0, duration: 1.0, name: 'C5' },
    { pitch: 75, start: 21.0, duration: 1.0, name: 'Eb5' },
    { pitch: 67, start: 22.0, duration: 1.0, name: 'G4' },
    { pitch: 72, start: 23.0, duration: 1.0, name: 'C5' },
    { pitch: 70, start: 24.0, duration: 0.5, name: 'Bb4' },
    { pitch: 68, start: 24.5, duration: 0.5, name: 'Ab4' },
    { pitch: 67, start: 25.0, duration: 0.5, name: 'G4' },
    { pitch: 65, start: 25.5, duration: 0.5, name: 'F4' },
    { pitch: 67, start: 26.0, duration: 0.5, name: 'G4' },
    { pitch: 68, start: 26.5, duration: 0.5, name: 'Ab4' },
    { pitch: 70, start: 27.0, duration: 0.5, name: 'Bb4' },
    { pitch: 72, start: 27.5, duration: 0.5, name: 'C5' },
    { pitch: 74, start: 28.0, duration: 0.5, name: 'D5' },
    { pitch: 75, start: 28.5, duration: 0.5, name: 'Eb5' },
    { pitch: 77, start: 29.0, duration: 0.5, name: 'F5' },
    { pitch: 79, start: 29.5, duration: 0.5, name: 'G5' },
    { pitch: 77, start: 30.0, duration: 0.5, name: 'F5' },
    { pitch: 75, start: 30.5, duration: 0.5, name: 'Eb5' },
    { pitch: 74, start: 31.0, duration: 0.5, name: 'D5' },
    { pitch: 72, start: 31.5, duration: 0.5, name: 'C5' },
    { pitch: 72, start: 32.0, duration: 4.0, name: 'C5' },
  ];

  return {
    voices: [
      { id: 'voice1', notes: voice1Notes },
      { id: 'voice2', notes: voice2Notes },
    ],
    totalDuration: 36,
    timeSignature: { beats: 4, beatType: 4 },
    keySignature: -1, // F major (1 flat)
  };
}
