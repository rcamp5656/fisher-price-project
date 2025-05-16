
# converted_select_screen.py

import os
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
from common import CONVERTED_FOLDER, play_midi_file, stop_all_midi, make_nav
from tools.auto_chunk_playback import AutoChunkPlayer

class ConvertedSelectScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page = 0
        self.last_folder = None
        self.auto_player = None
        self.folders = sorted([
            f for f in os.listdir(CONVERTED_FOLDER)
            if os.path.isdir(os.path.join(CONVERTED_FOLDER, f))
        ])

        root = BoxLayout(orientation='vertical')
        self.grid = GridLayout(cols=7, rows=7, spacing=2, padding=2, size_hint=(1, 0.85))
        root.add_widget(self.grid)

        nav = [
            ('Prev', self.prev_page),
            ('Next', self.next_page),
            ('View Roller', self.view_roller),
            ('Auto-Play All', self.auto_play_all),
            ('Back', lambda *_: setattr(self.manager, 'current', 'file_select')),
            ('Exit', lambda *_: App.get_running_app().stop())
        ]
        root.add_widget(make_nav(nav))
        self.add_widget(root)

        self.populate_grid()

    def populate_grid(self):
        self.grid.clear_widgets()
        start = self.page * 49
        end = start + 49
        for folder in self.folders[start:end]:
            btn = Button(
                text=self.split_name(folder),
                background_color=(0.5, 1, 0.5, 1),
                color=(1, 0, 0, 1)
            )
            btn.bind(on_release=lambda inst, f=folder: self.select_folder(f))
            self.grid.add_widget(btn)

    def split_name(self, name):
        lines = [name[i:i + 20] for i in range(0, len(name), 20)]
        return '\n'.join(lines[:5])

    def select_folder(self, folder):
        stop_all_midi()
        self.last_folder = folder
        full_path = os.path.join(CONVERTED_FOLDER, folder)
        files = sorted([f for f in os.listdir(full_path) if f.lower().endswith('.mid')])
        if files:
            play_midi_file(os.path.join(full_path, files[0]))

    def view_roller(self, *_):
        if not self.last_folder:
            print("No folder selected yet.")
            return
        files = sorted([f for f in os.listdir(os.path.join(CONVERTED_FOLDER, self.last_folder)) if f.lower().endswith('.mid')])
        if not files:
            print("No chunks in last selected folder.")
            return
        chunk_path = os.path.join(CONVERTED_FOLDER, self.last_folder, files[0])
        self.manager.get_screen('fisher_roller').load_chunk(chunk_path)
        self.manager.current = 'fisher_roller'

    def auto_play_all(self, *_):
        if not self.last_folder:
            print("No folder selected.")
            return
        stop_all_midi()
        self.auto_player = AutoChunkPlayer(self.last_folder)
        self.auto_player.start()

    def next_page(self, *_):
        if (self.page + 1) * 49 < len(self.folders):
            self.page += 1
            self.populate_grid()

    def prev_page(self, *_):
        if self.page > 0:
            self.page -= 1
            self.populate_grid()
