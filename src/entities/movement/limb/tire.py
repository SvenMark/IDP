from entities.movement.limb.limb import Limb


class Tire(Limb):
    def __init__(self):
        super(Tire, self).__init__('tire')
