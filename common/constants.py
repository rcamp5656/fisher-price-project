import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIDI_FOLDER = os.path.join(ROOT_DIR, "MIDI")
CONVERTED_FOLDER = os.path.join(ROOT_DIR, "Converted")
LIVE_MIDI_FILE = os.path.join(ROOT_DIR, "live.mid")
