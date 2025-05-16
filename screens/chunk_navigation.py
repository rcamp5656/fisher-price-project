
# chunk_navigation.py

import os
from common import CONVERTED_FOLDER, stop_all_midi, play_midi_file

class ChunkNavigator:
    def __init__(self, folder_name):
        self.folder_path = os.path.join(CONVERTED_FOLDER, folder_name)
        self.chunk_files = sorted([
            f for f in os.listdir(self.folder_path)
            if f.lower().endswith('.mid')
        ])
        self.index = 0

    def current_chunk_path(self):
        if 0 <= self.index < len(self.chunk_files):
            return os.path.join(self.folder_path, self.chunk_files[self.index])
        return None

    def play_current(self):
        stop_all_midi()
        path = self.current_chunk_path()
        if path:
            play_midi_file(path)
        return path

    def next_chunk(self):
        if self.index + 1 < len(self.chunk_files):
            self.index += 1
        return self.play_current()

    def prev_chunk(self):
        if self.index > 0:
            self.index -= 1
        return self.play_current()
