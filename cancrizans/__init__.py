"""
Cancrizans: Explore and render J.S. Bach's Crab Canon as a strict palindrome.

This package provides tools for analyzing, verifying, and rendering
palindromic musical structures, with a focus on Bach's Canon Cancrizans
from The Musical Offering (BWV 1079).
"""

__version__ = "0.27.0"

from cancrizans.canon import (
    # Basic transformations
    retrograde,
    invert,
    augmentation,
    diminution,
    mirror_canon,
    time_align,
    # Advanced canonical techniques
    stretto,
    canon_at_interval,
    proportional_canon,
    # Advanced canon types (Phase 9)
    table_canon,
    mensuration_canon,
    spiral_canon,
    solve_puzzle_canon,
    # Verification and analysis
    is_time_palindrome,
    pairwise_symmetry_map,
    interval_analysis,
    harmonic_analysis,
    rhythm_analysis,
    counterpoint_check,
    # Advanced analysis tools
    spectral_analysis,
    symmetry_metrics,
    chord_progression_analysis,
    compare_canons,
    # Music theory & counterpoint analysis
    voice_leading_analysis,
    cadence_detection,
    modulation_detection,
    species_counterpoint_check,
    # Phase 11: Harmonic Enhancement
    analyze_chord_progressions,
    functional_harmony_analysis,
    analyze_nonchord_tones,
    generate_figured_bass,
)
from cancrizans.bach_crab import assemble_crab_from_theme, load_bach_crab_canon
from cancrizans.transformation_chain import TransformationChain
from cancrizans.generator import CanonGenerator
from cancrizans.io import (
    # Basic I/O
    to_midi,
    to_musicxml,
    to_lilypond,
    to_abc,
    load_score,
    # Advanced I/O
    export_all,
    convert_format,
    validate_import,
    # Metadata
    set_metadata,
    get_metadata,
    # Score manipulation
    merge_scores,
    extract_parts,
    # Advanced MIDI
    apply_velocity_curve,
    set_midi_program,
    apply_tempo_curve,
    to_midi_advanced,
    analyze_midi_file,
)
from cancrizans.research import (
    # Analysis classes
    CanonAnalyzer,
    BatchAnalyzer,
    ResearchExporter,
    # Corpus analysis
    analyze_corpus,
    # Advanced research tools
    batch_visualize,
    generate_educational_examples,
    generate_research_report,
    compare_corpus_canons,
)

__all__ = [
    # Basic transformations
    "retrograde",
    "invert",
    "augmentation",
    "diminution",
    "mirror_canon",
    "time_align",
    # Advanced canonical techniques
    "stretto",
    "canon_at_interval",
    "proportional_canon",
    # Advanced canon types (Phase 9)
    "table_canon",
    "mensuration_canon",
    "spiral_canon",
    "solve_puzzle_canon",
    # Verification and analysis
    "is_time_palindrome",
    "pairwise_symmetry_map",
    "interval_analysis",
    "harmonic_analysis",
    "rhythm_analysis",
    "counterpoint_check",
    # Advanced analysis tools
    "spectral_analysis",
    "symmetry_metrics",
    "chord_progression_analysis",
    "compare_canons",
    # Music theory & counterpoint analysis
    "voice_leading_analysis",
    "cadence_detection",
    "modulation_detection",
    "species_counterpoint_check",
    # Phase 11: Harmonic Enhancement
    "analyze_chord_progressions",
    "functional_harmony_analysis",
    "analyze_nonchord_tones",
    "generate_figured_bass",
    # Theme and utilities
    "assemble_crab_from_theme",
    "load_bach_crab_canon",
    "TransformationChain",
    # Algorithmic generation
    "CanonGenerator",
    # Basic I/O
    "to_midi",
    "to_musicxml",
    "to_lilypond",
    "to_abc",
    "load_score",
    # Advanced I/O
    "export_all",
    "convert_format",
    "validate_import",
    # Metadata
    "set_metadata",
    "get_metadata",
    # Score manipulation
    "merge_scores",
    "extract_parts",
    # Advanced MIDI
    "apply_velocity_curve",
    "set_midi_program",
    "apply_tempo_curve",
    "to_midi_advanced",
    "analyze_midi_file",
    # Research & analysis
    "CanonAnalyzer",
    "BatchAnalyzer",
    "ResearchExporter",
    "analyze_corpus",
    "batch_visualize",
    "generate_educational_examples",
    "generate_research_report",
    "compare_corpus_canons",
]
