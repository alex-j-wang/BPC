import sys
from pathlib import Path
from PIL import Image

def overlay_images(base_path, overlays_folder, output_path="output.png"):
    base = Image.open(base_path).convert("RGBA")

    overlay_paths = sorted(Path(overlays_folder).glob("*.png"))

    for overlay_path in overlay_paths:
        overlay = Image.open(overlay_path).convert("RGBA")

        # convert to grayscale while preserving alpha
        overlay = overlay.convert("LA").convert("RGBA")

        if overlay.size != base.size:
            raise ValueError(f"Overlay {overlay_path} has different dimensions than base image")

        base = Image.alpha_composite(base, overlay)

    base.save(output_path)
    print(f"Saved {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python overlay.py base.png overlays_folder [output.png]")
        sys.exit(1)

    base_path = sys.argv[1]
    overlays_folder = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else "output.png"

    overlay_images(base_path, overlays_folder, output_path)