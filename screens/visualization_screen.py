from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class VisualizationScreen(Screen):
    note_count_label = ObjectProperty(None)
    duration_label = ObjectProperty(None)

    def display_analysis(self, analysis_data):
        note_counts = analysis_data.get('note_counts', {})
        total_time = analysis_data.get('total_time', 0)
        total_notes = sum(note_counts.values())
        self.note_count_label.text = f"Notes played: {total_notes}"
        self.duration_label.text = f"Duration: {total_time:.2f} sec"