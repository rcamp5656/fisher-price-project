# midi_visualizer.py
"""
Show real-time note events in the terminal with names and velocities.
"""
from note_mapper import note_name


def visualize(events: list[tuple]):
    """Print a summary for each event: On/Off, note name, original note, velocity."""
    for status, note, vel, timestamp in events:
        action = 'On ' if status == 144 and vel > 0 else 'Off'
        name = note_name(note)
        print(f"{action} {name} (orig {note}) Vel={vel}")
