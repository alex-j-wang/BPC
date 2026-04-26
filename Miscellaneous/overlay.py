from PIL import Image

def overlay_pngs(bottom_path, top_path, output_path):
    # Open images in RGBA mode (preserves transparency)
    bottom = Image.open(bottom_path).convert("RGBA")
    top = Image.open(top_path).convert("RGBA")

    # Ensure they are the same size (optional if you already guarantee it)
    if bottom.size != top.size:
        raise ValueError("Images must be the same size!")

    # Overlay: top image drawn over bottom
    combined = Image.alpha_composite(bottom, top)

    # Save the result
    combined.save(output_path, format="PNG")

    print(f"Output saved to {output_path}")

# Example usage
overlay_pngs("menu_star_1.png", "menu_star_1.png", "menu_star_1.png")
