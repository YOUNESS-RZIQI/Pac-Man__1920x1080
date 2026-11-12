"""Resize PNG images of a directory according to their current size."""

import sys
from pathlib import Path
from typing import Dict, Tuple

from PIL import Image

SIZE_MAP: Dict[Tuple[int, int], Tuple[int, int]] = {
    (2020, 1184): (1010, 592),
    (1280, 720): (640, 360),
    (3840, 2080): (1920, 1080),
    (1920, 1080): (960, 540),
}


def resize_png(png_path: Path) -> bool:
    """Resize one PNG if its size is in SIZE_MAP.

    The file is overwritten. Images whose size is not in SIZE_MAP are
    left untouched.

    Args:
        png_path: The path of the .png file.

    Returns:
        True if the image was resized, False otherwise.
    """

    with Image.open(png_path) as img:
        new_size = SIZE_MAP.get(img.size)
        if new_size is None:
            return False

        rgba: Image.Image = img.convert("RGBA")

    resampling = getattr(Image, "Resampling", Image)
    resized: Image.Image = rgba.resize(new_size, resampling.LANCZOS)
    resized.save(png_path, format="PNG")
    return True


def resize_directory(directory: Path, recursive: bool = False) -> None:
    """Resize all the PNG files of a directory that match SIZE_MAP.

    Args:
        directory: The directory to scan.
        recursive: If True, also scan the sub-directories.
    """

    pattern: str = "**/*.png" if recursive else "*.png"

    for png_path in sorted(directory.glob(pattern)):
        try:
            if resize_png(png_path):
                print(f"Resized: {png_path.name}")
            else:
                print(f"Skip (size not in the list): {png_path.name}")
        except Exception as e:
            print(f"Failed: {png_path.name} ({type(e).__name__}: {e})")


if __name__ == "__main__":
    target_dir: Path = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    resize_directory(target_dir)