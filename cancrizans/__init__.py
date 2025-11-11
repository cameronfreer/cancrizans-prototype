"""
Cancrizans: Explore and render J.S. Bach's Crab Canon as a strict palindrome.

This package provides tools for analyzing, verifying, and rendering
palindromic musical structures, with a focus on Bach's Canon Cancrizans
from The Musical Offering (BWV 1079).
"""

__version__ = "0.1.0"

from cancrizans.canon import (
    retrograde,
    invert,
    time_align,
    is_time_palindrome,
    pairwise_symmetry_map,
)
from cancrizans.bach_crab import assemble_crab_from_theme, load_bach_crab_canon

__all__ = [
    "retrograde",
    "invert",
    "time_align",
    "is_time_palindrome",
    "pairwise_symmetry_map",
    "assemble_crab_from_theme",
    "load_bach_crab_canon",
]
