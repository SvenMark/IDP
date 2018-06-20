import sys
import time

sys.path.insert(0, '../../../src')


def run(name, movement, speed_factor, shared_object, dead_zone):
    print("[RUN] " + str(name))

    while not shared_object.has_to_stop():

        s = shared_object.bluetooth_settings.s
        v = shared_object.bluetooth_settings.v
        h = shared_object.bluetooth_settings.h
        d = shared_object.bluetooth_settings.d
        x = shared_object.bluetooth_settings.x
        y = shared_object.bluetooth_settings.y

        # Send controller tracks input to tracks
        movement.tracks.handle_controller_input(stop_motors=s,
                                                vertical_speed=h * speed_factor,
                                                horizontal_speed=v * speed_factor,
                                                dead_zone=dead_zone)

        if hasattr(movement, 'legs'):
            # Send controller leg input to legs
            movement.legs.handle_controller_input(deploy=d,
                                                  x_axis=x,
                                                  y_axis=y)

    # Notify shared object that this thread has been stopped
    print("[STOPPED] {}".format(name))
    shared_object.has_been_stopped()
