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

tracks = Tracks(
    track_0_pin=13,
    track_1_pin=18,
    track_0_forward=22,
    track_0_backward=27,
    track_1_forward=19,
    track_1_backward=26
)

legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=None, sequence=dablinks)
tracks.turn_left(50, 50, 0, 5)
time.sleep(5)
tracks.stop()
for i in range(5):
    legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=None, sequence=dabrechts)
for i in range(5):
    legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=None, sequence=clap)
for i in range(5):
    legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=None, sequence=ballerina)
for i in range(5):
    legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=None, sequence=extend_arms)
for i in range(5):
    legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=None, sequence=vagedraai)
for i in range(5):
    legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=None, sequence=runningman)
for i in range(5):
    legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=None, sequence=shakeass)

legs.retract(150)
