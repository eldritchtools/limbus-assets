from pathlib import Path
from PIL import Image

INPUT = Path("temp")
OUTPUT = Path("output")  # or the final assets folder

for png in INPUT.rglob("*.png"):
    rel = png.relative_to(INPUT)
    output = OUTPUT / rel

    output.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(png) as img:
        r, g, b, a = img.convert("RGBA").split()
        swapped = Image.merge("RGBA", (b, g, r, a))
        swapped.save(output, "PNG")

    print(f"Swapped {png} -> {output}")