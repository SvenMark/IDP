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
    
    beat_led_pin = 16
    beat_detect_pin = 20  # clean code
    beat_pin = 21

    GPIO.setup(beat_led_pin, GPIO.OUT)
    GPIO.setup(beat_detect_pin, GPIO.OUT)
    GPIO.output(beat_led_pin, 1)
    GPIO.output(beat_detect_pin, 1)

    p = pyaudio.PyAudio()  # start the PyAudio class
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True,
                    frames_per_buffer=10000)  # uses default input device

    test = BeatDetection()
    test.detect(stream, 10)

    stream.stop_stream()
    stream.close()
    p.terminate()

    while not shared_object.has_to_stop():
        if GPIO.input(beat_pin) is True:
            if movement.legs.deployed:
                movement.legs.retract()
            else:
                movement.legs.deploy()

    GPIO.output(beat_led_pin, 0)
    GPIO.output(beat_detect_pin, 0)
    GPIO.cleanup()

    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()


# End of def run
if __name__ == '__main__':
    run()
