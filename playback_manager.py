import pygame.midi

class PlaybackManager:
    def __init__(self):
        pygame.midi.init()

        self.output_id = 4  # Axiom 25 MIDI OUT (to Yamaha)

        try:
            info = pygame.midi.get_device_info(self.output_id)
            name = info[1].decode()
            print(f"Using MIDI Output ID {self.output_id}: {name}")
            self.player = pygame.midi.Output(self.output_id)
        except Exception as e:
            raise Exception(f"Could not open MIDI Output ID {self.output_id}: {e}")

    def play_note(self, note, velocity=127):
        if self.player:
            self.player.note_on(note, velocity)

    def stop_note(self, note):
        if self.player:
            self.player.note_off(note, 0)

    def stop_all(self):
        if self.player:
            for n in range(128):
                self.player.note_off(n, 0)

    def close(self):
        if self.player:
            self.player.close()
            pygame.midi.quit()
