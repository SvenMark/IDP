import unittest

from entities.movement.legs import Legs
from entities.movement.tracks import Tracks
from entities.movement.limb.tire import Tire
from entities.movement.movement import Movement


class CommonTestClass(unittest.TestCase):
    def setUp(self):
        limbs = [
            Legs(leg_0_servos=[
                    14,
                    61,
                    63
                ],
                leg_1_servos=[
                    21,
                    31,
                    53
                ],
                leg_2_servos=[
                    61,
                    63,
                    111
                ],
                leg_3_servos=[
                    111,
                    111,
                    111
                ]
            ),
            Tracks(track_0_pin=18, track_1_pin=13),
            Tire()
        ]

        lights = []

        self.movement = Movement(limbs, lights)

    def test_forward(self):
        # test if implemented
        self.assertIsNone(self.movement.forward())
        self.assertIsNone(self.movement.backward())
