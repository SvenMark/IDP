from entities.movement.limb.limb import Limb


class Tire(Limb):
    def __init__(self):
        super(Tire, self).__init__('tire')
        self.type = 'tire'

    def forward(self):
        print('{} forward'.format(self.limb_type))

    def backward(self):
        print('{} backward'.format(self.limb_type))
