
# live_input_handler.py

import mido
import time
from midi_input import get_axiom_input_port
from midi_output import get_yamaha_output_port
import os

def get_timestamped_filename():
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    folder = os.path.join("Converted", "Live")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, f"live_{timestamp}.mid")

def start_live_recording():
    input_port = get_axiom_input_port()
    output_port = get_yamaha_output_port()

    if input_port is None or output_port is None:
        print("Unable to start recording: MIDI port not available.")
        return

    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    start_time = time.time()

    print("Recording... Press Ctrl+C to stop.")

    try:
        for msg in input_port:
            if msg.type in ['note_on', 'note_off']:
                now = time.time()
                delta = int((now - start_time) * 1000)
                msg.time = delta / 1000.0
                start_time = now

                track.append(msg.copy(time=msg.time))
                output_port.send(msg)
    except KeyboardInterrupt:
        filename = get_timestamped_filename()
        mid.save(filename)
        print(f"Recording saved to {filename}")
