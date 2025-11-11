/**
 * Accessibility enhancements
 * ARIA labels, keyboard navigation, focus management
 */

export class AccessibilityManager {
  private announcer: HTMLElement;

  constructor() {
    // Create live region for screen reader announcements
    this.announcer = this.createAnnouncer();
    this.setupKeyboardNav();
    this.setupFocusManagement();
  }

  private createAnnouncer(): HTMLElement {
    const announcer = document.createElement('div');
    announcer.setAttribute('role', 'status');
    announcer.setAttribute('aria-live', 'polite');
    announcer.setAttribute('aria-atomic', 'true');
    announcer.className = 'sr-only';
    document.body.appendChild(announcer);
    return announcer;
  }

  announce(message: string): void {
    this.announcer.textContent = message;
    setTimeout(() => {
      this.announcer.textContent = '';
    }, 1000);
  }

  private setupKeyboardNav(): void {
    document.addEventListener('keydown', (e) => {
      // Skip if typing in input
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) {
        return;
      }

      switch (e.key) {
        case ' ':
          // Space bar handled in ui.ts
          break;
        case 'Escape':
          // Close any open dialogs/modals
          this.announce('Interaction cancelled');
          break;
        case 'Tab':
          // Let browser handle tab navigation
          break;
      }
    });
  }

  private setupFocusManagement(): void {
    // Add focus visible indicators
    document.addEventListener('mousedown', () => {
      document.body.classList.add('using-mouse');
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        document.body.classList.remove('using-mouse');
      }
    });
  }

  announcePlayback(isPlaying: boolean): void {
    this.announce(isPlaying ? 'Playback started' : 'Playback stopped');
  }

  announceNoteAdded(pitch: string): void {
    this.announce(`Note ${pitch} added`);
  }

  announceNoteRemoved(): void {
    this.announce('Note removed');
  }

  announceTemplateLoaded(name: string): void {
    this.announce(`Template ${name} loaded`);
  }

  announceError(message: string): void {
    this.announce(`Error: ${message}`);
  }
}

// Focus trap for modals
export class FocusTrap {
  private container: HTMLElement;
  private firstFocusable: HTMLElement | null = null;
  private lastFocusable: HTMLElement | null = null;
  private previouslyFocused: HTMLElement | null = null;

  constructor(container: HTMLElement) {
    this.container = container;
    this.previouslyFocused = document.activeElement as HTMLElement;
    this.updateFocusables();
    this.activate();
  }

  private updateFocusables(): void {
    const focusables = this.container.querySelectorAll(
      'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'
    );

    if (focusables.length > 0) {
      this.firstFocusable = focusables[0] as HTMLElement;
      this.lastFocusable = focusables[focusables.length - 1] as HTMLElement;
    }
  }

  private activate(): void {
    this.container.addEventListener('keydown', this.handleKeydown.bind(this));
    this.firstFocusable?.focus();
  }

  private handleKeydown(e: KeyboardEvent): void {
    if (e.key !== 'Tab') return;

    if (e.shiftKey) {
      if (document.activeElement === this.firstFocusable) {
        e.preventDefault();
        this.lastFocusable?.focus();
      }
    } else {
      if (document.activeElement === this.lastFocusable) {
        e.preventDefault();
        this.firstFocusable?.focus();
      }
    }
  }

  deactivate(): void {
    this.container.removeEventListener('keydown', this.handleKeydown.bind(this));
    this.previouslyFocused?.focus();
  }
}
