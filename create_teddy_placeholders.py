from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder(filename, text, color):
    img = Image.new('RGB', (800, 800), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    # Draw simple bear shape (circle)
    d.ellipse([200, 200, 600, 600], fill=color, outline="black")
    
    # Add text
    try:
        # Use a default font
        font = ImageFont.load_default()
        # Scale isn't possible with load_default, so just draw text
        d.text((300, 400), text, fill="black")
    except:
        pass

    # Save
    img.save(filename)
    print(f"Created {filename}")

bear_map = {
    "teddy_brown_bow.png": ("Brown Bear + Bow", "#8B4513"),
    "teddy_brown_shades.png": ("Brown Bear + Shades", "#8B4513"),
    "teddy_brown_letter.png": ("Brown Bear + Letter", "#8B4513"),
    "teddy_white_bow.png": ("Polar Bear + Bow", "#F0F8FF"),
    "teddy_white_shades.png": ("Polar Bear + Shades", "#F0F8FF"),
    "teddy_white_letter.png": ("Polar Bear + Letter", "#F0F8FF"),
    "teddy_panda_bow.png": ("Panda + Bow", "#FFFFFF"),
    "teddy_panda_shades.png": ("Panda + Shades", "#FFFFFF"),
    "teddy_panda_letter.png": ("Panda + Letter", "#FFFFFF"),
}

if __name__ == "__main__":
    for filename, (text, color) in bear_map.items():
        if not os.path.exists(filename):
            create_placeholder(filename, text, color)
        else:
            print(f"Skipping {filename} (already exists)")
