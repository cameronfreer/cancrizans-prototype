"""Fix notebooks to use assemble_crab_from_theme instead of mirror_canon."""

import nbformat
from pathlib import Path

def fix_notebook(notebook_path: Path) -> None:
    """Fix a notebook by replacing mirror_canon with assemble_crab_from_theme."""
    print(f"Fixing {notebook_path.name}...")

    # Read notebook
    nb = nbformat.read(notebook_path, as_version=4)

    # Fix imports
    for cell in nb.cells:
        if cell.cell_type == 'code':
            source = cell.source

            # Replace import
            if 'mirror_canon' in source and 'from cancrizans import' in source:
                source = source.replace(
                    'mirror_canon',
                    'assemble_crab_from_theme'
                )
                cell.source = source
                print(f"  ✓ Fixed imports")

            # Replace function calls
            if 'mirror_canon(' in source:
                # Replace mirror_canon(x) with assemble_crab_from_theme(x)
                source = source.replace('mirror_canon(', 'assemble_crab_from_theme(')
                cell.source = source
                print(f"  ✓ Fixed function call")

    # Write back
    nbformat.write(nb, notebook_path)
    print(f"  ✓ Saved\n")


if __name__ == '__main__':
    notebooks_dir = Path('notebooks')

    notebooks = [
        notebooks_dir / 'transformation_techniques.ipynb',
        notebooks_dir / 'symmetry_analysis.ipynb',
    ]

    for nb_path in notebooks:
        if nb_path.exists():
            fix_notebook(nb_path)
        else:
            print(f"Notebook not found: {nb_path}")

    print("✓ All notebooks fixed!")
