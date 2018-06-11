import sys
import time

sys.path.insert(0, '../../../src')

from entities.movement.sequences.sequences import *


def run(name, movement, s, v, h, speed_factor, shared_object):
    print("run " + str(name))

    while not shared_object.has_to_stop():
        movement.tracks.handle_controller_input(stop_motors=s,
                                                vertical_speed=h * speed_factor,
                                                horizontal_speed=v * speed_factor,
                                                dead_zone=5)
        movement.legs.run_sequence([150, 150, 150], True, None, march)

    # Notify shared object that this thread has been stopped
    print("Stopped " + str(name))
    shared_object.has_been_stopped()
