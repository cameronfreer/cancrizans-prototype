# Cancrizans Examples

This directory contains practical examples demonstrating the features of the Cancrizans library.

## Microtonal Examples

### Running the Examples

To run the comprehensive microtonal examples:

```bash
cd examples
python microtonal_examples.py
```

This will generate:
- MIDI files for various canons
- PNG visualizations of scales
- Scala (.scl) format scale files

All outputs are saved to `output/microtonal_examples/`

### What's Demonstrated

The `microtonal_examples.py` script showcases:

1. **Baroque Canon Generation** - Create canons using historical temperaments like Werckmeister III
2. **Arabic Maqam Canon** - Generate canons with quarter-tone Arabic scales
3. **Scale Blending** - Create hybrid scales by blending two tuning systems
4. **Modulating Canon** - Compose canons that transition between different scales
5. **World Music Comparison** - Compare scales from Arabic, Indian, Indonesian, and Japanese traditions
6. **Scala File Workflow** - Import and export industry-standard Scala (.scl) files
7. **Complete Catalog** - Browse 76+ scales across 11 musical traditions
8. **Style-Specific Canons** - Generate canons optimized for different musical styles

### Example Outputs

After running the examples, you'll find:

**MIDI Files:**
- `baroque_werckmeister.mid` - Canon in Werckmeister III tuning
- `arabic_maqam.mid` - Canon in Maqam Rast
- `modulating_canon.mid` - Canon that modulates between scales
- `canon_baroque.mid`, `canon_indian.mid`, `canon_gamelan.mid`, `canon_experimental.mid`

**Visualizations:**
- `werckmeister_scale.png` - Circular diagram of Werckmeister III
- `maqam_rast_scale.png` - Maqam Rast scale visualization
- `scale_blending_comparison.png` - Side-by-side comparison of blended scales
- `modulation_path.png` - Visualization of modulation between scales
- `world_music_comparison.png` - Comparison of 4 world music scales

**Scala Files:**
- `werckmeister_iii.scl` - Werckmeister III in Scala format
- `19_tet.scl` - 19-tone equal temperament
- `bohlen_pierce.scl` - Bohlen-Pierce scale

### Requirements

The examples require:
- `music21` - Musical notation library
- `matplotlib` - For visualizations
- `numpy` - For numerical operations

Install with:
```bash
pip install music21 matplotlib numpy
```

### Customization

You can easily modify the examples to:
- Generate longer or shorter canons by changing the `length` parameter
- Use different root notes by changing the `root` parameter
- Explore different tuning systems from the catalog
- Export to different formats (MusicXML, LilyPond, ABC)

### Code Examples

#### Generate a Canon in a Specific Tuning

```python
from cancrizans import CanonGenerator
from cancrizans.microtonal import TuningSystem

gen = CanonGenerator(seed=42)
canon = gen.generate_microtonal_canon(
    style='baroque',
    root='D4',
    length=16,
    tuning_system=TuningSystem.WERCKMEISTER_III
)
```

#### Visualize a Scale

```python
from cancrizans.microtonal import create_tuning_system_scale, TuningSystem
from cancrizans.viz import visualize_microtonal_scale

scale = create_tuning_system_scale(TuningSystem.WERCKMEISTER_III, 60)
visualize_microtonal_scale(scale, 'my_scale.png', dpi=300)
```

#### Export to Scala Format

```python
from cancrizans.microtonal_utils import export_scala_file

export_scala_file(scale, 'my_scale.scl', description="My Custom Scale")
```

### Additional Resources

- [Microtonal Features Summary](../MICROTONAL_FEATURES_SUMMARY.md) - Comprehensive documentation
- [Main README](../README.md) - Full project documentation
- [Scala Archive](http://www.huygens-fokker.org/scala/) - Database of microtonal scales

## Future Examples

Planned examples for future releases:
- Audio synthesis with microtonal accuracy
- Machine learning-based style analysis
- Interactive scale editor
- Real-time MIDI performance with microtonal pitch bend
