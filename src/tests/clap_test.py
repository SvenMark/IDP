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

for i in range(5):
    legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=None, sequence=dablinks)
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
