from entities.movement.tracks import Tracks


class Movement(object):
    """
    Base class for movement
    """

    def __init__(self, limbs, lights):
        legs = limbs[0]
        tracks = limbs[1]
        tire = limbs[2]

        for limb in limbs:
            if limb.type == 'track':
                tracks.append(limb)
            elif limb.type == 'leg':
                legs.append(limb)
            elif limb.type == 'tire':
                tire.append(limb)

        self.limbs = limbs
        self.lights = lights

        self.legs = legs
        self.tracks = tracks
        self.tire = tire

    def forward(self):
        self.tracks.forward()

    def backward(self):
        self.tracks.backward()

    def turn_left(self):
        self.tracks.turn_left()

    def turn_right(self):
        self.tracks.turn_right()
