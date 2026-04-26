import sys
import random
from pathlib import Path
from PIL import Image, ImageDraw


def generate_placeholders(folder_name):
    folder = Path(folder_name)
    base_image_path = folder / f"{folder.name}.png"
    icons_folder = folder / "icons"

    icons_folder.mkdir(parents=True, exist_ok=True)

    # read base image size
    with Image.open(base_image_path) as img:
        width, height = img.size

    # grid to distribute rectangles
    cols = 3
    rows = 2
    cells = [(c, r) for r in range(rows) for c in range(cols)]
    random.shuffle(cells)

    for i in range(5):
        canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        col, row = cells[i]

        cell_w = width // cols
        cell_h = height // rows

        # rectangle size (random but reasonable)
        rect_w = cell_w // 2
        rect_h = cell_h // 4

        # position within cell
        x0 = col * cell_w + random.randint(0, cell_w - rect_w)
        y0 = row * cell_h + random.randint(0, cell_h - rect_h)

        x1 = x0 + rect_w
        y1 = y0 + rect_h

        # red rectangle
        draw.rectangle([x0, y0, x1, y1], fill=(255, 0, 0, 255))

        output_path = icons_folder / f"placeholder{i+1}.png"
        canvas.save(output_path)

        print(f"Created {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_placeholders.py folder_name")
        sys.exit(1)

    generate_placeholders(sys.argv[1])