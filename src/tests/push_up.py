import time
import sys

sys.path.insert(0, '../../src')

from entities.movement.legs import Legs
from entities.movement.sequences.sequences import *

legs = Legs(
    leg_0_servos=[21, 41, 52],
    leg_1_servos=[16, 17, 18],
    leg_2_servos=[61, 62, 63],
    leg_3_servos=[6, 14, 15]
)

while True:
    legs.move(leg_0_moves=[354, 166, 853],
              leg_1_moves=[682, 166, 853],
              leg_2_moves=[354, 166, 853],
              leg_3_moves=[682, 166, 853],
              speeds=[150, 150, 150],
              self_update=True)

