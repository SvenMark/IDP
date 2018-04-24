class Movement(object):
    """
    Base class for movement
    """

    def __init__(self, limbs, lights):
        self.limbs = limbs
        self.lights = lights

    @property
    def get_limb_count(self):
        return len(self.limbs)

    @property
    def get_light_count(self):
        return len(self.lights)
