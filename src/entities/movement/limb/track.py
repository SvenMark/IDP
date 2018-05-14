from entities.movement.limb.limb import Limb


class Track(Limb):
    def __init__(self):
        super(Track, self).__init__('track')

    def forward(self):
        print('{} forward'.format(self.limb_type))

    def backward(self):
        print('{} backward'.format(self.limb_type))
