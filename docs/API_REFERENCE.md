# API Reference

**Last Updated**: 2025-11-12
**Version**: 0.11.0

This document provides comprehensive API documentation for the Cancrizans library.

## Table of Contents

1. [Core Functions (`cancrizans.canon`)](#canrizanscanon)
2. [Bach Utilities (`cancrizans.bach_crab`)](#canrizansbach_crab)
3. [Visualization (`cancrizans.viz`)](#cancrizansviz)
4. [Research Tools (`cancrizans.research`)](#canrizansresearch)
5. [I/O Functions (`cancrizans.io`)](#canrizansio)
6. [Usage Examples](#usage-examples)

---

### `cancrizans.canon`

Core transformations for canonical music analysis: retrograde, inversion,
augmentation, diminution, time alignment, and palindrome verification.


#### Functions

##### `augmentation(stream_obj: music21.stream.base.Stream, factor: float = 2.0) -> music21.stream.base.Stream`

  Return augmentation of a stream (durations multiplied by factor).

  In augmentation canon, one voice plays notes with longer durations.

  Args:
      stream_obj: A music21 Stream to augment
      factor: Multiplication factor for durations (default 2.0 = double)

  Returns:
      A new Stream with augmented durations


##### `diminution(stream_obj: music21.stream.base.Stream, factor: float = 2.0) -> music21.stream.base.Stream`

  Return diminution of a stream (durations divided by factor).

  In diminution canon, one voice plays notes with shorter durations.

  Args:
      stream_obj: A music21 Stream to diminish
      factor: Division factor for durations (default 2.0 = half)

  Returns:
      A new Stream with diminished durations


##### `harmonic_analysis(score: music21.stream.base.Score) -> Dict[str, <built-in function any>]`

  Perform basic harmonic analysis on a score.

  Analyzes vertical sonorities (chords) when multiple voices sound together.

  Args:
      score: A Score with multiple parts

  Returns:
      Dictionary with harmonic statistics


##### `interval_analysis(score_or_stream: Union[music21.stream.base.Score, music21.stream.base.Stream]) -> Dict[str, <built-in function any>]`

  Analyze melodic intervals in a score or stream.

  Returns statistics about the intervals used, including:
  - Histogram of interval sizes
  - Most common intervals
  - Average interval size
  - Interval distribution

  Args:
      score_or_stream: A Score or Stream to analyze

  Returns:
      Dictionary with interval statistics


##### `invert(stream_or_sequence: ~StreamType, axis_pitch: Union[str, music21.pitch.Pitch] = 'C4') -> ~StreamType`

  Return the pitch inversion of a musical stream around an axis pitch.

  Each pitch is reflected around the axis: if the original is N semitones above
  the axis, the inverted pitch is N semitones below the axis.

  Args:
      stream_or_sequence: A music21 Stream or sequence to invert
      axis_pitch: The pitch to use as the axis of inversion (default C4)

  Returns:
      The inverted stream, same type as input


##### `is_time_palindrome(score: music21.stream.base.Score) -> bool`

  Verify if a score represents a time palindrome (crab canon).

  A true crab canon has two voices where one is the exact retrograde of the other,
  possibly with an offset. This function checks if the score exhibits this property.

  Args:
      score: A Score with two voices to check

  Returns:
      True if the score is a time palindrome, False otherwise


##### `mirror_canon(stream_obj: music21.stream.base.Stream, axis_pitch: Union[str, music21.pitch.Pitch] = 'C4') -> music21.stream.base.Stream`

  Create a mirror canon: retrograde + inversion combined.

  This is both backwards in time AND upside-down in pitch.

  Args:
      stream_obj: A music21 Stream
      axis_pitch: The pitch axis for inversion

  Returns:
      A new Stream that is the mirror (retrograde-inversion)


##### `pairwise_symmetry_map(voice: music21.stream.base.Stream) -> List[Tuple[int, int]]`

  Generate a mapping of symmetric pairs in a voice for palindrome visualization.

  For a voice with N events, returns pairs (i, N-1-i) showing which events
  correspond in a retrograde transformation.

  Args:
      voice: A Stream representing a single voice

  Returns:
      List of (forward_index, backward_index) pairs


##### `retrograde(stream_or_sequence: ~StreamType) -> ~StreamType`

  Return the retrograde (time reversal) of a musical stream or sequence.

  For a Stream, notes are reversed in time but keep their original pitches and durations.
  The retrograde of a sequence [A, B, C] is [C, B, A].

  Args:
      stream_or_sequence: A music21 Stream or sequence to reverse

  Returns:
      The retrograde of the input, same type as input


##### `rhythm_analysis(score_or_stream: Union[music21.stream.base.Score, music21.stream.base.Stream]) -> Dict[str, <built-in function any>]`

  Analyze rhythmic patterns in a score or stream.

  Returns statistics about durations and rhythmic patterns.

  Args:
      score_or_stream: A Score or Stream to analyze

  Returns:
      Dictionary with rhythm statistics


##### `time_align(voice_a: music21.stream.base.Stream, voice_b: music21.stream.base.Stream, offset_quarters: float) -> music21.stream.base.Score`

  Align two voices with a specified offset in quarter notes.

  Creates a Score with two parts, where voice_b starts offset_quarters
  after voice_a begins.

  Args:
      voice_a: First voice (Stream)
      voice_b: Second voice (Stream)
      offset_quarters: Quarter note offset for voice_b (positive = later start)

  Returns:
      A Score containing both voices aligned with the specified offset



#### Classes

##### `class TypeVar`

  Type variable.

  Usage::

    T = TypeVar('T')  # Can be anything
    A = TypeVar('A', str, bytes)  # Must be str or bytes

  Type variables exist primarily for the benefit of static type
  checkers.  They serve as the parameters for generic types as well
  as for generic function definitions.  See class Generic for more
  information on generic types.  Generic functions work as follows:

    def repeat(x: T, n: int) -> List[T]:
        '''Return a list containing n references to x.'''
        return [x]*n

    def longest(x: A, y: A) -> A:
        '''Return the longest of two strings.'''
        return x if len(x) >= len(y) else y

  The latter example's signature is essentially the overloading
  of (str, str) -> str and (bytes, bytes) -> bytes.  Also note
  that if the arguments are instances of some subclass of str,
  the return type is still plain str.

  At runtime, isinstance(x, T) and issubclass(C, T) will raise TypeError.

  Type variables defined with covariant=True or contravariant=True
  can be used to declare covariant or contravariant generic types.
  See PEP 484 for more details. By default generic types are invariant
  in all type variables.

  Type variables can be introspected. e.g.:

    T.__name__ == 'T'
    T.__constraints__ == ()
    T.__covariant__ == False
    T.__contravariant__ = False
    A.__constraints__ == (str, bytes)

  Note that only type variables defined in global scope can be pickled.

  **Methods:**

  - `__init__(self, name, *constraints, bound=None, covariant=False, contravariant=False)`
: Initialize self.  See help(type(self)) for accurate signature.




### `cancrizans.bach_crab`

Bach's Crab Canon (Canon Cancrizans) from BWV 1079 - The Musical Offering.

This module provides the canonical Bach Crab Canon theme and functions to
assemble a crab canon from a monophonic theme.


#### Functions

##### `assemble_crab_from_theme(theme: music21.stream.base.Stream, offset_quarters: float = 0.0) -> music21.stream.base.Score`

  Assemble a crab canon from a monophonic theme.

  Creates a two-voice canon where the second voice is the exact retrograde
  of the first voice, with an optional offset.

  Args:
      theme: A monophonic Stream to use as the forward voice
      offset_quarters: Quarter note offset for the retrograde voice (default 0)

  Returns:
      A Score with two parts: the forward theme and its retrograde


##### `ensure_data_dir() -> pathlib.Path`

  Ensure the data directory exists and return its path.


##### `load_bach_crab_canon() -> music21.stream.base.Score`

  Load Bach's Crab Canon from the embedded MusicXML.

  Returns:
      A Score object containing the crab canon


##### `retrograde(stream_or_sequence: ~StreamType) -> ~StreamType`

  Return the retrograde (time reversal) of a musical stream or sequence.

  For a Stream, notes are reversed in time but keep their original pitches and durations.
  The retrograde of a sequence [A, B, C] is [C, B, A].

  Args:
      stream_or_sequence: A music21 Stream or sequence to reverse

  Returns:
      The retrograde of the input, same type as input


##### `save_crab_canon_xml(force: bool = False) -> pathlib.Path`

  Save the embedded MusicXML to disk.

  Args:
      force: If True, overwrite existing file

  Returns:
      Path to the saved MusicXML file



#### Classes

##### `class Path`

  PurePath subclass that can make system calls.

  Path represents a filesystem path but unlike PurePath, also offers
  methods to do system calls on path objects. Depending on your system,
  instantiating a Path will return either a PosixPath or a WindowsPath
  object. You can also instantiate a PosixPath or WindowsPath directly,
  but cannot instantiate a WindowsPath on a POSIX system or vice versa.

  **Methods:**

  - `absolute(self)`
: Return an absolute version of this path by prepending the current


  - `as_posix(self)`
: Return the string representation of the path with forward (/)


  - `as_uri(self)`
: Return the path as a 'file' URI.


  - `chmod(self, mode, *, follow_symlinks=True)`
: Change the permissions of the path, like os.chmod().


  - `exists(self)`
: Whether this path exists.


  - `expanduser(self)`
: Return a new path with expanded ~ and ~user constructs


  - `glob(self, pattern)`
: Iterate over this subtree and yield all existing files (of any


  - `group(self)`
: Return the group name of the file gid.


  - `hardlink_to(self, target)`
: Make this path a hard link pointing to the same file as *target*.


  - `is_absolute(self)`
: True if the path is absolute (has both a root and, if applicable,


  - `is_block_device(self)`
: Whether this path is a block device.


  - `is_char_device(self)`
: Whether this path is a character device.


  - `is_dir(self)`
: Whether this path is a directory.


  - `is_fifo(self)`
: Whether this path is a FIFO.


  - `is_file(self)`
: Whether this path is a regular file (also True for symlinks pointing


  - `is_mount(self)`
: Check if this path is a POSIX mount point


  - `is_relative_to(self, *other)`
: Return True if the path is relative to another path or False.


  - `is_reserved(self)`
: Return True if the path contains one of the special names reserved


  - `is_socket(self)`
: Whether this path is a socket.


  - `is_symlink(self)`
: Whether this path is a symbolic link.


  - `iterdir(self)`
: Iterate over the files in this directory.  Does not yield any


  - `joinpath(self, *args)`
: Combine this path with one or several arguments, and return a


  - `lchmod(self, mode)`
: Like chmod(), except if the path points to a symlink, the symlink's


  - `link_to(self, target)`
: Make the target path a hard link pointing to this path.


  - `lstat(self)`
: Like stat(), except if the path points to a symlink, the symlink's


  - `match(self, path_pattern)`
: Return True if this path matches the given pattern.


  - `mkdir(self, mode=511, parents=False, exist_ok=False)`
: Create a new directory at this given path.


  - `open(self, mode='r', buffering=-1, encoding=None, errors=None, newline=None)`
: Open the file pointed by this path and return a file object, as


  - `owner(self)`
: Return the login name of the file owner.


  - `read_bytes(self)`
: Open the file in bytes mode, read it, and close the file.


  - `read_text(self, encoding=None, errors=None)`
: Open the file in text mode, read it, and close the file.


  - `readlink(self)`
: Return the path to which the symbolic link points.


  - `relative_to(self, *other)`
: Return the relative path to another path identified by the passed


  - `rename(self, target)`
: Rename this path to the target path.


  - `replace(self, target)`
: Rename this path to the target path, overwriting if that path exists.


  - `resolve(self, strict=False)`
: Make the path absolute, resolving all symlinks on the way and also


  - `rglob(self, pattern)`
: Recursively yield all existing files (of any kind, including


  - `rmdir(self)`
: Remove this directory.  The directory must be empty.


  - `samefile(self, other_path)`
: Return whether other_path is the same or not as this file


  - `stat(self, *, follow_symlinks=True)`
: Return the result of the stat() system call on this path, like


  - `symlink_to(self, target, target_is_directory=False)`
: Make this path a symlink pointing to the target path.


  - `touch(self, mode=438, exist_ok=True)`
: Create this file with the given access mode, if it doesn't exist.


  - `unlink(self, missing_ok=False)`
: Remove this file or link.


  - `with_name(self, name)`
: Return a new path with the file name changed.


  - `with_stem(self, stem)`
: Return a new path with the stem changed.


  - `with_suffix(self, suffix)`
: Return a new path with the file suffix changed.  If the path


  - `write_bytes(self, data)`
: Open the file in bytes mode, write to it, and close the file.


  - `write_text(self, data, encoding=None, errors=None, newline=None)`
: Open the file in text mode, write to it, and close the file.




### `cancrizans.viz`

Visualization utilities for musical analysis: piano rolls and symmetry plots.


#### Functions

##### `pairwise_symmetry_map(voice: music21.stream.base.Stream) -> List[Tuple[int, int]]`

  Generate a mapping of symmetric pairs in a voice for palindrome visualization.

  For a voice with N events, returns pairs (i, N-1-i) showing which events
  correspond in a retrograde transformation.

  Args:
      voice: A Stream representing a single voice

  Returns:
      List of (forward_index, backward_index) pairs


##### `piano_roll(score: music21.stream.base.Score, path: Union[str, pathlib.Path], dpi: int = 100) -> pathlib.Path`

  Generate a piano roll visualization of a score.

  Shows notes as horizontal bars on a pitch-time grid, with different
  colors for different voices.

  Args:
      score: The Score to visualize
      path: Destination file path for the PNG image
      dpi: Resolution in dots per inch (default 100)

  Returns:
      Path to the saved image


##### `symmetry(score: music21.stream.base.Score, path: Union[str, pathlib.Path], dpi: int = 100) -> pathlib.Path`

  Generate a symmetry visualization showing palindromic structure.

  Displays notes on a horizontal time axis mirrored about the piece's
  midpoint, with connecting lines between symmetric pairs.

  Args:
      score: The Score to visualize
      path: Destination file path for the PNG image
      dpi: Resolution in dots per inch (default 100)

  Returns:
      Path to the saved image



#### Classes

##### `class Path`

  PurePath subclass that can make system calls.

  Path represents a filesystem path but unlike PurePath, also offers
  methods to do system calls on path objects. Depending on your system,
  instantiating a Path will return either a PosixPath or a WindowsPath
  object. You can also instantiate a PosixPath or WindowsPath directly,
  but cannot instantiate a WindowsPath on a POSIX system or vice versa.

  **Methods:**

  - `absolute(self)`
: Return an absolute version of this path by prepending the current


  - `as_posix(self)`
: Return the string representation of the path with forward (/)


  - `as_uri(self)`
: Return the path as a 'file' URI.


  - `chmod(self, mode, *, follow_symlinks=True)`
: Change the permissions of the path, like os.chmod().


  - `exists(self)`
: Whether this path exists.


  - `expanduser(self)`
: Return a new path with expanded ~ and ~user constructs


  - `glob(self, pattern)`
: Iterate over this subtree and yield all existing files (of any


  - `group(self)`
: Return the group name of the file gid.


  - `hardlink_to(self, target)`
: Make this path a hard link pointing to the same file as *target*.


  - `is_absolute(self)`
: True if the path is absolute (has both a root and, if applicable,


  - `is_block_device(self)`
: Whether this path is a block device.


  - `is_char_device(self)`
: Whether this path is a character device.


  - `is_dir(self)`
: Whether this path is a directory.


  - `is_fifo(self)`
: Whether this path is a FIFO.


  - `is_file(self)`
: Whether this path is a regular file (also True for symlinks pointing


  - `is_mount(self)`
: Check if this path is a POSIX mount point


  - `is_relative_to(self, *other)`
: Return True if the path is relative to another path or False.


  - `is_reserved(self)`
: Return True if the path contains one of the special names reserved


  - `is_socket(self)`
: Whether this path is a socket.


  - `is_symlink(self)`
: Whether this path is a symbolic link.


  - `iterdir(self)`
: Iterate over the files in this directory.  Does not yield any


  - `joinpath(self, *args)`
: Combine this path with one or several arguments, and return a


  - `lchmod(self, mode)`
: Like chmod(), except if the path points to a symlink, the symlink's


  - `link_to(self, target)`
: Make the target path a hard link pointing to this path.


  - `lstat(self)`
: Like stat(), except if the path points to a symlink, the symlink's


  - `match(self, path_pattern)`
: Return True if this path matches the given pattern.


  - `mkdir(self, mode=511, parents=False, exist_ok=False)`
: Create a new directory at this given path.


  - `open(self, mode='r', buffering=-1, encoding=None, errors=None, newline=None)`
: Open the file pointed by this path and return a file object, as


  - `owner(self)`
: Return the login name of the file owner.


  - `read_bytes(self)`
: Open the file in bytes mode, read it, and close the file.


  - `read_text(self, encoding=None, errors=None)`
: Open the file in text mode, read it, and close the file.


  - `readlink(self)`
: Return the path to which the symbolic link points.


  - `relative_to(self, *other)`
: Return the relative path to another path identified by the passed


  - `rename(self, target)`
: Rename this path to the target path.


  - `replace(self, target)`
: Rename this path to the target path, overwriting if that path exists.


  - `resolve(self, strict=False)`
: Make the path absolute, resolving all symlinks on the way and also


  - `rglob(self, pattern)`
: Recursively yield all existing files (of any kind, including


  - `rmdir(self)`
: Remove this directory.  The directory must be empty.


  - `samefile(self, other_path)`
: Return whether other_path is the same or not as this file


  - `stat(self, *, follow_symlinks=True)`
: Return the result of the stat() system call on this path, like


  - `symlink_to(self, target, target_is_directory=False)`
: Make this path a symlink pointing to the target path.


  - `touch(self, mode=438, exist_ok=True)`
: Create this file with the given access mode, if it doesn't exist.


  - `unlink(self, missing_ok=False)`
: Remove this file or link.


  - `with_name(self, name)`
: Return a new path with the file name changed.


  - `with_stem(self, stem)`
: Return a new path with the stem changed.


  - `with_suffix(self, suffix)`
: Return a new path with the file suffix changed.  If the path


  - `write_bytes(self, data)`
: Open the file in bytes mode, write to it, and close the file.


  - `write_text(self, data, encoding=None, errors=None, newline=None)`
: Open the file in text mode, write to it, and close the file.




### `cancrizans.research`

Research tools for batch analysis, data export, and comparative studies.

This module provides utilities for musicological research:
- Batch processing of multiple canons
- Statistical analysis and comparison
- Export to research data formats (CSV, JSON, LaTeX tables)
- Corpus analysis helpers


#### Functions

##### `analyze_corpus(directory: pathlib.Path, pattern: str = '*.mid') -> Tuple[List[Dict[str, Any]], Dict[str, Any]]`

  Analyze all canons in a directory.

  Args:
      directory: Path to directory containing MIDI/MusicXML files
      pattern: Glob pattern for file matching

  Returns:
      Tuple of (individual analyses, comparative statistics)


##### `harmonic_analysis(score: music21.stream.base.Score) -> Dict[str, <built-in function any>]`

  Perform basic harmonic analysis on a score.

  Analyzes vertical sonorities (chords) when multiple voices sound together.

  Args:
      score: A Score with multiple parts

  Returns:
      Dictionary with harmonic statistics


##### `interval_analysis(score_or_stream: Union[music21.stream.base.Score, music21.stream.base.Stream]) -> Dict[str, <built-in function any>]`

  Analyze melodic intervals in a score or stream.

  Returns statistics about the intervals used, including:
  - Histogram of interval sizes
  - Most common intervals
  - Average interval size
  - Interval distribution

  Args:
      score_or_stream: A Score or Stream to analyze

  Returns:
      Dictionary with interval statistics


##### `is_time_palindrome(score: music21.stream.base.Score) -> bool`

  Verify if a score represents a time palindrome (crab canon).

  A true crab canon has two voices where one is the exact retrograde of the other,
  possibly with an offset. This function checks if the score exhibits this property.

  Args:
      score: A Score with two voices to check

  Returns:
      True if the score is a time palindrome, False otherwise


##### `rhythm_analysis(score_or_stream: Union[music21.stream.base.Score, music21.stream.base.Stream]) -> Dict[str, <built-in function any>]`

  Analyze rhythmic patterns in a score or stream.

  Returns statistics about durations and rhythmic patterns.

  Args:
      score_or_stream: A Score or Stream to analyze

  Returns:
      Dictionary with rhythm statistics



#### Classes

##### `class Any`

  Special type indicating an unconstrained type.

  - Any is compatible with every type.
  - Any assumed to have all methods.
  - All values assumed to be instances of Any.

  Note that all the above statements are true from the point of view of
  static type checkers. At runtime, Any should not be used with instance
  checks.


##### `class BatchAnalyzer`

  Batch process multiple canons for comparative analysis.

  **Methods:**

  - `__init__(self)`
: Initialize self.  See help(type(self)) for accurate signature.


  - `add_canon(self, score: music21.stream.base.Score, name: str)`
: Add a canon to the batch.


  - `add_from_file(self, filepath: pathlib.Path, name: Optional[str] = None)`
: Load and add a canon from a file.


  - `analyze_all(self) -> List[Dict[str, Any]]`
: Analyze all canons in the batch.


  - `compare(self) -> Dict[str, Any]`
: Generate comparative statistics across all canons.




##### `class CanonAnalyzer`

  Analyzes a single crab canon with comprehensive metrics.

  **Methods:**

  - `__init__(self, score: music21.stream.base.Score, name: str = 'Untitled')`
: Initialize self.  See help(type(self)) for accurate signature.


  - `analyze(self) -> Dict[str, Any]`
: Perform comprehensive analysis and cache results.




##### `class Path`

  PurePath subclass that can make system calls.

  Path represents a filesystem path but unlike PurePath, also offers
  methods to do system calls on path objects. Depending on your system,
  instantiating a Path will return either a PosixPath or a WindowsPath
  object. You can also instantiate a PosixPath or WindowsPath directly,
  but cannot instantiate a WindowsPath on a POSIX system or vice versa.

  **Methods:**

  - `absolute(self)`
: Return an absolute version of this path by prepending the current


  - `as_posix(self)`
: Return the string representation of the path with forward (/)


  - `as_uri(self)`
: Return the path as a 'file' URI.


  - `chmod(self, mode, *, follow_symlinks=True)`
: Change the permissions of the path, like os.chmod().


  - `exists(self)`
: Whether this path exists.


  - `expanduser(self)`
: Return a new path with expanded ~ and ~user constructs


  - `glob(self, pattern)`
: Iterate over this subtree and yield all existing files (of any


  - `group(self)`
: Return the group name of the file gid.


  - `hardlink_to(self, target)`
: Make this path a hard link pointing to the same file as *target*.


  - `is_absolute(self)`
: True if the path is absolute (has both a root and, if applicable,


  - `is_block_device(self)`
: Whether this path is a block device.


  - `is_char_device(self)`
: Whether this path is a character device.


  - `is_dir(self)`
: Whether this path is a directory.


  - `is_fifo(self)`
: Whether this path is a FIFO.


  - `is_file(self)`
: Whether this path is a regular file (also True for symlinks pointing


  - `is_mount(self)`
: Check if this path is a POSIX mount point


  - `is_relative_to(self, *other)`
: Return True if the path is relative to another path or False.


  - `is_reserved(self)`
: Return True if the path contains one of the special names reserved


  - `is_socket(self)`
: Whether this path is a socket.


  - `is_symlink(self)`
: Whether this path is a symbolic link.


  - `iterdir(self)`
: Iterate over the files in this directory.  Does not yield any


  - `joinpath(self, *args)`
: Combine this path with one or several arguments, and return a


  - `lchmod(self, mode)`
: Like chmod(), except if the path points to a symlink, the symlink's


  - `link_to(self, target)`
: Make the target path a hard link pointing to this path.


  - `lstat(self)`
: Like stat(), except if the path points to a symlink, the symlink's


  - `match(self, path_pattern)`
: Return True if this path matches the given pattern.


  - `mkdir(self, mode=511, parents=False, exist_ok=False)`
: Create a new directory at this given path.


  - `open(self, mode='r', buffering=-1, encoding=None, errors=None, newline=None)`
: Open the file pointed by this path and return a file object, as


  - `owner(self)`
: Return the login name of the file owner.


  - `read_bytes(self)`
: Open the file in bytes mode, read it, and close the file.


  - `read_text(self, encoding=None, errors=None)`
: Open the file in text mode, read it, and close the file.


  - `readlink(self)`
: Return the path to which the symbolic link points.


  - `relative_to(self, *other)`
: Return the relative path to another path identified by the passed


  - `rename(self, target)`
: Rename this path to the target path.


  - `replace(self, target)`
: Rename this path to the target path, overwriting if that path exists.


  - `resolve(self, strict=False)`
: Make the path absolute, resolving all symlinks on the way and also


  - `rglob(self, pattern)`
: Recursively yield all existing files (of any kind, including


  - `rmdir(self)`
: Remove this directory.  The directory must be empty.


  - `samefile(self, other_path)`
: Return whether other_path is the same or not as this file


  - `stat(self, *, follow_symlinks=True)`
: Return the result of the stat() system call on this path, like


  - `symlink_to(self, target, target_is_directory=False)`
: Make this path a symlink pointing to the target path.


  - `touch(self, mode=438, exist_ok=True)`
: Create this file with the given access mode, if it doesn't exist.


  - `unlink(self, missing_ok=False)`
: Remove this file or link.


  - `with_name(self, name)`
: Return a new path with the file name changed.


  - `with_stem(self, stem)`
: Return a new path with the stem changed.


  - `with_suffix(self, suffix)`
: Return a new path with the file suffix changed.  If the path


  - `write_bytes(self, data)`
: Open the file in bytes mode, write to it, and close the file.


  - `write_text(self, data, encoding=None, errors=None, newline=None)`
: Open the file in text mode, write to it, and close the file.




##### `class ResearchExporter`

  Export analysis results to various research formats.

  **Methods:**

  - `to_csv(analyses: List[Dict[str, Any]], output_path: pathlib.Path)`
: Export analyses to CSV format.


  - `to_json(analyses: List[Dict[str, Any]], output_path: pathlib.Path)`
: Export analyses to JSON format.


  - `to_latex_table(analyses: List[Dict[str, Any]], output_path: pathlib.Path)`
: Export analyses to LaTeX table format.


  - `to_markdown_table(analyses: List[Dict[str, Any]], output_path: pathlib.Path)`
: Export analyses to Markdown table format.




##### `class datetime`

  datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])

  The year, month and day arguments are required. tzinfo may be None, or an
  instance of a tzinfo subclass. The remaining arguments may be ints.


### `cancrizans.io`

Input/output utilities for MIDI, MusicXML, and WAV export.


#### Functions

##### `load_score(path: Union[str, pathlib.Path]) -> music21.stream.base.Score`

  Load a score from a MusicXML or MIDI file.

  Args:
      path: Path to the file to load

  Returns:
      The loaded Score object


##### `to_midi(score: music21.stream.base.Score, path: Union[str, pathlib.Path]) -> pathlib.Path`

  Export a score to MIDI format.

  Args:
      score: The Score to export
      path: Destination file path

  Returns:
      Path to the written MIDI file


##### `to_musicxml(score: music21.stream.base.Score, path: Union[str, pathlib.Path]) -> pathlib.Path`

  Export a score to MusicXML format.

  Args:
      score: The Score to export
      path: Destination file path

  Returns:
      Path to the written MusicXML file


##### `to_wav_via_sf2(midi_path: Union[str, pathlib.Path], sf2_path: Union[str, pathlib.Path], wav_path: Union[str, pathlib.Path]) -> Optional[pathlib.Path]`

  Convert MIDI to WAV using a SoundFont file.

  This function requires either FluidSynth or the midi2audio library.
  If neither is available, it returns None and prints a message.

  Args:
      midi_path: Path to input MIDI file
      sf2_path: Path to SoundFont (.sf2) file
      wav_path: Path for output WAV file

  Returns:
      Path to the WAV file if successful, None otherwise



#### Classes

##### `class Path`

  PurePath subclass that can make system calls.

  Path represents a filesystem path but unlike PurePath, also offers
  methods to do system calls on path objects. Depending on your system,
  instantiating a Path will return either a PosixPath or a WindowsPath
  object. You can also instantiate a PosixPath or WindowsPath directly,
  but cannot instantiate a WindowsPath on a POSIX system or vice versa.

  **Methods:**

  - `absolute(self)`
: Return an absolute version of this path by prepending the current


  - `as_posix(self)`
: Return the string representation of the path with forward (/)


  - `as_uri(self)`
: Return the path as a 'file' URI.


  - `chmod(self, mode, *, follow_symlinks=True)`
: Change the permissions of the path, like os.chmod().


  - `exists(self)`
: Whether this path exists.


  - `expanduser(self)`
: Return a new path with expanded ~ and ~user constructs


  - `glob(self, pattern)`
: Iterate over this subtree and yield all existing files (of any


  - `group(self)`
: Return the group name of the file gid.


  - `hardlink_to(self, target)`
: Make this path a hard link pointing to the same file as *target*.


  - `is_absolute(self)`
: True if the path is absolute (has both a root and, if applicable,


  - `is_block_device(self)`
: Whether this path is a block device.


  - `is_char_device(self)`
: Whether this path is a character device.


  - `is_dir(self)`
: Whether this path is a directory.


  - `is_fifo(self)`
: Whether this path is a FIFO.


  - `is_file(self)`
: Whether this path is a regular file (also True for symlinks pointing


  - `is_mount(self)`
: Check if this path is a POSIX mount point


  - `is_relative_to(self, *other)`
: Return True if the path is relative to another path or False.


  - `is_reserved(self)`
: Return True if the path contains one of the special names reserved


  - `is_socket(self)`
: Whether this path is a socket.


  - `is_symlink(self)`
: Whether this path is a symbolic link.


  - `iterdir(self)`
: Iterate over the files in this directory.  Does not yield any


  - `joinpath(self, *args)`
: Combine this path with one or several arguments, and return a


  - `lchmod(self, mode)`
: Like chmod(), except if the path points to a symlink, the symlink's


  - `link_to(self, target)`
: Make the target path a hard link pointing to this path.


  - `lstat(self)`
: Like stat(), except if the path points to a symlink, the symlink's


  - `match(self, path_pattern)`
: Return True if this path matches the given pattern.


  - `mkdir(self, mode=511, parents=False, exist_ok=False)`
: Create a new directory at this given path.


  - `open(self, mode='r', buffering=-1, encoding=None, errors=None, newline=None)`
: Open the file pointed by this path and return a file object, as


  - `owner(self)`
: Return the login name of the file owner.


  - `read_bytes(self)`
: Open the file in bytes mode, read it, and close the file.


  - `read_text(self, encoding=None, errors=None)`
: Open the file in text mode, read it, and close the file.


  - `readlink(self)`
: Return the path to which the symbolic link points.


  - `relative_to(self, *other)`
: Return the relative path to another path identified by the passed


  - `rename(self, target)`
: Rename this path to the target path.


  - `replace(self, target)`
: Rename this path to the target path, overwriting if that path exists.


  - `resolve(self, strict=False)`
: Make the path absolute, resolving all symlinks on the way and also


  - `rglob(self, pattern)`
: Recursively yield all existing files (of any kind, including


  - `rmdir(self)`
: Remove this directory.  The directory must be empty.


  - `samefile(self, other_path)`
: Return whether other_path is the same or not as this file


  - `stat(self, *, follow_symlinks=True)`
: Return the result of the stat() system call on this path, like


  - `symlink_to(self, target, target_is_directory=False)`
: Make this path a symlink pointing to the target path.


  - `touch(self, mode=438, exist_ok=True)`
: Create this file with the given access mode, if it doesn't exist.


  - `unlink(self, missing_ok=False)`
: Remove this file or link.


  - `with_name(self, name)`
: Return a new path with the file name changed.


  - `with_stem(self, stem)`
: Return a new path with the stem changed.


  - `with_suffix(self, suffix)`
: Return a new path with the file suffix changed.  If the path


  - `write_bytes(self, data)`
: Open the file in bytes mode, write to it, and close the file.


  - `write_text(self, data, encoding=None, errors=None, newline=None)`
: Open the file in text mode, write to it, and close the file.




## Usage Examples

### Basic Retrograde

```python
from cancrizans import retrograde, load_bach_crab_canon

# Load Bach's Crab Canon
score = load_bach_crab_canon()

# Get the first part
theme = score.parts[0]

# Apply retrograde transformation
retrograded = retrograde(theme)

print(f"Original duration: {theme.duration.quarterLength} quarters")
print(f"Retrograded duration: {retrograded.duration.quarterLength} quarters")
```

### Palindrome Verification

```python
from cancrizans import is_time_palindrome, load_bach_crab_canon

# Load Bach's Crab Canon
score = load_bach_crab_canon()

# Verify it's a perfect palindrome
is_palindrome, details = is_time_palindrome(score, details=True)

print(f"Is palindrome: {is_palindrome}")
print(f"Symmetry pairs: {len(details['pairs'])}")
```

### Creating a Mirror Canon

```python
from cancrizans import mirror_canon
from music21 import note, stream

# Create a simple melody
melody = stream.Part()
for pitch in ['C4', 'D4', 'E4', 'F4', 'G4']:
    melody.append(note.Note(pitch, quarterLength=1.0))

# Create mirror canon (retrograde + alignment)
canon = mirror_canon(melody)

print(f"Mirror canon has {len(canon.parts)} parts")
print(f"Duration: {canon.duration.quarterLength} quarters")
```

### Interval Analysis

```python
from cancrizans import interval_analysis, load_bach_crab_canon

# Analyze Bach's Crab Canon
score = load_bach_crab_canon()
analysis = interval_analysis(score)

print(f"Most common interval: {analysis['most_common_interval']}")
print(f"Interval diversity: {analysis['interval_diversity']:.2f}")
print(f"Average interval size: {analysis['average_interval_size']:.2f}")
```

### Batch Research

```python
from cancrizans.research import analyze_corpus

# Analyze all MIDI files in examples directory
analyses, comparison = analyze_corpus(
    input_dir='./examples',
    pattern='*.mid'
)

print(f"Analyzed {len(analyses)} canons")
print(f"Average duration: {comparison['avg_duration']:.2f} quarters")
print(f"Average tempo: {comparison['avg_tempo']:.1f} BPM")
```

### Visualization

```python
from cancrizans import load_bach_crab_canon
from cancrizans.viz import piano_roll, symmetry

# Load and visualize
score = load_bach_crab_canon()

# Create piano roll visualization
piano_roll(score, 'bach_piano_roll.png')

# Create symmetry visualization
symmetry(score, 'bach_symmetry.png')

print("Visualizations saved!")
```

### Transformation Chain

```python
from cancrizans import retrograde, invert, augmentation
from music21 import note, stream

# Create melody
melody = stream.Part()
for pitch in ['C4', 'E4', 'G4', 'C5']:
    melody.append(note.Note(pitch, quarterLength=1.0))

# Apply transformation chain
result = melody
result = augmentation(result, factor=2)  # Slower
result = invert(result, axis=65)         # Invert around F4
result = retrograde(result)              # Reverse

print(f"Original: {melody.duration.quarterLength}q")
print(f"Transformed: {result.duration.quarterLength}q")
```
