
# playback_live.py

import mido
import time
import os
from midi_output import get_yamaha_output_port

def find_latest_live_file():
    folder = os.path.join("Converted", "Live")
    if not os.path.exists(folder):
        print("Live folder not found.")
        return None

    midis = [f for f in os.listdir(folder) if f.lower().endswith('.mid')]
    if not midis:
        print("No live MIDI files found.")
        return None

    midis.sort(reverse=True)
    return os.path.join(folder, midis[0])

def play_latest_live_file():
    output_port = get_yamaha_output_port()
    if output_port is None:
        print("Cannot open output port for Yamaha.")
        return

    midi_path = find_latest_live_file()
    if not midi_path:
        return

    print(f"Playing back: {midi_path}")
    mid = mido.MidiFile(midi_path)

    for msg in mid.play():
        if not msg.is_meta:
            output_port.send(msg)

    print("Playback complete.")
