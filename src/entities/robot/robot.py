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



