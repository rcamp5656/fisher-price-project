
# fisher_price_display_screen.py

import os
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock
from kivy.app import App
from common import CONVERTED_FOLDER, stop_all_midi, make_nav
from mido import MidiFile
from tools.chunk_navigation import ChunkNavigator
from tools.chunk_controls import ChunkControls
from tools.auto_chunk_playback import AutoChunkPlayer

class FisherPriceDisplayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.navigator = None
        self.auto_player = None
        self.canvas_widget = BoxLayout(orientation='vertical')
        self.add_widget(self.canvas_widget)

        nav = [
            ('Back', lambda *_: setattr(self.manager, 'current', 'converted')),
            ('Auto-Play All', self.auto_play_all),
            ('Exit', lambda *_: App.get_running_app().stop())
        ]
        self.add_widget(make_nav(nav))

    def load_chunk(self, chunk_path):
        folder = os.path.basename(os.path.dirname(chunk_path))
        self.navigator = ChunkNavigator(folder)
        filename = os.path.basename(chunk_path)
        if filename in self.navigator.chunk_files:
            self.navigator.index = self.navigator.chunk_files.index(filename)

        Clock.schedule_once(lambda dt: self.draw_roller_view(), 0.1)

    def draw_roller_view(self):
        self.canvas_widget.clear_widgets()

        path = self.navigator.current_chunk_path()
        roller = RollerCanvas(path)

        self.canvas_widget.add_widget(roller)
        self.canvas_widget.add_widget(ChunkControls(self.navigator, reload_callback=self.reload_chunk))

    def reload_chunk(self, chunk_path):
        stop_all_midi()
        self.load_chunk(chunk_path)

    def auto_play_all(self, *_):
        if not self.navigator:
            print("No folder loaded yet.")
            return
        folder = os.path.basename(self.navigator.folder_path)
        self.auto_player = AutoChunkPlayer(folder, on_chunk_play=self.load_chunk)
        self.auto_player.start()

class RollerCanvas(BoxLayout):
    def __init__(self, midi_file, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.midi_file = midi_file
        self.bind(size=self.redraw)
        self.redraw()

    def redraw(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 0, 1)
            mid = MidiFile(self.midi_file)
            tick = 0
            for msg in mid:
                if not msg.is_meta and msg.type == 'note_on' and msg.velocity > 0:
                    tick += msg.time
                    x = tick * 120
                    y = (msg.note - 60) * 10 + 100
                    Ellipse(pos=(x, y), size=(10, 10))
