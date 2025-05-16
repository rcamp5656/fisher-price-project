
# midi_output.py

import mido

def get_yamaha_output_port():
    """
    Opens Axiom 25 MIDI Out 1 to route MIDI to external Yamaha device via DIN.
    """
    try:
        port = mido.open_output('Axiom 25 MIDI Out 1')
        print("Output port: Axiom 25 MIDI Out 1 (Yamaha via DIN)")
        return port
    except IOError as e:
        print("[ERROR] Could not open Axiom 25 MIDI Out 1:", e)
        return None
