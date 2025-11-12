"""Fix notebooks to use correct interval_analysis keys."""

import nbformat
from pathlib import Path
import re

def fix_interval_analysis(notebook_path: Path) -> None:
    """Fix interval_analysis usage in notebooks."""
    print(f"Fixing interval analysis in {notebook_path.name}...")

    # Read notebook
    nb = nbformat.read(notebook_path, as_version=4)
    modified = False

    # Fix cells
    for cell in nb.cells:
        if cell.cell_type == 'code':
            source = cell.source

            if 'interval_analysis' in source and '['  in source:
                # Replace the problematic keys
                new_source = source

                # Fix most_common_interval -> most_common
                new_source = re.sub(
                    r"\['most_common_interval'\]",
                    "['most_common'][0][0] if ['most_common'] else None",
                    new_source
                )

                # Remove interval_diversity (not available)
                lines = new_source.split('\n')
                new_lines = [line for line in lines if 'interval_diversity' not in line]
                new_source = '\n'.join(new_lines)

                # Fix average_interval_size -> average
                new_source = new_source.replace("['average_interval_size']", "['average']")

                if new_source != source:
                    cell.source = new_source
                    modified = True
                    print(f"  ✓ Fixed analysis keys")

    if modified:
        # Write back
        nbformat.write(nb, notebook_path)
        print(f"  ✓ Saved\n")
    else:
        print(f"  - No changes needed\n")


if __name__ == '__main__':
    notebooks_dir = Path('notebooks')

    notebooks = [
        notebooks_dir / 'transformation_techniques.ipynb',
        notebooks_dir / 'symmetry_analysis.ipynb',
    ]

    for nb_path in notebooks:
        if nb_path.exists():
            fix_interval_analysis(nb_path)
        else:
            print(f"Notebook not found: {nb_path}")

    print("✓ All notebooks fixed!")
