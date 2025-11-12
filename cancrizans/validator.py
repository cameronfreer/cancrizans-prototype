"""
Canon Quality Validator

Assess and validate palindromic canons for quality metrics.
"""

from typing import Dict, List, Any
from music21 import stream, interval, pitch
from cancrizans.canon import is_time_palindrome, pairwise_symmetry_map, interval_analysis


class CanonValidator:
    """Validate and assess quality of palindromic canons."""

    def __init__(self):
        """Initialize validator."""
        pass

    def validate(self, score: stream.Score) -> Dict[str, Any]:
        """Complete validation of a canon.

        Args:
            score: Musical score to validate

        Returns:
            Dictionary with validation results and quality scores
        """
        results = {
            'is_valid_canon': True,
            'errors': [],
            'warnings': [],
            'quality_scores': {},
            'metrics': {},
            'overall_quality': 0.0
        }

        # Check basic structure
        structure_valid = self._check_structure(score, results)

        if not structure_valid:
            results['is_valid_canon'] = False
            return results

        # Check palindrome property
        palindrome_valid = self._check_palindrome(score, results)

        # Assess musical qualities
        self._assess_melodic_quality(score, results)
        self._assess_harmonic_quality(score, results)
        self._assess_rhythmic_quality(score, results)
        self._assess_range_quality(score, results)
        self._assess_intervallic_quality(score, results)

        # Calculate overall quality score
        results['overall_quality'] = self._calculate_overall_quality(results)

        return results

    def _check_structure(self, score: stream.Score, results: Dict) -> bool:
        """Check basic structural requirements."""
        # Check for parts
        if len(score.parts) < 2:
            results['errors'].append("Canon must have at least 2 parts")
            return False

        # Check for notes (use flatten to handle measures)
        total_notes = sum(len(list(part.flatten().notes)) for part in score.parts)
        if total_notes == 0:
            results['errors'].append("Canon has no notes")
            return False

        # Check durations
        for i, part in enumerate(score.parts):
            if part.duration.quarterLength == 0:
                results['errors'].append(f"Part {i+1} has zero duration")
                return False

        results['metrics']['num_parts'] = len(score.parts)
        results['metrics']['total_notes'] = total_notes
        results['metrics']['duration'] = score.duration.quarterLength

        return True

    def _check_palindrome(self, score: stream.Score, results: Dict) -> bool:
        """Check if canon is a valid palindrome."""
        is_palindrome = is_time_palindrome(score)
        results['metrics']['is_palindrome'] = is_palindrome

        if not is_palindrome:
            results['warnings'].append("Canon is not a perfect time palindrome")

        # Get symmetry details
        symmetry_map = pairwise_symmetry_map(score)
        results['metrics']['symmetry_pairs'] = len(symmetry_map)

        return is_palindrome

    def _assess_melodic_quality(self, score: stream.Score, results: Dict):
        """Assess melodic quality."""
        melodic_score = 0.0
        part_scores = []

        for part in score.parts:
            if len(list(part.flatten().notes)) < 2:
                continue

            # Check for melodic motion
            pitches = [n.pitch.midi for n in part.flatten().notes]

            # Penalize excessive repetition
            unique_pitches = len(set(pitches))
            repetition_ratio = unique_pitches / len(pitches)

            # Penalize large leaps
            large_leaps = sum(1 for i in range(len(pitches)-1)
                            if abs(pitches[i+1] - pitches[i]) > 7)
            leap_penalty = large_leaps / (len(pitches) - 1)

            # Reward stepwise motion
            steps = sum(1 for i in range(len(pitches)-1)
                       if abs(pitches[i+1] - pitches[i]) <= 2)
            stepwise_ratio = steps / (len(pitches) - 1)

            # Calculate part score
            score_value = (
                repetition_ratio * 0.4 +
                (1 - leap_penalty) * 0.3 +
                stepwise_ratio * 0.3
            )
            part_scores.append(score_value)

        if part_scores:
            melodic_score = sum(part_scores) / len(part_scores)

        results['quality_scores']['melodic'] = melodic_score
        results['metrics']['melodic_variety'] = repetition_ratio if 'repetition_ratio' in locals() else 0
        results['metrics']['stepwise_motion'] = stepwise_ratio if 'stepwise_ratio' in locals() else 0

    def _assess_harmonic_quality(self, score: stream.Score, results: Dict):
        """Assess harmonic quality (when parts play together)."""
        harmonic_score = 0.7  # Default neutral score

        if len(score.parts) < 2:
            results['quality_scores']['harmonic'] = harmonic_score
            return

        # Sample points in time
        max_time = score.duration.quarterLength
        sample_points = [i * 0.25 for i in range(int(max_time / 0.25))]

        consonances = 0
        dissonances = 0

        for t in sample_points:
            sounding_notes = []
            for part in score.parts:
                for n in part.flatten().notes:
                    if n.offset <= t < n.offset + n.duration.quarterLength:
                        sounding_notes.append(n.pitch.midi)
                        break

            if len(sounding_notes) >= 2:
                # Check interval between voices
                interval_size = abs(sounding_notes[0] - sounding_notes[1]) % 12

                # Consonant intervals: unison, 3rds, 4ths, 5ths, 6ths, octaves
                if interval_size in [0, 3, 4, 5, 7, 8, 9]:
                    consonances += 1
                else:
                    dissonances += 1

        if consonances + dissonances > 0:
            harmonic_score = consonances / (consonances + dissonances)

        results['quality_scores']['harmonic'] = harmonic_score
        results['metrics']['consonance_ratio'] = harmonic_score

    def _assess_rhythmic_quality(self, score: stream.Score, results: Dict):
        """Assess rhythmic quality."""
        rhythmic_score = 0.0
        all_durations = []

        for part in score.parts:
            durations = [n.quarterLength for n in part.flatten().notes]
            all_durations.extend(durations)

        if not all_durations:
            results['quality_scores']['rhythmic'] = 0.0
            return

        # Assess rhythm variety
        unique_durations = len(set(all_durations))
        variety_score = min(unique_durations / 5.0, 1.0)  # Up to 5 different durations

        # Check for rhythmic patterns
        if len(all_durations) > 1:
            pattern_score = 0.5  # Neutral

            # Penalize if all durations are the same
            if unique_durations == 1:
                pattern_score = 0.3
        else:
            pattern_score = 0.5

        rhythmic_score = (variety_score + pattern_score) / 2

        results['quality_scores']['rhythmic'] = rhythmic_score
        results['metrics']['rhythm_variety'] = variety_score

    def _assess_range_quality(self, score: stream.Score, results: Dict):
        """Assess pitch range quality."""
        range_score = 0.0
        ranges = []

        for part in score.parts:
            if len(list(part.flatten().notes)) == 0:
                continue

            pitches = [n.pitch.midi for n in part.flatten().notes]
            part_range = max(pitches) - min(pitches)
            ranges.append(part_range)

            # Check if within reasonable range
            min_pitch = min(pitches)
            max_pitch = max(pitches)

            # Penalize if too low or too high
            if min_pitch < 48 or max_pitch > 84:  # C3 to C6
                results['warnings'].append(f"Part has extreme range: {min_pitch}-{max_pitch}")

        if ranges:
            avg_range = sum(ranges) / len(ranges)

            # Ideal range: 12-24 semitones (octave to two octaves)
            if 12 <= avg_range <= 24:
                range_score = 1.0
            elif avg_range < 12:
                range_score = avg_range / 12.0
            else:
                range_score = max(0.5, 1.0 - (avg_range - 24) / 24.0)

        results['quality_scores']['range'] = range_score
        results['metrics']['average_range'] = sum(ranges) / len(ranges) if ranges else 0

    def _assess_intervallic_quality(self, score: stream.Score, results: Dict):
        """Assess interval usage quality."""
        try:
            analysis = interval_analysis(score)

            # Good if interval diversity is high
            diversity_score = min(analysis['interval_diversity'] / 0.8, 1.0)

            # Good if average interval is reasonable (not too large)
            avg_interval = analysis['average_interval_size']
            interval_score = 1.0 if avg_interval <= 3 else max(0.5, 1.0 - (avg_interval - 3) / 5.0)

            intervallic_score = (diversity_score + interval_score) / 2

            results['quality_scores']['intervallic'] = intervallic_score
            results['metrics']['interval_diversity'] = analysis['interval_diversity']
            results['metrics']['avg_interval_size'] = avg_interval

        except Exception as e:
            results['warnings'].append(f"Could not analyze intervals: {e}")
            results['quality_scores']['intervallic'] = 0.5

    def _calculate_overall_quality(self, results: Dict) -> float:
        """Calculate overall quality score."""
        scores = results['quality_scores']

        # Weighted average
        weights = {
            'melodic': 0.25,
            'harmonic': 0.20,
            'rhythmic': 0.15,
            'range': 0.15,
            'intervallic': 0.25
        }

        overall = sum(scores.get(key, 0.5) * weight
                     for key, weight in weights.items())

        # Penalize if not a palindrome
        if not results['metrics'].get('is_palindrome', False):
            overall *= 0.8

        return overall

    def get_quality_grade(self, overall_quality: float) -> str:
        """Get letter grade for quality score.

        Args:
            overall_quality: Quality score (0-1)

        Returns:
            Letter grade (A+ to F)
        """
        if overall_quality >= 0.95:
            return 'A+'
        elif overall_quality >= 0.90:
            return 'A'
        elif overall_quality >= 0.85:
            return 'A-'
        elif overall_quality >= 0.80:
            return 'B+'
        elif overall_quality >= 0.75:
            return 'B'
        elif overall_quality >= 0.70:
            return 'B-'
        elif overall_quality >= 0.65:
            return 'C+'
        elif overall_quality >= 0.60:
            return 'C'
        elif overall_quality >= 0.55:
            return 'C-'
        elif overall_quality >= 0.50:
            return 'D'
        else:
            return 'F'

    def get_recommendations(self, results: Dict) -> List[str]:
        """Get improvement recommendations based on validation results.

        Args:
            results: Validation results

        Returns:
            List of recommendation strings
        """
        recommendations = []
        scores = results['quality_scores']

        if scores.get('melodic', 0) < 0.6:
            recommendations.append(
                "Improve melodic quality: Use more stepwise motion and avoid excessive leaps"
            )

        if scores.get('harmonic', 0) < 0.6:
            recommendations.append(
                "Improve harmonic quality: Increase consonant intervals between voices"
            )

        if scores.get('rhythmic', 0) < 0.6:
            recommendations.append(
                "Improve rhythmic quality: Add more variety in note durations"
            )

        if scores.get('range', 0) < 0.6:
            recommendations.append(
                "Improve range: Aim for 1-2 octave range per part"
            )

        if scores.get('intervallic', 0) < 0.6:
            recommendations.append(
                "Improve interval usage: Increase interval diversity and reduce large leaps"
            )

        if not results['metrics'].get('is_palindrome', False):
            recommendations.append(
                "⚠ This is not a perfect palindrome. Use mirror_canon() to ensure symmetry."
            )

        if not recommendations:
            recommendations.append("✓ Excellent canon! No improvements needed.")

        return recommendations
