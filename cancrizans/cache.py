"""
Performance optimization utilities including caching and memoization.

This module provides caching decorators and utilities to improve
performance of expensive operations like:
- Score analysis
- Transformation computations
- Validation checks
"""

import functools
import hashlib
import pickle
from pathlib import Path
from typing import Any, Callable, Optional
import tempfile


# Cache directory
CACHE_DIR = Path(tempfile.gettempdir()) / 'cancrizans_cache'
CACHE_DIR.mkdir(exist_ok=True)


def memoize(func: Callable) -> Callable:
    """
    Simple memoization decorator for functions.

    Caches results in memory based on function arguments.
    Best for functions called multiple times with same arguments.

    Example:
        @memoize
        def expensive_function(x, y):
            # Complex computation
            return result
    """
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create cache key from args and kwargs
        key = (args, tuple(sorted(kwargs.items())))

        # Convert to hashable if possible
        try:
            key_hash = hash(key)
        except TypeError:
            # If not hashable, use string representation
            key_hash = str(key)

        if key_hash not in cache:
            cache[key_hash] = func(*args, **kwargs)

        return cache[key_hash]

    # Add cache management methods
    wrapper.cache = cache
    wrapper.cache_clear = lambda: cache.clear()
    wrapper.cache_info = lambda: {'size': len(cache), 'maxsize': None}

    return wrapper


def disk_cache(maxsize: int = 100) -> Callable:
    """
    Disk-based caching decorator for expensive computations.

    Caches results to disk, surviving across program runs.
    Useful for very expensive operations on large scores.

    Args:
        maxsize: Maximum number of cached items (LRU eviction)

    Example:
        @disk_cache(maxsize=50)
        def analyze_large_score(score):
            # Very expensive analysis
            return results
    """
    def decorator(func: Callable) -> Callable:
        cache_file = CACHE_DIR / f"{func.__name__}_cache.pkl"

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Load cache from disk
            cache = {}
            if cache_file.exists():
                try:
                    with open(cache_file, 'rb') as f:
                        cache = pickle.load(f)
                except (pickle.PickleError, EOFError):
                    cache = {}

            # Create cache key
            key_str = f"{args}_{kwargs}"
            key_hash = hashlib.md5(key_str.encode()).hexdigest()

            # Check cache
            if key_hash in cache:
                return cache[key_hash]

            # Compute result
            result = func(*args, **kwargs)

            # Update cache
            cache[key_hash] = result

            # Enforce maxsize (LRU)
            if len(cache) > maxsize:
                # Remove oldest entries
                cache = dict(list(cache.items())[-maxsize:])

            # Save cache to disk
            try:
                with open(cache_file, 'wb') as f:
                    pickle.dump(cache, f)
            except (pickle.PickleError, IOError):
                pass  # Silently fail if caching fails

            return result

        def cache_clear():
            """Clear the disk cache."""
            if cache_file.exists():
                cache_file.unlink()

        def cache_info():
            """Get cache statistics."""
            if cache_file.exists():
                try:
                    with open(cache_file, 'rb') as f:
                        cache = pickle.load(f)
                    return {'size': len(cache), 'maxsize': maxsize}
                except (pickle.PickleError, EOFError):
                    return {'size': 0, 'maxsize': maxsize}
            return {'size': 0, 'maxsize': maxsize}

        wrapper.cache_clear = cache_clear
        wrapper.cache_info = cache_info

        return wrapper

    return decorator


def lru_cache(maxsize: int = 128) -> Callable:
    """
    Wrapper around functools.lru_cache for consistency.

    LRU (Least Recently Used) cache with bounded memory.

    Args:
        maxsize: Maximum cache size

    Example:
        @lru_cache(maxsize=256)
        def compute_intervals(notes):
            return intervals
    """
    return functools.lru_cache(maxsize=maxsize)


def clear_all_caches():
    """Clear all disk caches."""
    if CACHE_DIR.exists():
        for cache_file in CACHE_DIR.glob('*_cache.pkl'):
            try:
                cache_file.unlink()
            except OSError:
                pass


def get_cache_stats() -> dict:
    """Get statistics for all disk caches."""
    stats = {}
    if CACHE_DIR.exists():
        for cache_file in CACHE_DIR.glob('*_cache.pkl'):
            try:
                with open(cache_file, 'rb') as f:
                    cache = pickle.load(f)
                stats[cache_file.stem] = {
                    'size': len(cache),
                    'file_size': cache_file.stat().st_size
                }
            except (pickle.PickleError, EOFError, OSError):
                stats[cache_file.stem] = {'size': 0, 'file_size': 0}
    return stats
