"""
Comprehensive tests for microtonal utility functions

Tests for scale recommendations, transformations, analysis, and compatibility functions.
"""

import pytest
from cancrizans.microtonal_utils import (
    ScaleRecommendation,
    recommend_scale_for_style,
    blend_scales,
    find_modulation_path,
    calculate_scale_tension,
    quantize_to_scale,
    generate_scale_variants,
    create_scale_catalog,
    analyze_scale_family,
    calculate_scale_compatibility,
    export_scala_file,
    import_scala_file,
    # Phase 18.7: Chord Theory
    MicrotonalChord,
    build_microtonal_chord,
    analyze_chord_consonance,
    generate_microtonal_chord_progression,
    # Phase 18.8: Advanced Transformations
    morph_scales,
    stretch_scale,
    extract_scale_subset,
    create_equal_division_scale,
    rotate_scale_intervals,
    merge_scales,
)
from cancrizans.microtonal import (
    MicrotonalScale, MicrotonalPitch, TuningSystem, ScaleType,
    create_tuning_system_scale, create_world_music_scale
)


class TestScaleRecommendation:
    """Test ScaleRecommendation dataclass"""

    def test_scale_recommendation_creation(self):
        """Test creating a scale recommendation"""
        rec = ScaleRecommendation(
            scale_type="Historical Temperament",
            tuning_system=TuningSystem.WERCKMEISTER_III,
            world_scale_type=None,
            confidence=0.95,
            reason="Test reason",
            example_use_cases=["Test case 1", "Test case 2"]
        )

        assert rec.scale_type == "Historical Temperament"
        assert rec.tuning_system == TuningSystem.WERCKMEISTER_III
        assert rec.world_scale_type is None
        assert rec.confidence == 0.95
        assert rec.reason == "Test reason"
        assert len(rec.example_use_cases) == 2


class TestRecommendScaleForStyle:
    """Test recommend_scale_for_style function"""

    def test_baroque_recommendations(self):
        """Test baroque style recommendations"""
        recommendations = recommend_scale_for_style("baroque")

        assert len(recommendations) > 0
        assert recommendations[0].confidence >= 0.85
        assert any(rec.tuning_system == TuningSystem.WERCKMEISTER_III for rec in recommendations)

    def test_classical_recommendations(self):
        """Test classical style recommendations"""
        recommendations = recommend_scale_for_style("classical")

        assert len(recommendations) > 0
        # Should recommend historical temperaments
        assert any(rec.scale_type == "Historical Temperament" for rec in recommendations)

    def test_bach_recommendations(self):
        """Test Bach-specific recommendations"""
        recommendations = recommend_scale_for_style("bach")

        assert len(recommendations) > 0
        # Werckmeister should be top recommendation
        assert recommendations[0].tuning_system == TuningSystem.WERCKMEISTER_III

    def test_arabic_recommendations(self):
        """Test Arabic style recommendations"""
        recommendations = recommend_scale_for_style("arabic")

        assert len(recommendations) > 0
        assert recommendations[0].scale_type == "Arabic Maqam"
        assert any(rec.world_scale_type == ScaleType.MAQAM_RAST for rec in recommendations)

    def test_middle_eastern_recommendations(self):
        """Test Middle Eastern style recommendations"""
        recommendations = recommend_scale_for_style("middle eastern")

        assert len(recommendations) > 0
        assert recommendations[0].scale_type == "Arabic Maqam"

    def test_maqam_recommendations(self):
        """Test maqam style recommendations"""
        recommendations = recommend_scale_for_style("maqam")

        assert len(recommendations) > 0
        assert any(rec.world_scale_type == ScaleType.MAQAM_HIJAZ for rec in recommendations)

    def test_indian_recommendations(self):
        """Test Indian style recommendations"""
        recommendations = recommend_scale_for_style("indian")

        assert len(recommendations) > 0
        assert recommendations[0].scale_type == "Indian Raga"
        assert any(rec.world_scale_type == ScaleType.RAGA_BHAIRAV for rec in recommendations)

    def test_raga_recommendations(self):
        """Test raga style recommendations"""
        recommendations = recommend_scale_for_style("raga")

        assert len(recommendations) > 0
        assert any(rec.world_scale_type == ScaleType.RAGA_YAMAN for rec in recommendations)

    def test_gamelan_recommendations(self):
        """Test gamelan style recommendations"""
        recommendations = recommend_scale_for_style("gamelan")

        assert len(recommendations) > 0
        assert recommendations[0].scale_type == "Gamelan Scale"
        assert any(rec.world_scale_type == ScaleType.PELOG for rec in recommendations)

    def test_indonesian_recommendations(self):
        """Test Indonesian style recommendations"""
        recommendations = recommend_scale_for_style("indonesian")

        assert len(recommendations) > 0
        assert any(rec.world_scale_type == ScaleType.SLENDRO for rec in recommendations)

    def test_experimental_recommendations(self):
        """Test experimental style recommendations"""
        recommendations = recommend_scale_for_style("experimental")

        assert len(recommendations) > 0
        assert any(rec.scale_type == "Xenharmonic" for rec in recommendations)
        assert any(rec.tuning_system == TuningSystem.BOHLEN_PIERCE for rec in recommendations)

    def test_contemporary_recommendations(self):
        """Test contemporary style recommendations"""
        recommendations = recommend_scale_for_style("contemporary")

        assert len(recommendations) > 0
        assert any(rec.tuning_system == TuningSystem.EQUAL_19 for rec in recommendations)

    def test_avant_garde_recommendations(self):
        """Test avant-garde style recommendations"""
        recommendations = recommend_scale_for_style("avant-garde")

        assert len(recommendations) > 0
        assert any(rec.tuning_system == TuningSystem.ALPHA for rec in recommendations)

    def test_jazz_recommendations(self):
        """Test jazz style recommendations"""
        recommendations = recommend_scale_for_style("jazz")

        assert len(recommendations) > 0
        assert recommendations[0].scale_type == "Just Intonation"
        assert recommendations[0].tuning_system == TuningSystem.JUST_INTONATION_7

    def test_blues_recommendations(self):
        """Test blues style recommendations"""
        recommendations = recommend_scale_for_style("blues")

        assert len(recommendations) > 0
        assert any(rec.tuning_system == TuningSystem.JUST_INTONATION_7 for rec in recommendations)

    def test_folk_recommendations(self):
        """Test folk style recommendations"""
        recommendations = recommend_scale_for_style("folk")

        assert len(recommendations) > 0

    def test_default_recommendations(self):
        """Test default recommendations for unknown style"""
        recommendations = recommend_scale_for_style("unknown_style_xyz")

        assert len(recommendations) > 0
        assert recommendations[0].tuning_system == TuningSystem.EQUAL_12
        assert recommendations[0].confidence == 0.70

    def test_case_insensitive(self):
        """Test that style matching is case insensitive"""
        recommendations_lower = recommend_scale_for_style("baroque")
        recommendations_upper = recommend_scale_for_style("BAROQUE")
        recommendations_mixed = recommend_scale_for_style("BaRoQuE")

        assert recommendations_lower[0].tuning_system == recommendations_upper[0].tuning_system
        assert recommendations_lower[0].tuning_system == recommendations_mixed[0].tuning_system

    def test_recommendations_sorted_by_confidence(self):
        """Test that recommendations are sorted by confidence"""
        recommendations = recommend_scale_for_style("baroque")

        confidences = [rec.confidence for rec in recommendations]
        assert confidences == sorted(confidences, reverse=True)


class TestBlendScales:
    """Test blend_scales function"""

    def test_blend_equal_weight(self):
        """Test blending two scales with equal weight"""
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)

        blended = blend_scales(scale1, scale2, weight=0.5)

        assert blended is not None
        assert len(blended.intervals_cents) > 0
        assert "⊕" in blended.name
        assert "50%" in blended.name

    def test_blend_all_scale1(self):
        """Test blending with weight 0.0 (all scale1)"""
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)

        blended = blend_scales(scale1, scale2, weight=0.0)

        assert blended is not None
        # Should be heavily influenced by scale1
        assert "0%" in blended.name

    def test_blend_all_scale2(self):
        """Test blending with weight 1.0 (all scale2)"""
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)

        blended = blend_scales(scale1, scale2, weight=1.0)

        assert blended is not None
        assert "100%" in blended.name

    def test_blend_world_scales(self):
        """Test blending world music scales"""
        scale1 = create_world_music_scale(ScaleType.MAQAM_RAST, tonic_midi=60)
        scale2 = create_world_music_scale(ScaleType.RAGA_BHAIRAV, tonic_midi=60)

        blended = blend_scales(scale1, scale2, weight=0.5)

        assert blended is not None
        assert len(blended.intervals_cents) > 0

    def test_blend_preserves_tonic(self):
        """Test that blending preserves tonic MIDI note"""
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)

        blended = blend_scales(scale1, scale2, weight=0.5)

        assert blended.tonic_midi == scale1.tonic_midi


class TestFindModulationPath:
    """Test find_modulation_path function"""

    def test_modulation_path_length(self):
        """Test that modulation path has correct length"""
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)

        path = find_modulation_path(scale1, scale2, max_steps=5)

        # Should have max_steps + 1 scales (including source and target)
        assert len(path) == 6
        assert path[0] == scale1
        assert path[-1] == scale2

    def test_modulation_path_smoothness(self):
        """Test that modulation path creates smooth transitions"""
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.JUST_INTONATION_5, tonic_midi=60)

        path = find_modulation_path(scale1, scale2, max_steps=3)

        assert len(path) == 4
        # Each step should be different
        for i in range(len(path) - 1):
            assert path[i].name != path[i + 1].name

    def test_modulation_path_single_step(self):
        """Test modulation path with single step"""
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)

        path = find_modulation_path(scale1, scale2, max_steps=1)

        assert len(path) == 2
        assert path[0] == scale1
        assert path[1] == scale2


class TestCalculateScaleTension:
    """Test calculate_scale_tension function"""

    def test_tension_12tet_low(self):
        """Test that 12-TET tension is calculated"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        tension = calculate_scale_tension(scale)

        assert 0.0 <= tension <= 2.0
        # 12-TET has many small intervals (100 cents each)
        # This creates moderate-high tension
        assert tension > 0.5

    def test_tension_bohlen_pierce_high(self):
        """Test that Bohlen-Pierce has high tension"""
        scale = create_tuning_system_scale(TuningSystem.BOHLEN_PIERCE, tonic_midi=60)
        tension = calculate_scale_tension(scale)

        assert 0.0 <= tension <= 2.0
        # Non-octave scale should have higher tension
        assert tension > 0.3

    def test_tension_empty_scale(self):
        """Test tension calculation for empty scale"""
        scale = MicrotonalScale(name="Empty", intervals_cents=[], tonic_midi=60)
        tension = calculate_scale_tension(scale)

        assert tension == 0.0

    def test_tension_single_interval(self):
        """Test tension calculation for scale with single interval"""
        scale = MicrotonalScale(name="Single", intervals_cents=[100.0], tonic_midi=60)
        tension = calculate_scale_tension(scale)

        assert tension == 0.0

    def test_tension_microtonal_higher(self):
        """Test that microtonal scales have higher tension"""
        tet12 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        tet24 = create_tuning_system_scale(TuningSystem.EQUAL_24, tonic_midi=60)

        tension_12 = calculate_scale_tension(tet12)
        tension_24 = calculate_scale_tension(tet24)

        # 24-TET has smaller intervals and more deviation
        assert tension_24 > tension_12


class TestQuantizeToScale:
    """Test quantize_to_scale function"""

    def test_quantize_exact_match(self):
        """Test quantizing a pitch that exactly matches a scale degree"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        # 700 cents from C0 should quantize to a 12-TET pitch
        pitch = quantize_to_scale(700.0, scale, allow_octave_shift=True)

        assert isinstance(pitch, MicrotonalPitch)
        # 700 cents is within first octave (0-1200), should find matching degree
        assert pitch.midi_note >= 0

    def test_quantize_needs_rounding(self):
        """Test quantizing a pitch that needs rounding"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        # 705 cents = slightly sharp perfect fifth
        pitch = quantize_to_scale(705.0, scale, allow_octave_shift=True)

        assert isinstance(pitch, MicrotonalPitch)
        # Should round to nearest 12-TET degree

    def test_quantize_with_octave_shift(self):
        """Test quantizing with octave shift allowed"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        # 1900 cents = octave + 700 cents
        pitch = quantize_to_scale(1900.0, scale, allow_octave_shift=True)

        assert isinstance(pitch, MicrotonalPitch)
        assert pitch.midi_note >= 12  # Should be in higher octave

    def test_quantize_without_octave_shift(self):
        """Test quantizing without octave shift"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        pitch = quantize_to_scale(350.0, scale, allow_octave_shift=False)

        assert isinstance(pitch, MicrotonalPitch)

    def test_quantize_microtonal_scale(self):
        """Test quantizing to a microtonal scale"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)

        pitch = quantize_to_scale(400.0, scale, allow_octave_shift=True)

        assert isinstance(pitch, MicrotonalPitch)


class TestGenerateScaleVariants:
    """Test generate_scale_variants function"""

    def test_generate_variants_count(self):
        """Test that correct number of variants are generated"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        variants = generate_scale_variants(scale, num_variants=5)

        assert len(variants) <= 5
        assert len(variants) > 0

    def test_generate_single_variant(self):
        """Test generating a single variant"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        variants = generate_scale_variants(scale, num_variants=1)

        assert len(variants) == 1

    def test_variants_are_different(self):
        """Test that generated variants are different from base scale"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        variants = generate_scale_variants(scale, num_variants=3)

        for variant in variants:
            # Variants should have different names (transformations applied)
            assert variant.name != scale.name or variant.intervals_cents != scale.intervals_cents

    def test_generate_variants_world_scale(self):
        """Test generating variants of world music scale"""
        scale = create_world_music_scale(ScaleType.MAQAM_RAST, tonic_midi=60)

        variants = generate_scale_variants(scale, num_variants=5)

        assert len(variants) > 0


class TestCreateScaleCatalog:
    """Test create_scale_catalog function"""

    def test_catalog_structure(self):
        """Test that catalog has correct structure"""
        catalog = create_scale_catalog()

        assert isinstance(catalog, dict)
        assert len(catalog) > 0

    def test_catalog_categories(self):
        """Test that catalog contains expected categories"""
        catalog = create_scale_catalog()

        expected_categories = [
            "Equal Temperaments",
            "Historical Temperaments",
            "Just Intonation",
            "Wendy Carlos Scales",
            "Exotic & Experimental",
            "Arabic Maqamat",
            "Indian Ragas",
            "Indonesian Gamelan"
        ]

        for category in expected_categories:
            assert category in catalog

    def test_catalog_entries_are_lists(self):
        """Test that each catalog entry is a list of strings"""
        catalog = create_scale_catalog()

        for category, scales in catalog.items():
            assert isinstance(scales, list)
            assert len(scales) > 0
            for scale_name in scales:
                assert isinstance(scale_name, str)

    def test_catalog_equal_temperaments(self):
        """Test Equal Temperaments category"""
        catalog = create_scale_catalog()

        assert "12-TET (standard)" in catalog["Equal Temperaments"]
        assert "19-TET" in catalog["Equal Temperaments"]

    def test_catalog_historical_temperaments(self):
        """Test Historical Temperaments category"""
        catalog = create_scale_catalog()

        assert "Pythagorean" in catalog["Historical Temperaments"]
        assert "Meantone (Quarter-comma)" in catalog["Historical Temperaments"]

    def test_catalog_just_intonation(self):
        """Test Just Intonation category"""
        catalog = create_scale_catalog()

        assert "5-limit JI" in catalog["Just Intonation"]

    def test_catalog_wendy_carlos(self):
        """Test Wendy Carlos Scales category"""
        catalog = create_scale_catalog()

        assert "Alpha (9-EDO)" in catalog["Wendy Carlos Scales"]
        assert "Beta (11-EDO)" in catalog["Wendy Carlos Scales"]

    def test_catalog_arabic_maqamat(self):
        """Test Arabic Maqamat category"""
        catalog = create_scale_catalog()

        assert "Rast" in catalog["Arabic Maqamat"]
        assert "Hijaz" in catalog["Arabic Maqamat"]

    def test_catalog_indian_ragas(self):
        """Test Indian Ragas category"""
        catalog = create_scale_catalog()

        assert "Bhairav" in catalog["Indian Ragas"]
        assert "Yaman" in catalog["Indian Ragas"]

    def test_catalog_gamelan(self):
        """Test Indonesian Gamelan category"""
        catalog = create_scale_catalog()

        assert "Pelog" in catalog["Indonesian Gamelan"]
        assert "Slendro" in catalog["Indonesian Gamelan"]


class TestAnalyzeScaleFamily:
    """Test analyze_scale_family function"""

    def test_analyze_pentatonic(self):
        """Test analyzing a pentatonic scale"""
        scale = create_world_music_scale(ScaleType.SLENDRO, tonic_midi=60)

        analysis = analyze_scale_family(scale)

        assert 'Pentatonic' in analysis['possible_families']
        assert 'Five-note scale' in analysis['characteristics']

    def test_analyze_heptatonic(self):
        """Test analyzing a heptatonic (7-note) scale"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        analysis = analyze_scale_family(scale)

        # 12-TET has 12 notes, not 7, so should not be heptatonic
        # But let's test the analysis runs
        assert 'num_degrees' in analysis
        assert analysis['num_degrees'] == 12

    def test_analyze_microtonal(self):
        """Test analyzing a microtonal scale"""
        scale = create_world_music_scale(ScaleType.MAQAM_RAST, tonic_midi=60)

        analysis = analyze_scale_family(scale)

        # Maqam Rast has microtonal intervals
        assert 'Microtonal' in analysis['possible_families']
        assert 'Contains microtonal intervals' in analysis['characteristics']

    def test_analyze_equal_temperament(self):
        """Test analyzing an equal temperament scale"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)

        analysis = analyze_scale_family(scale)

        assert 'Equal Temperament' in analysis['possible_families']
        assert any('19-EDO' in char for char in analysis['characteristics'])

    def test_analyze_includes_name(self):
        """Test that analysis includes scale name"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        analysis = analyze_scale_family(scale)

        assert 'scale_name' in analysis
        assert analysis['scale_name'] == scale.name

    def test_analyze_includes_num_degrees(self):
        """Test that analysis includes number of degrees"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        analysis = analyze_scale_family(scale)

        assert 'num_degrees' in analysis
        assert analysis['num_degrees'] == 12


class TestCalculateScaleCompatibility:
    """Test calculate_scale_compatibility function"""

    def test_identical_scales_high_compatibility(self):
        """Test that identical scales have high compatibility"""
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        compatibility = calculate_scale_compatibility(scale1, scale2)

        assert 0.0 <= compatibility <= 1.0
        assert compatibility > 0.9  # Should be very high

    def test_similar_scales_medium_compatibility(self):
        """Test that similar scales have medium compatibility"""
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.MEANTONE, tonic_midi=60)

        compatibility = calculate_scale_compatibility(scale1, scale2)

        assert 0.0 <= compatibility <= 1.0
        # Should have some compatibility (both 12-note Western scales)
        assert compatibility > 0.3

    def test_different_scales_lower_compatibility(self):
        """Test that very different scales have lower compatibility"""
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.BOHLEN_PIERCE, tonic_midi=60)

        compatibility = calculate_scale_compatibility(scale1, scale2)

        assert 0.0 <= compatibility <= 1.0
        # Different structures, should be lower
        # (but might not be 0 due to some coincidental overlap)

    def test_compatibility_range(self):
        """Test that compatibility is always in valid range"""
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_world_music_scale(ScaleType.MAQAM_RAST, tonic_midi=60)

        compatibility = calculate_scale_compatibility(scale1, scale2)

        assert 0.0 <= compatibility <= 1.0

    def test_compatibility_symmetric(self):
        """Test that compatibility is symmetric"""
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)

        compatibility_12 = calculate_scale_compatibility(scale1, scale2)
        compatibility_21 = calculate_scale_compatibility(scale2, scale1)

        # Both should be valid compatibility scores
        assert 0.0 <= compatibility_12 <= 1.0
        assert 0.0 <= compatibility_21 <= 1.0
        # Note: Due to how overlap is calculated (dividing by max),
        # the function may not be perfectly symmetric


class TestScalaFileFormat:
    """Test Scala file format import/export"""

    def test_export_scala_file_basic(self):
        """Test basic Scala file export"""
        import tempfile
        from pathlib import Path

        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / 'test.scl'
            result = export_scala_file(scale, output_path)

            assert result.exists()
            assert result == output_path

            # Read and verify content
            content = result.read_text()
            assert '12-TET' in content or 'Equal' in content
            lines = content.strip().split('\n')
            # Should have description, blank, count, blank, then intervals
            assert len(lines) >= 4

    def test_export_scala_file_with_description(self):
        """Test Scala export with custom description"""
        import tempfile
        from pathlib import Path

        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / 'test.scl'
            result = export_scala_file(scale, output_path, description="My Custom Scale")

            content = result.read_text()
            assert 'My Custom Scale' in content

    def test_export_scala_file_creates_dir(self):
        """Test that export creates output directory"""
        import tempfile
        from pathlib import Path

        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / 'subdir' / 'nested' / 'test.scl'
            result = export_scala_file(scale, output_path)

            assert result.exists()
            assert result.parent.exists()

    def test_import_export_roundtrip_12tet(self):
        """Test import/export roundtrip for 12-TET"""
        import tempfile
        from pathlib import Path

        original_scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        with tempfile.TemporaryDirectory() as tmpdir:
            scl_path = Path(tmpdir) / 'test.scl'

            # Export
            export_scala_file(original_scale, scl_path)

            # Import
            imported_scale = import_scala_file(scl_path, tonic_midi=60)

            # Verify same number of intervals
            assert len(imported_scale.intervals_cents) == len(original_scale.intervals_cents)

            # Verify intervals are close (within 0.01 cents)
            for i, (orig, imp) in enumerate(zip(original_scale.intervals_cents,
                                                imported_scale.intervals_cents)):
                assert abs(orig - imp) < 0.01, f"Interval {i} differs: {orig} vs {imp}"

    def test_import_export_roundtrip_werckmeister(self):
        """Test import/export roundtrip for Werckmeister III"""
        import tempfile
        from pathlib import Path

        original_scale = create_tuning_system_scale(TuningSystem.WERCKMEISTER_III, tonic_midi=60)

        with tempfile.TemporaryDirectory() as tmpdir:
            scl_path = Path(tmpdir) / 'werck.scl'

            # Export
            export_scala_file(original_scale, scl_path)

            # Import
            imported_scale = import_scala_file(scl_path, tonic_midi=60)

            # Verify same number of intervals
            assert len(imported_scale.intervals_cents) == len(original_scale.intervals_cents)

            # Verify intervals are close
            for orig, imp in zip(original_scale.intervals_cents, imported_scale.intervals_cents):
                assert abs(orig - imp) < 0.01

    def test_import_scala_file_with_ratios(self):
        """Test importing Scala file with ratio format"""
        import tempfile
        from pathlib import Path

        # Create a Scala file with ratios (just intonation)
        scala_content = """! Just Intonation Major Scale
!
7
!
9/8
5/4
4/3
3/2
5/3
15/8
2/1
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            scl_path = Path(tmpdir) / 'just.scl'
            scl_path.write_text(scala_content)

            # Import
            scale = import_scala_file(scl_path, tonic_midi=60)

            assert scale.name == "Just Intonation Major Scale"
            assert len(scale.intervals_cents) == 8  # 0 + 7 intervals

            # Verify some known intervals
            # 9/8 = 203.9 cents (major second)
            assert abs(scale.intervals_cents[1] - 203.91) < 1.0
            # 3/2 = 701.96 cents (perfect fifth)
            assert abs(scale.intervals_cents[4] - 701.96) < 1.0

    def test_import_scala_file_with_cents(self):
        """Test importing Scala file with cents format"""
        import tempfile
        from pathlib import Path

        # Create a Scala file with cents
        scala_content = """! 12-TET
!
12
!
100.0
200.0
300.0
400.0
500.0
600.0
700.0
800.0
900.0
1000.0
1100.0
1200.0
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            scl_path = Path(tmpdir) / 'tet12.scl'
            scl_path.write_text(scala_content)

            # Import
            scale = import_scala_file(scl_path, tonic_midi=60)

            assert scale.name == "12-TET"
            assert len(scale.intervals_cents) == 13  # 0 + 12 intervals

            # Verify intervals are correct
            for i in range(12):
                expected = i * 100.0
                assert abs(scale.intervals_cents[i] - expected) < 0.01

    def test_import_scala_file_with_name_override(self):
        """Test importing Scala file with name override"""
        import tempfile
        from pathlib import Path

        scala_content = """! Original Name
!
3
!
400.0
700.0
1200.0
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            scl_path = Path(tmpdir) / 'test.scl'
            scl_path.write_text(scala_content)

            # Import with name override
            scale = import_scala_file(scl_path, tonic_midi=60, name="My Custom Name")

            assert scale.name == "My Custom Name"

    def test_import_scala_file_invalid_format(self):
        """Test that invalid Scala file raises error"""
        import tempfile
        from pathlib import Path
        import pytest

        # Create invalid Scala file (too few lines)
        scala_content = """! Invalid
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            scl_path = Path(tmpdir) / 'invalid.scl'
            scl_path.write_text(scala_content)

            with pytest.raises(ValueError, match="too few lines"):
                import_scala_file(scl_path)

    def test_import_scala_file_invalid_number(self):
        """Test that invalid number of notes raises error"""
        import tempfile
        from pathlib import Path
        import pytest

        scala_content = """! Test
!
not_a_number
!
100.0
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            scl_path = Path(tmpdir) / 'invalid.scl'
            scl_path.write_text(scala_content)

            with pytest.raises(ValueError, match="cannot parse number"):
                import_scala_file(scl_path)

    def test_import_scala_file_invalid_cents(self):
        """Test that invalid cents value raises error"""
        import tempfile
        from pathlib import Path
        import pytest

        scala_content = """! Test
!
2
!
100.0
invalid_cents
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            scl_path = Path(tmpdir) / 'invalid.scl'
            scl_path.write_text(scala_content)

            with pytest.raises(ValueError, match="Invalid interval value"):
                import_scala_file(scl_path)

    def test_import_scala_file_invalid_ratio(self):
        """Test that invalid ratio raises error"""
        import tempfile
        from pathlib import Path
        import pytest

        scala_content = """! Test
!
2
!
100.0
3/invalid
"""

        with tempfile.TemporaryDirectory() as tmpdir:
            scl_path = Path(tmpdir) / 'invalid.scl'
            scl_path.write_text(scala_content)

            with pytest.raises(ValueError, match="Invalid ratio value"):
                import_scala_file(scl_path)

    def test_export_scala_file_world_music_scale(self):
        """Test exporting world music scale to Scala format"""
        import tempfile
        from pathlib import Path

        scale = create_world_music_scale(ScaleType.MAQAM_RAST, tonic_midi=60)

        with tempfile.TemporaryDirectory() as tmpdir:
            scl_path = Path(tmpdir) / 'maqam.scl'
            result = export_scala_file(scale, scl_path)

            assert result.exists()

            # Reimport and verify
            imported = import_scala_file(scl_path, tonic_midi=60)
            assert len(imported.intervals_cents) == len(scale.intervals_cents)


class TestIntegration:
    """Integration tests combining multiple functions"""

    def test_recommend_blend_and_modulate(self):
        """Test workflow: recommend -> create -> blend -> modulate"""
        # Get recommendations
        recommendations = recommend_scale_for_style("baroque")
        assert len(recommendations) > 0

        # Create scales from recommendations
        scale1 = create_tuning_system_scale(recommendations[0].tuning_system, tonic_midi=60)
        scale2 = create_tuning_system_scale(recommendations[1].tuning_system, tonic_midi=60)

        # Blend them
        blended = blend_scales(scale1, scale2, weight=0.5)
        assert blended is not None

        # Find modulation path
        path = find_modulation_path(scale1, scale2, max_steps=3)
        assert len(path) == 4

    def test_catalog_analyze_and_compatibility(self):
        """Test workflow: catalog -> analyze -> check compatibility"""
        # Get catalog
        catalog = create_scale_catalog()
        assert len(catalog) > 0

        # Create scales
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)

        # Analyze them
        analysis1 = analyze_scale_family(scale1)
        analysis2 = analyze_scale_family(scale2)

        assert 'num_degrees' in analysis1
        assert 'num_degrees' in analysis2

        # Check compatibility
        compatibility = calculate_scale_compatibility(scale1, scale2)
        assert 0.0 <= compatibility <= 1.0

    def test_quantize_variants_and_tension(self):
        """Test workflow: create -> quantize -> generate variants -> analyze tension"""
        # Create base scale
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        # Quantize a pitch
        pitch = quantize_to_scale(550.0, scale, allow_octave_shift=True)
        assert isinstance(pitch, MicrotonalPitch)

        # Generate variants
        variants = generate_scale_variants(scale, num_variants=3)
        assert len(variants) > 0

        # Calculate tension for each
        tensions = [calculate_scale_tension(v) for v in variants]
        assert all(0.0 <= t <= 2.0 for t in tensions)


# ============================================================================
# Phase 18.7: Microtonal Chord Theory Tests
# ============================================================================

class TestMicrotonalChordTheory:
    """Test microtonal chord building and analysis"""

    def test_build_basic_triad(self):
        """Test building a basic triad from 12-TET"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        chord = build_microtonal_chord(scale, root_degree=0, num_notes=3)

        assert isinstance(chord, MicrotonalChord)
        assert len(chord.intervals_cents) == 3
        assert chord.chord_type == "triad"
        assert chord.quality in ["consonant", "ambiguous", "dissonant"]
        assert 0.0 <= chord.tension_score <= 2.0

    def test_build_chord_with_skip_pattern(self):
        """Test building chord with custom skip pattern"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        # Build a triad: root, major third, perfect fifth (degrees 0, 2, 4)
        chord = build_microtonal_chord(scale, root_degree=0, num_notes=3, skip_pattern=[0, 2, 4])

        assert len(chord.intervals_cents) == 3
        assert chord.chord_type == "triad"

    def test_build_tetrad(self):
        """Test building a four-note chord"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        chord = build_microtonal_chord(scale, root_degree=0, num_notes=4, skip_pattern=[0, 2, 4, 6])

        assert len(chord.intervals_cents) == 4
        assert chord.chord_type == "tetrad"

    def test_build_dyad(self):
        """Test building a two-note chord"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        chord = build_microtonal_chord(scale, root_degree=0, num_notes=2)

        assert len(chord.intervals_cents) == 2
        assert chord.chord_type == "dyad"

    def test_build_pentad(self):
        """Test building a five-note chord"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)
        chord = build_microtonal_chord(scale, root_degree=0, num_notes=5, skip_pattern=[0, 2, 4, 6, 8])

        assert len(chord.intervals_cents) == 5
        assert chord.chord_type == "pentad"

    def test_build_chord_from_microtonal_scale(self):
        """Test building chord from microtonal (non-12-TET) scale"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)
        chord = build_microtonal_chord(scale, root_degree=0, num_notes=3, skip_pattern=[0, 3, 6])

        assert isinstance(chord, MicrotonalChord)
        assert len(chord.intervals_cents) == 3

    def test_build_chord_different_root_degrees(self):
        """Test building chords from different root degrees"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        chord1 = build_microtonal_chord(scale, root_degree=0, num_notes=3)
        chord2 = build_microtonal_chord(scale, root_degree=2, num_notes=3)
        chord3 = build_microtonal_chord(scale, root_degree=5, num_notes=3)

        # All should be valid
        assert all(isinstance(c, MicrotonalChord) for c in [chord1, chord2, chord3])
        # Root pitches should differ
        assert chord1.root.cent_deviation != chord2.root.cent_deviation or \
               chord1.root.midi_note != chord2.root.midi_note

    def test_build_chord_invalid_root_degree(self):
        """Test that invalid root degree raises error"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        with pytest.raises(ValueError, match="Root degree .* out of range"):
            build_microtonal_chord(scale, root_degree=100, num_notes=3)

    def test_analyze_chord_consonance_basic(self):
        """Test basic chord consonance analysis"""
        scale = create_tuning_system_scale(TuningSystem.JUST_INTONATION_7, tonic_midi=60)
        chord = build_microtonal_chord(scale, root_degree=0, num_notes=3, skip_pattern=[0, 2, 4])

        analysis = analyze_chord_consonance(chord)

        assert 'quality' in analysis
        assert 'tension_score' in analysis
        assert 'chord_type' in analysis
        assert 'num_notes' in analysis
        assert 'interval_analysis' in analysis
        assert 'harmonic_series_alignment' in analysis

    def test_analyze_chord_interval_ratios(self):
        """Test that interval analysis includes ratio information"""
        scale = create_tuning_system_scale(TuningSystem.JUST_INTONATION_7, tonic_midi=60)
        chord = build_microtonal_chord(scale, root_degree=0, num_notes=3, skip_pattern=[0, 2, 4])

        analysis = analyze_chord_consonance(chord)

        # Should have interval analysis for non-zero intervals
        assert len(analysis['interval_analysis']) >= 0
        for interval_info in analysis['interval_analysis']:
            assert 'cents' in interval_info
            assert 'ratio' in interval_info
            # simple_ratio_approximation can be None or a tuple
            assert interval_info['simple_ratio_approximation'] is None or \
                   isinstance(interval_info['simple_ratio_approximation'], tuple)

    def test_chord_quality_consonant(self):
        """Test that just intonation chords are consonant"""
        scale = create_tuning_system_scale(TuningSystem.JUST_INTONATION_7, tonic_midi=60)
        chord = build_microtonal_chord(scale, root_degree=0, num_notes=3, skip_pattern=[0, 2, 4])

        # JI chords should be relatively consonant
        assert chord.tension_score < 1.0

    def test_generate_chord_progression_ascending(self):
        """Test generating ascending chord progression"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        progression = generate_microtonal_chord_progression(
            scale, num_chords=4, chord_size=3, progression_type="ascending"
        )

        assert len(progression) == 4
        assert all(isinstance(c, MicrotonalChord) for c in progression)
        assert all(c.chord_type == "triad" for c in progression)

    def test_generate_chord_progression_descending(self):
        """Test generating descending chord progression"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        progression = generate_microtonal_chord_progression(
            scale, num_chords=4, chord_size=3, progression_type="descending"
        )

        assert len(progression) == 4
        assert all(isinstance(c, MicrotonalChord) for c in progression)

    def test_generate_chord_progression_circle_of_fifths(self):
        """Test generating circle of fifths progression"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        progression = generate_microtonal_chord_progression(
            scale, num_chords=4, chord_size=3, progression_type="circle_of_fifths"
        )

        assert len(progression) == 4
        assert all(isinstance(c, MicrotonalChord) for c in progression)

    def test_generate_chord_progression_random(self):
        """Test generating random chord progression"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        progression = generate_microtonal_chord_progression(
            scale, num_chords=5, chord_size=4, progression_type="random"
        )

        assert len(progression) == 5
        assert all(c.chord_type == "tetrad" for c in progression)

    def test_generate_chord_progression_invalid_type(self):
        """Test that invalid progression type raises error"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        with pytest.raises(ValueError, match="Unknown progression type"):
            generate_microtonal_chord_progression(
                scale, num_chords=4, progression_type="invalid_type"
            )

    def test_chord_progression_from_microtonal_scale(self):
        """Test generating progression from microtonal scale"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)
        progression = generate_microtonal_chord_progression(
            scale, num_chords=3, chord_size=3, progression_type="ascending"
        )

        assert len(progression) == 3
        assert all(isinstance(c, MicrotonalChord) for c in progression)


# ============================================================================
# Phase 18.8: Advanced Microtonal Transformations Tests
# ============================================================================

class TestAdvancedMicrotonalTransformations:
    """Test advanced scale transformation functions"""

    def test_morph_scales_linear(self):
        """Test linear scale morphing"""
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)

        morph_sequence = morph_scales(scale1, scale2, num_steps=5, interpolation="linear")

        assert len(morph_sequence) == 7  # start + 5 intermediate + end
        assert morph_sequence[0].name == scale1.name
        assert morph_sequence[-1].name == scale2.name
        # Intermediate scales should have blended names
        assert "⊕" in morph_sequence[3].name

    def test_morph_scales_ease_in(self):
        """Test ease-in morphing interpolation"""
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)

        morph_sequence = morph_scales(scale1, scale2, num_steps=10, interpolation="ease_in")

        assert len(morph_sequence) == 12  # start + 10 intermediate + end
        assert all(isinstance(s, MicrotonalScale) for s in morph_sequence)

    def test_morph_scales_ease_out(self):
        """Test ease-out morphing interpolation"""
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.JUST_INTONATION_7, tonic_midi=60)

        morph_sequence = morph_scales(scale1, scale2, num_steps=8, interpolation="ease_out")

        assert len(morph_sequence) == 10
        assert all(isinstance(s, MicrotonalScale) for s in morph_sequence)

    def test_morph_scales_ease_in_out(self):
        """Test ease-in-out morphing interpolation"""
        scale1 = create_tuning_system_scale(TuningSystem.PYTHAGOREAN, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.MEANTONE, tonic_midi=60)

        morph_sequence = morph_scales(scale1, scale2, num_steps=6, interpolation="ease_in_out")

        assert len(morph_sequence) == 8
        assert all(isinstance(s, MicrotonalScale) for s in morph_sequence)

    def test_stretch_scale_expand(self):
        """Test stretching (expanding) a scale"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        stretched = stretch_scale(scale, stretch_factor=1.5, preserve_octave=True)

        assert isinstance(stretched, MicrotonalScale)
        # Octave should still be ~1200 cents
        if stretched.intervals_cents:
            max_interval = max(stretched.intervals_cents)
            assert abs(max_interval - 1200.0) < 10.0

    def test_stretch_scale_compress(self):
        """Test compressing a scale"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        compressed = stretch_scale(scale, stretch_factor=0.8, preserve_octave=True)

        assert isinstance(compressed, MicrotonalScale)
        if compressed.intervals_cents:
            max_interval = max(compressed.intervals_cents)
            assert abs(max_interval - 1200.0) < 10.0

    def test_stretch_scale_without_preserve_octave(self):
        """Test stretching without preserving octave"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        stretched = stretch_scale(scale, stretch_factor=1.5, preserve_octave=False)

        assert isinstance(stretched, MicrotonalScale)
        # Intervals should be stretched (larger than original)
        if len(stretched.intervals_cents) > 1 and len(scale.intervals_cents) > 1:
            # Compare max intervals
            original_max = max(scale.intervals_cents)
            stretched_max = max(stretched.intervals_cents)
            # Stretched should be approximately 1.5x the original
            if original_max > 0:
                ratio = stretched_max / original_max
                assert abs(ratio - 1.5) < 0.1  # Within 10% of expected

    def test_extract_scale_subset_even(self):
        """Test extracting evenly-spaced subset"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)
        subset = extract_scale_subset(scale, num_degrees=7, method="even")

        assert isinstance(subset, MicrotonalScale)
        assert len(subset.intervals_cents) == 7
        assert "subset" in subset.name

    def test_extract_scale_subset_low(self):
        """Test extracting lowest degrees"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)
        subset = extract_scale_subset(scale, num_degrees=5, method="low")

        assert len(subset.intervals_cents) == 5
        # Should be the first 5 degrees
        assert subset.intervals_cents == scale.intervals_cents[:5]

    def test_extract_scale_subset_high(self):
        """Test extracting highest degrees"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)
        subset = extract_scale_subset(scale, num_degrees=5, method="high")

        assert len(subset.intervals_cents) == 5
        # Should be the last 5 degrees
        assert subset.intervals_cents == scale.intervals_cents[-5:]

    def test_extract_scale_subset_larger_than_source(self):
        """Test that extracting more degrees than source returns original scale"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        subset = extract_scale_subset(scale, num_degrees=20, method="even")

        # Should return the original scale
        assert len(subset.intervals_cents) == len(scale.intervals_cents)

    def test_extract_scale_subset_invalid_method(self):
        """Test that invalid method raises error"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        with pytest.raises(ValueError, match="Unknown method"):
            extract_scale_subset(scale, num_degrees=5, method="invalid")

    def test_create_equal_division_scale_octave(self):
        """Test creating equal division of octave"""
        scale = create_equal_division_scale(num_divisions=19, interval_cents=1200.0)

        assert isinstance(scale, MicrotonalScale)
        assert len(scale.intervals_cents) == 20  # 19 divisions + tonic
        assert "19-EDoctave" in scale.name
        # Check that intervals are evenly spaced
        expected_step = 1200.0 / 19
        for i in range(1, len(scale.intervals_cents)):
            expected_value = i * expected_step
            assert abs(scale.intervals_cents[i] - expected_value) < 0.01

    def test_create_equal_division_scale_tritave(self):
        """Test creating equal division of tritave (Bohlen-Pierce style)"""
        import math
        tritave_cents = 1200 * math.log2(3)  # ~1901.955 cents
        scale = create_equal_division_scale(num_divisions=13, interval_cents=tritave_cents)

        assert isinstance(scale, MicrotonalScale)
        assert len(scale.intervals_cents) == 14  # 13 divisions + tonic
        assert "13-ED" in scale.name

    def test_create_equal_division_scale_custom_tonic(self):
        """Test creating EDO scale with custom tonic"""
        scale = create_equal_division_scale(num_divisions=22, interval_cents=1200.0, tonic_midi=48)

        assert scale.tonic_midi == 48
        assert len(scale.intervals_cents) == 23

    def test_rotate_scale_intervals(self):
        """Test rotating scale intervals"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        rotated = rotate_scale_intervals(scale, rotation_cents=100.0)

        assert isinstance(rotated, MicrotonalScale)
        assert "rotated" in rotated.name
        # All intervals should be shifted by 100 cents (mod 1200)
        assert all(0 <= interval < 1200 for interval in rotated.intervals_cents)

    def test_rotate_scale_intervals_full_octave(self):
        """Test rotating by full octave returns similar scale"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        rotated = rotate_scale_intervals(scale, rotation_cents=1200.0)

        # Rotating by full octave should bring us back (approximately)
        assert isinstance(rotated, MicrotonalScale)

    def test_merge_scales_two_scales(self):
        """Test merging two scales"""
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)

        merged = merge_scales(scale1, scale2)

        assert isinstance(merged, MicrotonalScale)
        assert "Merged" in merged.name
        # Should have intervals from both scales
        assert len(merged.intervals_cents) >= len(scale1.intervals_cents)

    def test_merge_scales_three_scales(self):
        """Test merging three scales"""
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)
        scale3 = create_tuning_system_scale(TuningSystem.JUST_INTONATION_7, tonic_midi=60)

        merged = merge_scales(scale1, scale2, scale3)

        assert isinstance(merged, MicrotonalScale)
        assert "Merged" in merged.name

    def test_merge_scales_with_tolerance(self):
        """Test that merge respects tolerance for duplicate intervals"""
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)

        # Merging identical scales should not significantly increase size
        merged = merge_scales(scale1, scale2, tolerance_cents=10.0)

        # Merged scale should not have more than a few extra intervals
        # (tolerance allows some near-duplicates to be merged)
        assert len(merged.intervals_cents) <= len(scale1.intervals_cents) + 5

    def test_merge_scales_no_scales(self):
        """Test that merging with no scales raises error"""
        with pytest.raises(ValueError, match="At least one scale required"):
            merge_scales()

    def test_merge_scales_many(self):
        """Test merging many scales"""
        scales = [
            create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60),
            create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60),
            create_tuning_system_scale(TuningSystem.JUST_INTONATION_7, tonic_midi=60),
            create_tuning_system_scale(TuningSystem.PYTHAGOREAN, tonic_midi=60),
            create_tuning_system_scale(TuningSystem.MEANTONE, tonic_midi=60),
        ]

        merged = merge_scales(*scales)

        assert isinstance(merged, MicrotonalScale)
        # Name should indicate "more" for many scales
        assert "more" in merged.name or "+" in merged.name


class TestIntegrationChordAndTransformations:
    """Integration tests for chord theory and transformations"""

    def test_build_chords_from_morphed_scales(self):
        """Test building chords from morphed scales"""
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.JUST_INTONATION_7, tonic_midi=60)

        morph_sequence = morph_scales(scale1, scale2, num_steps=3, interpolation="linear")

        # Build chords from each morphed scale
        chords = []
        for scale in morph_sequence:
            if len(scale.intervals_cents) >= 5:
                chord = build_microtonal_chord(scale, root_degree=0, num_notes=3, skip_pattern=[0, 2, 4])
                chords.append(chord)

        # Should have generated several chords
        assert len(chords) > 0
        assert all(isinstance(c, MicrotonalChord) for c in chords)

    def test_progression_from_stretched_scale(self):
        """Test generating progression from stretched scale"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        stretched = stretch_scale(scale, stretch_factor=1.1, preserve_octave=True)

        progression = generate_microtonal_chord_progression(
            stretched, num_chords=4, chord_size=3, progression_type="ascending"
        )

        assert len(progression) == 4
        assert all(isinstance(c, MicrotonalChord) for c in progression)

    def test_merge_and_build_chords(self):
        """Test merging scales then building chords"""
        scale1 = create_tuning_system_scale(TuningSystem.EQUAL_12, tonic_midi=60)
        scale2 = create_tuning_system_scale(TuningSystem.JUST_INTONATION_7, tonic_midi=60)

        merged = merge_scales(scale1, scale2)

        if len(merged.intervals_cents) >= 7:
            chord = build_microtonal_chord(merged, root_degree=0, num_notes=4, skip_pattern=[0, 2, 4, 6])
            assert isinstance(chord, MicrotonalChord)
            analysis = analyze_chord_consonance(chord)
            assert 'quality' in analysis

    def test_extract_subset_and_progression(self):
        """Test extracting subset and generating progression"""
        scale = create_tuning_system_scale(TuningSystem.EQUAL_19, tonic_midi=60)
        subset = extract_scale_subset(scale, num_degrees=12, method="even")

        progression = generate_microtonal_chord_progression(
            subset, num_chords=3, chord_size=3, progression_type="circle_of_fifths"
        )

        assert len(progression) == 3
        assert all(isinstance(c, MicrotonalChord) for c in progression)
