import os
import time
import sys
sys.path.insert(0, '../../../src')


def run(shared_object):
    print("run element2")

    while not shared_object.has_to_stop():
        print("Doing calculations and stuff")
        time.sleep(0.5)

    # Notify shared object that this thread has been stopped
    shared_object.has_been_stopped()

