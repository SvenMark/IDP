import sys
import time

sys.path.insert(0, '../../../src')

from entities.movement.sequences.sequences import *


def run(name, control):
    movement = control.movement
    emotion = control.emotion
    shared_object = control.shared_object
    speed_factor = 1
    dead_zone = control.dead_zone

    print("[RUN] " + str(name))

    if hasattr(movement, 'legs'):
        movement.legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=None, sequence=extend_arms)

    while not shared_object.has_to_stop():
        grab = shared_object.bluetooth_settings.d

        movement.tracks.handle_controller_input(stop_motors=shared_object.bluetooth_settings.s,
                                                vertical_speed=shared_object.bluetooth_settings.h * speed_factor,
                                                horizontal_speed=shared_object.bluetooth_settings.v * speed_factor,
                                                dead_zone=dead_zone)

        if hasattr(movement, 'grabber'):
            if movement.grabber.grabbed and grab is 0:
                movement.grabber.loosen(150)
            if not movement.grabber.grabbed and grab is 1:
                movement.grabber.grab_flag(150)

    if hasattr(movement, 'legs'):
        movement.legs.retract()

    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()
