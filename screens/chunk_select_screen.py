# screens/chunk_select_screen.py

import os
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window

from tools.ui_helpers import make_nav
from tools.logging_setup import logger

class ChunkSelectScreen(Screen):
    """Displays a 7×7 grid of rectangular chunk .mid buttons with playback controls."""
    def __init__(self, dir_path, **kwargs):
        super().__init__(**kwargs)
        self.dir_path = dir_path
        self._last_chunk = None

        layout = BoxLayout(orientation='vertical', spacing=5, padding=5)
        self.grid = GridLayout(cols=7, spacing=4, padding=4, size_hint=(1, 0.9))
        layout.add_widget(self.grid)

        nav_buttons = [
            ('Back', lambda *_: setattr(self.manager, 'current', 'converted')),
            ('Play', self.play_last),
            ('Pause', self.pause_playback),
            ('Stop', self.stop_playback),
            ('Files', lambda *_: setattr(self.manager, 'current', 'file_select')),
            ('Exit', lambda *_: App.get_running_app().stop()),
        ]
        layout.add_widget(make_nav(nav_buttons))
        self.add_widget(layout)

    def on_enter(self, *_):
        self.grid.clear_widgets()

        if not os.path.isdir(self.dir_path):
            logger.warning(f"Invalid chunk directory: {self.dir_path}")
            return

        # Calculate rectangular block size
        total_spacing = self.grid.spacing[0] * 6 + self.grid.padding[0] * 2
        btn_width = (Window.width - total_spacing) / 7
        btn_height = btn_width * 0.6  # rectangular

        for fname in sorted(os.listdir(self.dir_path)):
            if fname.lower().endswith('.mid'):
                # Split into 20-character lines, max 6 lines
                lines = [fname[i:i + 20] for i in range(0, len(fname), 20)][:6]
                display_text = '\n'.join(lines)

                btn = Button(
                    text=display_text,
                    size_hint=(None, None),
                    size=(btn_width, btn_height),
                    background_color=(1, 1, 0, 1),  # yellow
                    color=(0, 0, 0, 1),             # black text
                    text_size=(btn_width - 10, None),
                    halign='center',
                    valign='middle',
                    font_size='11sp'
                )
                btn.full_path = os.path.join(self.dir_path, fname)
                btn.bind(on_release=self.select_chunk)
                self.grid.add_widget(btn)

    def select_chunk(self, instance):
        self._last_chunk = instance.full_path
        self.manager.get_screen('player').play_midi(self._last_chunk)

    def play_last(self, *_):
        if self._last_chunk:
            self.manager.get_screen('player').play_midi(self._last_chunk)

    def pause_playback(self, *_):
        self.manager.get_screen('player').pause_playback()

    def stop_playback(self, *_):
        self.manager.get_screen('player').stop_playback()

    def on_leave(self, *args):
        self.manager.get_screen('player').stop_playback()
