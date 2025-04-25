import os
from PIL import Image

INPUT_DIR = "sprites-outlined"         # Change this to your folder
OUTPUT_DIR = "sprites-finalized"       # Optional: set to None to overwrite originals

def crop_to_content(image: Image.Image) -> Image.Image:
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    # Get the alpha channel
    alpha = image.getchannel("A")

    # Find the bounding box of non-transparent pixels
    bbox = alpha.getbbox()
    if not bbox:
        return image  # return original if completely transparent

    # Crop to bounding box
    return image.crop(bbox)

def process_directory(input_dir, output_dir=None):
    os.makedirs(output_dir, exist_ok=True) if output_dir else None

    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(".png"):
            continue

        input_path = os.path.join(input_dir, filename)
        img = Image.open(input_path)
        cropped = crop_to_content(img)

        save_path = (
            os.path.join(output_dir, filename) if output_dir else input_path
        )
        cropped.save(save_path)
        print(f"Processed: {filename}")

if __name__ == "__main__":
    process_directory(INPUT_DIR, OUTPUT_DIR)