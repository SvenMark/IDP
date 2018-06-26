import sys
import time
from threading import Timer

import RPi.GPIO as GPIO
from entities.movement.sequences.sequences import *
sys.path.insert(0, '../../../src')

seconds = 0


def routine():
    global seconds
    seconds += 1
    t = Timer(1, routine)
    t.start()


def run(name, control):
    movement = control.movement
    emotion = control.emotion
    shared_object = control.shared_object
    speed_factor = control.speed_factor
    dead_zone = control.dead_zone

    routine()

    print("[RUN] " + str(name))

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    beat_led_pin = 16
    beat_detect_pin = 20
    beat_pin = 21
    sequences = [clap, ballerina, extend_arms, vagedraai, runningman, shakeass,
                dabrechts, dablinks, dabrechts, dablinks, dabrechts]
    GPIO.setup(beat_led_pin, GPIO.OUT)
    GPIO.setup(beat_detect_pin, GPIO.OUT)
    GPIO.setup(beat_pin, GPIO.IN)
    GPIO.output(beat_led_pin, 1)
    GPIO.output(beat_detect_pin, 1)

    while not shared_object.has_to_stop():
        print("test")
        if GPIO.input(beat_pin):
            print(str(seconds))
            if seconds < 5:
                movement.tracks.tracks.turn_left(50, 50, 0, 5)
            elif seconds < 13:
                pass
            elif seconds < 21:
                pass
            elif seconds < 36:
                pass
            elif seconds < 48:
                pass
            elif seconds < 54:
                pass
            elif seconds < 61:
                pass
            elif seconds < 93:
                pass
            elif seconds < 102:
                pass
            elif seconds < 105:
                pass
            elif seconds < 120:
                pass
            else:
                print("DONE")
                shared_object.stop = True

    GPIO.output(beat_led_pin, 0)
    GPIO.output(beat_detect_pin, 0)
    GPIO.cleanup(beat_led_pin)
    GPIO.cleanup(beat_detect_pin)
    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()
