import time
import RPi.GPIO as GPIO
import pyaudio
import numpy as np
from entities.audio.beat_detection import BeatDetection

import sys
sys.path.insert(0, '../../../src')


def run(name, movement, shared_object):
    print("run " + str(name))

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    pin_jurjen1 = 16
    pin_jurjen2 = 20  # clean code
    GPIO.setup(pin_jurjen1, GPIO.OUT)
    GPIO.setup(pin_jurjen2, GPIO.OUT)
    GPIO.output(pin_jurjen1, 1)
    GPIO.output(pin_jurjen2, 1)

    p = pyaudio.PyAudio()  # start the PyAudio class
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True,
                    frames_per_buffer=10000)  # uses default input device

    test = BeatDetection()
    test.detect(stream, 10)

    stream.stop_stream()
    stream.close()
    p.terminate()

    while not shared_object.has_to_stop():
        print("Doing calculations and stuff")
        time.sleep(0.5)

    GPIO.output(pin_jurjen1, 0)
    GPIO.output(pin_jurjen2, 0)

    # Notify shared object that this thread has been stopped
    print("Stopped" + str(name))
    shared_object.has_been_stopped()


# End of def run
if __name__ == '__main__':
    run()
