"""
Cancrizans: Explore and render J.S. Bach's Crab Canon as a strict palindrome.

This package provides tools for analyzing, verifying, and rendering
palindromic musical structures, with a focus on Bach's Canon Cancrizans
from The Musical Offering (BWV 1079).
"""

__version__ = "0.19.0"

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
)
from cancrizans.bach_crab import assemble_crab_from_theme, load_bach_crab_canon
from cancrizans.transformation_chain import TransformationChain

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
    # Theme and utilities
    "assemble_crab_from_theme",
    "load_bach_crab_canon",
    "TransformationChain",
]
