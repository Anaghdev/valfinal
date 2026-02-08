import wave
import math
import struct
import os

def create_tone(filename, duration=3, frequency=440.0):
    """Creates a simple sine wave tone and saves it as a .wav file."""
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wav_file.setframerate(sample_rate)
        
        for i in range(n_samples):
            # Generate sine wave
            value = int(32767.0 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
            data = struct.pack('<h', value)
            wav_file.writeframes(data)
    
    print(f"Created {filename}")

# List of expected audio files (songs and voice notes)
# We use .wav for placeholders to avoid external dependencies like ffmpeg/lame
audio_files = [
    # Songs / Background Music
    ("rose_song.wav", 440),     # A4
    ("propose_song.wav", 494),  # B4
    ("chocolate_song.wav", 523),# C5
    ("teddy_song.wav", 587),    # D5
    ("promise_song.wav", 659),  # E5
    ("hug_song.wav", 698),      # F5
    ("kiss_song.wav", 784),     # G5
    ("valentine_song.wav", 880),# A5
    
    # Voice Notes
    ("rose_note.wav", 440),
    ("propose_note.wav", 494),
    ("chocolate_note.wav", 523),
    ("teddy_note.wav", 587),
    ("promise_note.wav", 659),
    ("hug_note.wav", 698),
    ("kiss_note.wav", 784),
    ("valentine_note.wav", 880),
]

if __name__ == "__main__":
    for filename, freq in audio_files:
        if not os.path.exists(filename) and not os.path.exists(filename.replace(".wav", ".mp3")):
            create_tone(filename, duration=2, frequency=freq)
        else:
            print(f"Skipping {filename} (already exists as wav or mp3)")
