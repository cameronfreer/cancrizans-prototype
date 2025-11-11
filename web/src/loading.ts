/**
 * Loading state management
 * Shows loading indicators and handles async operations
 */

export class LoadingManager {
  private loadingOverlay: HTMLElement | null = null;
  private loadingCount: number = 0;

  constructor() {
    this.createLoadingOverlay();
  }

  private createLoadingOverlay(): void {
    this.loadingOverlay = document.createElement('div');
    this.loadingOverlay.id = 'loading-overlay';
    this.loadingOverlay.className = 'loading-overlay hidden';
    this.loadingOverlay.setAttribute('role', 'alert');
    this.loadingOverlay.setAttribute('aria-busy', 'true');
    this.loadingOverlay.innerHTML = `
      <div class="loading-spinner">
        <div class="spinner"></div>
        <p id="loading-message">Loading...</p>
      </div>
    `;
    document.body.appendChild(this.loadingOverlay);
  }

  show(message: string = 'Loading...'): void {
    this.loadingCount++;
    if (this.loadingOverlay) {
      const messageEl = this.loadingOverlay.querySelector('#loading-message');
      if (messageEl) {
        messageEl.textContent = message;
      }
      this.loadingOverlay.classList.remove('hidden');
    }
  }

  hide(): void {
    this.loadingCount = Math.max(0, this.loadingCount - 1);
    if (this.loadingCount === 0 && this.loadingOverlay) {
      this.loadingOverlay.classList.add('hidden');
    }
  }

  async withLoading<T>(promise: Promise<T>, message: string = 'Loading...'): Promise<T> {
    this.show(message);
    try {
      const result = await promise;
      return result;
    } finally {
      this.hide();
    }
  }
}

// Error boundary
export class ErrorHandler {
  private errorContainer: HTMLElement | null = null;

  constructor() {
    this.createErrorContainer();
    this.setupGlobalErrorHandlers();
  }

  private createErrorContainer(): void {
    this.errorContainer = document.createElement('div');
    this.errorContainer.id = 'error-container';
    this.errorContainer.className = 'error-container hidden';
    this.errorContainer.setAttribute('role', 'alert');
    this.errorContainer.setAttribute('aria-live', 'assertive');
    document.body.appendChild(this.errorContainer);
  }

  private setupGlobalErrorHandlers(): void {
    window.addEventListener('error', (event) => {
      console.error('Global error:', event.error);
      this.showError('An unexpected error occurred. Please refresh the page.');
    });

    window.addEventListener('unhandledrejection', (event) => {
      console.error('Unhandled rejection:', event.reason);
      this.showError('An error occurred while loading data.');
    });
  }

  showError(message: string, details?: string): void {
    if (!this.errorContainer) return;

    this.errorContainer.innerHTML = `
      <div class="error-content">
        <div class="error-icon">⚠️</div>
        <div class="error-text">
          <h3>Error</h3>
          <p>${message}</p>
          ${details ? `<details><summary>Details</summary><pre>${details}</pre></details>` : ''}
        </div>
        <button class="error-close" onclick="this.parentElement.parentElement.classList.add('hidden')">
          ✕
        </button>
      </div>
    `;

    this.errorContainer.classList.remove('hidden');

    // Auto-hide after 10 seconds
    setTimeout(() => {
      this.hideError();
    }, 10000);
  }

  hideError(): void {
    this.errorContainer?.classList.add('hidden');
  }

  async wrapAsync<T>(
    fn: () => Promise<T>,
    errorMessage: string = 'Operation failed'
  ): Promise<T | null> {
    try {
      return await fn();
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      this.showError(errorMessage, message);
      return null;
    }
  }
}
