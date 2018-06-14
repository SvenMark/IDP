import unittest
import sys

sys.path.insert(0, '../../../src')

from entities.movement.legs import Legs
from entities.movement.tracks import Tracks
from entities.movement.movement import Movement
from entities.movement.sequences.sequences import *


class CommonTestClass(unittest.TestCase):
    """
    Setup joints for robot, also register leds and audio if required
    """
    def setUp(self):
        limbs = [
            Legs(leg_0_servos=[
                14,
                61,
                63
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
            ),
            Tracks(track_0_pin=18,
                   track_1_pin=13,
                   track_0_forward=22,
                   track_0_backward=27,
                   track_1_forward=10,  # 19
                   track_1_backward=9),  # 26
        ]

        lights = []

        self.movement = Movement(limbs, lights)

    def test_forward(self):
        # test if implemented
        self.assertIsNone(self.movement.forward())
        self.assertIsNone(self.movement.backward())
        self.assertIsNone(self.movement.legs.run_sequence([250, 250, 250],
                                                          self_update=True,
                                                          sequences=None,
                                                          sequence=forward))
