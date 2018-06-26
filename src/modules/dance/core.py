import sys
import time
import RPi.GPIO as GPIO
from entities.movement.sequences.sequences import *
sys.path.insert(0, '../../../src')


def run(name, control):
    movement = control.movement
    emotion = control.emotion
    shared_object = control.shared_object
    speed_factor = control.speed_factor
    dead_zone = control.dead_zone

    print("[RUN] " + str(name))

    #GPIO.setmode(GPIO.BCM)
    #GPIO.setwarnings(False)

    #beat_led_pin = 16
    #beat_detect_pin = 20
    #beat_pin = 21
    #sequences = [clap, ballerina, extend_arms, vagedraai, runningman, shakeass,
    #             dabrechts, dablinks, dabrechts, dablinks, dabrechts]
    #GPIO.setup(beat_led_pin, GPIO.OUT)
    #GPIO.setup(beat_detect_pin, GPIO.OUT)
    #GPIO.setup(beat_pin, GPIO.IN)
    #GPIO.output(beat_led_pin, 1)
    #GPIO.output(beat_detect_pin, 1)

    #step = 0
    #current = 0

    while not shared_object.has_to_stop():




        # Als hij een beat hoort
        #if GPIO.input(beat_pin):
        #    movement.legs.move(sequences[current][step][0], sequences[current][step][1],sequences[current][step][2],
        #                       sequences[current][step][3], [100, 100, 100], True)
        #    step += 1
        #    if step >= len(sequences[current]):
        #        step = 0
        #        current += 1
        #        if current >= len(sequences):
        #            shared_object.stop = True

    #GPIO.output(beat_led_pin, 0)
    #GPIO.output(beat_detect_pin, 0)
    #GPIO.cleanup(beat_led_pin)
    #GPIO.cleanup(beat_detect_pin)
    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()
