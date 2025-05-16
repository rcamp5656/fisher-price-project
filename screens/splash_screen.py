from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle


class SplashScreen(Screen):
    """Medium-brown full-window splash that hands off to FileSelect after 2 s."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ---- full-window background ----------------------------------------
        with self.canvas.before:
            Color(0.60, 0.40, 0.20, 1)          # medium brown
            self._bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        # ---- simple centre label ------------------------------------------
        self.add_widget(
            Label(text='Fisher-Price MIDI Converter',
                  font_size='42sp',
                  bold=True,
                  halign='center',
                  valign='middle')
        )

        # ---- auto-advance --------------------------------------------------
        Clock.schedule_once(self._go_next, 2)

    # ----------------------------------------------------------------------
    def _update_bg(self, *_):
        self._bg.size = self.size
        self._bg.pos = self.pos

    def _go_next(self, *_):
        # make sure the screen exists before switching
        if self.manager and 'file_select' in self.manager.screen_names:
            self.manager.current = 'file_select'
