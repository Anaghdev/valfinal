import os

def create_dummy_video(filename):
    # Minimal MP4 header (ftyp isom) - not a playable video but valid container start
    # Enough to tricker st.video to try loading it (it might show error or black screen, but confirms path finding)
    # A fully valid mp4 is too complex to forge effectively without libraries.
    # We'll just rely on the tip message if it fails, or create a file to trigger the 'exists' check.
    with open(filename, "wb") as f:
        f.write(b'\x00\x00\x00\x18\x66\x74\x79\x70\x69\x73\x6F\x6D\x00\x00\x02\x00\x69\x73\x6F\x6D\x69\x73\x6F\x32\x61\x76\x63\x31')
    print(f"Created dummy video {filename}")

if __name__ == "__main__":
   if not os.path.exists("celebration.mp4"):
       create_dummy_video("celebration.mp4")
