from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

def make_nav(buttons):
    layout = GridLayout(cols=len(buttons), size_hint=(1, 0.1), spacing=2, padding=2)
    for label, callback in buttons:
        btn = Button(text=label, background_color=(0.6, 0, 0, 1), color=(0, 1, 0, 1))
        btn.bind(on_press=callback)
        layout.add_widget(btn)
    return layout
