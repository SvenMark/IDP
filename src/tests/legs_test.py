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

legs.deploy(80)
