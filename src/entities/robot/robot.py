from entities.movement.movement import Movement


class Robot(object):
    """
    Robot class
    """

    def __init__(self, name, limbs, lights):
        self.name = name
        self.limbs = limbs
        self.lights = lights
        self.movement = Movement(limbs, lights)

    @property
    def get_name(self):
        return self.name

    @property
    def get_limb_count(self):
        return len(self.limbs)

    @property
    def get_light_count(self):
        return len(self.lights)
