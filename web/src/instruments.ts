/**
 * Instrument presets for Tone.js
 */

import * as Tone from 'tone';

export type InstrumentType = 'synth' | 'piano' | 'harpsichord' | 'strings' | 'organ';

export interface InstrumentConfig {
  name: string;
  settings: any;  // Simplified type to avoid Tone.js strict type checking
}

export const INSTRUMENTS: Record<InstrumentType, InstrumentConfig> = {
  synth: {
    name: 'Synthesizer',
    settings: {
      oscillator: { type: 'triangle' },
      envelope: {
        attack: 0.005,
        decay: 0.1,
        sustain: 0.3,
        release: 0.5,
      },
    },
  },

  piano: {
    name: 'Piano',
    settings: {
      oscillator: { type: 'triangle' },
      envelope: {
        attack: 0.002,
        decay: 0.3,
        sustain: 0.1,
        release: 1.2,
      },
    },
  },

  harpsichord: {
    name: 'Harpsichord',
    settings: {
      oscillator: { type: 'sawtooth' },
      envelope: {
        attack: 0.001,
        decay: 0.15,
        sustain: 0.0,
        release: 0.15,
      },
    },
  },

  strings: {
    name: 'Strings',
    settings: {
      oscillator: { type: 'sawtooth' },
      envelope: {
        attack: 0.1,
        decay: 0.2,
        sustain: 0.8,
        release: 1.0,
      },
    },
  },

  organ: {
    name: 'Organ',
    settings: {
      oscillator: { type: 'sine' },
      envelope: {
        attack: 0.01,
        decay: 0.1,
        sustain: 0.9,
        release: 0.2,
      },
    },
  },
};

export function createInstrument(type: InstrumentType): Tone.Synth {
  const config = INSTRUMENTS[type];
  return new Tone.Synth(config.settings).toDestination();
}

export function getInstrumentNames(): { value: InstrumentType; label: string }[] {
  return Object.entries(INSTRUMENTS).map(([key, value]) => ({
    value: key as InstrumentType,
    label: value.name,
  }));
}
