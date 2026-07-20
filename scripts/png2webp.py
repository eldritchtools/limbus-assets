from pathlib import Path
from PIL import Image

INPUT = Path("temp")
OUTPUT = Path("output")  # or the final assets folder

QUALITY = 90

for png in INPUT.rglob("*.png"):
    rel = png.relative_to(INPUT)
    webp = OUTPUT / rel.with_suffix(".webp")

    webp.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(png) as img:
        img.save(
            webp,
            "WEBP",
            quality=QUALITY,
            method=6,
        )

    print(f"Converted {png} -> {webp}")