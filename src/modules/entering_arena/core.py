import sys
import time

sys.path.insert(0, '../../../src')

from entities.movement.sequences.sequences import *
from entities.visual.emotion import Emotion
from entities.audio.speak import Speak
from entities.audio.audio import Audio


def run(name, movement, speed_factor, shared_object):
    print("[RUN] " + str(name))

    audio = Audio()
    emotion = Emotion(audio.speak)
    emotion.set_emotion('anthem')

    while not shared_object.has_to_stop():
        s = shared_object.bluetooth_settings.s
        v = shared_object.bluetooth_settings.v
        h = shared_object.bluetooth_settings.h

        movement.tracks.handle_controller_input(stop_motors=s,
                                                vertical_speed=h * speed_factor,
                                                horizontal_speed=v * speed_factor,
                                                dead_zone=5)
        movement.legs.run_sequence([150, 150, 150], True, None, march)

    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()
