/**
 * Main entry point for the Cancrizans web application
 */

import './styles.css';
import { loadBachCrabCanon } from './scoreLoader';
import { Player } from './player';
import { MirrorView } from './mirrorView';
import { NotationRenderer } from './notation';
import { UIController } from './ui';

// Initialize the application
async function init() {
  console.log('Initializing Cancrizans...');

  // Load the score
  const score = loadBachCrabCanon();
  console.log('Score loaded:', score);

  // Get containers
  const notationContainer = document.getElementById('notation-container');
  const mirrorCanvas = document.getElementById('mirror-canvas') as HTMLCanvasElement;

  if (!notationContainer || !mirrorCanvas) {
    console.error('Required containers not found');
    return;
  }

  // Create instances
  const player = new Player(score);
  const mirrorView = new MirrorView(mirrorCanvas, score);
  const notationRenderer = new NotationRenderer(notationContainer, score);

  // Render initial views
  notationRenderer.render();
  mirrorView.render();

  // Initialize UI controller
  const uiController = new UIController(player, mirrorView, notationRenderer);

  console.log('Cancrizans initialized successfully');

  // Add info to the page
  displayInfo(score);
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

// Start the application when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
