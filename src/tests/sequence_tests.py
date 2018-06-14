import time
import sys

sys.path.insert(0, '../../src')

from entities.movement.legs import Legs
from entities.movement.sequences.sequences import *

legs = Legs(
    leg_0_servos=[6, 14, 15],
    leg_1_servos=[16, 17, 18],
    leg_2_servos=[21, 41, 52],
    leg_3_servos=[61, 62, 63]
    )

for i in range(5):
    legs.run_sequence([250, 250, 250], self_update=True, sequences=None, sequence=forward)

for i in range(5):
    legs.run_sequence([250, 250, 250], True, None, backward)
for i in range(5):
    legs.run_sequence([200, 200, 200], True, None, pull)

for i in range(5):
    legs.run_sequence([200, 200, 200], True, None, push)

for i in range(5):
    legs.run_sequence([150, 150, 150], True, None, wave)

for i in range(5):
    legs.run_sequence([150, 150, 150], True, None, march)

for i in range(5):
    legs.run_sequence([150, 150, 150], True, None, dab)
    legs.deploy(200)
