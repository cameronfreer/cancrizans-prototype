"""
Tests for transformation chain functionality.

This module tests the TransformationChain class which allows
composing multiple musical transformations.
"""

import pytest
from music21 import stream, note
from cancrizans.transformation_chain import TransformationChain
from cancrizans.canon import retrograde, invert, augmentation, diminution


class TestTransformationChainBasics:
    """Test basic TransformationChain functionality."""

    def test_chain_creation(self):
        """Test creating an empty transformation chain."""
        chain = TransformationChain()
        assert chain is not None
        assert len(chain) == 0

    def test_chain_add_transformation(self):
        """Test adding a single transformation to chain."""
        chain = TransformationChain()
        chain.add(retrograde)
        assert len(chain) == 1

    def test_chain_add_multiple_transformations(self):
        """Test adding multiple transformations to chain."""
        chain = TransformationChain()
        chain.add(retrograde)
        chain.add(invert)
        chain.add(augmentation)
        assert len(chain) == 3

    def test_chain_apply_single_transformation(self):
        """Test applying a single transformation."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('D4', quarterLength=1.0))
        theme.append(note.Note('E4', quarterLength=1.0))

        chain = TransformationChain()
        chain.add(retrograde)

        result = chain.apply(theme)

        # Should be reversed
        notes = list(result.flatten().notes)
        assert notes[0].pitch.nameWithOctave == 'E4'
        assert notes[1].pitch.nameWithOctave == 'D4'
        assert notes[2].pitch.nameWithOctave == 'C4'

    def test_chain_apply_multiple_transformations(self):
        """Test applying multiple transformations in sequence."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('D4', quarterLength=1.0))

        chain = TransformationChain()
        chain.add(retrograde)
        chain.add(lambda s: augmentation(s, factor=2.0))

        result = chain.apply(theme)

        # Should be reversed and durations doubled
        notes = list(result.flatten().notes)
        assert notes[0].pitch.nameWithOctave == 'D4'
        assert notes[1].pitch.nameWithOctave == 'C4'
        assert notes[0].quarterLength == 2.0
        assert notes[1].quarterLength == 2.0

    def test_chain_with_params(self):
        """Test transformations with parameters."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('E4', quarterLength=1.0))

        chain = TransformationChain()
        chain.add(lambda s: invert(s, axis_pitch='C4'))

        result = chain.apply(theme)
        assert result is not None

    def test_chain_builder_pattern(self):
        """Test fluent builder pattern."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('D4', quarterLength=1.0))

        result = (TransformationChain()
                  .add(retrograde)
                  .add(lambda s: augmentation(s, factor=2.0))
                  .apply(theme))

        notes = list(result.flatten().notes)
        assert len(notes) == 2
        assert notes[0].quarterLength == 2.0


class TestTransformationChainAdvanced:
    """Test advanced transformation chain features."""

    def test_chain_clear(self):
        """Test clearing all transformations from chain."""
        chain = TransformationChain()
        chain.add(retrograde)
        chain.add(invert)
        assert len(chain) == 2

        chain.clear()
        assert len(chain) == 0

    def test_chain_repr(self):
        """Test string representation of chain."""
        chain = TransformationChain()
        chain.add(retrograde, name="Retrograde")
        chain.add(invert, name="Invert")

        repr_str = repr(chain)
        assert "TransformationChain" in repr_str
        assert "2" in repr_str or "transformations" in repr_str

    def test_chain_get_transformations(self):
        """Test getting list of transformations."""
        chain = TransformationChain()
        chain.add(retrograde)
        chain.add(invert)

        transformations = chain.get_transformations()
        assert len(transformations) == 2

    def test_chain_apply_empty(self):
        """Test applying empty chain returns copy of input."""
        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))

        chain = TransformationChain()
        result = chain.apply(theme)

        # Should be a copy
        assert result is not theme
        notes_orig = list(theme.flatten().notes)
        notes_result = list(result.flatten().notes)
        assert len(notes_orig) == len(notes_result)

    def test_chain_named_transformations(self):
        """Test adding transformations with names."""
        chain = TransformationChain()
        chain.add(retrograde, name="Crab")
        chain.add(invert, name="Mirror")

        names = chain.get_transformation_names()
        assert "Crab" in names
        assert "Mirror" in names


class TestTransformationChainPresets:
    """Test preset transformation chains."""

    def test_crab_canon_preset(self):
        """Test creating a crab canon preset."""
        chain = TransformationChain.crab_canon()
        assert len(chain) == 1

        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('D4', quarterLength=1.0))

        result = chain.apply(theme)
        notes = list(result.flatten().notes)
        # Should be reversed
        assert notes[0].pitch.nameWithOctave == 'D4'

    def test_mirror_canon_preset(self):
        """Test creating a mirror canon preset."""
        chain = TransformationChain.mirror_canon()
        assert len(chain) >= 1

        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))

        result = chain.apply(theme)
        assert result is not None

    def test_table_canon_preset(self):
        """Test creating a table canon preset (retrograde + inversion)."""
        chain = TransformationChain.table_canon()
        assert len(chain) == 2  # retrograde and invert

        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))
        theme.append(note.Note('E4', quarterLength=1.0))

        result = chain.apply(theme)
        notes = list(result.flatten().notes)
        # Should be transformed
        assert len(notes) == 2


class TestTransformationChainEdgeCases:
    """Test edge cases for transformation chains."""

    def test_chain_with_empty_stream(self):
        """Test applying chain to empty stream."""
        empty_stream = stream.Stream()
        chain = TransformationChain()
        chain.add(retrograde)

        result = chain.apply(empty_stream)
        assert len(list(result.flatten().notes)) == 0

    def test_chain_with_single_note(self):
        """Test applying chain to single note."""
        single_note = stream.Stream()
        single_note.append(note.Note('C4', quarterLength=1.0))

        chain = TransformationChain()
        chain.add(retrograde)

        result = chain.apply(single_note)
        assert len(list(result.flatten().notes)) == 1

    def test_chain_invalid_transformation(self):
        """Test adding invalid transformation raises error."""
        chain = TransformationChain()

        with pytest.raises((TypeError, ValueError)):
            chain.add("not a function")

    def test_chain_transformation_exception_handling(self):
        """Test that transformation exceptions are handled gracefully."""
        def broken_transform(s):
            raise ValueError("Transformation failed")

        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))

        chain = TransformationChain()
        chain.add(broken_transform)

        with pytest.raises(ValueError):
            chain.apply(theme)

    def test_chain_named_transformation_exception(self):
        """Test named transformation exception includes name (line 91)."""
        def broken_transform(s):
            raise RuntimeError("Something went wrong")

        theme = stream.Stream()
        theme.append(note.Note('C4', quarterLength=1.0))

        chain = TransformationChain()
        chain.add(broken_transform, name="MyBrokenTransform")

        with pytest.raises(ValueError) as exc_info:
            chain.apply(theme)

        # Should include the transformation name in the error message
        assert "MyBrokenTransform" in str(exc_info.value)
        assert "failed" in str(exc_info.value).lower()
