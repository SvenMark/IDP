import unittest

from entities.movement.limb.leg import Leg
from entities.movement.limb.limb import Limb
from entities.movement.limb.tire import Tire
from entities.movement.limb.track import Track
from entities.robot.robot import Robot


class CommonTestClass(unittest.TestCase):

    def setUp(self):
        limbs = [
            Leg(),
            Tire(),
            Track()
        ]
        self.boris = Robot('Boris', limbs, [])

    def test_name(self):
        self.assertEqual(self.boris.name, 'Boris')

    def test_limbs(self):
        self.assertEqual(self.boris.get_limb_count, 3)
        for limb in self.boris.limbs:
            # Inherited of Limb
            self.assertIsInstance(limb, Limb)
            self.assertIsNotNone(limb.limb_type)


if __name__ == '__main__':
    unittest.main()