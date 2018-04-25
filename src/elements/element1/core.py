from entities.movement.limb.leg import Leg
from entities.movement.limb.tire import Tire
from entities.movement.limb.track import Track
from entities.robot.robot import Robot


# todo implement according to truth
def run():
    lights = []
    limbs = [
        Leg(),
        Tire(),
        Track()
    ]
    name = 'Boris'

    boris = Robot(name, limbs, lights)
    boris.movement.forward()
    boris.movement.backward()
