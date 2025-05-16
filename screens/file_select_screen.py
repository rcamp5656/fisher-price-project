# screens/file_select_screen.py

import os
import threading

from kivy.app import App
from kivy.logger import Logger
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from screens.utils import flatten_and_chunk_midi, FILES_PER_PAGE
from common import MIDI_FOLDER, CONVERTED_FOLDER, make_nav

class FileSelectScreen(Screen):
    """Displays a 7×7 grid of available MIDI files + navigation bar."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page = 0
        self.selected = None

        # Ensure your folders exist
        MIDI_FOLDER.mkdir(exist_ok=True)
        CONVERTED_FOLDER.mkdir(exist_ok=True)

        # List all .mid files
        self.files = sorted(
            f for f in os.listdir(MIDI_FOLDER)
            if f.lower().endswith(".mid")
        )

        # Root vertical layout
        root = BoxLayout(orientation="vertical")

        # 7×7 grid of MIDI filenames (90% height)
        self.grid = GridLayout(
            cols=7, rows=7, spacing=2, padding=2, size_hint=(1, 0.9)
        )
        root.add_widget(self.grid)

        # Navigation bar (10% height)
        nav_buttons = [
            ("Prev",  self.prev_page),
            ("Next",  self.next_page),
            ("Play",  self.play_selected),
            ("Pause", self.pause_playback),
            ("Stop",  self.stop_playback),
            ("Show Converted", lambda *_: setattr(self.manager, "current", "converted")),
        ]
        root.add_widget(make_nav(nav_buttons))

        self.add_widget(root)
        self.populate_grid()

    def split_name(self, name: str) -> str:
        # Wrap up to 100 chars in lines of 20
        lines = [name[i : i + 20] for i in range(0, min(len(name), 100), 20)]
        return "\n".join(lines)

    def populate_grid(self):
        """Refresh the 7×7 grid for the current page."""
        self.grid.clear_widgets()
        start = self.page * FILES_PER_PAGE
        for fname in self.files[start : start + FILES_PER_PAGE]:
            btn = Button(
                text=self.split_name(fname),
                background_color=(0, 0.4, 0, 1),
                color=(1, 1, 0, 1),
            )
            btn.full = fname
            btn.bind(on_release=self.select_file)
            self.grid.add_widget(btn)

    def select_file(self, instance):
        self.selected = instance.full
        Logger.info(f"Selected MIDI: {self.selected}")
        # Stop any playback in the player screen
        self.manager.get_screen("player").stop_playback()
        # Trigger play & chunk
        self.play_selected()

    def play_selected(self, *_):
        if not self.selected:
            return
        path = os.path.join(MIDI_FOLDER, self.selected)
        Logger.info(f"Playing original MIDI: {path}")
        self.manager.get_screen("player").play_midi(path)
        # And chunk in the background
        threading.Thread(
            target=lambda: flatten_and_chunk_midi(path, CONVERTED_FOLDER),
            daemon=True,
        ).start()

    def pause_playback(self, *_):
        self.manager.get_screen("player").pause_playback()

    def stop_playback(self, *_):
        self.manager.get_screen("player").stop_playback()

    def next_page(self, *_):
        if (self.page + 1) * FILES_PER_PAGE < len(self.files):
            self.page += 1
            self.populate_grid()

    def prev_page(self, *_):
        if self.page > 0:
            self.page -= 1
            self.populate_grid()
