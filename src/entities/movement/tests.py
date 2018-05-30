import unittest
import sys

from entities.movement.legs import Legs
from entities.movement.tracks import Tracks
from entities.movement.limb.tire import Tire
from entities.movement.movement import Movement

sys.path.insert(0, '../../../src')


class CommonTestClass(unittest.TestCase):
    def setUp(self):
        limbs = [
            Legs(leg_0_servos=[
                    14,
                    61,
                    63
                ]
                # leg_1_servos=[
                #     14,
                #     61,
                #     63
                # ],
                # leg_2_servos=[
                #     14,
                #     61,
                #     63
                # ],
                # leg_3_servos=[
                #     14,
                #     61,
                #     63
                # ]
            ),
            Tracks(track_0_pin=18, track_1_pin=13),
            Tire(servo_id=69, position=500)
        ]

        lights = []

        self.movement = Movement(limbs, lights)

    def test_forward(self):
        # test if implemented
        self.assertIsNone(self.movement.forward())
        self.assertIsNone(self.movement.backward())
        self.assertIsNone(self.movement.legs.move(leg_0_moves=[530, 766, 850],
                                                  leg_1_moves=[650, 400, 400],
                                                  leg_2_moves=[400, 400, 400],
                                                  leg_3_moves=[600, 400, 400],
                                                  delay=0,
                                                  speeds=[200, 200, 200]))
