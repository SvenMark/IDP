class Limb(object):
    """
    Base class for limb
    """
    def __init__(self, limb_type):
        self.limb_type = limb_type

    @property
    def get_limb_type(self):
        return self.limb_type

    def forward(self):
        raise NotImplementedError('Should be overridden in the child class')

    def backward(self):
        raise NotImplementedError('Should be overridden in the child class')
