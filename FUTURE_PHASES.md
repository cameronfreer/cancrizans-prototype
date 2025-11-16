# Future Development Phases

This document outlines potential future enhancements for the Cancrizans project.

## Phase 10: Advanced Pattern Analysis

**Goal**: Add sophisticated musical pattern detection and tracking capabilities.

### Proposed Features:

1. **Motif Detection and Tracking**
   - Identify recurring melodic/rhythmic motifs
   - Track motif transformations throughout a piece
   - Analyze motif development and variation

2. **Melodic Sequence Identification**
   - Detect sequential patterns (rising/falling sequences)
   - Identify transposition levels
   - Analyze sequence consistency

3. **Imitation Point Detection**
   - Find points where voices imitate each other
   - Measure delay between imitations
   - Classify imitation types (exact, tonal, rhythmic)

4. **Thematic Development Analysis**
   - Track how themes evolve over time
   - Identify fragmentation and recombination
   - Analyze thematic relationships

### Implementation Notes:
- Use dynamic programming for pattern matching
- Implement fuzzy matching for approximate patterns
- Add visualization of pattern occurrences
- Export pattern analysis to structured formats (JSON, CSV)

---

## Phase 11: Harmonic Enhancement

**Goal**: Add comprehensive harmonic analysis capabilities.

### Proposed Features:

1. **Chord Progression Analysis**
   - Identify chord changes
   - Roman numeral analysis
   - Functional harmony classification
   - Common progression detection (e.g., ii-V-I)

2. **Functional Harmony Analysis**
   - Tonic/dominant/subdominant relationships
   - Secondary dominants
   - Modulation analysis
   - Harmonic rhythm

3. **Non-Chord Tone Analysis**
   - Passing tones
   - Neighbor tones
   - Suspensions and anticipations
   - Appoggiaturas
   - Escape tones

4. **Figured Bass Generation**
   - Generate figured bass from counterpoint
   - Validate figured bass accuracy
   - Support for baroque notation conventions

### Implementation Notes:
- Integrate with existing modulation_detection
- Use music21's chord detection as foundation
- Add custom rules for baroque/classical styles
- Provide LaTeX output for figured bass

---

## Phase 12: Performance Analysis

**Goal**: Analyze and generate performance-related aspects.

### Proposed Features:

1. **Articulation Analysis**
   - Detect articulation patterns
   - Suggest appropriate articulations
   - Style-specific articulation rules

2. **Dynamics Planning**
   - Suggest dynamic markings based on structure
   - Analyze terraced vs. crescendo dynamics
   - Period-appropriate dynamic ranges

3. **Ornamentation**
   - Detect ornament opportunities
   - Generate baroque ornaments (trills, mordents, turns)
   - Style-appropriate ornamentation rules

4. **Tempo Relationships**
   - Analyze proportional tempo relationships
   - Suggest metronome markings
   - Historical tempo conventions

---

## Phase 13: Extended Canon Types

**Goal**: Implement additional historical canon types.

### Proposed Features:

1. **Canon per tonos** (Circle canon)
   - Canon that modulates through all keys
   - Return to starting key
   - Infinite loop capability

2. **Canon in hypodiapasson** (Canon at the octave below)
   - Voice enters an octave lower
   - Support for multiple voice entries

3. **Canon in contrario motu** (already partially implemented as inversion)
   - Enhance existing inversion capabilities
   - Add axis selection heuristics

4. **Crab canon variants**
   - Multiple voices reading from different orientations
   - Combined retrograde + inversion canons
   - Asymmetric crab canons

---

## Implementation Priority

Based on project goals (analysis of palindromic structures and Bach canons):

1. **High Priority**: Phase 11 (Harmonic Enhancement)
   - Directly supports counterpoint analysis
   - Essential for baroque music understanding

2. **Medium Priority**: Phase 10 (Pattern Analysis)
   - Useful for musicological research
   - Complements existing analysis tools

3. **Medium Priority**: Phase 13 (Extended Canon Types)
   - Aligns with core "canon" focus
   - Historical authenticity

4. **Lower Priority**: Phase 12 (Performance Analysis)
   - Less critical for analysis focus
   - More relevant for score preparation

---

## Notes for Future Implementers

- All phases should maintain 100% test coverage
- Add examples to EXAMPLES.md for each new feature
- Update API documentation automatically
- Consider performance implications for large scores
- Maintain backward compatibility with existing APIs
