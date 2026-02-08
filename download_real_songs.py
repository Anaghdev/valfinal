import requests
import os

# Mapping of file names to direct download URLs
songs = {
    "rose_song.mp3": "https://upload.wikimedia.org/wikipedia/commons/2/2a/Gymnopedie_No._1_%28ISRC_USUAN1100787%29.mp3",
    "propose_song.mp3": "https://upload.wikimedia.org/wikipedia/commons/8/82/Nocturne_in_E_flat_major%2C_Op._9_no._2.mp3",
    "chocolate_song.mp3": "https://upload.wikimedia.org/wikipedia/commons/1/13/Dance_of_the_Sugar_Plum_Fairies_%28ISRC_USUAN1100270%29.mp3",
    "teddy_song.ogg": "https://upload.wikimedia.org/wikipedia/commons/8/87/Brahms_-_Schumann-Heink_-_Wiegenlied_%28Berceuse%29_%281915%29.ogg",
    "promise_song.ogg": "https://upload.wikimedia.org/wikipedia/commons/5/59/Kevin_MacLeod_-_Canon_in_D_Major.ogg",
    "hug_song.ogg": "https://upload.wikimedia.org/wikipedia/commons/d/d8/Saint-Saens_-_The_Carnival_of_the_Animals_-_13_Le_cygne.ogg",
    "kiss_song.ogg": "https://upload.wikimedia.org/wikipedia/commons/0/02/Franz_Liszt_-_Liebestraum%2C_Ab_Major.ogg",
    "valentine_song.ogg": "https://upload.wikimedia.org/wikipedia/commons/b/be/Clair_de_lune_%28Claude_Debussy%29_Suite_bergamasque.ogg"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def download_file(url, filename):
    print(f"Downloading {filename}...")
    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"[OK] Saved {filename}")
    except Exception as e:
        print(f"[ERROR] Failed to download {filename}: {e}")

if __name__ == "__main__":
    print("Starting download of Real Songs...")
    for filename, url in songs.items():
        # Remove existing wav placeholder if it exists to avoid confusion, 
        # though app.py will prioritize mp3/ogg if updated correctly.
        wav_name = filename.replace(".mp3", ".wav").replace(".ogg", ".wav")
        if os.path.exists(wav_name):
            try:
                os.remove(wav_name)
                print(f"🗑️ Removed placeholder {wav_name}")
            except:
                pass
        
        download_file(url, filename)
    print("Download complete!")
