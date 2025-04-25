from PIL import Image

def create_transparent_image(width, height, output_path):
    # Create an RGBA image with full transparency (alpha = 0)
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    img.save(output_path, "PNG")
    print(f"Saved transparent image: {output_path}")

# Example usage
create_transparent_image(400, 1150, "/Users/alexwang/Desktop/College/Clubs/BPC/2025-bph-site/public/map/sprites-finalized/drop-the.png")
create_transparent_image(800, 800, "/Users/alexwang/Desktop/College/Clubs/BPC/2025-bph-site/public/map/sprites-finalized/aha-erlebnis.png")
create_transparent_image(700, 700, "/Users/alexwang/Desktop/College/Clubs/BPC/2025-bph-site/public/map/sprites-finalized/balloon-animals.png")
create_transparent_image(650, 650, "/Users/alexwang/Desktop/College/Clubs/BPC/2025-bph-site/public/map/sprites-finalized/boring-plot.png")
create_transparent_image(450, 750, "/Users/alexwang/Desktop/College/Clubs/BPC/2025-bph-site/public/map/sprites-finalized/six-degrees.png")
create_transparent_image(750, 850, "/Users/alexwang/Desktop/College/Clubs/BPC/2025-bph-site/public/map/sprites-finalized/cutting-room-floor.png")