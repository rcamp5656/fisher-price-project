# tools/ui_utils.py

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

def make_nav(buttons, height=0.1):
    """
    Creates a horizontal navigation bar with buttons.
    :param buttons: List of (label, callback) tuples.
    :param height: Height of the navigation bar as a fraction of the screen.
    :return: BoxLayout containing all buttons.
    """
    bar = BoxLayout(size_hint=(1, height), spacing=5, padding=5)
    for label, callback in buttons:
        btn = Button(text=label, on_release=callback)
        bar.add_widget(btn)
    return bar
