
# midi_input.py

import mido

def get_axiom_input_port():
    """
    Opens only the Axiom 25 internal MIDI input.
    """
    try:
        port = mido.open_input('Axiom 25 MIDI In 0')
        print("Input port: Axiom 25 MIDI In 0 (internal keys only)")
        return port
    except IOError as e:
        print("[ERROR] Could not open Axiom 25 MIDI In 0:", e)
        return None
