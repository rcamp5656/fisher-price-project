import os
import mido
import time
import pygame
from mido import MidiFile
from common import convert_to_fisher_price_chord, FISHER_PRICE_RANGE

# Initialize Pygame for sound playback
pygame.init()
pygame.mixer.init()

# Load .wav samples for Fisher-Price notes (60–74)
SAMPLE_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'samples')
SAMPLES = {}

for note in FISHER_PRICE_RANGE:
    filename = f"{note}.wav"
    path = os.path.join(SAMPLE_FOLDER, filename)
    if os.path.exists(path):
        SAMPLES[note] = pygame.mixer.Sound(path)
    else:
        print(f"[WARNING] Missing sample: {filename}")

def play_sample(note):
    """Play a single .wav sample corresponding to a Fisher-Price note."""
    if note in SAMPLES:
        SAMPLES[note].play()
    else:
        print(f"[WARN] Sample for note {note} not loaded.")

def play_midi_notes(path):
    """Play a MIDI file using Fisher-Price note samples."""
    mid = MidiFile(path)
    tempo = 500000  # default MIDI tempo (120 BPM)
    ticks_per_beat = mid.ticks_per_beat

    for msg in mid:
        time.sleep(mido.tick2second(msg.time, ticks_per_beat, tempo))

        if msg.type == 'set_tempo':
            tempo = msg.tempo

        elif msg.type == 'note_on' and msg.velocity > 0:
            for n in convert_to_fisher_price_chord(msg.note):
                play_sample(n)

# Optional: keep chunking/conversion functions here as well if needed
# ---------------------------------------------------------------------------
# Pause / Resume helpers
# ---------------------------------------------------------------------------

# These are minimal placeholders so the rest of the program can import them.
# Right now “pause” is implemented as a full stop; “resume” does nothing.
# We’ll flesh out true pause-and-continue behaviour in a later step.

def pause_midi():
    """
    Temporarily stop playback.

    Current implementation: just call stop_all_midi().
    A future enhancement will cache the playback position so we can resume.
    """
    stop_all_midi()


def resume_midi():
    """
    Resume playback after pause_midi().

    Placeholder: no-op for now.  Will be replaced with real resume logic.
    """
    pass
