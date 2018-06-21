import time
import sys

sys.path.insert(0, '../../src')

from entities.movement.legs import Legs
from entities.movement.tracks import Tracks
from entities.movement.sequences.sequences import *

legs = Legs(
    leg_0_servos=[21, 41, 52],
    leg_1_servos=[16, 17, 18],
    leg_2_servos=[61, 62, 63],
    leg_3_servos=[6, 14, 15]
)
tracks = Tracks(track_0_pin=13,
                track_1_pin=18,
                track_0_forward=22,
                track_0_backward=27,
                track_1_forward=19,
                track_1_backward=26)

for i in range(5):
    tracks.stop()
    legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=[0], sequence=stair)
    time.sleep(1.)
    tracks.forward(50, 50, 2, 0)
    legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=[1], sequence=stair)
    time.sleep(2)

legs.retract(150)
