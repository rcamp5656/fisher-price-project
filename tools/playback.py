# tools/playback.py

import pygame.midi
import mido
import time
import logging

pygame.midi.init()

_midi_out = None

def get_output_device():
    """Find Axiom 25 output port, fallback to Microsoft GS if not found."""
    axiom_keywords = [b'Axiom', b'M-Audio']
    ms_keywords = [b'Microsoft', b'GS']

    for i in range(pygame.midi.get_count()):
        interf, name, is_input, is_output, opened = pygame.midi.get_device_info(i)
        if is_output and any(k in name for k in axiom_keywords):
            logging.info(f"Using Axiom output: {name.decode()}")
            return i
    for i in range(pygame.midi.get_count()):
        interf, name, is_input, is_output, opened = pygame.midi.get_device_info(i)
        if is_output and any(k in name for k in ms_keywords):
            logging.info(f"Using fallback Microsoft output: {name.decode()}")
            return i
    logging.warning("No valid MIDI output found. Using default.")
    return pygame.midi.get_default_output_id()

def play_midi_note(note, velocity=127, duration=0.5):
    """Play a single MIDI note and stop after the duration."""
    global _midi_out
    if _midi_out is None:
        _midi_out = pygame.midi.Output(get_output_device())
    _midi_out.note_on(note, velocity)
    time.sleep(duration)
    _midi_out.note_off(note, velocity)

def stop_all_midi():
    """Turn off all possible notes (for all channels)."""
    global _midi_out
    if _midi_out:
        for note in range(128):
            for channel in range(16):
                _midi_out.write_short(0x80 | channel, note, 0)

def play_midi_file(filename):
    """Play a full MIDI file through the selected output device."""
    global _midi_out
    if _midi_out is None:
        _midi_out = pygame.midi.Output(get_output_device())

    mid = mido.MidiFile(filename)
    for msg in mid:
        time.sleep(msg.time)
        if msg.type == 'note_on':
            _midi_out.note_on(msg.note, msg.velocity)
        elif msg.type == 'note_off':
            _midi_out.note_off(msg.note, msg.velocity)
