import sys

sys.path.insert(0, '../../../src')

from entities.movement.grabber import Grabber
from entities.movement.legs import Legs
from entities.movement.tracks import Tracks


class Movement(object):
    """
    Base class for movement
    """

    def __init__(self, limbs):
        """
        Constructor for movement
        :param limbs: Array of limbs
        :param lights: Array of lights
        """
        self.limbs = limbs
        for limb in limbs:
            if type(limb) is Grabber:
                self.grabber = limb
            if type(limb) is Legs:
                self.legs = Legs
            if type(limb) is Tracks:
                self.tracks = limb

    def forward(self):
        self.tracks.forward(duty_cycle=20,
                            delay=0,
                            acceleration=2)

    def backward(self):
        self.tracks.backward(duty_cycle=20,
                             delay=0,
                             acceleration=2)

    def turn_left(self):
        self.tracks.turn_left(duty_cycle_track_left=70,
                              duty_cycle_track_right=20,
                              delay=8,
                              acceleration=12)

    def turn_right(self):
        self.tracks.turn_right(duty_cycle_track_left=70,
                               duty_cycle_track_right=20,
                               delay=8,
                               acceleration=12)
