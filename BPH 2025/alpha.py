import os
import re
from pathlib import Path
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

# Directory to scan
INPUT_DIR = "/Users/alexwang/Desktop/College/Clubs/BPC/2025-bph-site/public/map/layout"
OUTPUT_DIR = "transparent"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Regex pattern: matches ????1?.png
pattern = re.compile(r"^.{4}1.\.png$")

def process_image(file_path):
    try:
        with Image.open(file_path).convert("RGBA") as img:
            pixels = img.getdata()
            new_pixels = [(r, g, b, 0) if a < 10 else (r, g, b, a) for (r, g, b, a) in pixels]
            img.putdata(new_pixels)

            output_path = Path(OUTPUT_DIR) / Path(file_path).name
            img.save(output_path, "PNG")
            print(f"Processed: {output_path.name}")
    except Exception as e:
        print(f"Failed: {file_path} -> {e}")

def main():
    files = [str(Path(INPUT_DIR) / f)
             for f in os.listdir(INPUT_DIR)
             if pattern.match(f) and f.endswith(".png")]

    print(f"Found {len(files)} matching files.")

    with ThreadPoolExecutor() as executor:
        executor.map(process_image, files)

if __name__ == "__main__":
    main()