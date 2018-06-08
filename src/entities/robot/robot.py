import sys

sys.path.insert(0, '../../../src')

from entities.movement.movement import Movement
from entities.vision.vision import Vision


class Robot(object):
    """
    Robot class
    """

    def __init__(self, name, limbs, lights, color_range):
        """
        Constructor for the robot class
        :param name: Name for the robot
        :param limbs: Array of limbs
        :param lights: Array of lights
        """
        self.name = name
        self.limbs = limbs
        self.lights = lights
        self.movement = Movement(limbs, lights)
        self.vision = Vision(color_range,
                             saved_buildings=None,
                             img=None,
                             min_block_size=1000,
                             max_block_size=10000,
                             settings=None)

    @property
    def get_name(self):
        return self.name

    @property
    def get_limb_count(self):
        return len(self.limbs)

    @property
    def get_light_count(self):
        return len(self.lights)
