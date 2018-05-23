from entities.movement.movement import Movement


class Robot(object):
    """
    Robot class
    """

    def __init__(self, name, tracks, lights):
        self.name = name
        # self.limbs = limbs
        self.lights = lights
        # self.movement = Movement(limbs, lights)
        self.tracks = tracks

    @property
    def get_name(self):
        return self.name

    @property
    def get_light_count(self):
        return len(self.lights)
