import sys

sys.path.insert(0, '../../../src')


class Movement(object):
    """
    Base class for movement
    """

    def __init__(self, limbs, lights):
        """
        Constructor for movement
        :param limbs: Array of limbs
        :param lights: Array of lights
        """
        self.limbs = limbs
        self.lights = lights
        self.legs = limbs[0]
        self.tracks = limbs[1]
        self.grabber = limbs[2]

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
