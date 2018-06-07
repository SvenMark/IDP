from entities.movement.limb.leg import Leg
from entities.movement.tracks import Tracks
from entities.robot.robot import Robot


# todo implement according to truth
def run():
    lights = []
    limbs = [
        # Leg(),
        # Tire(),
        # Tracks()
    ]
    name = 'Boris'

    boris = Robot(name, limbs, lights)
