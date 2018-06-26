import time
import sys

sys.path.insert(0, '../../src')

from entities.movement.tracks import Tracks

tracks = Tracks(track_0_pin=13,
                track_1_pin=18,
                track_0_forward=22,
                track_0_backward=27,
                track_1_forward=19,
                track_1_backward=26)

while True:
    tracks.forward(75, 75, 0, 0)
    time.sleep(0.5)
    tracks.stop()
    time.sleep(0.5)

