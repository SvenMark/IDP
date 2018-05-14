class Movement(object):
    """
    Base class for movement
    """

    def __init__(self, limbs, lights):
        self.limbs = limbs
        self.lights = lights

    def forward(self):
        for limb in self.limbs:
            limb.forward()

    def backward(self):
        for limb in self.limbs:
            limb.backward()
