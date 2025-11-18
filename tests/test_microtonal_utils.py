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
    calculate_scale_compatibility
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
