import sys

from entities.movement.sequences.walking_sequences import *
from entities.movement.legs import Legs

sys.path.insert(0, '../../src')

legs = Legs(leg_0_servos=[
                14,
                61,
                63
            ]
            # leg_1_servos=[
            #     21,
            #     31,
            #     53
            # ],
            # leg_2_servos=[
            #     61,
            #     63,
            #     111
            # ],
            # leg_3_servos=[
            #     111,
            #     111,
            #     111
            # ]
            )

legs.deploy(150)
lol(legs, [250, 250, 250], 10)
