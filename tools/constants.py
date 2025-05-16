# tools/constants.py
import os

# Base directories
script_dir      = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT    = os.path.abspath(os.path.join(script_dir, os.pardir))

# Data folders in your project root
MIDI_FOLDER      = os.path.join(PROJECT_ROOT, 'MIDI')
CONVERTED_FOLDER = os.path.join(PROJECT_ROOT, 'Converted')
LIVE_FOLDER      = os.path.join(PROJECT_ROOT, 'Live')

# Pagination for 7×7 grids
FILES_PER_PAGE = 49

# Ensure data folders exist
for folder in (MIDI_FOLDER, CONVERTED_FOLDER, LIVE_FOLDER):
    os.makedirs(folder, exist_ok=True)
