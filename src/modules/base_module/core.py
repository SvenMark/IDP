import sys
import time

sys.path.insert(0, '../../../src')


def run(name, control):
    movement = control.movement
    emotion = control.emotion
    shared_object = control.shared_object
    speed_factor = control.speed_factor
    dead_zone = control.dead_zone

    print("[RUN] " + str(name))

    while not shared_object.has_to_stop():

        # Send controller tracks input to tracks
        movement.tracks.handle_controller_input(stop_motors=shared_object.bluetooth_settings.s,
                                                vertical_speed=shared_object.bluetooth_settings.h * speed_factor,
                                                horizontal_speed=shared_object.bluetooth_settings.v * speed_factor,
                                                dead_zone=dead_zone)

        if hasattr(movement, 'legs'):
            # Send controller leg input to legs
            movement.legs.handle_controller_input(deploy=shared_object.bluetooth_settings.d,
                                                  x_axis=shared_object.bluetooth_settings.x,
                                                  y_axis=shared_object.bluetooth_settings.y)

    # Notify shared object that this thread has been stopped
    print("[STOPPED] {}".format(name))
    shared_object.has_been_stopped()
