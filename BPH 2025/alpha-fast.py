import os
import re
from pathlib import Path
from PIL import Image
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# Set your folders
INPUT_DIR = "/Users/alexwang/Downloads/input"
OUTPUT_DIR = "/Users/alexwang/Downloads/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_image_numpy(file_path):
    try:
        with Image.open(file_path).convert("RGBA") as img:
            arr = np.array(img)

            # Zero alpha where a < 32
            mask = arr[:, :, 3] < 32
            arr[mask, 3] = 0

            # Convert back to image
            cleaned_img = Image.fromarray(arr, "RGBA")
            output_path = Path(OUTPUT_DIR) / Path(file_path).name
            cleaned_img.save(output_path)
            print(f"Processed: {output_path.name}")
    except Exception as e:
        print(f"Failed: {file_path} -> {e}")

def main():
    files = [str(Path(INPUT_DIR) / f)
             for f in os.listdir(INPUT_DIR)
             if f.endswith(".png")]

    print(f"Found {len(files)} matching files.")

    with ThreadPoolExecutor() as executor:
        executor.map(process_image_numpy, files)

if __name__ == "__main__":
    main()