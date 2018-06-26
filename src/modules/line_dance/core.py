import time
import RPi.GPIO as GPIO
import pyaudio
import numpy as np
import sys

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

    while not shared_object.has_to_stop():
        if GPIO.input(beat_pin):
            print("Beat detected")
            if hasattr(movement, 'legs'):
                legs_not_ready = [elem for elem in movement.legs if not elem.ready()]
                if legs_not_ready > 0:
                    print("Not all legs ready so do nothing")
                else:
                    if movement.legs.deployed:
                        movement.tracks.turn_right(40, 40, 0.1, 0)
                        movement.legs.retract(100)
                    else:
                        movement.tracks.turn_left(40, 40, 0.1, 0)
                        movement.legs.deploy(100)
        else:
            print("No beat detected")
        time.sleep(0.1)

    GPIO.output(beat_led_pin, 0)
    GPIO.output(beat_detect_pin, 0)
    GPIO.cleanup()

    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()
