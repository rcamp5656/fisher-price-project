# screens/converting_screen.py

import threading
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar

from .utils import make_nav

class ConvertingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # build UI
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.status_label = Label(text="Preparing to convert...", size_hint=(1, 0.2))
        root.add_widget(self.status_label)
        
        self.progress_bar = ProgressBar(max=100, value=0, size_hint=(1, 0.1))
        root.add_widget(self.progress_bar)
        
        # navigation bar: just a Cancel button
        nav_items = [
            ("Cancel", self.cancel_conversion),
        ]
        root.add_widget(make_nav(nav_items))
        
        self.add_widget(root)

    def on_enter(self):
        # start conversion in a background thread right after the screen appears
        Clock.schedule_once(lambda dt: threading.Thread(target=self.start_conversion, daemon=True).start(), 0)

    def start_conversion(self):
        """
        Replace this loop with your actual conversion logic.
        At each meaningful step, call update_progress(percent, message).
        """
        total_steps = 20  # set to however many steps your conversion has
        for step in range(1, total_steps + 1):
            # --- your real conversion step here ---
            # e.g. process a chunk of the MIDI or run music21 conversion
            # ----------------------------------------------------------
            
            # simulate work
            import time; time.sleep(0.1)
            
            # update UI
            percent = int(step / total_steps * 100)
            message = f"Converting... ({step}/{total_steps})"
            Clock.schedule_once(lambda dt, p=percent, m=message: self.update_progress(p, m), 0)
        
        # when done, switch to the ConvertedSelectScreen
        Clock.schedule_once(lambda dt: setattr(self.manager, "current", "converted"), 0)

    def update_progress(self, percent, message):
        self.progress_bar.value = percent
        self.status_label.text = message

    def cancel_conversion(self, *args):
        # simply go back to file select; you may want to set a flag
        # if your real conversion can be interrupted
        self.manager.current = "file_select"
