import numpy as np
import os
from scipy.io.wavfile import write

SAMPLE_RATE = 44100  # CD-quality
DURATION = 0.4       # seconds (short plink)
AMPLITUDE = 0.3      # base volume (0.0–1.0)
DECAY = 5.0          # exponential decay rate

FISHER_PRICE_RANGE = list(range(60, 75))  # MIDI 60 to 74

def midi_to_freq(note):
    """Convert MIDI note number to frequency in Hz."""
    return 440.0 * (2 ** ((note - 69) / 12.0))

def generate_plink(freq, duration, sample_rate, amp, decay):
    """Generate a decaying sine wave with light overtones (toy-like)."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    waveform = (
        amp * np.sin(2 * np.pi * freq * t) +
        (amp * 0.2) * np.sin(4 * np.pi * freq * t)
    ) * np.exp(-decay * t)
    return np.int16(waveform / np.max(np.abs(waveform)) * 32767)

def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    out_folder = "samples"
    ensure_folder(out_folder)

    for note in FISHER_PRICE_RANGE:
        freq = midi_to_freq(note)
        wave = generate_plink(freq, DURATION, SAMPLE_RATE, AMPLITUDE, DECAY)
        out_path = os.path.join(out_folder, f"{note}.wav")
        write(out_path, SAMPLE_RATE, wave)
        print(f"Saved: {out_path}")

if __name__ == "__main__":
    main()
