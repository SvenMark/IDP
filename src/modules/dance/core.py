import sys
import time

sys.path.insert(0, '../../../src')


def run(name, movement, shared_object, emotion):
    print("[RUN] " + str(name))

    while not shared_object.has_to_stop():
        print("Doing calculations and stuff")

        movement.tracks.turn_right(30, 30, 0.1, 0)
        time.sleep(0.2)

    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()
