import os
import pygame.midi
import time
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

# === Folder Constants ===
MIDI_FOLDER = os.path.join(os.getcwd(), 'MIDI')
CONVERTED_FOLDER = os.path.join(os.getcwd(), 'Converted')
LIVE_FOLDER = os.path.join(os.getcwd(), 'Live')

# === MIDI Playback Globals ===
_output = None
_playback_queue = []
_playback_start = None

def make_nav(buttons):
    layout = BoxLayout(size_hint=(1, 0.1), spacing=5)
    for label, callback in buttons:
        btn = Button(text=label)
        btn.bind(on_press=callback)
        layout.add_widget(btn)
    return layout

def init_midi_output():
    global _output
    if _output is not None:
        return
    pygame.midi.init()
    for i in range(pygame.midi.get_count()):
        info = pygame.midi.get_device_info(i)
        if info[1].decode().lower().find('microsoft') >= 0 and info[3]:
            _output = pygame.midi.Output(i)
            print(f"✔ Using MIDI output: {info[1].decode()}")
            return
    # Fallback
    _output = pygame.midi.Output(pygame.midi.get_default_output_id())
    print("✔ Using default MIDI output.")

def stop_all_midi():
    global _output, _playback_queue
    if _output:
        for note in range(128):
            _output.note_off(note, 0)
    _playback_queue.clear()

def play_midi_file(filename, delay=0):
    from mido import MidiFile
    global _output, _playback_queue, _playback_start
    if not os.path.exists(filename):
        print(f"✘ File not found: {filename}")
        return

    init_midi_output()
    mid = MidiFile(filename)
    tempo = 500000  # default tempo
    _playback_queue.clear()
    abs_time = 0

    for msg in mid:
        abs_time += mido.tick2second(msg.time, mid.ticks_per_beat, tempo)
        if msg.type == 'set_tempo':
            tempo = msg.tempo
        elif msg.type in ('note_on', 'note_off'):
            _playback_queue.append((abs_time + delay, msg))

    _playback_start = time.time()
    from kivy.clock import Clock
    Clock.schedule_interval(process_midi_queue, 1 / 60.)

def process_midi_queue(dt):
    global _playback_queue, _output, _playback_start
    now = time.time() - _playback_start
    while _playback_queue and _playback_queue[0][0] <= now:
        _, msg = _playback_queue.pop(0)
        if msg.type == 'note_on':
            _output.note_on(msg.note, msg.velocity)
        elif msg.type == 'note_off':
            _output.note_off(msg.note, msg.velocity)
    if not _playback_queue:
        return False
