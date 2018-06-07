import os
import time
import sys
sys.path.insert(0, '../../src')

from entities.audio.listen import Listen
from entities.audio.microphone_recognition import Microphone_recognition
from entities.audio.speak import Speak


def run(shared_object):
    print("run element2")

    while not shared_object.has_to_stop():
        print("Doing calculations and stuff")
        time.sleep(0.5)

    # Notify shared object that this thread has been stopped
    shared_object.has_been_stopped()

