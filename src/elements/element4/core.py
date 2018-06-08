import time

import pyaudio
import numpy as np
from entities.audio.beat_detection import BeatDetection

import sys
sys.path.insert(0, '../../../src')


def run(shared_object):
    print("run element4")

    p = pyaudio.PyAudio()  # start the PyAudio class
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True,
                    frames_per_buffer=10000)  # uses default input device

    test = BeatDetection()
    while True:
        test.detect(stream)

    stream.stop_stream()
    stream.close()
    p.terminate()

    while not shared_object.has_to_stop():
        print("Doing calculations and stuff")
        time.sleep(0.5)

    # Notify shared object that this thread has been stopped
    shared_object.has_been_stopped()


# End of def run
if __name__ == '__main__':
    run()
