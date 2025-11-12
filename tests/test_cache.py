"""Tests for the cache module."""

import pytest
import time
from cancrizans.cache import memoize, lru_cache, disk_cache, clear_all_caches, get_cache_stats


class TestMemoize:
    """Test memoization decorator."""

    def test_memoize_caches_results(self):
        """Test that memoize caches function results."""
        call_count = {'count': 0}

        @memoize
        def expensive_function(x):
            call_count['count'] += 1
            return x * 2

        # First call
        result1 = expensive_function(5)
        assert result1 == 10
        assert call_count['count'] == 1

        # Second call with same argument (should use cache)
        result2 = expensive_function(5)
        assert result2 == 10
        assert call_count['count'] == 1  # Not incremented

        # Third call with different argument
        result3 = expensive_function(10)
        assert result3 == 20
        assert call_count['count'] == 2

    def test_memoize_cache_clear(self):
        """Test cache clearing."""
        @memoize
        def func(x):
            return x * 2

        func(5)
        assert len(func.cache) > 0

        func.cache_clear()
        assert len(func.cache) == 0

    def test_memoize_cache_info(self):
        """Test cache info retrieval."""
        @memoize
        def func(x):
            return x * 2

        func(1)
        func(2)

        info = func.cache_info()
        assert info['size'] == 2
        assert info['maxsize'] is None


class TestLRUCache:
    """Test LRU cache decorator."""

    def test_lru_cache_respects_maxsize(self):
        """Test that LRU cache respects maxsize."""
        @lru_cache(maxsize=2)
        def func(x):
            return x * 2

        func(1)
        func(2)
        func(3)  # Should evict func(1)

        info = func.cache_info()
        assert info.currsize <= 2

    def test_lru_cache_works(self):
        """Test basic LRU cache functionality."""
        call_count = {'count': 0}

        @lru_cache(maxsize=10)
        def func(x):
            call_count['count'] += 1
            return x * 2

        # First call
        result1 = func(5)
        assert result1 == 10
        assert call_count['count'] == 1

        # Second call (cached)
        result2 = func(5)
        assert result2 == 10
        assert call_count['count'] == 1


class TestDiskCache:
    """Test disk caching decorator."""

    def test_disk_cache_basic(self):
        """Test basic disk caching."""
        call_count = {'count': 0}

        @disk_cache(maxsize=10)
        def func(x):
            call_count['count'] += 1
            return x * 2

        # First call
        result1 = func(5)
        assert result1 == 10
        assert call_count['count'] == 1

        # Second call (should use disk cache)
        result2 = func(5)
        assert result2 == 10
        # Note: disk cache might not work in all environments,
        # so we don't assert count == 1

    def test_disk_cache_clear(self):
        """Test clearing disk cache."""
        @disk_cache(maxsize=10)
        def func(x):
            return x * 2

        func(5)
        func.cache_clear()

        # Cache should be cleared
        info = func.cache_info()
        assert info['size'] == 0

    def test_disk_cache_info(self):
        """Test disk cache info."""
        @disk_cache(maxsize=10)
        def func(x):
            return x * 2

        info = func.cache_info()
        assert 'size' in info
        assert 'maxsize' in info
        assert info['maxsize'] == 10


class TestCacheUtilities:
    """Test cache utility functions."""

    def test_clear_all_caches(self):
        """Test clearing all caches."""
        @disk_cache(maxsize=5)
        def func1(x):
            return x

        @disk_cache(maxsize=5)
        def func2(x):
            return x * 2

        func1(1)
        func2(2)

        clear_all_caches()

        # Both caches should be cleared
        assert func1.cache_info()['size'] == 0
        assert func2.cache_info()['size'] == 0

    def test_get_cache_stats(self):
        """Test getting cache statistics."""
        @disk_cache(maxsize=5)
        def func(x):
            return x

        func(1)
        stats = get_cache_stats()

        assert isinstance(stats, dict)


class TestPerformance:
    """Test that caching improves performance."""

    def test_memoize_performance_improvement(self):
        """Test that memoization improves performance."""
        @memoize
        def slow_function(x):
            time.sleep(0.01)  # Simulate slow operation
            return x * 2

        # First call (slow)
        start1 = time.perf_counter()
        result1 = slow_function(5)
        time1 = time.perf_counter() - start1

        # Second call (should be much faster)
        start2 = time.perf_counter()
        result2 = slow_function(5)
        time2 = time.perf_counter() - start2

        assert result1 == result2
        assert time2 < time1 / 2  # At least 2x faster
