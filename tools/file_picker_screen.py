
# file_picker_screen.py

import os
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.button import Button
from kivy.app import App
from common import MIDI_FOLDER, make_nav, play_midi_file, stop_all_midi
import shutil

class FilePickerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.filechooser = FileChooserIconView(
            path=os.path.expanduser("~"),
            filters=["*.mid"],
            size_hint=(1, 0.85)
        )
        self.layout.add_widget(self.filechooser)

        nav = [
            ('Select', self.select_file),
            ('Back', lambda *_: setattr(self.manager, 'current', 'file_select')),
            ('Exit', lambda *_: App.get_running_app().stop())
        ]
        self.layout.add_widget(make_nav(nav))
        self.add_widget(self.layout)

    def select_file(self, *_):
        if not self.filechooser.selection:
            print("No file selected.")
            return
        selected_path = self.filechooser.selection[0]
        basename = os.path.basename(selected_path)
        dest_path = os.path.join(MIDI_FOLDER, basename)
        try:
            shutil.copy(selected_path, dest_path)
            print(f"Copied: {basename} → {dest_path}")
            self.manager.current = 'file_select'
        except Exception as e:
            print(f"Failed to copy file: {e}")
