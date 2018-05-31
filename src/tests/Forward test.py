import time
import sys

sys.path.insert(0, '../../src')

from entities.movement.legs import Legs
from entities.movement.sequences.walking_sequences import *
from entities.movement.sequences.sequences import *

legs = Legs(leg_0_servos=[
                14,
                61,
                63
            ]
#            leg_1_servos=[
#                21,
#                31,
#                53
#            ],
#            leg_2_servos=[
#                61,
#                63,
#                111
#            ],
#            leg_3_servos=[
#                111,
#                111,
#                111
#            ]
            )

walk_forward(legs, [200, 200, 200])
