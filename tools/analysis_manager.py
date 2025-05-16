from mido import MidiFile

class AnalysisManager:
    def analyze(self, midi_path):
        mid = MidiFile(midi_path)
        note_counts = {}
        total_time = 0.0
        for msg in mid:
            total_time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                note_counts[msg.note] = note_counts.get(msg.note, 0) + 1
        return {'note_counts': note_counts, 'total_time': total_time}