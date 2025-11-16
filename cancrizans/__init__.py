"""
Cancrizans: Explore and render J.S. Bach's Crab Canon as a strict palindrome.

This package provides tools for analyzing, verifying, and rendering
palindromic musical structures, with a focus on Bach's Canon Cancrizans
from The Musical Offering (BWV 1079).
"""

__version__ = "0.22.0"

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
]
