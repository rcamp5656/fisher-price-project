import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIDI_FOLDER = os.path.join(ROOT_DIR, 'MIDI')
CONVERTED_FOLDER = os.path.join(ROOT_DIR, 'Converted')
LIVE_FOLDER = os.path.join(CONVERTED_FOLDER, 'Live')
LOG_PATH = os.path.join(ROOT_DIR, 'log.txt')

# Ensure folders exist
os.makedirs(MIDI_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)
os.makedirs(LIVE_FOLDER, exist_ok=True)
