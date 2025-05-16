import os
import re

def natural_sort_key(text):
    """Sorts filenames in natural order (e.g., part1, part2, part10)."""
    return [int(s) if s.isdigit() else s.lower() for s in re.split('([0-9]+)', text)]

class ChunkNavigator:
    def __init__(self, folder_path):
        self.folder = folder_path
        self.chunks = self._scan_chunks()
        self.index = 0 if self.chunks else -1

    def _scan_chunks(self):
        """Return a naturally sorted list of .mid files in folder."""
        if not os.path.exists(self.folder):
            return []
        files = [f for f in os.listdir(self.folder) if f.lower().endswith('.mid')]
        return sorted(files, key=natural_sort_key)

    def current_chunk(self):
        if 0 <= self.index < len(self.chunks):
            return os.path.join(self.folder, self.chunks[self.index])
        return None

    def next(self):
        if self.index < len(self.chunks) - 1:
            self.index += 1
        return self.current_chunk()

    def prev(self):
        if self.index > 0:
            self.index -= 1
        return self.current_chunk()

    def reset(self):
        self.index = 0

    def count(self):
        return len(self.chunks)

    def position(self):
        return self.index + 1  # Human-readable
