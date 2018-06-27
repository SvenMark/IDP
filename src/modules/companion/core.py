import sys
import threading
import time

sys.path.insert(0, '../../../src')

from entities.vision.helpers.json_handler import JsonHandler
from entities.vision.helpers.vision_helper import Color


def run(name, control):
    movement = control.movement
    shared_object = control.shared_object
    speed_factor = control.speed_factor
    dead_zone = control.dead_zone
    vision = control.vision
    vision_settings = control.vision.settings
    emotion = control.emotion


    print("[RUN] " + str(name))

    # while not shared_object.has_to_stop():
    emotion.set_emotion("mad")
    #if hasattr(movement, 'grabber'):
    #    movement.grabber.grab(150, True)
    #    movement.grabber.loosen(150)
    time.sleep(5)
    emotion.set_emotion("happy")
    time.sleep(5)
    emotion.set_emotion("sad")
    time.sleep(11)
    emotion.set_emotion("pain")
    time.sleep(5)
    emotion.set_emotion("confused")
    time.sleep(5)
    emotion.set_emotion("searching")
    time.sleep(5)

    # Notify shared object that this thread has been stopped
    print("[STOPPED] {}".format(name))
    shared_object.has_been_stopped()
