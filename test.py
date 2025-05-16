import time
import pygame.midi

pygame.midi.init()
out = pygame.midi.Output(4)                # device ID 4 = your Axiom 25 Out
out.write_short(0x90, 60, 127)             # Note On, channel 1, note 60, velocity 127
time.sleep(1.0)
out.write_short(0x80, 60, 0)               # Note Off
out.close()
pygame.midi.quit()
