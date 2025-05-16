
# chunk_controls.py

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class ChunkControls(BoxLayout):
    def __init__(self, navigator, reload_callback=None, **kwargs):
        super().__init__(orientation='horizontal', size_hint=(1, 0.1), spacing=10, padding=10, **kwargs)
        self.navigator = navigator
        self.reload_callback = reload_callback

        self.prev_button = Button(
            text='⏮ Prev Chunk',
            font_size=20,
            background_color=(0.2, 0.2, 0.6, 1),
            color=(1, 1, 1, 1)
        )
        self.prev_button.bind(on_release=self.prev_chunk)
        self.add_widget(self.prev_button)

        self.next_button = Button(
            text='⏭ Next Chunk',
            font_size=20,
            background_color=(0.6, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        self.next_button.bind(on_release=self.next_chunk)
        self.add_widget(self.next_button)

    def prev_chunk(self, *_):
        path = self.navigator.prev_chunk()
        if self.reload_callback and path:
            self.reload_callback(path)

    def next_chunk(self, *_):
        path = self.navigator.next_chunk()
        if self.reload_callback and path:
            self.reload_callback(path)
