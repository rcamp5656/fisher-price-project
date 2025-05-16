from pathlib import Path

# Project folder constants
PROJECT_ROOT = Path(__file__).parent.parent
MIDI_FOLDER = PROJECT_ROOT / "MIDI"
CONVERTED_FOLDER = PROJECT_ROOT / "Converted"

# Re-export common playback and navigation utilities
from .midi_utils import (
    play_midi_file,
    stop_all_midi,
    pause_midi,
    resume_midi,
    make_nav,
)

__all__ = [
    "MIDI_FOLDER",
    "CONVERTED_FOLDER",
    "play_midi_file",
    "stop_all_midi",
    "pause_midi",
    "resume_midi",
    "make_nav",
]
