import sys
import time

sys.path.insert(0, '../../../src')

from entities.movement.sequences.sequences import *


def run(name, control):
    movement = control.movement
    emotion = control.emotion
    shared_object = control.shared_object
    speed_factor = control.speed_factor
    dead_zone = control.dead_zone

    print("[RUN] " + str(name))

    emotion.set_emotion('anthem')

    while not shared_object.has_to_stop():
        movement.tracks.handle_controller_input(stop_motors=shared_object.bluetooth_settings.s,
                                                vertical_speed=shared_object.bluetooth_settings.h * speed_factor,
                                                horizontal_speed=shared_object.bluetooth_settings.v * speed_factor,
                                                dead_zone=dead_zone)
        if hasattr(movement, 'legs'):
            movement.legs.run_sequence([100, 100, 100], True, None, march)

    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()
