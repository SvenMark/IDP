import sys
import time
sys.path.insert(0, '../../../src')

from entities.movement.limb.leg import Leg
from entities.movement.tracks import Tracks
from entities.robot.robot import Robot


# todo implement according to truth
def run(shared_object):
    print("Running element 1")

    while not shared_object.has_to_stop():
        print("Doing calculations and stuff")
        time.sleep(0.5)

    # Notify shared object that this thread has been stopped
    shared_object.has_been_stopped()

