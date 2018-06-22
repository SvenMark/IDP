import sys

sys.path.insert(0, '../../../src')


class Movement(object):
    """
    Base class for movement
    """

    def __init__(self, limbs):
        """
        Constructor for movement
        :param limbs: Array of limbs
        """
        self.limbs = limbs
        for limb in limbs:
            if limb.type == 'legs':
                self.legs = limb
            if limb.type == 'tracks':
                self.tracks = limb
            if limb.type == 'grabber':
                self.grabber = limb

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

    def move_towards(self, percentage, torque=0.5):
        left_speed = 25
        right_speed = 25
        if percentage < 50:
            left_speed = left_speed - percentage * torque
        else:
            right_speed = right_speed - (percentage - 50) * torque

        self.tracks.forward(left_speed, right_speed, 0.3, 0.3)
