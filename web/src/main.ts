/**
 * Main entry point for the Cancrizans web application
 */

import './styles.css';
import { loadBachCrabCanon } from './scoreLoader';
import { Player } from './player';
import { MirrorView } from './mirrorView';
import { NotationRenderer } from './notation';
import { UIController } from './ui';
import { CanonComposer, TEMPLATES, ComposerNote } from './composer';
import { WaveformVisualizer } from './waveform';
import { Exporter } from './exporter';
import { AccessibilityManager } from './accessibility';
import { LoadingManager, ErrorHandler } from './loading';
import { TutorialManager } from './tutorial';
import { Phase7Manager } from './phase7_integration';
import * as Tone from 'tone';

// Global managers
const a11y = new AccessibilityManager();
const loading = new LoadingManager();
const errorHandler = new ErrorHandler();
const tutorial = new TutorialManager();

// Initialize composer controls
function initComposer(composer: CanonComposer) {
  // Populate template select
  const templateSelect = document.getElementById('template-select') as HTMLSelectElement;
  if (templateSelect) {
    TEMPLATES.forEach((template, index) => {
      const option = document.createElement('option');
      option.value = String(index);
      option.textContent = `${template.name} - ${template.description}`;
      templateSelect.appendChild(option);
    });

    templateSelect.addEventListener('change', (e) => {
      const target = e.target as HTMLSelectElement;
      const index = parseInt(target.value);
      if (!isNaN(index) && TEMPLATES[index]) {
        composer.loadTemplate(TEMPLATES[index]);
      }
    });
  }

  // Clear button
  const clearBtn = document.getElementById('clear-composer-btn');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      composer.clearAll();
    });
  }

  // Play button
  const playBtn = document.getElementById('play-composer-btn');
  if (playBtn) {
    playBtn.addEventListener('click', async () => {
      await Tone.start();
      playComposerNotes(composer.getNotes(), composer.getRetrogradeNotes());
    });
  }

  // Note duration select
  const durationSelect = document.getElementById('note-duration-select') as HTMLSelectElement;
  if (durationSelect) {
    durationSelect.addEventListener('change', (e) => {
      const target = e.target as HTMLSelectElement;
      const duration = parseFloat(target.value);
      composer.setDuration(duration);
    });
  }

  // Snap to grid checkbox
  const snapCheckbox = document.getElementById('snap-to-grid') as HTMLInputElement;
  if (snapCheckbox) {
    snapCheckbox.addEventListener('change', (e) => {
      const target = e.target as HTMLInputElement;
      composer.setSnapToGrid(target.checked);
    });
  }

  // Update stats when notes change
  composer.onUpdate((notes) => {
    updateComposerStats(notes);
  });

  // Initial stats
  updateComposerStats([]);
}

function updateComposerStats(notes: ComposerNote[]) {
  const noteCountEl = document.getElementById('composer-note-count');
  const durationEl = document.getElementById('composer-duration');

  if (noteCountEl) {
    noteCountEl.textContent = `Notes: ${notes.length}`;
  }

  if (durationEl) {
    if (notes.length === 0) {
      durationEl.textContent = 'Duration: 0.0 quarters';
    } else {
      const maxEnd = Math.max(...notes.map(n => n.time + n.duration));
      durationEl.textContent = `Duration: ${maxEnd.toFixed(1)} quarters`;
    }
  }
}

function playComposerNotes(notes: ComposerNote[], retroNotes: ComposerNote[]) {
  if (notes.length === 0) {
    alert('Add some notes first!');
    return;
  }

  // Convert MIDI note numbers to note names
  const midiToNote = (midi: number): string => {
    const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
    const octave = Math.floor(midi / 12) - 1;
    const noteName = noteNames[midi % 12];
    return `${noteName}${octave}`;
  };

  // Create a simple synthesizer for playback
  const synth1 = new Tone.Synth().toDestination();
  const synth2 = new Tone.Synth({
    oscillator: { type: 'sawtooth' },
    envelope: { attack: 0.001, decay: 0.15, sustain: 0.0, release: 0.15 }
  }).toDestination();

  // Schedule voice 1 (forward)
  notes.forEach(note => {
    const noteName = midiToNote(note.pitch);
    synth1.triggerAttackRelease(noteName, note.duration, `+${note.time}`);
  });

  // Schedule voice 2 (retrograde)
  retroNotes.forEach(note => {
    const noteName = midiToNote(note.pitch);
    synth2.triggerAttackRelease(noteName, note.duration, `+${note.time}`);
  });

  console.log('Playing composed canon...');
}

// Initialize tutorial system
function initTutorial() {
  const tutorialBtn = document.getElementById('tutorial-start-btn');
  if (tutorialBtn) {
    tutorialBtn.addEventListener('click', () => {
      tutorial.start(() => {
        a11y.announce('Tutorial completed!');
      });
    });
  }
}

// Initialize the application
async function init() {
  loading.show('Initializing Cancrizans...');

  try {
    console.log('Initializing Cancrizans...');

    // Load the score
    const score = loadBachCrabCanon();
    console.log('Score loaded:', score);

    // Get containers
    const notationContainer = document.getElementById('notation-container');
    const mirrorCanvas = document.getElementById('mirror-canvas') as HTMLCanvasElement;
    const composerCanvas = document.getElementById('composer-canvas') as HTMLCanvasElement;
    const waveformCanvas = document.getElementById('waveform-canvas') as HTMLCanvasElement;

    if (!notationContainer || !mirrorCanvas || !composerCanvas || !waveformCanvas) {
      throw new Error('Required DOM containers not found');
    }

  // Create instances
  const player = new Player(score);
  const mirrorView = new MirrorView(mirrorCanvas, score);
  const notationRenderer = new NotationRenderer(notationContainer, score);
  const composer = new CanonComposer(composerCanvas);
  new WaveformVisualizer(waveformCanvas);  // Starts automatically
  new Exporter(score);  // Available for export functionality
  new UIController(player, mirrorView, notationRenderer);  // Sets up event listeners

  // Render initial views
  notationRenderer.render();
  mirrorView.render();

    // Initialize composer UI
    initComposer(composer);

    // Initialize tutorial
    initTutorial();

    // Initialize Phase 7 features
    new Phase7Manager();

    console.log('Cancrizans initialized successfully');
    a11y.announce('Application loaded successfully');

    // Add info to the page
    displayInfo(score);

    loading.hide();
  } catch (error) {
    loading.hide();
    const message = error instanceof Error ? error.message : 'Unknown error occurred';
    errorHandler.showError('Failed to initialize application', message);
    console.error('Initialization error:', error);
  }
}

function displayInfo(score: any) {
  const infoDiv = document.getElementById('info');
  if (!infoDiv) return;

  infoDiv.innerHTML = `
    <p><strong>Bach's Crab Canon</strong> from <em>The Musical Offering</em> (BWV 1079)</p>
    <p>Voices: ${score.voices.length} |
       Duration: ${score.totalDuration} quarter notes |
       Time: ${score.timeSignature.beats}/${score.timeSignature.beatType}</p>
  `;
}

// Register service worker for PWA functionality
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('SW registered:', registration.scope);
      })
      .catch((error) => {
        console.log('SW registration failed:', error);
      });
  });
}

// Start the application when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
