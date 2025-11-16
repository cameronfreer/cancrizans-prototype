"""
Transformation chain module for composing multiple musical transformations.

This module provides the TransformationChain class which allows users to
compose multiple transformations and apply them sequentially to a musical stream.
"""

from typing import Callable, List, Optional, Any
from music21 import stream
import copy


class TransformationChain:
    """
    A chain of musical transformations that can be applied sequentially.

    The TransformationChain class allows you to compose multiple transformations
    (like retrograde, inversion, augmentation) and apply them in sequence to
    a musical stream.

    Example:
        >>> from cancrizans import TransformationChain, retrograde, invert
        >>> from music21 import stream, note
        >>>
        >>> theme = stream.Stream()
        >>> theme.append(note.Note('C4', quarterLength=1.0))
        >>> theme.append(note.Note('D4', quarterLength=1.0))
        >>>
        >>> # Create a chain
        >>> chain = TransformationChain()
        >>> chain.add(retrograde)
        >>> chain.add(lambda s: invert(s, axis_pitch='C4'))
        >>>
        >>> # Apply all transformations
        >>> result = chain.apply(theme)
        >>>
        >>> # Or use builder pattern
        >>> result = (TransformationChain()
        ...           .add(retrograde)
        ...           .add(invert)
        ...           .apply(theme))
    """

    def __init__(self) -> None:
        """Initialize an empty transformation chain."""
        self._transformations: List[tuple[Callable, Optional[str]]] = []

    def add(self, transformation: Callable[[stream.Stream], stream.Stream],
            name: Optional[str] = None) -> 'TransformationChain':
        """
        Add a transformation to the chain.

        Args:
            transformation: A callable that takes a Stream and returns a Stream
            name: Optional name for the transformation

        Returns:
            Self (for method chaining)

        Raises:
            TypeError: If transformation is not callable
        """
        if not callable(transformation):
            raise TypeError(f"Transformation must be callable, got {type(transformation)}")

        self._transformations.append((transformation, name))
        return self

    def apply(self, input_stream: stream.Stream) -> stream.Stream:
        """
        Apply all transformations in the chain sequentially.

        Args:
            input_stream: The input musical stream

        Returns:
            The transformed stream after applying all transformations

        Raises:
            ValueError: If a transformation fails
        """
        # Start with a copy of the input
        result = copy.deepcopy(input_stream)

        # Apply each transformation in sequence
        for transformation, name in self._transformations:
            try:
                result = transformation(result)
            except Exception as e:
                if name:
                    raise ValueError(f"Transformation '{name}' failed: {e}") from e
                else:
                    raise ValueError(f"Transformation failed: {e}") from e

        return result

    def clear(self) -> None:
        """Remove all transformations from the chain."""
        self._transformations.clear()

    def get_transformations(self) -> List[Callable]:
        """
        Get the list of transformation functions.

        Returns:
            List of transformation callables
        """
        return [t[0] for t in self._transformations]

    def get_transformation_names(self) -> List[str]:
        """
        Get the list of transformation names.

        Returns:
            List of transformation names (empty string for unnamed)
        """
        return [t[1] or "" for t in self._transformations]

    def __len__(self) -> int:
        """Return the number of transformations in the chain."""
        return len(self._transformations)

    def __repr__(self) -> str:
        """Return string representation of the chain."""
        count = len(self._transformations)
        if count == 0:
            return "TransformationChain(empty)"
        elif count == 1:
            return f"TransformationChain(1 transformation)"
        else:
            return f"TransformationChain({count} transformations)"

    # Preset chains
    @classmethod
    def crab_canon(cls) -> 'TransformationChain':
        """
        Create a preset chain for a crab canon (retrograde only).

        Returns:
            A TransformationChain with retrograde transformation
        """
        from cancrizans.canon import retrograde
        chain = cls()
        chain.add(retrograde, name="Retrograde")
        return chain

    @classmethod
    def mirror_canon(cls, axis_pitch: str = 'C4') -> 'TransformationChain':
        """
        Create a preset chain for a mirror canon (inversion only).

        Args:
            axis_pitch: The pitch to invert around

        Returns:
            A TransformationChain with inversion transformation
        """
        from cancrizans.canon import invert
        chain = cls()
        chain.add(lambda s: invert(s, axis_pitch=axis_pitch), name="Invert")
        return chain

    @classmethod
    def table_canon(cls, axis_pitch: str = 'C4') -> 'TransformationChain':
        """
        Create a preset chain for a table canon (retrograde + inversion).

        A table canon can be read in any direction: forwards, backwards,
        upside down, or both.

        Args:
            axis_pitch: The pitch to invert around

        Returns:
            A TransformationChain with retrograde and inversion
        """
        from cancrizans.canon import retrograde, invert
        chain = cls()
        chain.add(retrograde, name="Retrograde")
        chain.add(lambda s: invert(s, axis_pitch=axis_pitch), name="Invert")
        return chain
