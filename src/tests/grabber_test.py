import sys
import time

sys.path.insert(0, '../../src')

from entities.movement.tracks import Tracks
from entities.movement.grabber import Grabber

grabber = Grabber(id_servo=[
            1,
            53,
            13
        ],
        initial_positions=[1023, 290, 690])

tracks = Tracks(track_0_pin=13,
                track_1_pin=18,
                track_0_forward=22,
                track_0_backward=27,
                track_1_forward=19,
                track_1_backward=26),

while True:
    grabber.grab([80, 80, 80])
    if grabber.reposition is True:
        tracks.forward(30, 30, 2, 3)
        grabber.reposition = False
