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
