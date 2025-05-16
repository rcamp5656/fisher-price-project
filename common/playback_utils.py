import pygame.midi
import time
import threading

# Initialize pygame.midi only once
pygame.midi.init()

# Holds the current MIDI output object
midi_out = None
playback_thread = None
playback_running = False

def get_output_device():
    """Get the best available MIDI output port (USB or Microsoft GS)."""
    preferred = ['Axiom', 'USB', 'Yamaha', 'Microsoft', 'GS']
    for i in range(pygame.midi.get_count()):
        interf, name, is_input, is_output, opened = pygame.midi.get_device_info(i)
        if is_output:
            name_str = name.decode()
            if any(p in name_str for p in preferred):
                return i
    return pygame.midi.get_default_output_id()

def init_output():
    """Initialize the MIDI output if not already."""
    global midi_out
    if midi_out is None:
        output_id = get_output_device()
        if output_id != -1:
            midi_out = pygame.midi.Output(output_id)
        else:
            raise RuntimeError("No MIDI output device found.")

def stop_all_sounds():
    """Send All Notes Off to all channels."""
    global midi_out
    if midi_out:
        for ch in range(16):
            midi_out.write_short(0xB0 + ch, 0x7B, 0x00)

def play_notes(note_sequence, tempo=500):
    """Play a list of (note, duration) tuples."""
    global playback_thread, playback_running

    def run():
        global playback_running
        playback_running = True
        init_output()
        for note, dur in note_sequence:
            if not playback_running:
                break
            midi_out.note_on(note, 127)
            time.sleep(dur / 1000.0)
            midi_out.note_off(note, 127)
        playback_running = False

    if playback_thread and playback_thread.is_alive():
        stop_playback()

    playback_thread = threading.Thread(target=run)
    playback_thread.start()

def stop_playback():
    """Stop ongoing playback."""
    global playback_running
    playback_running = False
    stop_all_sounds()
