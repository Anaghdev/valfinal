import wave
import math
import struct
import os

def create_melody(filename, notes, tempo=120):
    """
    Creates a .wav file from a list of notes.
    notes: list of (frequency, duration_in_beats) tuples.
    tempo: beats per minute.
    """
    sample_rate = 44100
    beat_duration = 60.0 / tempo
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wav_file.setframerate(sample_rate)
        
        for freq, beats in notes:
            # duration of this note in seconds
            duration = beats * beat_duration
            n_samples = int(sample_rate * duration)
            
            # envelope (attack and decay to avoid clicking)
            attack_samples = int(sample_rate * 0.05) # 50ms attack
            decay_samples = int(sample_rate * 0.05)  # 50ms decay
            
            for i in range(n_samples):
                t = i / sample_rate
                
                # Simple envelope to make it sound less harsh
                envelope = 1.0
                if i < attack_samples:
                    envelope = i / attack_samples
                elif i > n_samples - decay_samples:
                    envelope = (n_samples - i) / decay_samples
                
                # Generate wave (combining sine and triangle for a "chiptune" feel)
                if freq > 0:
                    # Sine
                    val_sin = math.sin(2.0 * math.pi * freq * t)
                    # Triangle-ish approximation
                    val_tri = 2.0 * abs(2.0 * ((freq * t) % 1.0) - 1.0) - 1.0
                    
                    # Mix them
                    sample_val = 0.7 * val_sin + 0.3 * val_tri
                    
                    # Apply envelope and volume
                    value = int(32767.0 * 0.5 * envelope * sample_val)
                else:
                    value = 0 # Rest
                
                data = struct.pack('<h', value)
                wav_file.writeframes(data)
    
    print(f"Generated {filename}")

# Note Frequencies
C4 = 261.63; D4 = 293.66; E4 = 329.63; F4 = 349.23; G4 = 392.00; A4 = 440.00; B4 = 493.88
C5 = 523.25; D5 = 587.33; E5 = 659.25; F5 = 698.46; G5 = 783.99; A5 = 880.00; B5 = 987.77
C6 = 1046.50
REST = 0

# Define Melodies (Song Placeholders)
# Rose Day: Gentle, rising melody
rose_melody = [
    (C4, 1), (E4, 1), (G4, 1), (C5, 2), 
    (B4, 1), (G4, 1), (E4, 1), (C4, 2)
]

# Propose Day: Fanfare-ish
propose_melody = [
    (C4, 0.5), (C4, 0.5), (C4, 0.5), (G4, 2),
    (E4, 0.5), (E4, 0.5), (C5, 2)
]

# Chocolate Day: Playful, bouncy
chocolate_melody = [
    (C5, 0.5), (E5, 0.5), (G5, 0.5), (C6, 0.5),
    (G5, 0.5), (E5, 0.5), (C5, 1)
]

# Teddy Day: Lullaby-ish
teddy_melody = [
    (E4, 1), (G4, 1), (G4, 2),
    (E4, 1), (G4, 1), (G4, 2),
    (E4, 1), (G4, 1), (C5, 1), (B4, 1), (A4, 1), (G4, 1), (F4, 2)
]

# Promise Day: Steady, anthem-like
promise_melody = [
    (C4, 1), (C4, 1), (D4, 1), (E4, 1),
    (F4, 2), (E4, 2),
    (D4, 2), (C4, 2)
]

# Hug Day: Warm, ascending
hug_melody = [
    (C4, 1), (E4, 1), (A4, 2),
    (D4, 1), (F4, 1), (B4, 2),
    (E4, 1), (G4, 1), (C5, 4)
]

# Define helper for high notes since they weren't in the list above
E6 = 1318.51; G6 = 1567.98

# Kiss Day: Quick, high pitched
kiss_melody = [
    (C6, 0.25), (E6, 0.25), (G6, 0.5), (REST, 0.5),
    (C6, 0.25), (E6, 0.25), (G6, 0.5)
]

kill_melody_updated = [
     (C6, 0.25), (E6, 0.25), (G6, 0.5), (REST, 0.5),
     (C6, 0.25), (E6, 0.25), (G6, 0.5)
]


# Valentine's Day: Classic romantic phrase
valentine_melody = [
    (C4, 1), (D4, 1), (E4, 1), (F4, 1),
    (G4, 2), (G4, 2),
    (A4, 1), (B4, 1), (C5, 4)
]

# Voice Notes (Simulated speech patterns - randomized slightly human feel)
def generate_speech_pattern(base_freq):
    return [
        (base_freq, 0.2), (base_freq * 1.05, 0.2), (base_freq * 0.95, 0.2),
        (base_freq, 0.4), (REST, 0.2),
        (base_freq * 0.9, 0.2), (base_freq * 1.1, 0.4)
    ]

songs = {
    "rose_song.wav": rose_melody,
    "propose_song.wav": propose_melody,
    "chocolate_song.wav": chocolate_melody,
    "teddy_song.wav": teddy_melody,
    "promise_song.wav": promise_melody,
    "hug_song.wav": hug_melody,
    "kiss_song.wav": kill_melody_updated,
    "valentine_song.wav": valentine_melody
}

voice_notes = {
    "rose_note.wav": generate_speech_pattern(440),
    "propose_note.wav": generate_speech_pattern(440),
    "chocolate_note.wav": generate_speech_pattern(500),
    "teddy_note.wav": generate_speech_pattern(350),
    "promise_note.wav": generate_speech_pattern(400),
    "hug_note.wav": generate_speech_pattern(440),
    "kiss_note.wav": generate_speech_pattern(600),
    "valentine_note.wav": generate_speech_pattern(440),
}


if __name__ == "__main__":
    print("Generating Melodies...")
    
    # Generate Songs
    for filename, melody in songs.items():
        create_melody(filename, melody, tempo=140)
        
    # Generate Voice Notes
    for filename, melody in voice_notes.items():
        create_melody(filename, melody, tempo=180)
        
    print("All audio files generated!")
