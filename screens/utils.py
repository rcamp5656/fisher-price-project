# screens/utils.py

import os
import mido
import threading

FILES_PER_PAGE = 49   # 7×7 grid

def flatten_and_chunk_midi(input_file: str, output_dir: str, chunk_length: float = 25.0) -> list[str]:
    """
    Flatten a multi-track MIDI into one track and split into ~25s chunks,
    saving them under output_dir/<basename>/chunkX.mid.
    Returns list of chunk filepaths.
    """
    mid = mido.MidiFile(input_file)
    ticks_per_beat = mid.ticks_per_beat

    # Flatten into a single track
    flat = mido.MidiFile(ticks_per_beat=ticks_per_beat)
    track = mido.MidiTrack()
    flat.tracks.append(track)
    for msg in mid:
        track.append(msg.copy(time=msg.time))

    base = os.path.splitext(os.path.basename(input_file))[0]
    subfolder = os.path.join(output_dir, base)
    os.makedirs(subfolder, exist_ok=True)

    # Save flattened file (optional)
    flat_path = os.path.join(subfolder, f"{base}_flat.mid")
    flat.save(flat_path)

    # Chunk loop
    chunks = []
    current = mido.MidiTrack()
    mf = mido.MidiFile(ticks_per_beat=ticks_per_beat)
    mf.tracks.append(current)
    elapsed = 0.0
    current_tempo = 500000

    for msg in track:
        if msg.type == "set_tempo":
            current_tempo = msg.tempo
        sec = mido.tick2second(msg.time, ticks_per_beat, current_tempo)
        # start new chunk if over length
        if elapsed + sec > chunk_length and len(current) > 0:
            out_path = os.path.join(subfolder, f"{base}_chunk{len(chunks)+1}.mid")
            mf.save(out_path)
            chunks.append(out_path)
            current = mido.MidiTrack()
            mf = mido.MidiFile(ticks_per_beat=ticks_per_beat)
            mf.tracks.append(current)
            elapsed = 0.0

        current.append(msg.copy(time=msg.time))
        elapsed += sec

    # final chunk
    if len(current) > 0:
        out_path = os.path.join(subfolder, f"{base}_chunk{len(chunks)+1}.mid")
        mf.save(out_path)
        chunks.append(out_path)

    return chunks
