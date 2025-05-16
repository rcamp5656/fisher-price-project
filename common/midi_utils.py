from __future__ import annotations

import threading
import time
from pathlib import Path
from typing import Optional, Callable

import pygame.midi
from mido import MidiFile

# Initialize the MIDI subsystem
def _init_midi():
    if not pygame.midi.get_init():
        pygame.midi.init()

_init_midi()

# ---------------------------------------------------------------------------
# Threaded MIDI playback
device_lock = threading.Lock()

class MidiPlayerThread(threading.Thread):
    def __init__(
        self,
        midi_path: Path,
        output_id: Optional[int] = None,
    ):
        super().__init__(daemon=True)
        self.midi = MidiFile(midi_path)
        self.output_id = (
            output_id
            if output_id is not None
            else pygame.midi.get_default_output_id()
        )
        self.output = pygame.midi.Output(self.output_id)
        self._stop_event = threading.Event()

    def run(self):
        start_time = time.time()
        for msg in self.midi:
            if self._stop_event.is_set():
                break
            time.sleep(msg.time)
            if msg.is_meta:
                continue
            data = msg.bytes()
            if len(data) <= 3:
                # For most messages use write_short
                self.output.write_short(*data)
            else:
                # Fallback for SysEx or long messages
                self.output.write(data)
        # On exit, send All Notes Off on every channel
        for ch in range(16):
            self.output.write_short(0xB0 | ch, 0x7B, 0)
        self.output.close()

    def stop(self):
        self._stop_event.set()

# ---------------------------------------------------------------------------
# Global player reference
_player: Optional[MidiPlayerThread] = None

def play_midi_file(path: Path, device_id: Optional[int] = None):
    """
    Stops any existing playback, then plays the given MIDI file on a background thread.
    """
    stop_all_midi()
    global _player
    _player = MidiPlayerThread(path, output_id=device_id)
    _player.start()


def stop_all_midi():
    """
    Stops and joins the current MIDI playback thread (if any), sending All Notes Off.
    """
    global _player
    if _player and _player.is_alive():
        _player.stop()
        _player.join()
        _player = None

# ---------------------------------------------------------------------------
# Stubs for future pause/resume functionality
def pause_midi():
    pass


def resume_midi():
    pass

# ---------------------------------------------------------------------------
# Directory navigation helper for Kivy screens
def make_nav(
    folder: Path,
    on_select: Callable[[Path], None],
    cols: int = 7,
) -> "kivy.uix.gridlayout.GridLayout":
    """
    Generates a GridLayout of Buttons for each file/folder in `folder`.
    `on_select` is called with the Path of the clicked item.
    """
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.button import Button

    grid = GridLayout(cols=cols, spacing=5, padding=5)
    for item in sorted(folder.iterdir()):
        btn = Button(text=item.name)
        btn.bind(on_release=lambda inst, it=item: on_select(it))
        grid.add_widget(btn)
    return grid
