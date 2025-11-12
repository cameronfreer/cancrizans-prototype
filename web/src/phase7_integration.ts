/**
 * Phase 7: Advanced Features Integration
 * Integrates MIDI import, palindrome detection, transformation composer,
 * animated visualization, and export/share features
 */

import { MidiImporter, type MidiFileInfo, type ParsedNote } from './midi_import.js';
import { PalindromeDetector } from './palindrome_detector.js';
import {
  TransformationComposer,
  type TransformationType
} from './transformation_composer.js';
import { AnimatedVisualization } from './animated_visualization.js';
import { ExportShareSystem, type Composition } from './export_share.js';

export class Phase7Manager {
  private midiImporter: MidiImporter;
  private palindromeDetector: PalindromeDetector;
  private transformationComposer: TransformationComposer;
  private animatedViz: AnimatedVisualization | null = null;
  private exportShare: ExportShareSystem;
  private currentNotes: ParsedNote[] = [];
  private currentChainId: string | null = null;

  constructor() {
    this.midiImporter = new MidiImporter();
    this.palindromeDetector = new PalindromeDetector();
    this.transformationComposer = new TransformationComposer();
    this.exportShare = new ExportShareSystem();

    this.initMidiImport();
    this.initPalindromeDetector();
    this.initTransformationComposer();
    this.initAnimatedVisualization();
    this.initExportShare();
    this.checkForSharedComposition();
  }

  /**
   * Initialize MIDI import functionality
   */
  private initMidiImport(): void {
    // File select button
    const selectBtn = document.getElementById('select-file-btn');
    if (selectBtn) {
      selectBtn.addEventListener('click', () => {
        this.midiImporter.triggerFileSelect();
      });
    }

    // Handle imported MIDI
    this.midiImporter.onImport((info: MidiFileInfo) => {
      this.handleMidiImport(info);
    });
  }

  /**
   * Handle imported MIDI file
   */
  private handleMidiImport(info: MidiFileInfo): void {
    this.currentNotes = info.notes;

    // Show import info
    const importInfo = document.getElementById('import-info');
    if (importInfo) {
      importInfo.innerHTML = `
        <h3>✓ Imported: ${info.name}</h3>
        <p>
          <strong>${info.notes.length}</strong> notes •
          <strong>${info.trackCount}</strong> track(s) •
          Duration: <strong>${info.duration.toFixed(2)}s</strong> •
          Tempo: <strong>${info.tempo}</strong> BPM
        </p>
      `;
      importInfo.classList.remove('hidden');
    }

    // Analyze for palindrome
    this.analyzePalindrome(info.notes);

    // Update animated visualization
    if (this.animatedViz) {
      this.animatedViz.setNotes(info.notes);
    }
  }

  /**
   * Initialize palindrome detector
   */
  private initPalindromeDetector(): void {
    // The analysis is triggered when MIDI is imported
  }

  /**
   * Analyze notes for palindromic patterns
   */
  private analyzePalindrome(notes: ParsedNote[]): void {
    const analysis = this.palindromeDetector.analyze(notes);

    // Show palindrome section
    const section = document.getElementById('palindrome-section');
    if (section) {
      section.hidden = false;
    }

    // Update overall score
    const overallScoreFill = document.getElementById('overall-score-fill');
    const overallScoreText = document.getElementById('overall-score-text');
    if (overallScoreFill && overallScoreText) {
      overallScoreFill.style.width = `${analysis.overallScore}%`;
      overallScoreText.textContent = `${analysis.overallScore}%`;
    }

    // Update individual scores
    this.updateScore('pitch-score', analysis.pitchSymmetry);
    this.updateScore('rhythm-score', analysis.rhythmSymmetry);
    this.updateScore('velocity-score', analysis.velocitySymmetry);
    this.updateScore('interval-score', analysis.intervalSymmetry);

    // Show verdict
    const verdict = document.getElementById('palindrome-verdict');
    if (verdict) {
      if (analysis.isPalindrome) {
        verdict.className = 'verdict palindrome';
        verdict.textContent = '✓ This is a palindromic composition!';
      } else {
        verdict.className = 'verdict not-palindrome';
        verdict.textContent = `⚠ Not a perfect palindrome (${analysis.overallScore}% symmetry)`;
      }
    }

    // Show palindromic segments
    const segments = document.getElementById('palindrome-segments');
    if (segments && analysis.palindromicSegments.length > 0) {
      segments.innerHTML = '<h4>Palindromic Segments Found:</h4>';
      analysis.palindromicSegments.forEach((segment) => {
        const div = document.createElement('div');
        div.className = 'segment-item';
        div.innerHTML = `
          <span>${segment.description}</span>
          <span class="score">${segment.symmetryScore}%</span>
        `;
        segments.appendChild(div);
      });
    }

    // Show recommendations
    const recommendations = document.getElementById('palindrome-recommendations');
    if (recommendations) {
      recommendations.innerHTML = '<h4>Analysis & Recommendations:</h4><ul>';
      analysis.recommendations.forEach((rec) => {
        const li = document.createElement('li');
        li.textContent = rec;
        recommendations.querySelector('ul')?.appendChild(li);
      });
      recommendations.innerHTML += '</ul>';
    }
  }

  /**
   * Update score display
   */
  private updateScore(elementId: string, score: number): void {
    const el = document.getElementById(elementId);
    if (el) {
      el.textContent = `${score}%`;
    }
  }

  /**
   * Initialize transformation composer
   */
  private initTransformationComposer(): void {
    // New chain button
    const newChainBtn = document.getElementById('new-chain-btn');
    if (newChainBtn) {
      newChainBtn.addEventListener('click', () => {
        const name = prompt('Enter chain name:', 'My Transformation');
        if (name) {
          this.currentChainId = this.transformationComposer.createChain(name);
          this.showChainEditor();
        }
      });
    }

    // Preset buttons
    document.getElementById('preset-crab-btn')?.addEventListener('click', () => {
      this.currentChainId = this.transformationComposer.createCrabCanon();
      this.showChainEditor();
    });

    document.getElementById('preset-table-btn')?.addEventListener('click', () => {
      this.currentChainId = this.transformationComposer.createTableCanon();
      this.showChainEditor();
    });

    document.getElementById('preset-complex-btn')?.addEventListener('click', () => {
      this.currentChainId = this.transformationComposer.createComplexExample();
      this.showChainEditor();
    });

    // Transform type selection
    const transformType = document.getElementById('transform-type') as HTMLSelectElement;
    if (transformType) {
      transformType.addEventListener('change', (e) => {
        this.showTransformParams((e.target as HTMLSelectElement).value as TransformationType);
      });
    }

    // Add transform button
    document.getElementById('add-transform-btn')?.addEventListener('click', () => {
      this.addTransformation();
    });

    // Apply chain button
    document.getElementById('apply-chain-btn')?.addEventListener('click', () => {
      this.applyTransformationChain();
    });

    // Export chain button
    document.getElementById('export-chain-btn')?.addEventListener('click', () => {
      this.exportTransformationChain();
    });
  }

  /**
   * Show chain editor
   */
  private showChainEditor(): void {
    if (!this.currentChainId) return;

    const editor = document.getElementById('chain-editor');
    if (editor) {
      editor.classList.remove('hidden');
    }

    const chain = this.transformationComposer.getChain(this.currentChainId);
    if (chain) {
      const nameEl = document.getElementById('chain-name');
      if (nameEl) {
        nameEl.textContent = chain.name;
      }

      this.updateChainSteps();
    }
  }

  /**
   * Show transformation parameters based on type
   */
  private showTransformParams(type: TransformationType): void {
    const paramsDiv = document.getElementById('transform-params');
    if (!paramsDiv) return;

    paramsDiv.innerHTML = '';

    if (!type) {
      paramsDiv.classList.add('hidden');
      return;
    }

    paramsDiv.classList.remove('hidden');

    switch (type) {
      case 'inversion':
      case 'reflect':
        paramsDiv.innerHTML = `
          <label>Axis (MIDI note): <input type="number" id="param-axis" value="60" min="0" max="127"></label>
        `;
        break;
      case 'augmentation':
      case 'diminution':
        paramsDiv.innerHTML = `
          <label>Factor: <input type="number" id="param-factor" value="2" min="1" max="8" step="0.5"></label>
        `;
        break;
      case 'transpose':
        paramsDiv.innerHTML = `
          <label>Semitones: <input type="number" id="param-semitones" value="0" min="-24" max="24"></label>
        `;
        break;
      case 'repeat':
        paramsDiv.innerHTML = `
          <label>Times: <input type="number" id="param-times" value="2" min="2" max="8"></label>
        `;
        break;
    }
  }

  /**
   * Add transformation to current chain
   */
  private addTransformation(): void {
    if (!this.currentChainId) return;

    const transformType = document.getElementById('transform-type') as HTMLSelectElement;
    const type = transformType.value as TransformationType;

    if (!type) {
      alert('Please select a transformation type');
      return;
    }

    // Get parameters
    const parameters: Record<string, number> = {};

    const axisInput = document.getElementById('param-axis') as HTMLInputElement;
    const factorInput = document.getElementById('param-factor') as HTMLInputElement;
    const semitonesInput = document.getElementById('param-semitones') as HTMLInputElement;
    const timesInput = document.getElementById('param-times') as HTMLInputElement;

    if (axisInput) parameters.axis = parseInt(axisInput.value);
    if (factorInput) parameters.factor = parseFloat(factorInput.value);
    if (semitonesInput) parameters.semitones = parseInt(semitonesInput.value);
    if (timesInput) parameters.times = parseInt(timesInput.value);

    // Add to chain
    this.transformationComposer.addTransformation(this.currentChainId, type, parameters);

    // Update display
    this.updateChainSteps();

    // Reset selection
    transformType.value = '';
    this.showTransformParams('' as TransformationType);
  }

  /**
   * Update chain steps display
   */
  private updateChainSteps(): void {
    if (!this.currentChainId) return;

    const stepsDiv = document.getElementById('chain-steps');
    if (!stepsDiv) return;

    const chain = this.transformationComposer.getChain(this.currentChainId);
    if (!chain) return;

    stepsDiv.innerHTML = '';

    if (chain.transformations.length === 0) {
      stepsDiv.innerHTML = '<p style="color: #7f8c8d; text-align: center;">No transformations yet</p>';
      return;
    }

    chain.transformations.forEach((transform, index) => {
      const stepDiv = document.createElement('div');
      stepDiv.className = 'chain-step';
      stepDiv.innerHTML = `
        <div class="step-number">${index + 1}</div>
        <div class="step-description">${transform.description}</div>
        <button class="step-remove" data-index="${index}">×</button>
      `;

      // Remove button
      const removeBtn = stepDiv.querySelector('.step-remove');
      if (removeBtn) {
        removeBtn.addEventListener('click', () => {
          // Remove transformation (would need to add this method to TransformationComposer)
          this.updateChainSteps();
        });
      }

      stepsDiv.appendChild(stepDiv);
    });
  }

  /**
   * Apply transformation chain to current notes
   */
  private applyTransformationChain(): void {
    if (!this.currentChainId || this.currentNotes.length === 0) {
      alert('Please import a MIDI file first');
      return;
    }

    const transformed = this.transformationComposer.applyChain(this.currentChainId, this.currentNotes);

    // Update visualization
    if (this.animatedViz) {
      this.animatedViz.setNotes(transformed);
    }

    // Update current notes
    this.currentNotes = transformed;

    // Re-analyze
    this.analyzePalindrome(transformed);

    alert(`Transformation applied! ${transformed.length} notes in result.`);
  }

  /**
   * Export transformation chain
   */
  private exportTransformationChain(): void {
    if (!this.currentChainId) return;

    const json = this.transformationComposer.exportChain(this.currentChainId);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'transformation_chain.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  /**
   * Initialize animated visualization
   */
  private initAnimatedVisualization(): void {
    const canvas = document.getElementById('animated-canvas') as HTMLCanvasElement;
    if (!canvas) return;

    this.animatedViz = new AnimatedVisualization(canvas);

    // Color scheme selector
    const colorScheme = document.getElementById('color-scheme') as HTMLSelectElement;
    if (colorScheme) {
      colorScheme.addEventListener('change', (e) => {
        const scheme = (e.target as HTMLSelectElement).value as any;
        this.animatedViz?.updateConfig({ colorScheme: scheme });
      });
    }

    // Show note names checkbox
    const showNoteNames = document.getElementById('show-note-names') as HTMLInputElement;
    if (showNoteNames) {
      showNoteNames.addEventListener('change', (e) => {
        this.animatedViz?.updateConfig({ showNoteNames: (e.target as HTMLInputElement).checked });
      });
    }
  }

  /**
   * Initialize export and share features
   */
  private initExportShare(): void {
    // Export MIDI button
    document.getElementById('export-midi-btn')?.addEventListener('click', () => {
      this.exportMIDI();
    });

    // Copy share link button
    document.getElementById('copy-share-link-btn')?.addEventListener('click', async () => {
      await this.copyShareLink();
    });

    // Save locally button
    document.getElementById('save-local-btn')?.addEventListener('click', () => {
      this.saveLocally();
    });

    // Load from local storage button
    document.getElementById('load-local-btn')?.addEventListener('click', () => {
      this.loadFromLocalStorage();
    });
  }

  /**
   * Export current notes as MIDI
   */
  private async exportMIDI(): Promise<void> {
    if (this.currentNotes.length === 0) {
      this.showStatus('No notes to export', 'error');
      return;
    }

    try {
      await this.exportShare.exportToMIDI(this.currentNotes, 'composition.mid', 120);
      this.showStatus('MIDI file exported successfully!', 'success');
    } catch (error) {
      this.showStatus('Error exporting MIDI file', 'error');
    }
  }

  /**
   * Copy share link to clipboard
   */
  private async copyShareLink(): Promise<void> {
    if (this.currentNotes.length === 0) {
      this.showStatus('No composition to share', 'error');
      return;
    }

    const composition: Composition = {
      version: '1.0.0',
      name: 'My Composition',
      description: 'Created with Cancrizans',
      notes: this.currentNotes,
      metadata: {
        created: new Date(),
        modified: new Date(),
        bpm: 120
      }
    };

    const success = await this.exportShare.copyShareLink(composition);

    if (success) {
      this.showStatus('✓ Share link copied to clipboard!', 'success');
    } else {
      this.showStatus('Failed to copy share link', 'error');
    }
  }

  /**
   * Save composition to local storage
   */
  private saveLocally(): void {
    if (this.currentNotes.length === 0) {
      this.showStatus('No composition to save', 'error');
      return;
    }

    const name = prompt('Enter a name for this composition:', 'My Composition');
    if (!name) return;

    const composition: Composition = {
      version: '1.0.0',
      name,
      description: 'Saved locally',
      notes: this.currentNotes,
      metadata: {
        created: new Date(),
        modified: new Date()
      }
    };

    try {
      this.exportShare.saveToLocalStorage(name, composition);
      this.showStatus(`✓ Saved "${name}" locally!`, 'success');
    } catch (error) {
      this.showStatus('Error saving composition', 'error');
    }
  }

  /**
   * Load composition from local storage
   */
  private loadFromLocalStorage(): void {
    const saved = this.exportShare.listSavedCompositions();

    if (saved.length === 0) {
      alert('No saved compositions found');
      return;
    }

    let message = 'Select a composition to load:\n\n';
    saved.forEach((item, index) => {
      message += `${index + 1}. ${item.name} (${item.modified.toLocaleDateString()})\n`;
    });

    const selection = prompt(message + '\nEnter number:');
    if (!selection) return;

    const index = parseInt(selection) - 1;
    if (index < 0 || index >= saved.length) {
      alert('Invalid selection');
      return;
    }

    const composition = this.exportShare.loadFromLocalStorage(saved[index].key);
    if (composition) {
      this.currentNotes = composition.notes;

      if (this.animatedViz) {
        this.animatedViz.setNotes(composition.notes);
      }

      this.analyzePalindrome(composition.notes);
      this.showStatus(`✓ Loaded "${composition.name}"!`, 'success');
    }
  }

  /**
   * Check for shared composition in URL
   */
  private checkForSharedComposition(): void {
    const composition = this.exportShare.decodeFromURL();
    if (composition) {
      this.currentNotes = composition.notes;

      if (this.animatedViz) {
        this.animatedViz.setNotes(composition.notes);
      }

      this.analyzePalindrome(composition.notes);
      this.showStatus(`✓ Loaded shared composition: "${composition.name}"`, 'success');
    }
  }

  /**
   * Show status message
   */
  private showStatus(message: string, type: 'success' | 'error'): void {
    const statusEl = document.getElementById('share-status');
    if (!statusEl) return;

    statusEl.textContent = message;
    statusEl.className = `status-message ${type}`;
    statusEl.classList.remove('hidden');

    setTimeout(() => {
      statusEl.classList.add('hidden');
    }, 3000);
  }

  /**
   * Start animated visualization playback
   */
  public startAnimation(): void {
    this.animatedViz?.start();
  }

  /**
   * Stop animated visualization playback
   */
  public stopAnimation(): void {
    this.animatedViz?.stop();
  }

  /**
   * Get current notes
   */
  public getCurrentNotes(): ParsedNote[] {
    return this.currentNotes;
  }
}
