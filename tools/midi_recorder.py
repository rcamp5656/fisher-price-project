# midi_recorder.py
"""
Record live events into a timestamped .mid file using mido.
"""
import datetime
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo, second2tick


def create_midi_file(tempo_bpm: int = 120, ticks_per_beat: int = 480):
    """Initialize a new MidiFile and track with program change and tempo meta-message."""
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    mid.ticks_per_beat = ticks_per_beat
    # Add initial messages
    track.append(Message('program_change', program=0, time=0))
    tempo = bpm2tempo(tempo_bpm)
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
    return mid, track


def timestamp_filename(prefix: str = 'live') -> str:
    """Generate a filename `prefix_YYYY-MM-DD_HHMM.mid`."""
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    return f"{prefix}_{ts}.mid"


def append_event(track: MidiTrack, msg_type: str, note: int, velocity: int, elapsed: float, mid: MidiFile):
    """Append a note_on or note_off event with proper delta time ticks."""
    ticks = int(second2tick(elapsed, mid.ticks_per_beat, mid.tracks[0][1].tempo))
    track.append(Message(msg_type, note=note, velocity=velocity, time=ticks))


def save_mid(mid: MidiFile, filename: str):
    """Write the MidiFile to disk."""
    mid.save(filename)
