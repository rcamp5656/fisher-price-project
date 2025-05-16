# tools/conversion_logic.py

import os
import logging
from mido import MidiFile, MidiTrack

logger = logging.getLogger()

def flatten_and_chunk_midi(in_path, out_folder, chunk_length=25):
    """
    Flatten multi-track MIDI and write 25-second chunks to out_folder.
    """
    mid = MidiFile(in_path)
    flat = MidiFile(type=1)
    flat.ticks_per_beat = mid.ticks_per_beat
    track = MidiTrack()
    flat.tracks.append(track)

    # Flatten: copy all non‐meta messages into one track
    for msg in mid:
        if not msg.is_meta:
            track.append(msg.copy())

    # Look for a set_tempo message; default to 500 000 µs/qn if none found
    tempo = 500000
    for m in mid.tracks[0]:
        if getattr(m, 'type', None) == 'set_tempo':
            tempo = m.tempo
            break

    # Calculate ticks per second and per chunk
    ticks_per_sec   = flat.ticks_per_beat / (tempo / 1_000_000)
    ticks_per_chunk = int(ticks_per_sec * chunk_length)

    base = os.path.splitext(os.path.basename(in_path))[0]
    count = 0

    # Split into chunks of ticks_per_chunk events
    for start in range(0, len(track), ticks_per_chunk):
        chunk_mid = MidiFile(type=1)
        chunk_mid.ticks_per_beat = flat.ticks_per_beat
        tk = MidiTrack()
        chunk_mid.tracks.append(tk)

        # Copy the slice of messages into the new track
        for m in track[start:start + ticks_per_chunk]:
            tk.append(m.copy(time=m.time))

        # Ensure all message times are integers for Mido
        for t in chunk_mid.tracks:
            for msg in t:
                msg.time = int(msg.time)

        # Save the chunk
        fname = f"fp_{base}_{count}.mid"
        out_path = os.path.join(out_folder, fname)
        chunk_mid.save(out_path)
        logger.info(f"Saved chunk: {out_path}")

        count += 1
