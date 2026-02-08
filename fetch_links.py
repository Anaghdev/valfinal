import requests
import re

pages = {
    "Rose": "https://commons.wikimedia.org/wiki/File:Gymnopedie_No._1_(ISRC_USUAN1100787).mp3",
    "Propose": "https://commons.wikimedia.org/wiki/File:Nocturne_in_E_flat_major,_Op._9_no._2.mp3",
    "Chocolate": "https://commons.wikimedia.org/wiki/File:Dance_of_the_Sugar_Plum_Fairies_(ISRC_USUAN1100270).oga",
    "Teddy": "https://commons.wikimedia.org/wiki/File:Brahms_-_Schumann-Heink_-_Wiegenlied_(Berceuse)_(1915).ogg",
    "Promise": "https://commons.wikimedia.org/wiki/File:Kevin_MacLeod_-_Canon_in_D_Major.ogg",
    "Hug": "https://commons.wikimedia.org/wiki/File:Saint-Saens_-_The_Carnival_of_the_Animals_-_13_Le_cygne.ogg",
    "Kiss": "https://commons.wikimedia.org/wiki/File:Franz_Liszt_-_Liebestraum,_Ab_Major.ogg",
    "Valentine": "https://commons.wikimedia.org/wiki/File:Clair_de_lune_(Claude_Debussy)_Suite_bergamasque.ogg"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for name, url in pages.items():
    print(f"Fetching {name}...")
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Simple regex to find the original upload link
            # Look for href="//upload.wikimedia.org/wikipedia/commons/..."
            # Adjust pattern to match what's usually in the "Original file" or "Full resolution" link
            
            # Pattern for MP3 or OGG file
            match = re.search(r'//upload\.wikimedia\.org/wikipedia/commons/[a-f0-9]/[a-f0-9]{2}/[^"]+\.(?:mp3|ogg)', response.text)
            if match:
                link = "https:" + match.group(0)
                print(f"FOUND {name}: {link}")
            else:
                print(f"NO MATCH for {name}")
                # debug: print snippet
                # print(response.text[:1000])
        else:
            print(f"Error {response.status_code} for {url}")
    except Exception as e:
        print(f"Exception for {name}: {e}")
