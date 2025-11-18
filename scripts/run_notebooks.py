#!/usr/bin/env python3
"""
Execute Jupyter notebooks and convert them to markdown with embedded images.

This script:
1. Executes all notebooks in the notebooks/ directory
2. Converts them to markdown
3. Embeds generated images
4. Saves output to docs/tutorials/
"""

import subprocess
import sys
from pathlib import Path


def execute_notebook(notebook_path: Path) -> bool:
    """Execute a Jupyter notebook in-place."""
    print(f"Executing {notebook_path.name}...")

    cmd = [
        "jupyter", "nbconvert",
        "--to", "notebook",
        "--execute",
        "--inplace",
        "--ExecutePreprocessor.timeout=300",
        str(notebook_path)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"  ✓ Executed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Execution failed:")
        print(f"    {e.stderr}")
        return False


def convert_to_markdown(notebook_path: Path, output_dir: Path) -> bool:
    """Convert executed notebook to markdown."""
    print(f"Converting {notebook_path.name} to markdown...")

    output_file = output_dir / f"{notebook_path.stem}.md"

    cmd = [
        "jupyter", "nbconvert",
        "--to", "markdown",
        "--output-dir", str(output_dir),
        str(notebook_path)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"  ✓ Converted to {output_file.name}")

        # Fix image paths in markdown (nbconvert creates a _files directory)
        if output_file.exists():
            content = output_file.read_text()
            # Update image paths to point to docs/images/
            content = content.replace(
                f"{notebook_path.stem}_files/",
                "../images/"
            )
            output_file.write_text(content)
            print(f"  ✓ Fixed image paths")

        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Conversion failed:")
        print(f"    {e.stderr}")
        return False


def main():
    """Main execution function."""
    # Set up paths
    project_root = Path(__file__).parent.parent
    notebooks_dir = project_root / "notebooks"
    docs_dir = project_root / "docs" / "tutorials"
    images_dir = project_root / "docs" / "images"

    # Create output directories
    docs_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)

    # Find all notebooks
    notebooks = list(notebooks_dir.glob("*.ipynb"))

    if not notebooks:
        print("No notebooks found in notebooks/ directory")
        return 0

    print(f"Found {len(notebooks)} notebook(s)")
    print("=" * 60)

    success_count = 0
    failed_notebooks = []

    for notebook in sorted(notebooks):
        print(f"\nProcessing: {notebook.name}")
        print("-" * 60)

        # Execute notebook
        if not execute_notebook(notebook):
            failed_notebooks.append(notebook.name)
            continue

        # Convert to markdown
        if not convert_to_markdown(notebook, docs_dir):
            failed_notebooks.append(notebook.name)
            continue

        success_count += 1

    # Print summary
    print("\n" + "=" * 60)
    print(f"Summary: {success_count}/{len(notebooks)} notebooks processed successfully")

    if failed_notebooks:
        print("\nFailed notebooks:")
        for nb in failed_notebooks:
            print(f"  - {nb}")
        return 1

    print("\n✓ All notebooks executed and converted successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
