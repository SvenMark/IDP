import sys
import time

sys.path.insert(0, '../../src')

from entities.movement.limb.joints.servo import Servo
from entities.movement.legs import Legs

legs = Legs(leg_0_servos=[
                1,
                13,
                53
            ],
            leg_1_servos=[
                13,
                21,
                31
            ],
            leg_2_servos=[
                14,
                61,
                63
            ],
            leg_3_servos=[
                14,
                61,
                63
            ]
        )

legs.move([850, 425, 595], [850, 425, 595], [850, 425, 595], [850, 425, 595], 0, [80, 80, 80], True)