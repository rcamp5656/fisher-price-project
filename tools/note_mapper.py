# note_mapper.py
"""
Map raw MIDI notes into the Fisher-Price 15-note range and provide human-readable names.
"""
FP_MIN = 60  # C4
FP_MAX = 74  # D5

NOTE_NAMES = {
    60: "C4", 61: "C#4", 62: "D4", 63: "D#4", 64: "E4",
    65: "F4", 66: "F#4", 67: "G4", 68: "G#4", 69: "A4",
    70: "A#4", 71: "B4", 72: "C5", 73: "C#5", 74: "D5"
}


def map_to_fisher_price(note: int) -> int:
    """Clamp any note into the Fisher-Price playable range."""
    return max(FP_MIN, min(FP_MAX, note))


def note_name(note: int) -> str:
    """Return a readable name for a mapped note (e.g., 'C4')."""
    return NOTE_NAMES.get(note, str(note))
