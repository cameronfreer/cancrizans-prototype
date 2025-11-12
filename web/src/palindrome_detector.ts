/**
 * Palindrome Detector
 * Analyzes MIDI files for palindromic and symmetrical patterns
 */

import type { ParsedNote } from './midi_import.js';

export interface SymmetryAnalysis {
  overallScore: number; // 0-100, where 100 is perfect palindrome
  pitchSymmetry: number;
  rhythmSymmetry: number;
  velocitySymmetry: number;
  intervalSymmetry: number;
  isPalindrome: boolean;
  palindromicSegments: PalindromicSegment[];
  recommendations: string[];
}

export interface PalindromicSegment {
  startTime: number;
  endTime: number;
  symmetryScore: number;
  type: 'exact' | 'pitch' | 'rhythm' | 'interval';
  description: string;
}

export class PalindromeDetector {
  private tolerance: number = 0.1; // Timing tolerance for comparison

  /**
   * Analyze a sequence of notes for palindromic patterns
   */
  analyze(notes: ParsedNote[]): SymmetryAnalysis {
    if (notes.length === 0) {
      return this.emptyAnalysis();
    }

    // Sort notes by time
    const sortedNotes = [...notes].sort((a, b) => a.time - b.time);

    // Calculate various symmetry metrics
    const pitchSymmetry = this.calculatePitchSymmetry(sortedNotes);
    const rhythmSymmetry = this.calculateRhythmSymmetry(sortedNotes);
    const velocitySymmetry = this.calculateVelocitySymmetry(sortedNotes);
    const intervalSymmetry = this.calculateIntervalSymmetry(sortedNotes);

    // Weighted overall score
    const overallScore = Math.round(
      pitchSymmetry * 0.4 +
      rhythmSymmetry * 0.3 +
      intervalSymmetry * 0.2 +
      velocitySymmetry * 0.1
    );

    // Detect palindromic segments
    const palindromicSegments = this.detectPalindromicSegments(sortedNotes);

    // Generate recommendations
    const recommendations = this.generateRecommendations(
      pitchSymmetry,
      rhythmSymmetry,
      velocitySymmetry,
      intervalSymmetry
    );

    return {
      overallScore,
      pitchSymmetry,
      rhythmSymmetry,
      velocitySymmetry,
      intervalSymmetry,
      isPalindrome: overallScore >= 90,
      palindromicSegments,
      recommendations
    };
  }

  /**
   * Calculate pitch symmetry (retrograde)
   */
  private calculatePitchSymmetry(notes: ParsedNote[]): number {
    if (notes.length < 2) return 100;

    const pitches = notes.map(n => n.pitch);
    const reversedPitches = [...pitches].reverse();

    let matches = 0;
    for (let i = 0; i < pitches.length; i++) {
      if (pitches[i] === reversedPitches[i]) {
        matches++;
      }
    }

    return Math.round((matches / pitches.length) * 100);
  }

  /**
   * Calculate rhythm symmetry (time intervals)
   */
  private calculateRhythmSymmetry(notes: ParsedNote[]): number {
    if (notes.length < 2) return 100;

    // Calculate inter-onset intervals (IOIs)
    const intervals: number[] = [];
    for (let i = 1; i < notes.length; i++) {
      intervals.push(notes[i].time - notes[i - 1].time);
    }

    if (intervals.length === 0) return 100;

    // Compare with reversed intervals
    const reversedIntervals = [...intervals].reverse();
    let matches = 0;

    for (let i = 0; i < intervals.length; i++) {
      const diff = Math.abs(intervals[i] - reversedIntervals[i]);
      if (diff <= this.tolerance) {
        matches++;
      }
    }

    return Math.round((matches / intervals.length) * 100);
  }

  /**
   * Calculate velocity symmetry (dynamics)
   */
  private calculateVelocitySymmetry(notes: ParsedNote[]): number {
    if (notes.length < 2) return 100;

    const velocities = notes.map(n => n.velocity);
    const reversedVelocities = [...velocities].reverse();

    let totalDiff = 0;
    for (let i = 0; i < velocities.length; i++) {
      totalDiff += Math.abs(velocities[i] - reversedVelocities[i]);
    }

    const maxPossibleDiff = velocities.length * 127; // Max MIDI velocity
    const similarity = 1 - (totalDiff / maxPossibleDiff);

    return Math.round(similarity * 100);
  }

  /**
   * Calculate interval symmetry (melodic contour)
   */
  private calculateIntervalSymmetry(notes: ParsedNote[]): number {
    if (notes.length < 3) return 100;

    // Calculate pitch intervals
    const intervals: number[] = [];
    for (let i = 1; i < notes.length; i++) {
      intervals.push(notes[i].pitch - notes[i - 1].pitch);
    }

    if (intervals.length === 0) return 100;

    // Compare with inverted retrograde (crab canon pattern)
    const reversedIntervals = [...intervals].reverse().map(x => -x);
    let matches = 0;

    for (let i = 0; i < intervals.length; i++) {
      if (intervals[i] === reversedIntervals[i]) {
        matches++;
      }
    }

    return Math.round((matches / intervals.length) * 100);
  }

  /**
   * Detect palindromic segments within the piece
   */
  private detectPalindromicSegments(notes: ParsedNote[]): PalindromicSegment[] {
    const segments: PalindromicSegment[] = [];
    const minSegmentLength = 4; // Minimum notes for a segment

    // Sliding window approach
    for (let windowSize = minSegmentLength; windowSize <= notes.length / 2; windowSize++) {
      for (let start = 0; start <= notes.length - windowSize * 2; start++) {
        const firstHalf = notes.slice(start, start + windowSize);
        const secondHalf = notes.slice(start + windowSize, start + windowSize * 2);

        const symmetry = this.compareSegments(firstHalf, secondHalf);

        if (symmetry.score >= 80) {
          segments.push({
            startTime: firstHalf[0].time,
            endTime: secondHalf[secondHalf.length - 1].time + secondHalf[secondHalf.length - 1].duration,
            symmetryScore: symmetry.score,
            type: symmetry.type,
            description: `${windowSize * 2}-note ${symmetry.type} palindrome (${symmetry.score}% match)`
          });
        }
      }
    }

    // Remove overlapping segments, keep highest scoring
    return this.deduplicateSegments(segments);
  }

  /**
   * Compare two segments for palindromic patterns
   */
  private compareSegments(
    segment1: ParsedNote[],
    segment2: ParsedNote[]
  ): { score: number; type: 'exact' | 'pitch' | 'rhythm' | 'interval' } {
    if (segment1.length !== segment2.length) {
      return { score: 0, type: 'exact' };
    }

    const reversed = [...segment2].reverse();

    // Check for exact palindrome
    let exactMatches = 0;
    let pitchMatches = 0;
    let rhythmMatches = 0;

    for (let i = 0; i < segment1.length; i++) {
      const timeDiff = Math.abs(
        (segment1[i].time - segment1[0].time) -
        (reversed[i].time - reversed[0].time)
      );

      if (segment1[i].pitch === reversed[i].pitch && timeDiff <= this.tolerance) {
        exactMatches++;
      }

      if (segment1[i].pitch === reversed[i].pitch) {
        pitchMatches++;
      }

      if (timeDiff <= this.tolerance) {
        rhythmMatches++;
      }
    }

    const exactScore = (exactMatches / segment1.length) * 100;
    const pitchScore = (pitchMatches / segment1.length) * 100;
    const rhythmScore = (rhythmMatches / segment1.length) * 100;

    // Return highest scoring type
    if (exactScore >= Math.max(pitchScore, rhythmScore)) {
      return { score: Math.round(exactScore), type: 'exact' };
    } else if (pitchScore >= rhythmScore) {
      return { score: Math.round(pitchScore), type: 'pitch' };
    } else {
      return { score: Math.round(rhythmScore), type: 'rhythm' };
    }
  }

  /**
   * Remove overlapping segments, keeping highest scoring ones
   */
  private deduplicateSegments(segments: PalindromicSegment[]): PalindromicSegment[] {
    if (segments.length === 0) return [];

    // Sort by score (descending)
    const sorted = [...segments].sort((a, b) => b.symmetryScore - a.symmetryScore);

    const result: PalindromicSegment[] = [];

    for (const segment of sorted) {
      // Check if this segment overlaps significantly with existing ones
      const overlaps = result.some(existing => {
        const overlapStart = Math.max(segment.startTime, existing.startTime);
        const overlapEnd = Math.min(segment.endTime, existing.endTime);
        const overlapDuration = Math.max(0, overlapEnd - overlapStart);

        const segmentDuration = segment.endTime - segment.startTime;
        const overlapRatio = overlapDuration / segmentDuration;

        return overlapRatio > 0.5; // 50% overlap threshold
      });

      if (!overlaps) {
        result.push(segment);
      }
    }

    return result.sort((a, b) => a.startTime - b.startTime);
  }

  /**
   * Generate recommendations for improving palindromic properties
   */
  private generateRecommendations(
    pitchSymmetry: number,
    rhythmSymmetry: number,
    velocitySymmetry: number,
    intervalSymmetry: number
  ): string[] {
    const recommendations: string[] = [];

    if (pitchSymmetry < 70) {
      recommendations.push(
        'To improve pitch symmetry, ensure the second half mirrors the first half in reverse order'
      );
    }

    if (rhythmSymmetry < 70) {
      recommendations.push(
        'To improve rhythm symmetry, make the timing of notes in the second half match the first half in reverse'
      );
    }

    if (velocitySymmetry < 70) {
      recommendations.push(
        'To improve velocity symmetry, match the dynamics (loudness) pattern in reverse'
      );
    }

    if (intervalSymmetry < 70) {
      recommendations.push(
        'To improve interval symmetry, ensure melodic intervals are inverted in the second half (crab canon style)'
      );
    }

    if (recommendations.length === 0) {
      recommendations.push('Excellent palindromic structure! This piece exhibits strong symmetry.');
    }

    return recommendations;
  }

  private emptyAnalysis(): SymmetryAnalysis {
    return {
      overallScore: 0,
      pitchSymmetry: 0,
      rhythmSymmetry: 0,
      velocitySymmetry: 0,
      intervalSymmetry: 0,
      isPalindrome: false,
      palindromicSegments: [],
      recommendations: ['No notes to analyze']
    };
  }
}
