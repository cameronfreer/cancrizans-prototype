/**
 * Interactive Tutorial System
 * Guided step-by-step introduction to crab canons
 */

export interface TutorialStep {
  id: string;
  title: string;
  content: string;
  action?: string;
  highlight?: string;  // CSS selector to highlight
  position?: 'top' | 'bottom' | 'left' | 'right';
}

export const TUTORIAL_STEPS: TutorialStep[] = [
  {
    id: 'welcome',
    title: 'Welcome to Cancrizans!',
    content: `
      <p>Learn about <strong>Crab Canons</strong> - musical palindromes where a melody is played forward and backward simultaneously!</p>
      <p>This tutorial will guide you through Bach's famous Crab Canon from <em>The Musical Offering</em>.</p>
    `,
    position: 'bottom',
  },
  {
    id: 'what-is-palindrome',
    title: 'What is a Musical Palindrome?',
    content: `
      <p>Just like "A man, a plan, a canal: Panama" reads the same forwards and backwards, a musical palindrome sounds the same in both directions.</p>
      <p>In Bach's Crab Canon, Voice 2 is the <strong>exact time-reversal</strong> of Voice 1.</p>
      <ul>
        <li>Voice 1 plays the melody forward</li>
        <li>Voice 2 plays it backward</li>
        <li>Both start at the same time</li>
      </ul>
    `,
    position: 'bottom',
  },
  {
    id: 'play-button',
    title: 'Listen to the Canon',
    content: `
      <p>Click the <strong>Play</strong> button to hear both voices simultaneously.</p>
      <p>Notice how they create perfect harmony while moving in opposite directions through time!</p>
    `,
    action: 'Click the ▶ Play button',
    highlight: '#play-btn',
    position: 'bottom',
  },
  {
    id: 'mirror-view',
    title: 'Visualize the Symmetry',
    content: `
      <p>The <strong>Mirror View</strong> shows the palindromic structure visually.</p>
      <p>Notice the perfect symmetry around the center line - each note in Voice 1 has a corresponding "mirror" note in Voice 2.</p>
      <ul>
        <li>Blue = Voice 1 (forward)</li>
        <li>Red = Voice 2 (backward)</li>
        <li>The vertical center line is the "mirror"</li>
      </ul>
    `,
    highlight: '#mirror-canvas',
    position: 'top',
  },
  {
    id: 'notation',
    title: 'Musical Notation',
    content: `
      <p>The traditional staff notation shows both voices on separate staves.</p>
      <p>Read Voice 1 normally (left to right), but imagine Voice 2 being read from right to left - that's the "crab" motion!</p>
    `,
    highlight: '#notation-container',
    position: 'top',
  },
  {
    id: 'tempo-control',
    title: 'Adjust the Tempo',
    content: `
      <p>Try changing the <strong>tempo</strong> to hear the canon at different speeds.</p>
      <p>Bach likely intended it around 84 BPM, but experiment to find what helps you hear the symmetry best!</p>
    `,
    highlight: '#tempo-slider',
    position: 'top',
  },
  {
    id: 'mute-voices',
    title: 'Isolate Each Voice',
    content: `
      <p>Use the <strong>Mute</strong> checkboxes to listen to each voice individually.</p>
      <p>First, mute Voice 2 to hear only the forward melody. Then mute Voice 1 to hear the retrograde!</p>
    `,
    highlight: '#mute-voice1',
    position: 'top',
  },
  {
    id: 'composer-intro',
    title: 'Create Your Own Canon',
    content: `
      <p>Now it's your turn! Use the <strong>Interactive Canon Builder</strong> to create your own crab canon.</p>
      <p><strong>How it works:</strong></p>
      <ul>
        <li><strong>Click</strong> on the grid to add notes</li>
        <li><strong>Drag</strong> notes to move them</li>
        <li><strong>Shift+Click</strong> to delete</li>
        <li>Red notes show the auto-generated retrograde!</li>
      </ul>
    `,
    highlight: '.composer-section',
    position: 'top',
  },
  {
    id: 'templates',
    title: 'Try a Template',
    content: `
      <p>Start with a <strong>template</strong> to see how different melodies create canons.</p>
      <p>Select "C Major Scale" or "Arpeggio" from the dropdown, then click <strong>Play My Canon</strong> to hear it!</p>
    `,
    highlight: '#template-select',
    position: 'bottom',
  },
  {
    id: 'experiment',
    title: 'Experiment!',
    content: `
      <p>Try creating your own melody:</p>
      <ol>
        <li>Clear the canvas (🗑️ button)</li>
        <li>Add a few notes by clicking</li>
        <li>Watch the red retrograde appear</li>
        <li>Click ▶ Play My Canon to hear it!</li>
      </ol>
      <p><strong>Tip:</strong> Start simple - even 3-4 notes make an interesting canon!</p>
    `,
    highlight: '#composer-canvas',
    position: 'top',
  },
  {
    id: 'complete',
    title: 'You\'re Ready!',
    content: `
      <p>🎉 Congratulations! You now understand the basics of crab canons.</p>
      <p><strong>Key Takeaways:</strong></p>
      <ul>
        <li>A crab canon is a musical palindrome</li>
        <li>Two voices play the same melody in opposite directions</li>
        <li>They start together and create harmony</li>
        <li>Bach's genius made this sound beautiful!</li>
      </ul>
      <p>Keep exploring and creating your own canons! 🦀</p>
    `,
    position: 'bottom',
  },
];

export class TutorialManager {
  private currentStep: number = 0;
  private overlay: HTMLElement | null = null;
  private tooltip: HTMLElement | null = null;
  private isActive: boolean = false;
  private onComplete?: () => void;

  constructor() {
    this.createOverlay();
    this.createTooltip();
  }

  private createOverlay(): void {
    this.overlay = document.createElement('div');
    this.overlay.className = 'tutorial-overlay hidden';
    this.overlay.addEventListener('click', () => this.next());
    document.body.appendChild(this.overlay);
  }

  private createTooltip(): void {
    this.tooltip = document.createElement('div');
    this.tooltip.className = 'tutorial-tooltip hidden';
    this.tooltip.innerHTML = `
      <div class="tutorial-header">
        <h3 class="tutorial-title"></h3>
        <button class="tutorial-close" aria-label="Close tutorial">✕</button>
      </div>
      <div class="tutorial-content"></div>
      <div class="tutorial-footer">
        <div class="tutorial-progress"></div>
        <div class="tutorial-buttons">
          <button class="tutorial-prev">← Previous</button>
          <button class="tutorial-next">Next →</button>
          <button class="tutorial-finish hidden">Finish</button>
        </div>
      </div>
    `;
    document.body.appendChild(this.tooltip);

    // Setup event listeners
    const closeBtn = this.tooltip.querySelector('.tutorial-close') as HTMLButtonElement;
    const prevBtn = this.tooltip.querySelector('.tutorial-prev') as HTMLButtonElement;
    const nextBtn = this.tooltip.querySelector('.tutorial-next') as HTMLButtonElement;
    const finishBtn = this.tooltip.querySelector('.tutorial-finish') as HTMLButtonElement;

    closeBtn?.addEventListener('click', () => this.stop());
    prevBtn?.addEventListener('click', () => this.previous());
    nextBtn?.addEventListener('click', () => this.next());
    finishBtn?.addEventListener('click', () => this.stop());
  }

  start(onComplete?: () => void): void {
    this.onComplete = onComplete;
    this.currentStep = 0;
    this.isActive = true;
    this.showStep(0);
    this.overlay?.classList.remove('hidden');
  }

  stop(): void {
    this.isActive = false;
    this.overlay?.classList.add('hidden');
    this.tooltip?.classList.add('hidden');
    this.clearHighlight();
    if (this.onComplete) {
      this.onComplete();
    }
  }

  next(): void {
    if (this.currentStep < TUTORIAL_STEPS.length - 1) {
      this.currentStep++;
      this.showStep(this.currentStep);
    } else {
      this.stop();
    }
  }

  previous(): void {
    if (this.currentStep > 0) {
      this.currentStep--;
      this.showStep(this.currentStep);
    }
  }

  private showStep(index: number): void {
    const step = TUTORIAL_STEPS[index];
    if (!step || !this.tooltip) return;

    // Update content
    const titleEl = this.tooltip.querySelector('.tutorial-title');
    const contentEl = this.tooltip.querySelector('.tutorial-content');
    const progressEl = this.tooltip.querySelector('.tutorial-progress');
    const prevBtn = this.tooltip.querySelector('.tutorial-prev') as HTMLButtonElement;
    const nextBtn = this.tooltip.querySelector('.tutorial-next') as HTMLButtonElement;
    const finishBtn = this.tooltip.querySelector('.tutorial-finish') as HTMLButtonElement;

    if (titleEl) titleEl.textContent = step.title;
    if (contentEl) contentEl.innerHTML = step.content;
    if (progressEl) {
      progressEl.textContent = `Step ${index + 1} of ${TUTORIAL_STEPS.length}`;
    }

    // Update buttons
    if (prevBtn) prevBtn.disabled = index === 0;
    if (nextBtn) {
      nextBtn.classList.toggle('hidden', index === TUTORIAL_STEPS.length - 1);
    }
    if (finishBtn) {
      finishBtn.classList.toggle('hidden', index !== TUTORIAL_STEPS.length - 1);
    }

    // Highlight element
    this.clearHighlight();
    if (step.highlight) {
      this.highlightElement(step.highlight);
    }

    // Position tooltip
    this.positionTooltip(step);

    this.tooltip.classList.remove('hidden');
  }

  private highlightElement(selector: string): void {
    const element = document.querySelector(selector) as HTMLElement;
    if (element) {
      element.classList.add('tutorial-highlighted');
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }

  private clearHighlight(): void {
    document.querySelectorAll('.tutorial-highlighted').forEach(el => {
      el.classList.remove('tutorial-highlighted');
    });
  }

  private positionTooltip(step: TutorialStep): void {
    if (!this.tooltip) return;

    if (step.highlight) {
      const element = document.querySelector(step.highlight) as HTMLElement;
      if (element) {
        const rect = element.getBoundingClientRect();
        const position = step.position || 'bottom';

        switch (position) {
          case 'top':
            this.tooltip.style.top = `${rect.top - this.tooltip.offsetHeight - 20}px`;
            this.tooltip.style.left = `${rect.left + rect.width / 2 - this.tooltip.offsetWidth / 2}px`;
            break;
          case 'bottom':
            this.tooltip.style.top = `${rect.bottom + 20}px`;
            this.tooltip.style.left = `${rect.left + rect.width / 2 - this.tooltip.offsetWidth / 2}px`;
            break;
          case 'left':
            this.tooltip.style.top = `${rect.top + rect.height / 2 - this.tooltip.offsetHeight / 2}px`;
            this.tooltip.style.left = `${rect.left - this.tooltip.offsetWidth - 20}px`;
            break;
          case 'right':
            this.tooltip.style.top = `${rect.top + rect.height / 2 - this.tooltip.offsetHeight / 2}px`;
            this.tooltip.style.left = `${rect.right + 20}px`;
            break;
        }
        return;
      }
    }

    // Default centered position
    this.tooltip.style.top = '50%';
    this.tooltip.style.left = '50%';
    this.tooltip.style.transform = 'translate(-50%, -50%)';
  }

  isRunning(): boolean {
    return this.isActive;
  }
}
