# screens/grid_select_screen.py

import os
import threading
import time
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from mido import MidiFile
from tools.ui_helpers import make_nav
from tools.logging_setup import logger

def split_filename(name, max_len=20, lines=6):
    parts = [name[i:i+max_len] for i in range(0, max_len*lines, max_len)]
    parts = parts[:lines] + ['']*(lines-len(parts))
    return "\n".join(parts)

class GridSelectScreen(Screen):
    """
    Generic 7×7 grid of .mid files from a folder, with nav buttons.
    Subclasses must implement `on_item_selected(self, path)`.
    """
    def __init__(self, dir_path, nav_buttons, **kwargs):
        super().__init__(**kwargs)
        Window.fullscreen = 'auto'
        self.dir_path = dir_path
        self.page = 0
        self.files = sorted(f for f in os.listdir(dir_path) if f.lower().endswith('.mid'))
        self._stop = threading.Event()
        self._pause = threading.Event()
        self._last = None

        # root layout
        root = BoxLayout(orientation='vertical', spacing=5, padding=5)
        self.add_widget(root)

        # grid: 85% height
        self.grid = GridLayout(cols=7, rows=7, spacing=2, padding=2, size_hint=(1, 0.85))
        root.add_widget(self.grid)

        # navigation: 15% height
        nav = make_nav(nav_buttons)
        nav.size_hint = (1, 0.15)
        root.add_widget(nav)

        self.populate()

    def populate(self):
        self.grid.clear_widgets()
        start = self.page * 49
        chunk = self.files[start:start+49]

        # compute cell size to exactly fill width
        cols = 7
        pad = sum(self.grid.padding) + sum(self.parent.padding if hasattr(self.parent,'padding') else (0,0))*2
        sp = self.grid.spacing[0]
        total = pad + sp*(cols-1)
        cell = (Window.width - total)/cols

        for name in chunk:
            btn = Button(
                text=split_filename(name),
                size_hint=(None,None),
                width=cell, height=cell,
                background_normal='',
                background_color=(0,0.2,0,1),
                color=(1,1,0,1),
                text_size=(cell-10, cell),
                halign='center', valign='middle'
            )
            full = os.path.join(self.dir_path, name)
            btn.bind(on_release=lambda btn, p=full: self._select(p))
            self.grid.add_widget(btn)

        # placeholders
        for _ in range(49 - len(chunk)):
            ph = Button(size_hint=(None,None), width=cell, height=cell,
                        background_normal='', background_color=(0,0.2,0,1),
                        disabled=True)
            self.grid.add_widget(ph)

    def _select(self, path):
        self._last = path
        logger.info(f"Selected {path}")
        threading.Thread(target=lambda: self.on_item_selected(path), daemon=True).start()

    def next_page(self, *_):
        if (self.page+1)*49 < len(self.files):
            self.page += 1
            self.populate()

    def prev_page(self, *_):
        if self.page > 0:
            self.page -= 1
            self.populate()

    def replay_last(self, *_):
        if self._last:
            threading.Thread(target=lambda: self.on_item_selected(self._last), daemon=True).start()

    def on_item_selected(self, path):
        """Called when a grid‐item is clicked. Must be implemented by subclass."""
        raise NotImplementedError
