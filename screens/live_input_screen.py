# screens/live_input_screen.py

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from pathlib import Path

from common import play_midi_file, stop_all_midi, make_nav, MIDI_FOLDER

class LiveInputScreen(Screen):
    """
    Screen for browsing and playing back live-recorded MIDI files.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout container
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Ensure there's a "live" subfolder under your MIDI folder
        live_folder = MIDI_FOLDER / "live"
        live_folder.mkdir(exist_ok=True)

        # Pass the folder itself so make_nav can iterate its contents
        layout.add_widget(make_nav(live_folder, self.on_nav_select))

        self.add_widget(layout)

    def on_nav_select(self, path: Path) -> None:
        """
        Called when the user taps one of the nav buttons.
        Stops any current playback, then plays the selected file.
        """
        stop_all_midi()
        if path.is_file():
            play_midi_file(path)
