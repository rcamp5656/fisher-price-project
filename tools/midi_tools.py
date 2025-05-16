# tools/midi_utils.py

FISHER_PRICE_RANGE = list(range(60, 75))  # C4 (60) to D#5 (74), 15 notes total

def closest_fisher_price_note(note):
    """Map any MIDI note to the nearest Fisher-Price-compatible note."""
    return min(FISHER_PRICE_RANGE, key=lambda x: abs(x - note))

def convert_to_fisher_price_chord(note):
    """Simulate major/minor triad chords constrained to the Fisher-Price range."""
    root = closest_fisher_price_note(note)
    major_third = closest_fisher_price_note(root + 4)
    perfect_fifth = closest_fisher_price_note(root + 7)
    return sorted({root, major_third, perfect_fifth})

def is_note_in_fisher_price_range(note):
    return 60 <= note <= 74
