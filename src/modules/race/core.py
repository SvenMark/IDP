import sys
import time

sys.path.insert(0, '../../../src')


def run(name, movement, speed_factor, shared_object, dead_zone):
    print("[RUN] " + str(name))

    while not shared_object.has_to_stop():

        stop_motors = shared_object.bluetooth_settings.s
        vertical_speed = shared_object.bluetooth_settings.v
        horizontal_speed = shared_object.bluetooth_settings.h

        movement.tracks.handle_controller_input(stop_motors=stop_motors,
                                                vertical_speed=horizontal_speed * speed_factor,
                                                horizontal_speed=vertical_speed * speed_factor,
                                                dead_zone=dead_zone)

    # Notify shared object that this thread has been stopped
    print("[STOPPED] {}".format(name))
    shared_object.has_been_stopped()
