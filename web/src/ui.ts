/**
 * UI controls and event handling
 */

import { Player, PlaybackMode } from './player';
import { MirrorView } from './mirrorView';
import { NotationRenderer } from './notation';

export class UIController {
  private player: Player;
  private mirrorView: MirrorView;
  private notationRenderer: NotationRenderer;

  // UI elements
  private playBtn: HTMLButtonElement;
  private pauseBtn: HTMLButtonElement;
  private stopBtn: HTMLButtonElement;
  private tempoSlider: HTMLInputElement;
  private tempoDisplay: HTMLSpanElement;
  private modeSelect: HTMLSelectElement;
  private muteVoice1: HTMLInputElement;
  private muteVoice2: HTMLInputElement;
  private metronomeToggle: HTMLInputElement;
  private highlightToggle: HTMLInputElement;
  private timeDisplay: HTMLSpanElement;

  constructor(
    player: Player,
    mirrorView: MirrorView,
    notationRenderer: NotationRenderer
  ) {
    this.player = player;
    this.mirrorView = mirrorView;
    this.notationRenderer = notationRenderer;

    // Get UI elements
    this.playBtn = this.getElement('play-btn');
    this.pauseBtn = this.getElement('pause-btn');
    this.stopBtn = this.getElement('stop-btn');
    this.tempoSlider = this.getElement('tempo-slider');
    this.tempoDisplay = this.getElement('tempo-display');
    this.modeSelect = this.getElement('mode-select');
    this.muteVoice1 = this.getElement('mute-voice1');
    this.muteVoice2 = this.getElement('mute-voice2');
    this.metronomeToggle = this.getElement('metronome-toggle');
    this.highlightToggle = this.getElement('highlight-toggle');
    this.timeDisplay = this.getElement('time-display');

    this.setupEventListeners();
    this.setupKeyboardShortcuts();
  }

  private getElement<T extends HTMLElement>(id: string): T {
    const el = document.getElementById(id);
    if (!el) throw new Error(`Element not found: ${id}`);
    return el as T;
  }

  private setupEventListeners(): void {
    // Playback controls
    this.playBtn.addEventListener('click', () => this.handlePlay());
    this.pauseBtn.addEventListener('click', () => this.handlePause());
    this.stopBtn.addEventListener('click', () => this.handleStop());

    // Tempo control
    this.tempoSlider.addEventListener('input', () => {
      const tempo = parseInt(this.tempoSlider.value);
      this.tempoDisplay.textContent = tempo.toString();
    });

    this.tempoSlider.addEventListener('change', () => {
      const tempo = parseInt(this.tempoSlider.value);
      this.player.setTempo(tempo);
    });

    // Mode selection
    this.modeSelect.addEventListener('change', () => {
      const mode = this.modeSelect.value as PlaybackMode;
      this.player.setMode(mode);
    });

    // Mute controls
    this.muteVoice1.addEventListener('change', () => {
      this.player.setMute(0, this.muteVoice1.checked);
    });

    this.muteVoice2.addEventListener('change', () => {
      this.player.setMute(1, this.muteVoice2.checked);
    });

    // Metronome
    this.metronomeToggle.addEventListener('change', () => {
      this.player.setMetronome(this.metronomeToggle.checked);
    });

    // Highlight symmetry
    this.highlightToggle.addEventListener('change', () => {
      this.mirrorView.setHighlightPairs(this.highlightToggle.checked);
    });

    // Player callbacks
    this.player.onUpdate((time) => {
      this.updateTimeDisplay(time);
      this.mirrorView.updateTime(time);
    });

    this.player.onNote((voiceIndex, note) => {
      // Find note index
      const noteIndex = 0; // Simplified - would need proper tracking
      this.mirrorView.highlightNote(voiceIndex, noteIndex);
    });

    // Window resize
    window.addEventListener('resize', () => {
      this.mirrorView.resize();
      this.mirrorView.render();
    });
  }

  private setupKeyboardShortcuts(): void {
    document.addEventListener('keydown', (e) => {
      // Ignore if typing in an input
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLSelectElement) {
        return;
      }

      switch (e.key.toLowerCase()) {
        case ' ':
          e.preventDefault();
          this.togglePlayPause();
          break;
        case 'h':
          this.highlightToggle.checked = !this.highlightToggle.checked;
          this.mirrorView.setHighlightPairs(this.highlightToggle.checked);
          break;
        case 'm':
          this.metronomeToggle.checked = !this.metronomeToggle.checked;
          this.player.setMetronome(this.metronomeToggle.checked);
          break;
      }
    });
  }

  private async handlePlay(): Promise<void> {
    await this.player.play();
    this.updatePlaybackButtons();
  }

  private handlePause(): void {
    this.player.pause();
    this.updatePlaybackButtons();
  }

  private handleStop(): void {
    this.player.stop();
    this.updatePlaybackButtons();
    this.updateTimeDisplay(0);
  }

  private togglePlayPause(): void {
    const state = this.player.getState();
    if (state.isPlaying) {
      this.handlePause();
    } else {
      this.handlePlay();
    }
  }

  private updatePlaybackButtons(): void {
    const state = this.player.getState();
    this.playBtn.disabled = state.isPlaying;
    this.pauseBtn.disabled = !state.isPlaying;
  }

  private updateTimeDisplay(time: number): void {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    const ms = Math.floor((time % 1) * 100);

    this.timeDisplay.textContent =
      `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}.${ms.toString().padStart(2, '0')}`;
  }
}
