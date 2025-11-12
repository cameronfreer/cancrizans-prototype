"""Update notebook cells to match actual API."""

import nbformat
from pathlib import Path

def fix_transformation_notebook():
    """Fix transformation_techniques.ipynb."""
    nb_path = Path('notebooks/transformation_techniques.ipynb')
    print(f"Fixing {nb_path.name}...")

    nb = nbformat.read(nb_path, as_version=4)

    # Find and fix cell 17 (interval analysis)
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code' and 'interval_analysis' in cell.source and 'most_common_interval' in cell.source:
            # Replace with corrected code
            cell.source = """# Analyze intervals
orig_analysis = interval_analysis(melody)
retro_analysis = interval_analysis(melody_retro)
inv_analysis = interval_analysis(melody_inv)

print("Interval Analysis:")
print("\\nOriginal:")
if orig_analysis['most_common']:
    interval, count = orig_analysis['most_common'][0]
    print(f"  Most common: {interval} semitones ({count} times)")
print(f"  Total intervals: {orig_analysis['total_intervals']}")
print(f"  Average size: {orig_analysis['average']:.2f} semitones")
print(f"  Largest leap: {orig_analysis['largest_leap']} semitones")

print("\\nRetrograde:")
if retro_analysis['most_common']:
    interval, count = retro_analysis['most_common'][0]
    print(f"  Most common: {interval} semitones ({count} times)")
print(f"  Total intervals: {retro_analysis['total_intervals']}")
print(f"  Average size: {retro_analysis['average']:.2f} semitones")

print("\\nInversion:")
if inv_analysis['most_common']:
    interval, count = inv_analysis['most_common'][0]
    print(f"  Most common: {interval} semitones ({count} times)")
print(f"  Total intervals: {inv_analysis['total_intervals']}")
print(f"  Average size: {inv_analysis['average']:.2f} semitones")
print(f"  Ascending: {inv_analysis['distribution']['ascending']}, Descending: {inv_analysis['distribution']['descending']}")"""
            print(f"  ✓ Fixed cell {i} (interval analysis)")

    nbformat.write(nb, nb_path)
    print(f"  ✓ Saved\n")


def fix_symmetry_notebook():
    """Fix symmetry_analysis.ipynb."""
    nb_path = Path('notebooks/symmetry_analysis.ipynb')
    print(f"Fixing {nb_path.name}...")

    nb = nbformat.read(nb_path, as_version=4)

    # Find and fix any interval_analysis calls
    modified = False
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code' and 'interval_analysis' in cell.source and 'most_common_interval' in cell.source:
            # Similar fix
            old_source = cell.source
            new_source = old_source.replace("['most_common_interval']", "['most_common'][0][0] if ['most_common'] else 'None'")
            new_source = new_source.replace("['average_interval_size']", "['average']")
            # Remove diversity lines
            lines = [line for line in new_source.split('\n') if 'interval_diversity' not in line]
            new_source = '\n'.join(lines)

            if new_source != old_source:
                cell.source = new_source
                modified = True
                print(f"  ✓ Fixed cell {i}")

    if modified:
        nbformat.write(nb, nb_path)
        print(f"  ✓ Saved\n")
    else:
        print(f"  - No interval_analysis issues found\n")


if __name__ == '__main__':
    fix_transformation_notebook()
    fix_symmetry_notebook()
    print("✓ All notebooks updated!")
