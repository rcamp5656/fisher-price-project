# screens/staff_screen.py

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from pathlib import Path

from common import MIDI_FOLDER, play_midi_file, stop_all_midi, make_nav

class StaffScreen(Screen):
    """
    Screen for browsing and viewing original MIDI files as musical staff.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Vertical layout container
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Ensure the base MIDI folder exists
        MIDI_FOLDER.mkdir(exist_ok=True)

        # Build a navigation grid of the original MIDI files
        layout.add_widget(make_nav(MIDI_FOLDER, self.on_nav_select))

        # Add the layout to this screen
        self.add_widget(layout)

    def on_nav_select(self, path: Path) -> None:
        """
        Stops any current playback, then plays the selected original MIDI file.
        (Later you can extend this to render staff notation of `path`.)
        """
        stop_all_midi()
        if path.is_file():
            play_midi_file(path)
