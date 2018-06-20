import sys
import time

sys.path.insert(0, '../../../src')


def run(name, movement, s, v, h, speed_factor, shared_object, grab):
    print("[RUN] " + str(name))

    if hasattr(movement, 'legs'):
        movement.legs.deploy()

    while not shared_object.has_to_stop():

        movement.tracks.handle_controller_input(stop_motors=s,
                                                vertical_speed=h * speed_factor,
                                                horizontal_speed=v * speed_factor,
                                                dead_zone=5)

        # Extend legs to max
        movement.legs.move()

        if movement.grabber.grabbed and grab is 0:
            movement.grabber.loosen([150, 150, 150])
        if not movement.grabber.grabbed and grab is 1:
            movement.grabber.grab([100, 100, 100])

    if hasattr(movement, 'legs'):
        movement.legs.retract()

    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()
