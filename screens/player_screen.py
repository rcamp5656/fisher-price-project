# screens/player_screen.py

import time
import threading
from mido import MidiFile
import pygame.midi
from kivy.uix.screenmanager import Screen

from tools.logging_setup import logger

# --- Safe MIDI output detection ---
pygame.midi.init()

def get_default_midi_output():
    """Find the first working output, fallback to Microsoft GS Synth if needed."""
    fallback_name = b"Microsoft GS Wavetable Synth"
    fallback_id = None

    for i in range(pygame.midi.get_count()):
        interf, name, is_input, is_output, opened = pygame.midi.get_device_info(i)
        if is_output:
            if name == fallback_name:
                fallback_id = i
            if not opened:
                try:
                    print(f"✔ Using MIDI output: {name.decode()}")
                    return pygame.midi.Output(i)
                except Exception:
                    continue

    if fallback_id is not None:
        try:
            print("✔ Using fallback: Microsoft GS Wavetable Synth")
            return pygame.midi.Output(fallback_id)
        except Exception:
            pass

    print("⚠️ No usable MIDI output found.")
    return None

PLAYER = get_default_midi_output()

class PlayerScreen(Screen):
    """Optional central player screen — handles playback control shared by others."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._last_path = None

    def play_midi(self, path):
        self.stop_playback()
        self._stop_event.clear()
        self._pause_event.clear()
        self._last_path = path
        threading.Thread(target=self._play_thread, args=(path,), daemon=True).start()
        logger.info(f"Started MIDI playback: {path}")

    def _play_thread(self, path):
        try:
            midi = MidiFile(path)
            for tr in midi.tracks:
                for msg in tr:
                    if msg.type == 'program_change' and PLAYER:
                        PLAYER.set_instrument(msg.program, msg.channel)
            for msg in midi:
                if self._stop_event.is_set():
                    break
                while self._pause_event.is_set():
                    time.sleep(0.1)
                time.sleep(msg.time)
                if not msg.is_meta and PLAYER:
                    if msg.type == 'note_on':
                        PLAYER.note_on(msg.note, msg.velocity, msg.channel)
                    elif msg.type == 'note_off':
                        PLAYER.note_off(msg.note, msg.velocity, msg.channel)
        except Exception as e:
            logger.error(f"Playback error: {e}")

    def pause_playback(self, *_):
        self._pause_event.set()
        logger.info("Playback paused")

    def stop_playback(self, *_):
        self._stop_event.set()
        if PLAYER:
            for ch in range(16):
                try:
                    PLAYER.write_short(0xB0+ch, 0x7B, 0)
                except:
                    pass
            for note in range(128):
                PLAYER.note_off(note, 0)
        logger.info("Playback stopped")

    def replay_last(self, *_):
        if self._last_path:
            self.play_midi(self._last_path)
