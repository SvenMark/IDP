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

    if hasattr(movement, 'legs'):
        movement.legs.deploy()

    while not shared_object.has_to_stop():
        grab = shared_object.bluetooth_settings.d

        movement.tracks.handle_controller_input(stop_motors=shared_object.bluetooth_settings.s,
                                                vertical_speed=shared_object.bluetooth_settings.h * speed_factor,
                                                horizontal_speed=shared_object.bluetooth_settings.v * speed_factor,
                                                dead_zone=dead_zone)

        # Extend legs to max
        if hasattr(movement, 'legs'):
            # TODO: add correct positions for extending
            movement.legs.move(
                leg_0_moves=[],
                leg_1_moves=[],
                leg_2_moves=[],
                leg_3_moves=[],
                speeds=[200, 200, 200],
                self_update=True)

        if movement.grabber.reposition:
            if movement.grabber.grabbed and grab is 1:
                movement.grabber.loosen(150)
            if not movement.grabber.grabbed and grab is 0:
                movement.grabber.grab(100, True)
        else:
            if movement.grabber.grabbed and grab is 0:
                movement.grabber.loosen(150)
            if not movement.grabber.grabbed and grab is 1:
                movement.grabber.grab(100, True)

    if hasattr(movement, 'legs'):
        movement.legs.retract()

    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()
