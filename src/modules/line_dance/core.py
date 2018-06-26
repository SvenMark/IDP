import time
import RPi.GPIO as GPIO
import pyaudio
import numpy as np
import sys
import random
from entities.movement.sequences.sequences import *

sys.path.insert(0, '../../../src')


def run(name, control):
    movement = control.movement
    shared_object = control.shared_object
    speed_factor = control.speed_factor
    dead_zone = control.dead_zone

    print("[RUN] " + str(name))

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    beat_led_pin = 16
    beat_detect_pin = 20
    beat_pin = 21

    GPIO.setup(beat_led_pin, GPIO.OUT)
    GPIO.setup(beat_detect_pin, GPIO.OUT)
    GPIO.setup(beat_pin, GPIO.IN)
    GPIO.output(beat_led_pin, 1)
    GPIO.output(beat_detect_pin, 1)

    sequences = [clap, ballerina, extendarms, vagedraai, runningman, shakeass]
    current = random.choice(sequences)
    step = 0

    while not shared_object.has_to_stop():
        if GPIO.input(beat_pin):
            print("Beat detected")
            if hasattr(movement, 'legs'):
                legs_not_ready = [elem for elem in movement.legs if not elem.ready()]
                if len(legs_not_ready) > 0:
                    print("Not all legs ready so do nothing")
                else:
                    movement.legs.run_sequence(speeds=[150, 150, 150],
                                               self_update=True,
                                               sequences=[step],
                                               sequence=current)
                    step += 1
                    if step >= len(current):
                        step = 0
                        current = random.choice(sequences)
        else:
            print("No beat detected")
        time.sleep(0.1)

    GPIO.output(beat_led_pin, 0)
    GPIO.output(beat_detect_pin, 0)
    GPIO.cleanup(beat_led_pin)
    GPIO.cleanup(beat_detect_pin)

    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()
