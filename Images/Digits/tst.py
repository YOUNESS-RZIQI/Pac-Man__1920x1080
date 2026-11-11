"""Convert every .xpm image of a directory to a 1920x1080 .png."""

import sys
from pathlib import Path
from typing import Tuple

from PIL import Image

TARGET_SIZE: Tuple[int, int] = (40, 40)


def convert_xpm_to_png(xpm_path: Path, png_path: Path,
                       size: Tuple[int, int] = TARGET_SIZE) -> None:
    """Convert one XPM image to a PNG of the given size.

    Args:
        xpm_path: The path of the source .xpm file.
        png_path: The path of the .png file to create.
        size: The (width, height) of the output image.
    """

    with Image.open(xpm_path) as img:
        rgba: Image.Image = img.convert("RGBA")
        resized: Image.Image = rgba.resize(size, Image.Resampling.LANCZOS)
        resized.save(png_path, format="PNG", optimize=False)


def convert_directory(directory: Path, recursive: bool = False) -> None:
    """Convert all the .xpm files of a directory that have no .png yet.

    Args:
        directory: The directory to scan.
        recursive: If True, also scan the sub-directories.
    """

    pattern: str = "**/*.xpm" if recursive else "*.xpm"

    for xpm_path in sorted(directory.glob(pattern)):
        png_path: Path = xpm_path.with_suffix(".png")

        if png_path.exists():
            print(f"Skip (png exists): {xpm_path.name}")
            continue

        try:
            convert_xpm_to_png(xpm_path, png_path)
            print(f"Converted: {xpm_path.name} -> {png_path.name}")
        except Exception as e:
            print(f"Failed: {xpm_path.name} ({e})")


if __name__ == "__main__":
    target_dir: Path = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    convert_directory(target_dir)