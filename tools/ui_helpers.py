# tools/ui_helpers.py
import time
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock

def make_nav(buttons):
    """
    Create a standardized navigation bar.
    `buttons` is a list of (label, callback) tuples.
    """
    nav = BoxLayout(size_hint=(1, 0.1), spacing=4, padding=2)
    for label, callback in buttons:
        btn = Button(text=label)
        if label in ('Pause', 'Stop', 'Edit Mode'):
            original_cb = callback
            def wrapped(instance, _cb=original_cb):
                instance.background_color = (1,1,0,1)
                Clock.schedule_once(lambda dt: setattr(instance, 'background_color', (1,0,0,1)), 0.25)
                _cb(instance)
            btn.bind(on_release=wrapped)
        else:
            btn.bind(on_release=callback)
        nav.add_widget(btn)
    return nav

def prompt_printer():
    """
    Popup to ask if a printer is connected.
    Returns True if yes, False if no.
    """
    result = {'value': False}
    content = BoxLayout(orientation='vertical', spacing=10, padding=10)
    content.add_widget(Label(text='Do you have a printer connected?'))
    btns = BoxLayout(size_hint=(1, 0.3), spacing=10)
    def yes(_): result['value'] = True; popup.dismiss()
    def no(_):  result['value'] = False; popup.dismiss()
    btns.add_widget(Button(text='Yes', on_release=yes))
    btns.add_widget(Button(text='No',  on_release=no))
    content.add_widget(btns)
    popup = Popup(title='Printer Confirmation', content=content, size_hint=(0.7,0.4))
    popup.open()
    # block until closed
    while popup._window:
        time.sleep(0.1)
    return result['value']
