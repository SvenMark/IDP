import sys

sys.path.insert(0, '../../../src')

from entities.movement.movement import Movement
# from entities.vision.vision import Vision
from entities.connection.bluetooth_controller import BluetoothController


class Robot(object):
    """
    Robot class
    """

    def __init__(self, name, limbs, lights, bluetooth_address):
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
        # self.vision = Vision()
        self.controller = BluetoothController(limbs, bluetooth_address)

    @property
    def get_name(self):
        return self.name

    @property
    def get_limb_count(self):
        return len(self.limbs)

    @property
    def get_light_count(self):
        return len(self.lights)
