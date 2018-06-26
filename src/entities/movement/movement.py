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

    def move_towards(self, offset, torque=1.2):
        left_speed = 60
        right_speed = 60
        if offset < 0:
            left_speed += offset * torque
        else:
            right_speed -= offset * torque
        self.tracks.forward(duty_cycle_track_left=right_speed,
                            duty_cycle_track_right=left_speed,
                            delay=0, acceleration=0)
