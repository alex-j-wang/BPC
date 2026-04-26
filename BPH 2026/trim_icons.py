import sys
from pathlib import Path
from PIL import Image
import json

import re

def parse_keys_from_data_tsx(folder: Path):
    data_file = folder / ".." / "data.tsx"
    lines = data_file.read_text().splitlines()

    keys = []
    in_icons = False
    brace_depth = 0

    for line in lines:
        stripped = line.strip()

        # find start
        if not in_icons and stripped.startswith("export const icons"):
            in_icons = True
            brace_depth = stripped.count("{") - stripped.count("}")
            continue

        if not in_icons:
            continue

        # track braces
        brace_depth += line.count("{") - line.count("}")

        # stop when leaving icons object
        if brace_depth <= 0:
            break

        # detect key line by indentation (2 spaces) + colon
        # matches:   key: {   OR   "key": {
        m = re.match(r'^\s{2}["\']?([^"\']+)["\']?\s*:\s*{', line)
        if m:
            keys.append(m.group(1))

    return keys

def process_image(image_path, output_folder, canvas_width, canvas_height):
    img = Image.open(image_path).convert("RGBA")

    if img.size != (canvas_width, canvas_height):
        raise ValueError(
            f"{image_path.name} has size {img.size}, expected {(canvas_width, canvas_height)}"
        )
        
    bbox = img.getbbox()
    if bbox is None:
        return None

    left, top, right, bottom = bbox
    trimmed = img.crop(bbox)

    # save trimmed image
    output_path = output_folder / image_path.name
    trimmed.save(output_path)

    # compute percentages
    x_pct = left / canvas_width * 100
    y_pct = top / canvas_height * 100
    w_pct = trimmed.width / canvas_width * 100
    h_pct = trimmed.height / canvas_height * 100

    return {
        "icon": image_path.name.rsplit(".", 1)[0],
        "x": round(x_pct, 4),
        "y": round(y_pct, 4),
        "w": round(w_pct, 4),
        "h": round(h_pct, 4),
    }


def main(input_folder, output_folder):
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    # determine canvas size from first image
    first = next(input_folder.glob("*.png"))
    with Image.open(first) as img:
        canvas_width, canvas_height = img.size

    # parse keys from data.tsx
    keys = parse_keys_from_data_tsx(input_folder)

    pngs = sorted(input_folder.glob("*.png"))
    if len(keys) != len(pngs):
        raise ValueError(
            f"Key count ({len(keys)}) != image count ({len(pngs)})"
        )

    results = {}

    for png, key in zip(pngs, keys):
        result = process_image(
            png, output_folder, canvas_width, canvas_height
        )
        results[key] = result

    # print TypeScript-ready output
    for v in results.values():
        print(f'import {v["icon"]} from "./icons/{v["icon"]}.png";')
    print()
    print("export const icons: Record<string, PuzzleIcon> = {")
    for k, v in results.items():
        print(
            f'  "{k}": {{ icon: {v["icon"]}, x: {v["x"]}, y: {v["y"]}, w: {v["w"]}, h: {v["h"]} }},'
        )
    print("};")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python trim_icons.py input_folder")
        sys.exit(1)

    main(sys.argv[1], sys.argv[1])