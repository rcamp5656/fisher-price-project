
# auto_chunk_playback.py

import os
import threading
import time
from mido import MidiFile
from common import CONVERTED_FOLDER, stop_all_midi, play_midi_file

class AutoChunkPlayer:
    def __init__(self, folder_name, on_chunk_play=None, on_done=None):
        self.folder = os.path.join(CONVERTED_FOLDER, folder_name)
        self.chunk_files = sorted(f for f in os.listdir(self.folder) if f.lower().endswith('.mid'))
        self.index = 0
        self.on_chunk_play = on_chunk_play
        self.on_done = on_done
        self._stop = False
        self.thread = None

    def start(self):
        self._stop = False
        self.thread = threading.Thread(target=self._play_loop)
        self.thread.start()

    def stop(self):
        self._stop = True
        stop_all_midi()

    def _play_loop(self):
        while not self._stop and self.index < len(self.chunk_files):
            path = os.path.join(self.folder, self.chunk_files[self.index])
            if self.on_chunk_play:
                self.on_chunk_play(path)

            mid = MidiFile(path)
            total_duration = sum(msg.time for msg in mid)

            play_midi_file(path)
            time.sleep(total_duration + 0.5)
            self.index += 1

        if self.on_done:
            self.on_done()
