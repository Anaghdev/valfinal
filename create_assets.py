from PIL import Image
import os

def create_image(filename, color):
    img = Image.new('RGB', (200, 200), color=color)
    img.save(filename)
    print(f"Created {filename}")

def create_dummy_audio(filename):
    # minimal valid mp3 frame (silent) or just bytes if we assume resilient browser handling, 
    # but let's just make a text file to avoid binary complexity if the browser just needs proper mime type to try loading.
    # Actually, let's just write some bytes.
    with open(filename, "wb") as f:
        f.write(b'\xFF\xE3\x18\xC4\x00\x00\x00\x03\x48\x00\x00\x00\x00\x4C\x41\x4D\x45\x33\x2E\x39\x39\x2E\x35') 
    print(f"Created {filename}")

if __name__ == "__main__":
    try:
        create_image("photo1.jpg", "pink")
        create_image("photo2.jpg", "red")
        create_image("photo3.jpg", "magenta")
        
        if not os.path.exists("love.mp3"):
            create_dummy_audio("love.mp3")
            
        print("Assets creation complete.")
    except Exception as e:
        print(f"Error: {e}")
