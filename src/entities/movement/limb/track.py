from entities.movement.limb.limb import Limb


class Track(Limb):
    def __init__(self):
        super(Track, self).__init__('tire')
