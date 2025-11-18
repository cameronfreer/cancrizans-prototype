"""
Tests for research module (research.py).
"""

import pytest
import tempfile
import json
import csv
from pathlib import Path
from music21 import stream, note
from cancrizans import assemble_crab_from_theme
from cancrizans.research import (
    CanonAnalyzer,
    BatchAnalyzer,
    ResearchExporter,
    analyze_corpus
)
from cancrizans.io import to_midi


@pytest.fixture
def simple_canon():
    """Create a simple crab canon for testing."""
    theme = stream.Part()
    theme.append(note.Note('C4', quarterLength=1.0))
    theme.append(note.Note('D4', quarterLength=1.0))
    theme.append(note.Note('E4', quarterLength=1.0))
    return assemble_crab_from_theme(theme)


@pytest.fixture
def complex_canon():
    """Create a more complex canon for testing."""
    theme = stream.Part()
    theme.append(note.Note('G4', quarterLength=0.5))
    theme.append(note.Note('A4', quarterLength=0.5))
    theme.append(note.Note('B4', quarterLength=1.0))
    theme.append(note.Note('C5', quarterLength=0.5))
    theme.append(note.Note('D5', quarterLength=0.5))
    return assemble_crab_from_theme(theme)


class TestCanonAnalyzer:
    """Test CanonAnalyzer class."""

    def test_analyzer_creation(self, simple_canon):
        """Test creating a CanonAnalyzer."""
        analyzer = CanonAnalyzer(simple_canon, "Test Canon")
        assert analyzer.name == "Test Canon"
        assert analyzer.score == simple_canon
        assert analyzer._analysis_cache is None

    def test_analyzer_default_name(self, simple_canon):
        """Test analyzer with default name."""
        analyzer = CanonAnalyzer(simple_canon)
        assert analyzer.name == "Untitled"

    def test_analyze_basic_structure(self, simple_canon):
        """Test basic analysis functionality."""
        analyzer = CanonAnalyzer(simple_canon, "Test")
        results = analyzer.analyze()

        assert 'name' in results
        assert 'timestamp' in results
        assert 'is_palindrome' in results
        assert 'basic_properties' in results
        assert 'intervals' in results
        assert 'harmony' in results
        assert 'rhythm' in results
        assert 'structure' in results

    def test_analyze_caching(self, simple_canon):
        """Test that analysis results are cached."""
        analyzer = CanonAnalyzer(simple_canon)
        results1 = analyzer.analyze()
        results2 = analyzer.analyze()

        # Should be the same object (cached)
        assert results1 is results2
        assert analyzer._analysis_cache is not None

    def test_basic_properties(self, simple_canon):
        """Test basic properties analysis."""
        analyzer = CanonAnalyzer(simple_canon)
        results = analyzer.analyze()
        props = results['basic_properties']

        assert 'num_voices' in props
        assert 'total_notes' in props
        assert 'duration_quarters' in props
        assert props['num_voices'] == 2  # crab canon has 2 voices

    def test_structure_analysis(self, simple_canon):
        """Test structure analysis."""
        analyzer = CanonAnalyzer(simple_canon)
        results = analyzer.analyze()
        structure = results['structure']

        assert 'pitch_ranges' in structure
        assert 'contour_correlation' in structure
        assert len(structure['pitch_ranges']) > 0

    def test_pitch_range_analysis(self, simple_canon):
        """Test pitch range analysis."""
        analyzer = CanonAnalyzer(simple_canon)
        results = analyzer.analyze()
        pitch_ranges = results['structure']['pitch_ranges']

        assert len(pitch_ranges) == 2  # two voices
        for pr in pitch_ranges:
            assert 'min' in pr
            assert 'max' in pr
            assert 'span' in pr
            assert pr['max'] >= pr['min']
            assert pr['span'] == pr['max'] - pr['min']

    def test_contour_correlation(self, simple_canon):
        """Test contour correlation calculation."""
        analyzer = CanonAnalyzer(simple_canon)
        results = analyzer.analyze()
        correlation = results['structure']['contour_correlation']

        # Should have a correlation value for 2-voice canon
        assert correlation is not None
        assert isinstance(correlation, float)

    def test_is_palindrome_detection(self, simple_canon):
        """Test palindrome detection in analysis."""
        analyzer = CanonAnalyzer(simple_canon)
        results = analyzer.analyze()

        # Crab canon should be detected as palindrome
        assert results['is_palindrome'] is True


class TestBatchAnalyzer:
    """Test BatchAnalyzer class."""

    def test_batch_creation(self):
        """Test creating a BatchAnalyzer."""
        batch = BatchAnalyzer()
        assert batch.canons == []

    def test_add_canon(self, simple_canon):
        """Test adding a canon to the batch."""
        batch = BatchAnalyzer()
        batch.add_canon(simple_canon, "Test Canon")

        assert len(batch.canons) == 1
        assert batch.canons[0].name == "Test Canon"

    def test_add_multiple_canons(self, simple_canon, complex_canon):
        """Test adding multiple canons."""
        batch = BatchAnalyzer()
        batch.add_canon(simple_canon, "Simple")
        batch.add_canon(complex_canon, "Complex")

        assert len(batch.canons) == 2
        assert batch.canons[0].name == "Simple"
        assert batch.canons[1].name == "Complex"

    def test_add_from_file(self, simple_canon):
        """Test adding a canon from file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / 'test.mid'
            to_midi(simple_canon, filepath)

            batch = BatchAnalyzer()
            batch.add_from_file(filepath)

            assert len(batch.canons) == 1
            assert batch.canons[0].name == 'test'

    def test_add_from_file_custom_name(self, simple_canon):
        """Test adding from file with custom name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / 'test.mid'
            to_midi(simple_canon, filepath)

            batch = BatchAnalyzer()
            batch.add_from_file(filepath, name="Custom Name")

            assert batch.canons[0].name == "Custom Name"

    def test_analyze_all(self, simple_canon, complex_canon):
        """Test analyzing all canons in batch."""
        batch = BatchAnalyzer()
        batch.add_canon(simple_canon, "Simple")
        batch.add_canon(complex_canon, "Complex")

        results = batch.analyze_all()

        assert len(results) == 2
        assert results[0]['name'] == "Simple"
        assert results[1]['name'] == "Complex"

    def test_compare_empty_batch(self):
        """Test comparison with empty batch."""
        batch = BatchAnalyzer()
        comparison = batch.compare()

        assert comparison == {}

    def test_compare_single_canon(self, simple_canon):
        """Test comparison with single canon."""
        batch = BatchAnalyzer()
        batch.add_canon(simple_canon, "Test")

        comparison = batch.compare()

        assert 'total_canons' in comparison
        assert comparison['total_canons'] == 1
        assert 'palindrome_count' in comparison
        assert 'average_duration' in comparison
        assert 'consonance_stats' in comparison
        assert 'interval_stats' in comparison

    def test_compare_multiple_canons(self, simple_canon, complex_canon):
        """Test comparison with multiple canons."""
        batch = BatchAnalyzer()
        batch.add_canon(simple_canon, "Simple")
        batch.add_canon(complex_canon, "Complex")

        comparison = batch.compare()

        assert comparison['total_canons'] == 2
        assert 'consonance_stats' in comparison
        assert 'mean' in comparison['consonance_stats']
        assert 'min' in comparison['consonance_stats']
        assert 'max' in comparison['consonance_stats']


class TestResearchExporter:
    """Test ResearchExporter class."""

    def test_to_csv(self, simple_canon):
        """Test CSV export."""
        analyzer = CanonAnalyzer(simple_canon, "Test")
        analyses = [analyzer.analyze()]

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'results.csv'
            ResearchExporter.to_csv(analyses, output)

            assert output.exists()

            # Verify CSV content
            with open(output, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                assert len(rows) == 1
                assert rows[0]['name'] == 'Test'
                assert 'is_palindrome' in rows[0]
                assert 'num_voices' in rows[0]

    def test_to_csv_empty(self):
        """Test CSV export with empty list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'results.csv'
            ResearchExporter.to_csv([], output)

            # Should not create file or should create empty file
            assert not output.exists() or output.stat().st_size == 0

    def test_to_json(self, simple_canon):
        """Test JSON export."""
        analyzer = CanonAnalyzer(simple_canon, "Test")
        analyses = [analyzer.analyze()]

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'results.json'
            ResearchExporter.to_json(analyses, output)

            assert output.exists()

            # Verify JSON content
            with open(output, 'r') as f:
                data = json.load(f)
                assert len(data) == 1
                assert data[0]['name'] == 'Test'

    def test_to_json_multiple(self, simple_canon, complex_canon):
        """Test JSON export with multiple canons."""
        batch = BatchAnalyzer()
        batch.add_canon(simple_canon, "Simple")
        batch.add_canon(complex_canon, "Complex")
        analyses = batch.analyze_all()

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'results.json'
            ResearchExporter.to_json(analyses, output)

            with open(output, 'r') as f:
                data = json.load(f)
                assert len(data) == 2

    def test_to_latex_table(self, simple_canon):
        """Test LaTeX table export."""
        analyzer = CanonAnalyzer(simple_canon, "Test_Canon")
        analyses = [analyzer.analyze()]

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'results.tex'
            ResearchExporter.to_latex_table(analyses, output)

            assert output.exists()

            # Verify LaTeX content
            content = output.read_text()
            assert r'\begin{table}' in content
            assert r'\end{table}' in content
            assert r'\begin{tabular}' in content
            assert 'Test\\_Canon' in content  # Escaped underscore

    def test_to_markdown_table(self, simple_canon):
        """Test Markdown table export."""
        analyzer = CanonAnalyzer(simple_canon, "Test")
        analyses = [analyzer.analyze()]

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'results.md'
            ResearchExporter.to_markdown_table(analyses, output)

            assert output.exists()

            # Verify Markdown content
            content = output.read_text()
            assert '| Canon |' in content
            assert '| Test |' in content
            assert '✓' in content or '✗' in content

    def test_to_markdown_palindrome_detection(self, simple_canon):
        """Test that Markdown export shows palindrome correctly."""
        analyzer = CanonAnalyzer(simple_canon, "Palindrome_Test")
        analyses = [analyzer.analyze()]

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'results.md'
            ResearchExporter.to_markdown_table(analyses, output)

            content = output.read_text()
            # Should show checkmark for palindromic canon
            assert '✓' in content


class TestAnalyzeCorpus:
    """Test analyze_corpus function."""

    def test_analyze_corpus_empty_directory(self):
        """Test corpus analysis with empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            analyses, comparison = analyze_corpus(Path(tmpdir))

            assert analyses == []
            assert comparison == {}

    def test_analyze_corpus_single_file(self, simple_canon):
        """Test corpus analysis with single file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / 'test.mid'
            to_midi(simple_canon, filepath)

            analyses, comparison = analyze_corpus(Path(tmpdir))

            assert len(analyses) == 1
            assert analyses[0]['name'] == 'test'
            assert comparison['total_canons'] == 1

    def test_analyze_corpus_multiple_files(self, simple_canon, complex_canon):
        """Test corpus analysis with multiple files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            to_midi(simple_canon, Path(tmpdir) / 'canon1.mid')
            to_midi(complex_canon, Path(tmpdir) / 'canon2.mid')

            analyses, comparison = analyze_corpus(Path(tmpdir))

            assert len(analyses) == 2
            assert comparison['total_canons'] == 2

    def test_analyze_corpus_pattern_filter(self, simple_canon):
        """Test corpus analysis with pattern filtering."""
        with tempfile.TemporaryDirectory() as tmpdir:
            to_midi(simple_canon, Path(tmpdir) / 'test.mid')
            to_midi(simple_canon, Path(tmpdir) / 'other.xml')  # Different extension

            # Should only find .mid files
            analyses, comparison = analyze_corpus(Path(tmpdir), pattern="*.mid")

            assert len(analyses) == 1
            assert analyses[0]['name'] == 'test'


class TestResearchIntegration:
    """Integration tests for research module."""

    def test_full_research_workflow(self, simple_canon, complex_canon):
        """Test complete research workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create batch
            batch = BatchAnalyzer()
            batch.add_canon(simple_canon, "Simple")
            batch.add_canon(complex_canon, "Complex")

            # Analyze
            analyses = batch.analyze_all()
            assert len(analyses) == 2

            # Export to all formats
            ResearchExporter.to_csv(analyses, tmppath / 'results.csv')
            ResearchExporter.to_json(analyses, tmppath / 'results.json')
            ResearchExporter.to_latex_table(analyses, tmppath / 'results.tex')
            ResearchExporter.to_markdown_table(analyses, tmppath / 'results.md')

            # Verify all files created
            assert (tmppath / 'results.csv').exists()
            assert (tmppath / 'results.json').exists()
            assert (tmppath / 'results.tex').exists()
            assert (tmppath / 'results.md').exists()

    def test_corpus_export_workflow(self, simple_canon, complex_canon):
        """Test corpus analysis and export workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create test corpus
            to_midi(simple_canon, tmppath / 'canon1.mid')
            to_midi(complex_canon, tmppath / 'canon2.mid')

            # Analyze corpus
            analyses, comparison = analyze_corpus(tmppath)

            # Export
            output_dir = tmppath / 'results'
            output_dir.mkdir()
            ResearchExporter.to_json(analyses, output_dir / 'analyses.json')

            # Verify
            assert len(analyses) == 2
            assert (output_dir / 'analyses.json').exists()

    def test_contour_correlation_single_note(self):
        """Test contour correlation returns 0.0 for voices with < 2 notes (line 112)."""
        from music21 import stream, note

        # Create voices with only 1 note each
        voice1 = stream.Part()
        voice1.append(note.Note('C4', quarterLength=1.0))

        voice2 = stream.Part()
        voice2.append(note.Note('G4', quarterLength=1.0))

        score = stream.Score()
        score.insert(0, voice1)
        score.insert(0, voice2)

        analyzer = CanonAnalyzer(score, name="Single Note Canon")
        analysis = analyzer.analyze()

        # Should return 0.0 when there are < 2 notes
        assert analysis['structure']['contour_correlation'] == 0.0


class TestAdvancedResearch:
    """Test advanced research functions."""

    def test_batch_visualize(self):
        """Test batch visualization generation."""
        from cancrizans.research import batch_visualize
        from cancrizans.generator import CanonGenerator
        from cancrizans.io import to_midi

        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create some test files
            gen = CanonGenerator(seed=42)
            for i in range(2):
                canon = gen.generate_scale_canon('C', 'major')
                to_midi(canon, tmppath / f'canon{i}.mid')

            # Generate visualizations
            output_dir = tmppath / 'viz'
            batch_visualize(tmppath, output_dir, pattern='*.mid')

            # Check outputs
            assert (output_dir / 'canon0_piano_roll.png').exists()
            assert (output_dir / 'canon0_symmetry.png').exists()
            assert (output_dir / 'canon1_piano_roll.png').exists()
            assert (output_dir / 'canon1_symmetry.png').exists()

    def test_batch_visualize_specific_types(self):
        """Test batch visualization with specific types."""
        from cancrizans.research import batch_visualize
        from cancrizans.generator import CanonGenerator
        from cancrizans.io import to_midi

        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create test file
            gen = CanonGenerator(seed=42)
            canon = gen.generate_scale_canon('C', 'major')
            to_midi(canon, tmppath / 'canon.mid')

            # Generate only piano rolls
            output_dir = tmppath / 'viz'
            batch_visualize(tmppath, output_dir, vis_types=['piano_roll'])

            # Check outputs
            assert (output_dir / 'canon_piano_roll.png').exists()
            assert not (output_dir / 'canon_symmetry.png').exists()

    def test_generate_educational_examples(self):
        """Test educational example generation."""
        from cancrizans.research import generate_educational_examples

        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Generate examples
            generate_educational_examples(tmppath, seed=42)

            # Check that all expected files exist
            expected_files = [
                'educational_scale_canon.mid',
                'educational_scale_canon.musicxml',
                'educational_arpeggio_canon.mid',
                'educational_arpeggio_canon.musicxml',
                'educational_modal_canon.mid',
                'educational_modal_canon.musicxml',
                'educational_markov_canon.mid',
                'educational_markov_canon.musicxml',
                'educational_contour_canon.mid',
                'educational_contour_canon.musicxml',
                'educational_motif_canon.mid',
                'educational_motif_canon.musicxml',
            ]

            for filename in expected_files:
                assert (tmppath / filename).exists(), f"Missing file: {filename}"

    def test_educational_examples_have_metadata(self):
        """Test that educational examples have proper metadata."""
        from cancrizans.research import generate_educational_examples
        from cancrizans.io import load_score, get_metadata

        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Generate examples
            generate_educational_examples(tmppath, seed=42)

            # Load one and check metadata
            score = load_score(tmppath / 'educational_scale_canon.musicxml')
            meta = get_metadata(score)

            # Should have title and composer
            assert 'title' in meta or 'movementName' in meta
            assert meta.get('composer') == 'Cancrizans Educational'

    def test_generate_research_report(self):
        """Test research report generation."""
        from cancrizans.research import generate_research_report

        # Create some mock analyses
        analyses = [
            {
                'name': 'Canon 1',
                'is_palindrome': True,
                'basic_properties': {
                    'duration_quarters': 32.0,
                    'total_notes': 40,
                },
                'harmony': {'consonance_ratio': 0.75},
                'intervals': {'average': 2.5},
            },
            {
                'name': 'Canon 2',
                'is_palindrome': False,
                'basic_properties': {
                    'duration_quarters': 24.0,
                    'total_notes': 30,
                },
                'harmony': {'consonance_ratio': 0.65},
                'intervals': {'average': 3.0},
            },
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            output_path = tmppath / 'report.md'

            # Generate report
            generate_research_report(analyses, output_path)

            # Verify output
            assert output_path.exists()
            content = output_path.read_text()

            # Check for key sections
            assert 'Crab Canon Research Report' in content
            assert 'Total canons analyzed: 2' in content
            assert 'Palindromic canons: 1' in content
            assert 'Canon 1' in content
            assert 'Canon 2' in content

    def test_research_report_with_advanced_metrics(self):
        """Test research report with spectral and symmetry metrics."""
        from cancrizans.research import generate_research_report

        # Create analyses with advanced metrics
        analyses = [
            {
                'name': 'Canon 1',
                'is_palindrome': True,
                'basic_properties': {'duration_quarters': 32.0, 'total_notes': 40},
                'harmony': {'consonance_ratio': 0.75},
                'intervals': {'average': 2.5},
                'spectral': {'tessitura': 60.0},
                'symmetry': {'pitch_symmetry': 0.95, 'rhythmic_symmetry': 0.98},
            },
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            output_path = tmppath / 'report.md'

            # Generate report
            generate_research_report(analyses, output_path)

            # Verify advanced sections
            content = output_path.read_text()
            assert 'Spectral Analysis' in content
            assert 'Symmetry Metrics' in content
            assert 'tessitura' in content.lower()

    def test_compare_corpus_canons(self):
        """Test pairwise canon comparison."""
        from cancrizans.research import compare_corpus_canons
        from cancrizans.generator import CanonGenerator

        gen = CanonGenerator(seed=42)
        canon1 = gen.generate_scale_canon('C', 'major')
        canon2 = gen.generate_scale_canon('D', 'minor')
        canon3 = gen.generate_arpeggio_canon('G', 'major')

        canons = [
            ('Canon 1', canon1),
            ('Canon 2', canon2),
            ('Canon 3', canon3),
        ]

        result = compare_corpus_canons(canons)

        # Check structure
        assert result['num_canons'] == 3
        assert result['num_comparisons'] == 3  # 3 choose 2
        assert 'avg_similarity' in result
        assert 'min_similarity' in result
        assert 'max_similarity' in result
        assert 'comparison_matrix' in result

    def test_compare_corpus_canons_with_export(self):
        """Test corpus comparison with JSON export."""
        from cancrizans.research import compare_corpus_canons
        from cancrizans.generator import CanonGenerator

        gen = CanonGenerator(seed=42)
        canon1 = gen.generate_scale_canon('C', 'major')
        canon2 = gen.generate_scale_canon('D', 'major')

        canons = [
            ('Canon 1', canon1),
            ('Canon 2', canon2),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            output_path = tmppath / 'comparisons.json'

            result = compare_corpus_canons(canons, output_path=output_path)

            # Check file was created
            assert output_path.exists()

            # Verify JSON content
            import json
            with open(output_path) as f:
                data = json.load(f)

            assert data['num_canons'] == 2
            assert data['num_comparisons'] == 1
            assert len(data['comparisons']) == 1

    def test_advanced_analysis_in_canon_analyzer(self):
        """Test that CanonAnalyzer includes advanced metrics."""
        from cancrizans.generator import CanonGenerator

        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        analyzer = CanonAnalyzer(canon, name="Test", advanced=True)
        analysis = analyzer.analyze()

        # Should have spectral analysis
        assert 'spectral' in analysis
        assert 'tessitura' in analysis['spectral']

        # Should have symmetry and chord progression (for 2-voice canons)
        if len(list(canon.parts)) == 2:
            assert 'symmetry' in analysis
            assert 'chord_progression' in analysis

    def test_advanced_analysis_disabled(self):
        """Test that advanced analysis can be disabled."""
        from cancrizans.generator import CanonGenerator

        gen = CanonGenerator(seed=42)
        canon = gen.generate_scale_canon('C', 'major')

        analyzer = CanonAnalyzer(canon, name="Test", advanced=False)
        analysis = analyzer.analyze()

        # Should NOT have advanced metrics
        assert 'spectral' not in analysis
        assert 'symmetry' not in analysis


class TestResearchIntegrationWorkflows:
    """Test complete research workflows."""

    def test_full_research_workflow(self):
        """Test complete research workflow: generate, analyze, visualize, report."""
        from cancrizans.research import (
            generate_educational_examples,
            analyze_corpus,
            batch_visualize,
            generate_research_report,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Step 1: Generate educational examples
            examples_dir = tmppath / 'examples'
            generate_educational_examples(examples_dir, seed=42)

            # Step 2: Analyze corpus
            analyses, comparison = analyze_corpus(examples_dir, pattern='*.mid')

            # Step 3: Generate visualizations
            viz_dir = tmppath / 'viz'
            batch_visualize(examples_dir, viz_dir, pattern='*.mid')

            # Step 4: Generate report
            report_path = tmppath / 'report.md'
            generate_research_report(analyses, report_path)

            # Verify all outputs
            assert len(analyses) == 6  # 6 educational examples
            assert len(list(viz_dir.glob('*.png'))) > 0
            assert report_path.exists()

    def test_comparative_study_workflow(self):
        """Test workflow for comparing multiple canons."""
        from cancrizans.research import compare_corpus_canons
        from cancrizans.generator import CanonGenerator
        from cancrizans.io import to_midi, load_score

        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create diverse canons
            gen = CanonGenerator(seed=42)
            canons_data = [
                ('Scale C Major', gen.generate_scale_canon('C', 'major')),
                ('Scale D Minor', gen.generate_scale_canon('D', 'minor')),
                ('Arpeggio G', gen.generate_arpeggio_canon('G', 'major')),
                ('Fibonacci', gen.generate_fibonacci_canon(length=12)),
            ]

            # Save and reload to ensure they work with file I/O
            saved_canons = []
            for name, canon in canons_data:
                path = tmppath / f'{name.replace(" ", "_")}.mid'
                to_midi(canon, path)
                loaded = load_score(path)
                saved_canons.append((name, loaded))

            # Perform comparative analysis
            results = compare_corpus_canons(saved_canons)

            # Verify results make sense
            assert results['num_canons'] == 4
            assert results['num_comparisons'] == 6  # 4 choose 2
            assert 0.0 <= results['avg_similarity'] <= 1.0
