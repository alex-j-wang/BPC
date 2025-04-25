import os
from PIL import Image

def list_png_dimensions(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.png'):
            filepath = os.path.join(folder_path, filename)
            try:
                with Image.open(filepath) as img:
                    width, height = img.size
                    print(f"{filename}: {width}x{height}")
            except Exception as e:
                print(f"Failed to open {filename}: {e}")

# 🔧 Replace with your folder path
folder = "/Users/alexwang/Desktop/College/Clubs/BPC/2025-bph-site/public/map/sprites-finalized"
list_png_dimensions(folder)