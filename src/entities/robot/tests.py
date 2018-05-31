import unittest
import sys

sys.path.insert(0, '../../../src')

from entities.movement.limb.tire import Tire
from entities.movement.tracks import Tracks
from entities.movement.legs import Legs
from entities.robot.robot import Robot

TYPES = ['legs',
         'tracks',
         'tire']


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
        self.boris = Robot('Boris', limbs, lights)

    def test_name(self):
        self.assertEqual(self.boris.name, 'Boris')

    def test_limbs(self):
        self.assertEqual(self.boris.get_limb_count, 3)

        count = 0
        for limb in self.boris.limbs:
            self.assertIsInstance(limb, Tracks or Legs or Tire)
            self.assertIsNotNone(limb.limb_type)

            # check correct type
            self.assertEqual(limb.limb_type, TYPES[count])
            count += 1


if __name__ == '__main__':
    unittest.main()
