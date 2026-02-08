from gtts import gTTS
import os

# Romantic Messages for each day
messages = {
    "rose_note.mp3": "Happy Rose Day! I’m sending you this virtual rose to let you know that you are the most beautiful flower in the garden of my life. I love you!",
    
    "propose_note.mp3": "Happy Propose Day! Today, I want to ask you the most important question. Will you walk this path of life with me, forever and always?",
    
    "chocolate_note.mp3": "Happy Chocolate Day! You are sweeter than the finest chocolate, and my life is delicious because you are in it.",
    
    "teddy_note.mp3": "Happy Teddy Day! Sending you this beary big hug to remind you that I'm always here for you, soft and warm like a teddy bear.",
    
    "promise_note.mp3": "Happy Promise Day! I promise to stand by your side, to listen, to care, and to love you more with every passing day.",
    
    "hug_note.mp3": "Happy Hug Day! If I could, I would wrap you in my arms right now and never let go. Consider this message a giant virtual hug!",
    
    "kiss_note.mp3": "Happy Kiss Day! Sending you a thousand kisses to brighten your day. Mwah!",
    
    "valentine_note.mp3": "Happy Valentine's Day, my love! You are my everything, my today, and all of my tomorrows. I love you more than words can say."
}

def create_voice_note(filename, text):
    print(f"Generating {filename}...")
    try:
        # Generate TTS audio
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Save to file
        tts.save(filename)
        print(f"[OK] Saved {filename}")
        
    except Exception as e:
        print(f"[ERROR] Failed to generate {filename}: {e}")

if __name__ == "__main__":
    print("Starting generation of Voice Notes...")
    
    for filename, message in messages.items():
        # Clean up old placeholders if they exist (optional, but good for cleanliness)
        wav_name = filename.replace(".mp3", ".wav")
        if os.path.exists(wav_name):
            try:
                os.remove(wav_name)
                print(f"Removed placeholder {wav_name}")
            except:
                pass
                
        create_voice_note(filename, message)
        
    print("Voice Note generation complete!")
