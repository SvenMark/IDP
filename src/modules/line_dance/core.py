import time
import RPi.GPIO as GPIO
import pyaudio
import numpy as np
import sys

sys.path.insert(0, '../../../src')

from entities.audio.beat_detection import BeatDetection


def run(name, control):
    movement = control.movement
    shared_object = control.shared_object
    speed_factor = control.speed_factor
    dead_zone = control.dead_zone

    print("[RUN] " + str(name))

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
    GPIO.cleanup()

    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()


# End of def run
if __name__ == '__main__':
    run()
