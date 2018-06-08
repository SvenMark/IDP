import sys
import time

sys.path.insert(0, '../../../src')


def run(name, stop_motors, vertical_speed, horizontal_speed, dead_zone, speed_factor, movement, shared_object):
    print("run " + str(name))

    while not shared_object.has_to_stop():
        movement.tracks.handle_controller_input(stop_motors=stop_motors,
                                                vertical_speed=horizontal_speed * speed_factor,
                                                horizontal_speed=vertical_speed * speed_factor,
                                                dead_zone=dead_zone)

    # Notify shared object that this thread has been stopped
    shared_object.has_been_stopped()
