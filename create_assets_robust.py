import os

def create_dummy_image(filename):
    # Create a valid minimal PEG to avoid "broken image" if possible, 
    # but simplest is just some bytes or even a copied valid image if we had one.
    # We will just write bytes. Browser will show broken image icon, which is acceptable for placeholder.
    with open(filename, "wb") as f:
        f.write(b'\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46\x00\x01') # Partial header
    print(f"Created dummy image {filename}")

def create_color_image(filename, color):
    try:
        from PIL import Image
        img = Image.new('RGB', (200, 200), color=color)
        img.save(filename)
        print(f"Created real image {filename}")
    except ImportError:
        create_dummy_image(filename)

def create_dummy_audio(filename):
    # Minimal MP3 header
    with open(filename, "wb") as f:
        f.write(b'\xFF\xE3\x18\xC4\x00\x00\x00\x03\x48\x00\x00\x00\x00\x4C\x41\x4D\x45\x33\x2E\x39\x39\x2E\x35') 
    print(f"Created audio {filename}")

if __name__ == "__main__":
    create_color_image("photo1.jpg", "pink")
    create_color_image("photo2.jpg", "red")
    create_color_image("photo3.jpg", "magenta")
    
    if not os.path.exists("love.mp3"):
        create_dummy_audio("love.mp3")
