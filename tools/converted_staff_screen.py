
# converted_staff_screen.py

import os
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Line
from kivy.clock import Clock
from kivy.app import App
from common import CONVERTED_FOLDER, stop_all_midi, make_nav
from mido import MidiFile
from tools.chunk_navigation import ChunkNavigator
from tools.chunk_controls import ChunkControls

class ConvertedStaffScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.navigator = None
        self.canvas_widget = BoxLayout(orientation='vertical')
        self.add_widget(self.canvas_widget)

        nav = [
            ('Back', lambda *_: setattr(self.manager, 'current', 'converted')),
            ('Exit', lambda *_: App.get_running_app().stop())
        ]
        self.add_widget(make_nav(nav))

    def load_chunk(self, chunk_path):
        # Parse folder and index for navigation
        folder = os.path.basename(os.path.dirname(chunk_path))
        self.navigator = ChunkNavigator(folder)
        # Find current index based on file
        filename = os.path.basename(chunk_path)
        if filename in self.navigator.chunk_files:
            self.navigator.index = self.navigator.chunk_files.index(filename)

        Clock.schedule_once(lambda dt: self.draw_notes(), 0.1)

    def draw_notes(self):
        self.canvas_widget.clear_widgets()

        path = self.navigator.current_chunk_path()
        note_area = StaffCanvas(path)

        self.canvas_widget.add_widget(note_area)
        self.canvas_widget.add_widget(ChunkControls(self.navigator, reload_callback=self.reload_chunk))

    def reload_chunk(self, chunk_path):
        stop_all_midi()
        self.load_chunk(chunk_path)

class StaffCanvas(BoxLayout):
    def __init__(self, midi_file, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.midi_file = midi_file
        self.bind(size=self.redraw)
        self.redraw()

    def redraw(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            mid = MidiFile(self.midi_file)
            tick = 0
            for msg in mid:
                if not msg.is_meta and msg.type == 'note_on' and msg.velocity > 0:
                    tick += msg.time
                    x = tick * 100
                    y = (msg.note - 60) * 10 + 100
                    Line(points=[x, y, x + 20, y], width=1.5)
