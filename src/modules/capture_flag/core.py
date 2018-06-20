import sys
import time

sys.path.insert(0, '../../../src')


def run(name, movement, speed_factor, shared_object, dead_zone, emotion):
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
            movement.legs.move()

        if movement.grabber.grabbed and grab is 0:
            movement.grabber.loosen(150)
        if not movement.grabber.grabbed and grab is 1:
            movement.grabber.grab(100, True)

    if hasattr(movement, 'legs'):
        movement.legs.retract()

    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()
