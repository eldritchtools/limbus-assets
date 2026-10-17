from pathlib import Path
from PIL import Image

INPUT_DIR = Path("temp")
OUTPUT_DIR = Path("output")
MAX_WIDTH = 400
MAX_HEIGHT = 400

SUPPORTED_FORMATS = {".png", ".webp", ".jpg", ".jpeg"}

for path in INPUT_DIR.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in SUPPORTED_FORMATS:
        continue

    relative_path = path.relative_to(INPUT_DIR)
    output_path = OUTPUT_DIR / relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(path) as image:
        width, height = image.size

        # Only downsize images that exceed the bounding box.
        if width > MAX_WIDTH or height > MAX_HEIGHT:
            image.thumbnail(
                (MAX_WIDTH, MAX_HEIGHT),
                Image.Resampling.LANCZOS
            )

        # Preserve the original format and transparency.
        output_path.parent.mkdir(parents=True, exist_ok=True)

        save_options = {}
        if image.format == "PNG":
            save_options["optimize"] = True
        elif image.format == "WEBP":
            save_options["quality"] = 90
        elif image.format in ("JPEG", "JPG"):
            save_options["quality"] = 90
            save_options["optimize"] = True

        image.save(output_path, **save_options)

    print(f"Processed: {relative_path}")

print("Done!")
