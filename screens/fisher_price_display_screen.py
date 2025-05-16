# screens/fisher_price_display_screen.py

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from pathlib import Path

from common import CONVERTED_FOLDER, play_midi_file, stop_all_midi, make_nav

class FisherPriceDisplayScreen(Screen):
    """
    Screen for browsing and playing back converted MIDI chunks
    with Fisher‑Price roller‑style visualization.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Container layout
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Ensure the Converted folder exists
        conv_folder = CONVERTED_FOLDER
        conv_folder.mkdir(exist_ok=True)

        # Build a navigation grid of everything under Converted/
        # Pass in self.on_nav_select so make_nav hooks up taps correctly
        layout.add_widget(make_nav(conv_folder, self.on_nav_select))

        self.add_widget(layout)

    def on_nav_select(self, path: Path) -> None:
        """
        Called when the user taps one of the nav buttons.
        Stops any current playback, then plays the selected file.
        """
        stop_all_midi()
        if path.is_file():
            play_midi_file(path)
            # You can trigger your roller‑style animation here using `path`
