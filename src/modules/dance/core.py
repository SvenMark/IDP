import sys
import time

sys.path.insert(0, '../../../src')


def run(name, control):
    movement = control.movement
    emotion = control.emotion
    shared_object = control.shared_object
    speed_factor = control.speed_factor
    dead_zone = control.dead_zone

    BPM = 150
    delay = 60 / 150

    print("[RUN] " + str(name))

    while not shared_object.has_to_stop():
        print("Doing calculations and stuff")

        movement.tracks.turn_right(30, 30, 0.1, 0)
        time.sleep(delay)

    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()
