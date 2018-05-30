import sys

from entities.movement.legs import Legs
from entities.movement.sequences.walking_sequences import *

sys.path.insert(0, '../../src')

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


for i in range(5):
    push(legs, [200, 200, 200])
