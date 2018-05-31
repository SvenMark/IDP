import time
import sys

sys.path.insert(0, '../../src')

from entities.movement.legs import Legs
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

for i in range(5):
    legs.run_sequence([150, 150, 150], True, None, forward)

for i in range(5):
    legs.run_sequence([150, 150, 150], True, None, backward)

for i in range(5):
    legs.run_sequence([150, 150, 150], True, None, pull)

for i in range(5):
    legs.run_sequence([150, 150, 150], True, None, push)

for i in range(5):
    legs.run_sequence([150, 150, 150], True, None, wave)

for i in range(5):
    legs.run_sequence([150, 150, 150], True, None, march)

for i in range(5):
    legs.run_sequence([150, 150, 150], True, None, dab)
    legs.deploy(200)
