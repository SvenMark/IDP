import unittest

from entities.movement.limb.leg import Leg
from entities.movement.limb.limb import Limb
from entities.movement.limb.tire import Tire
from entities.movement.tracks import Tracks
from entities.robot.robot import Robot

TYPES = ['leg',
         'tire',
         'tracks']


class CommonTestClass(unittest.TestCase):

    def setUp(self):
        limbs = [
            Leg(),
            Tire(),
            Tracks()
        ]
        self.boris = Robot('Boris', limbs, [])

    def test_name(self):
        self.assertEqual(self.boris.name, 'Boris')

    def test_limbs(self):
        self.assertEqual(self.boris.get_limb_count, 3)

        count = 0
        for limb in self.boris.limbs:
            # Inherited of Limb
            self.assertIsInstance(limb, Limb)
            self.assertIsNotNone(limb.limb_type)

            # check correct type
            self.assertEqual(limb.limb_type, TYPES[count])
            count += 1


if __name__ == '__main__':
    unittest.main()
