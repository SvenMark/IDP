import sys
import time

sys.path.insert(0, '../../../src')


def run(name, shared_object, movement):
    print("run " + str(name))

    legs = movement[0]
    tracks = movement[1]

    while not shared_object.has_to_stop():
        print("Doing calculations and stuff")

        tracks.turn_right(100, 100, 5, 10)

    # Notify shared object that this thread has been stopped
    shared_object.has_been_stopped()