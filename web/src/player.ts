/**
 * Audio playback using Tone.js
 */

import * as Tone from 'tone';
import { Note, Score } from './scoreLoader';

export type PlaybackMode = 'normal' | 'first-half' | 'second-half' | 'from-middle';

export interface PlaybackState {
  isPlaying: boolean;
  currentTime: number;
  tempo: number;
  mode: PlaybackMode;
}

export class Player {
  private score: Score;
  private synths: Tone.Synth[];
  private parts: Tone.Part[];
  private currentTime: number = 0;
  private isPlaying: boolean = false;
  private tempo: number = 84;
  private mode: PlaybackMode = 'normal';
  private onTimeUpdate?: (time: number) => void;
  private onNotePlay?: (voiceIndex: number, note: Note) => void;
  private muteStates: boolean[] = [false, false];
  private metronomeEnabled: boolean = false;
  private metronomePart?: Tone.Part;

  constructor(score: Score) {
    this.score = score;

    // Create a synth for each voice with different panning
    this.synths = [
      new Tone.Synth({
        oscillator: { type: 'triangle' },
        envelope: { attack: 0.005, decay: 0.1, sustain: 0.3, release: 0.5 },
      }).toDestination(),
      new Tone.Synth({
        oscillator: { type: 'triangle' },
        envelope: { attack: 0.005, decay: 0.1, sustain: 0.3, release: 0.5 },
      }).toDestination(),
    ];

    // Pan voices left and right
    this.synths[0].set({ volume: -6 });
    this.synths[1].set({ volume: -6 });

    // Create parts for each voice
    this.parts = [];
    this.createParts();

    // Set initial tempo
    Tone.getTransport().bpm.value = this.tempo;

    // Update current time
    Tone.getTransport().scheduleRepeat((time) => {
      this.currentTime = Tone.getTransport().seconds * (this.tempo / 60);
      this.onTimeUpdate?.(this.currentTime);
    }, 0.1);
  }

  private createParts(): void {
    this.parts = this.score.voices.map((voice, voiceIndex) => {
      const part = new Tone.Part((time, note: Note) => {
        if (!this.muteStates[voiceIndex]) {
          const freq = Tone.Frequency(note.pitch, 'midi').toFrequency();
          this.synths[voiceIndex].triggerAttackRelease(
            freq,
            note.duration * (60 / this.tempo),
            time
          );

          // Notify listeners
          this.onNotePlay?.(voiceIndex, note);
        }
      }, voice.notes.map(note => [note.start * (60 / this.tempo), note]));

      part.loop = false;
      return part;
    });
  }

  async play(): Promise<void> {
    if (this.isPlaying) return;

    await Tone.start();

    // Calculate start and end times based on mode
    let startTime = 0;
    let endTime = this.score.totalDuration * (60 / this.tempo);

    switch (this.mode) {
      case 'first-half':
        endTime = (this.score.totalDuration / 2) * (60 / this.tempo);
        break;
      case 'second-half':
        startTime = (this.score.totalDuration / 2) * (60 / this.tempo);
        break;
      case 'from-middle':
        // Start from middle and play outward (requires special handling)
        // For now, just play from middle to end
        startTime = (this.score.totalDuration / 2) * (60 / this.tempo);
        break;
    }

    // Start transport
    if (Tone.getTransport().state !== 'started') {
      this.parts.forEach(part => part.start(0));
      if (this.metronomeEnabled && this.metronomePart) {
        this.metronomePart.start(0);
      }
      Tone.getTransport().start('+0.1', startTime);
    } else {
      Tone.getTransport().start();
    }

    this.isPlaying = true;
  }

  pause(): void {
    if (!this.isPlaying) return;

    Tone.getTransport().pause();
    this.isPlaying = false;
  }

  stop(): void {
    Tone.getTransport().stop();
    this.parts.forEach(part => part.stop());
    this.metronomePart?.stop();
    this.currentTime = 0;
    this.isPlaying = false;
  }

  setTempo(bpm: number): void {
    this.tempo = bpm;
    Tone.getTransport().bpm.value = bpm;

    // Recreate parts with new tempo
    this.parts.forEach(part => part.dispose());
    this.createParts();

    if (this.metronomeEnabled) {
      this.setupMetronome();
    }
  }

  setMode(mode: PlaybackMode): void {
    this.mode = mode;
    this.stop();
  }

  setMute(voiceIndex: number, muted: boolean): void {
    if (voiceIndex >= 0 && voiceIndex < this.muteStates.length) {
      this.muteStates[voiceIndex] = muted;
    }
  }

  setMetronome(enabled: boolean): void {
    this.metronomeEnabled = enabled;

    if (enabled) {
      this.setupMetronome();
    } else {
      this.metronomePart?.dispose();
      this.metronomePart = undefined;
    }
  }

  private setupMetronome(): void {
    this.metronomePart?.dispose();

    const clickSynth = new Tone.MembraneSynth({
      pitchDecay: 0.05,
      octaves: 10,
      oscillator: { type: 'sine' },
      envelope: { attack: 0.001, decay: 0.4, sustain: 0.01, release: 0.4 },
    }).toDestination();

    clickSynth.volume.value = -10;

    const beats: [number, { accent: boolean }][] = [];
    const beatDuration = 60 / this.tempo;

    for (let i = 0; i < this.score.totalDuration; i++) {
      beats.push([i * beatDuration, { accent: i % 4 === 0 }]);
    }

    this.metronomePart = new Tone.Part((time, value: { accent: boolean }) => {
      clickSynth.triggerAttackRelease(
        value.accent ? 'C5' : 'C4',
        '8n',
        time
      );
    }, beats);

    this.metronomePart.loop = false;
  }

  onUpdate(callback: (time: number) => void): void {
    this.onTimeUpdate = callback;
  }

  onNote(callback: (voiceIndex: number, note: Note) => void): void {
    this.onNotePlay = callback;
  }

  getState(): PlaybackState {
    return {
      isPlaying: this.isPlaying,
      currentTime: this.currentTime,
      tempo: this.tempo,
      mode: this.mode,
    };
  }

  dispose(): void {
    this.stop();
    this.parts.forEach(part => part.dispose());
    this.synths.forEach(synth => synth.dispose());
    this.metronomePart?.dispose();
  }
}
