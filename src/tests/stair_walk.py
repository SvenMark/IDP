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

# tracks.forward(30, 30, 0, 0)
# tracks.forward(75, 75, 0, 3)
#
# while True:
#     tracks.forward(75, 75, 0, 0)
#     legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=[0], sequence=stair)
#     time.sleep(0.1)
#     legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=[1], sequence=stair)
#     time.sleep(0.1)
#     legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=[2], sequence=stair)
#     time.sleep(0.1)
#     legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=[3], sequence=stair)
#     time.sleep(0.1)

for i in range(5):
    tracks.stop()
    legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=[0], sequence=stair_3)
    time.sleep(2)
    tracks.forward(40, 40, 0, 0)
    tracks.forward(80, 80, 0.2, 4)
    legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=[1], sequence=stair_3)
    tracks.forward(80, 80, 0.3, 4)
    time.sleep(0.2)

tracks.stop()
legs.retract(150)
