"""Convert every .xpm image of a directory to a .png of a given size."""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

from PIL import Image, ImageColor

TARGET_SIZE: Tuple[int, int] = (60, 60)
RGBA = Tuple[int, int, int, int]


def read_xpm(xpm_path: Path) -> Image.Image:
    """Read an XPM file (any chars-per-pixel) into an RGBA image.

    Rows shorter than expected (for example because trailing spaces were
    stripped) are padded with spaces, which are the transparent pixels.

    Args:
        xpm_path: The path of the .xpm file.

    Returns:
        The image as RGBA, with "None" colors fully transparent.
    """

    text: str = xpm_path.read_text(encoding="latin-1")
    lines: List[str] = re.findall(r'"((?:[^"\\]|\\.)*)"', text)

    width, height, ncolors, cpp = (int(v) for v in lines[0].split()[:4])

    colors: Dict[str, RGBA] = {}
    for line in lines[1:1 + ncolors]:
        key: str = line[:cpp]
        tokens: List[str] = line[cpp:].split()
        value: str = tokens[tokens.index("c") + 1]
        if value.lower() == "none":
            colors[key] = (0, 0, 0, 0)
        elif value.startswith("#"):
            hex_part: str = value[1:]
            step: int = len(hex_part) // 3
            r, g, b = (int(hex_part[i:i + step][:2], 16)
                       for i in range(0, step * 3, step))
            colors[key] = (r, g, b, 255)
        else:
            r, g, b = ImageColor.getrgb(value)[:3]
            colors[key] = (r, g, b, 255)

    transparent: RGBA = colors.get(" " * cpp, (0, 0, 0, 0))

    pixels: List[RGBA] = []
    rows: List[str] = lines[1 + ncolors:1 + ncolors + height]
    for row in rows:
        row = row.ljust(width * cpp)
        for i in range(width):
            pixels.append(
                colors.get(row[i * cpp:(i + 1) * cpp], transparent))

    # If the file has fewer rows than "height", fill the rest transparent.
    missing: int = height - len(rows)
    if missing > 0:
        pixels.extend([transparent] * (missing * width))

    img: Image.Image = Image.new("RGBA", (width, height))
    img.putdata(pixels)
    return img


def convert_xpm_to_png(xpm_path: Path, png_path: Path,
                       size: Tuple[int, int] = TARGET_SIZE) -> None:
    """Convert one XPM image to a PNG of the given size.

    Args:
        xpm_path: The path of the source .xpm file.
        png_path: The path of the .png file to create.
        size: The (width, height) of the output image.
    """

    rgba: Image.Image = read_xpm(xpm_path)
    resampling = getattr(Image, "Resampling", Image)
    resized: Image.Image = rgba.resize(size, resampling.LANCZOS)
    resized.save(png_path, format="PNG", optimize=False)


def convert_directory(directory: Path, recursive: bool = False,
                      extension: str = ".xpm12") -> None:
    """Convert all the XPM files of a directory that have no .png yet.

    Args:
        directory: The directory to scan.
        recursive: If True, also scan the sub-directories.
        extension: The extension of the source files (".xpm" or ".xpm1").
    """

    pattern: str = f"**/*{extension}" if recursive else f"*{extension}"

    for xpm_path in sorted(directory.glob(pattern)):
        png_path: Path = xpm_path.with_suffix(".png")

        if png_path.exists():
            print(f"Skip (png exists): {xpm_path.name}")
            continue

        try:
            convert_xpm_to_png(xpm_path, png_path)
            print(f"Converted: {xpm_path.name} -> {png_path.name}")
        except Exception as e:
            print(f"Failed: {xpm_path.name} ({type(e).__name__}: {e})")


if __name__ == "__main__":
    target_dir: Path = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    convert_directory(target_dir)