from entities.movement.limb.limb import Limb


class Leg(Limb):
    def __init__(self):
        super(Leg, self).__init__('leg')

    def forward(self):
        print('{} forward'.format(self.limb_type))

    def backward(self):
        print('{} backward'.format(self.limb_type))
