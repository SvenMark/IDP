import unittest

from entities.movement.limb.leg import Leg
from entities.movement.limb.tire import Tire
from entities.movement.limb.track import Track
from entities.movement.movement import Movement


class CommonTestClass(unittest.TestCase):
    def setUp(self):
        limbs = [
            Leg(),
            Tire(),
            Track()
        ]
        lights = []
        self.movement = Movement(limbs, lights)

    def test_forward(self):
        # test if implemented
        self.assertIsNone(self.movement.forward())
        self.assertIsNone(self.movement.backward())
