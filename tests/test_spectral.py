"""
Tests for timbral palindromes and spectral symmetry

Phase 19 - v0.36.0
"""

import pytest
import math
from music21 import stream, note

from cancrizans.spectral import (
    SpectralFrame,
    TimbralTrajectory,
    SpectralShape,
    create_spectral_shape,
    create_timbral_palindrome,
    analyze_spectral_symmetry,
    brightness_palindrome,
    formant_trajectory,
    spectral_inversion,
    spectral_retrograde,
    create_harmonic_series_canon,
    spectral_distance,
    apply_spectral_envelope_to_stream,
    detect_timbral_palindrome,
    generate_spectral_canon_metadata
)


class TestSpectralFrame:
    """Test SpectralFrame dataclass"""

    def test_creation_basic(self):
        """Test creating basic spectral frame"""
        frame = SpectralFrame(
            fundamental_hz=440.0,
            harmonic_amplitudes=[1.0, 0.5, 0.25, 0.125]
        )

        assert frame.fundamental_hz == 440.0
        assert len(frame.harmonic_amplitudes) == 4
        assert frame.spectral_centroid is not None
        assert frame.brightness is not None

    def test_centroid_calculation(self):
        """Test spectral centroid calculation"""
        frame = SpectralFrame(
            fundamental_hz=100.0,
            harmonic_amplitudes=[1.0, 0.5, 0.25]
        )

        # Centroid should be weighted average of frequencies
        assert frame.spectral_centroid > 100.0
        assert frame.spectral_centroid < 300.0

    def test_brightness_calculation(self):
        """Test brightness calculation"""
        # Dark spectrum (only low harmonics)
        dark = SpectralFrame(
            fundamental_hz=100.0,
            harmonic_amplitudes=[1.0, 0.5, 0.25, 0.1, 0.0, 0.0, 0.0]
        )

        # Bright spectrum (high harmonics emphasized)
        bright = SpectralFrame(
            fundamental_hz=100.0,
            harmonic_amplitudes=[0.1, 0.1, 0.2, 0.3, 0.8, 0.9, 1.0]
        )

        assert dark.brightness < bright.brightness

    def test_harmonic_count(self):
        """Test harmonic count"""
        frame = SpectralFrame(
            fundamental_hz=440.0,
            harmonic_amplitudes=[1.0, 0.5, 0.1, 0.05, 0.001, 0.0001]
        )

        # Should count harmonics above 0.01 threshold
        assert frame.harmonic_count == 4


class TestTimbralTrajectory:
    """Test TimbralTrajectory dataclass"""

    def test_creation(self):
        """Test creating timbral trajectory"""
        frames = [
            SpectralFrame(440.0, [1.0, 0.5]),
            SpectralFrame(440.0, [1.0, 0.6]),
            SpectralFrame(440.0, [1.0, 0.7])
        ]

        traj = TimbralTrajectory(
            frames=frames,
            duration_seconds=2.0,
            is_palindrome=True
        )

        assert len(traj.frames) == 3
        assert traj.duration_seconds == 2.0
        assert traj.is_palindrome is True

    def test_get_frame_at_time_start(self):
        """Test getting frame at start time"""
        frames = [
            SpectralFrame(440.0, [1.0, 0.5]),
            SpectralFrame(440.0, [1.0, 0.7])
        ]
        traj = TimbralTrajectory(frames=frames, duration_seconds=2.0)

        frame = traj.get_frame_at_time(0.0)
        assert frame.harmonic_amplitudes == [1.0, 0.5]

    def test_get_frame_at_time_end(self):
        """Test getting frame at end time"""
        frames = [
            SpectralFrame(440.0, [1.0, 0.5]),
            SpectralFrame(440.0, [1.0, 0.7])
        ]
        traj = TimbralTrajectory(frames=frames, duration_seconds=2.0)

        frame = traj.get_frame_at_time(3.0)  # Beyond end
        assert frame.harmonic_amplitudes == [1.0, 0.7]

    def test_get_frame_empty_trajectory(self):
        """Test getting frame from empty trajectory raises error"""
        traj = TimbralTrajectory(frames=[], duration_seconds=1.0)

        with pytest.raises(ValueError):
            traj.get_frame_at_time(0.5)


class TestSpectralShapes:
    """Test spectral shape creation"""

    def test_bright_shape(self):
        """Test bright spectral shape"""
        frame = create_spectral_shape(SpectralShape.BRIGHT, 440.0, num_harmonics=8)

        # Brightness should increase with harmonic number
        assert frame.harmonic_amplitudes[-1] > frame.harmonic_amplitudes[0]

    def test_dark_shape(self):
        """Test dark spectral shape"""
        frame = create_spectral_shape(SpectralShape.DARK, 440.0, num_harmonics=8)

        # Amplitude should decrease with harmonic number
        assert frame.harmonic_amplitudes[0] > frame.harmonic_amplitudes[-1]

    def test_hollow_shape(self):
        """Test hollow spectral shape (odd harmonics)"""
        frame = create_spectral_shape(SpectralShape.HOLLOW, 440.0, num_harmonics=8)

        # Even harmonics should be zero or very small
        assert frame.harmonic_amplitudes[1] < 0.01  # 2nd harmonic (index 1)
        assert frame.harmonic_amplitudes[3] < 0.01  # 4th harmonic (index 3)

        # Odd harmonics should be present
        assert frame.harmonic_amplitudes[0] > 0.1  # 1st harmonic
        assert frame.harmonic_amplitudes[2] > 0.1  # 3rd harmonic

    def test_nasal_shape(self):
        """Test nasal spectral shape"""
        frame = create_spectral_shape(SpectralShape.NASAL, 440.0, num_harmonics=8)

        # Should have peak around 5th harmonic (index 4)
        peak_idx = frame.harmonic_amplitudes.index(max(frame.harmonic_amplitudes))
        assert 3 <= peak_idx <= 5

    def test_flute_shape(self):
        """Test flute spectral shape"""
        frame = create_spectral_shape(SpectralShape.FLUTE, 440.0, num_harmonics=8)

        # Fundamental should dominate
        assert frame.harmonic_amplitudes[0] > 0.9
        assert all(amp < 0.2 for amp in frame.harmonic_amplitudes[1:])

    def test_all_shapes_normalized(self):
        """Test that all shapes are normalized"""
        for shape in SpectralShape:
            frame = create_spectral_shape(shape, 440.0, num_harmonics=16)
            max_amp = max(frame.harmonic_amplitudes)
            assert 0.99 <= max_amp <= 1.01  # Should be normalized to 1.0


class TestTimbralPalindrome:
    """Test timbral palindrome creation"""

    def test_palindrome_structure(self):
        """Test palindrome has symmetric structure"""
        traj = create_timbral_palindrome(
            SpectralShape.DARK,
            SpectralShape.BRIGHT,
            440.0,
            duration_seconds=2.0,
            num_frames=10
        )

        assert traj.is_palindrome is True
        assert len(traj.frames) == 10

    def test_palindrome_symmetry(self):
        """Test palindrome is actually symmetric"""
        traj = create_timbral_palindrome(
            SpectralShape.DARK,
            SpectralShape.BRIGHT,
            440.0,
            num_frames=8
        )

        # Compare first and last frames
        first = traj.frames[0]
        last = traj.frames[-1]

        # Should be similar (within tolerance due to interpolation)
        distance = spectral_distance(first, last)
        assert distance < 0.1

    def test_palindrome_midpoint(self):
        """Test palindrome reaches peak at midpoint"""
        traj = create_timbral_palindrome(
            SpectralShape.DARK,
            SpectralShape.BRIGHT,
            440.0,
            num_frames=10
        )

        # Brightness should peak near middle
        brightnesses = [f.brightness for f in traj.frames]
        max_idx = brightnesses.index(max(brightnesses))
        assert 4 <= max_idx <= 5  # Middle of 10 frames


class TestSpectralSymmetry:
    """Test spectral symmetry analysis"""

    def test_perfect_palindrome(self):
        """Test analyzing perfect palindrome"""
        traj = create_timbral_palindrome(
            SpectralShape.DARK,
            SpectralShape.BRIGHT,
            440.0,
            num_frames=8
        )

        analysis = analyze_spectral_symmetry(traj)

        assert analysis['is_symmetric'] is True
        assert analysis['symmetry_score'] > 0.9

    def test_non_palindrome(self):
        """Test analyzing non-palindromic trajectory"""
        # Create linear trajectory (not palindrome)
        frames = []
        for i in range(8):
            brightness = i / 7.0
            amps = [1.0 - brightness, brightness]
            frames.append(SpectralFrame(440.0, amps))

        traj = TimbralTrajectory(frames=frames, duration_seconds=2.0)
        analysis = analyze_spectral_symmetry(traj)

        assert analysis['symmetry_score'] < 0.5

    def test_asymmetry_detection(self):
        """Test detection of asymmetric regions"""
        # Create mostly symmetric with one asymmetric frame
        frames = [
            SpectralFrame(440.0, [1.0, 0.0]),
            SpectralFrame(440.0, [0.5, 0.5]),
            SpectralFrame(440.0, [0.0, 1.0]),  # Peak
            SpectralFrame(440.0, [0.9, 0.1]),  # Asymmetric!
            SpectralFrame(440.0, [1.0, 0.0])
        ]

        traj = TimbralTrajectory(frames=frames, duration_seconds=2.0)
        analysis = analyze_spectral_symmetry(traj)

        assert len(analysis['asymmetry_regions']) > 0


class TestBrightnessPalindrome:
    """Test brightness palindrome"""

    def test_triangle_curve(self):
        """Test triangle brightness curve"""
        notes = [note.Note('C4') for _ in range(10)]
        result = brightness_palindrome(notes, brightness_curve="triangle")

        brightnesses = [r['brightness'] for r in result]

        # Should start low, peak in middle, end low
        assert brightnesses[0] < brightnesses[5]
        assert brightnesses[-1] < brightnesses[5]

    def test_arch_curve(self):
        """Test arch brightness curve"""
        notes = [note.Note('C4') for _ in range(10)]
        result = brightness_palindrome(notes, brightness_curve="arch")

        brightnesses = [r['brightness'] for r in result]

        # Should be parabolic
        max_idx = brightnesses.index(max(brightnesses))
        assert 4 <= max_idx <= 5

    def test_valley_curve(self):
        """Test valley brightness curve"""
        notes = [note.Note('C4') for _ in range(10)]
        result = brightness_palindrome(notes, brightness_curve="valley")

        brightnesses = [r['brightness'] for r in result]

        # Should be inverted (darkest in middle)
        min_idx = brightnesses.index(min(brightnesses))
        assert 4 <= min_idx <= 5

    def test_empty_notes(self):
        """Test brightness palindrome with empty notes"""
        result = brightness_palindrome([], brightness_curve="triangle")
        assert result == []


class TestFormantTrajectory:
    """Test formant trajectory"""

    def test_single_vowel(self):
        """Test trajectory with single vowel"""
        traj = formant_trajectory(200.0, ['a'], num_frames=4)

        assert len(traj.frames) == 4
        # All frames should be similar
        distances = [spectral_distance(traj.frames[0], f) for f in traj.frames[1:]]
        assert all(d < 0.3 for d in distances)

    def test_vowel_morphing(self):
        """Test morphing between vowels"""
        traj = formant_trajectory(200.0, ['a', 'i'], num_frames=8)

        # Spectral content should change over time
        first = traj.frames[0]
        last = traj.frames[-1]
        distance = spectral_distance(first, last)

        assert distance > 0.1  # Should be different

    def test_complex_sequence(self):
        """Test complex vowel sequence"""
        traj = formant_trajectory(200.0, ['a', 'e', 'i', 'o', 'u'], num_frames=16)

        assert len(traj.frames) == 16


class TestSpectralOperations:
    """Test spectral operations"""

    def test_spectral_inversion(self):
        """Test spectral inversion"""
        frame = SpectralFrame(440.0, [1.0, 0.8, 0.6, 0.4, 0.2])
        inverted = spectral_inversion(frame)

        # Amplitudes should be reversed
        assert inverted.harmonic_amplitudes == [0.2, 0.4, 0.6, 0.8, 1.0]

    def test_spectral_retrograde(self):
        """Test spectral retrograde"""
        frames = [
            SpectralFrame(440.0, [1.0]),
            SpectralFrame(440.0, [0.5]),
            SpectralFrame(440.0, [0.2])
        ]
        traj = TimbralTrajectory(frames=frames, duration_seconds=1.0)

        retro = spectral_retrograde(traj)

        assert retro.frames[0].harmonic_amplitudes == [0.2]
        assert retro.frames[-1].harmonic_amplitudes == [1.0]

    def test_spectral_distance_identical(self):
        """Test distance between identical frames"""
        frame1 = SpectralFrame(440.0, [1.0, 0.5, 0.25])
        frame2 = SpectralFrame(440.0, [1.0, 0.5, 0.25])

        distance = spectral_distance(frame1, frame2)
        assert distance < 0.001

    def test_spectral_distance_different(self):
        """Test distance between different frames"""
        frame1 = SpectralFrame(440.0, [1.0, 0.0, 0.0])
        frame2 = SpectralFrame(440.0, [0.0, 0.0, 1.0])

        distance = spectral_distance(frame1, frame2)
        assert distance > 1.0


class TestHarmonicSeriesCanon:
    """Test harmonic series canon"""

    def test_frame_count(self):
        """Test correct number of frames generated"""
        frames = create_harmonic_series_canon(440.0, num_harmonics=8)

        assert len(frames) == 8

    def test_emphasis_shifts(self):
        """Test that emphasis shifts through harmonics"""
        frames = create_harmonic_series_canon(440.0, num_harmonics=4)

        # Each frame should emphasize different harmonic
        for i, frame in enumerate(frames):
            max_idx = frame.harmonic_amplitudes.index(max(frame.harmonic_amplitudes))
            assert max_idx == i


class TestStreamApplication:
    """Test applying spectral envelopes to streams"""

    def test_apply_to_empty_stream(self):
        """Test applying to empty stream"""
        s = stream.Stream()
        traj = create_timbral_palindrome(SpectralShape.DARK, SpectralShape.BRIGHT, 440.0)

        result = apply_spectral_envelope_to_stream(s, traj)
        assert result == []

    def test_apply_to_stream(self):
        """Test applying spectral envelope"""
        s = stream.Stream()
        s.append(note.Note('C4', quarterLength=1.0))
        s.append(note.Note('D4', quarterLength=1.0))

        traj = create_timbral_palindrome(SpectralShape.DARK, SpectralShape.BRIGHT, 440.0)
        result = apply_spectral_envelope_to_stream(s, traj)

        assert len(result) == 2
        assert 'spectral_frame' in result[0]
        assert 'brightness' in result[0]

    def test_brightness_varies_over_stream(self):
        """Test that brightness varies across notes"""
        s = stream.Stream()
        for i in range(5):
            s.append(note.Note('C4', quarterLength=1.0))

        traj = create_timbral_palindrome(SpectralShape.DARK, SpectralShape.BRIGHT, 440.0)
        result = apply_spectral_envelope_to_stream(s, traj)

        brightnesses = [r['brightness'] for r in result]

        # Should have variation (palindromic)
        assert len(set(brightnesses)) > 1


class TestPalindromeDetection:
    """Test palindrome detection"""

    def test_detect_perfect_palindrome(self):
        """Test detecting perfect palindrome"""
        traj = create_timbral_palindrome(SpectralShape.DARK, SpectralShape.BRIGHT, 440.0)

        assert detect_timbral_palindrome(traj, tolerance=0.1) is True

    def test_detect_non_palindrome(self):
        """Test detecting non-palindrome"""
        frames = [SpectralFrame(440.0, [1.0, float(i) / 10]) for i in range(10)]
        traj = TimbralTrajectory(frames=frames, duration_seconds=2.0)

        assert detect_timbral_palindrome(traj, tolerance=0.1) is False

    def test_tolerance_parameter(self):
        """Test tolerance parameter affects detection"""
        frames = [
            SpectralFrame(440.0, [1.0, 0.0]),
            SpectralFrame(440.0, [0.5, 0.5]),
            SpectralFrame(440.0, [0.5, 0.5]),
            SpectralFrame(440.0, [0.9, 0.1])  # Slightly asymmetric
        ]
        traj = TimbralTrajectory(frames=frames, duration_seconds=1.0)

        # With high tolerance, should detect
        assert detect_timbral_palindrome(traj, tolerance=0.5) is True

        # With low tolerance, should not detect
        assert detect_timbral_palindrome(traj, tolerance=0.01) is False


class TestMetadataGeneration:
    """Test spectral canon metadata generation"""

    def test_metadata_structure(self):
        """Test metadata has correct structure"""
        traj = create_timbral_palindrome(SpectralShape.DARK, SpectralShape.BRIGHT, 440.0)
        metadata = generate_spectral_canon_metadata(traj, title="Test Canon")

        assert metadata['title'] == "Test Canon"
        assert 'duration_seconds' in metadata
        assert 'symmetry_score' in metadata
        assert 'brightness_range' in metadata
        assert 'spectral_centroid_range' in metadata

    def test_palindrome_metadata(self):
        """Test metadata for palindromic trajectory"""
        traj = create_timbral_palindrome(SpectralShape.DARK, SpectralShape.BRIGHT, 440.0)
        metadata = generate_spectral_canon_metadata(traj)

        assert metadata['is_palindrome'] is True
        assert metadata['symmetry_score'] > 0.9

    def test_brightness_analysis(self):
        """Test brightness analysis in metadata"""
        traj = create_timbral_palindrome(SpectralShape.DARK, SpectralShape.BRIGHT, 440.0)
        metadata = generate_spectral_canon_metadata(traj)

        min_b, max_b = metadata['brightness_range']
        assert 0.0 <= min_b <= max_b <= 1.0
        assert 0.0 <= metadata['average_brightness'] <= 1.0


class TestSpectralShapeEnum:
    """Test SpectralShape enum"""

    def test_enum_values(self):
        """Test enum has expected values"""
        assert SpectralShape.BRIGHT.value == "bright"
        assert SpectralShape.DARK.value == "dark"
        assert SpectralShape.HOLLOW.value == "hollow"
        assert SpectralShape.FLUTE.value == "flute"
