import sys
import threading
import time

sys.path.insert(0, '../../../src')

from entities.vision.vision import Vision
from entities.vision.helpers.vision_helper import Color, BuildingSide
from entities.vision.recognize_settings import Recognize_settings
from entities.vision.helpers.json_handler import Json_Handler
from entities.movement.movement import Movement
from entities.threading.utils import SharedObject


# from entities.movement.tracks import Tracks

def run(name, movement, s, v, h, speed_factor, shared_object, grab):
    print("[RUN] " + str(name))
    json_handler = Json_Handler()
    color_range = json_handler.get_color_range()
    tape = [Color("zwarte_tape", [0, 0, 0], [15, 35, 90])]

    saved_buildings = json_handler.get_save_buildings()

    settings = Recognize_settings()
    vision = Vision(color_range=color_range,
                    saved_buildings=saved_buildings,
                    settings=settings, min_block_size=0)

    rotate_speed = 50
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == "hsv" and sys.argv[2] == "picker":
                threading.Thread(target=vision.helpers.hsv_picker.run).start()
            elif sys.argv[1] == "saving":
                threading.Thread(target=vision.saving.run).start()
            elif sys.argv[1] == "recognize":
                threading.Thread(target=vision.recognize.run).start()
            else:
                print("[ERROR] Wrong argument given..")
                run(name, movement, shared_object)

        # Default no argument
        else:
            threading.Thread(target=vision.recognize.run).start()
    except AttributeError:
        print("[ERROR] Something went wrong..")
        run(name, movement, shared_object)

    while not shared_object.has_to_stop():

        movement.grabber.grab([80, 80, 80])
        if movement.grabber.reposition is True:
            movement.tracks.forward(20, 20, 10, 0.5)
            movement.grabber.reposition = False

    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()


run("", "", SharedObject)

# TESTING
# tracks = Tracks(track_0_pin=18,
#                 track_1_pin=13,
#                 track_0_forward=22,
#                 track_0_backward=27,
#                 track_1_forward=10,
#                 track_1_backward=9)
#
# while True:
#     if settings.update:
#         settings.update = False
#         if settings.new:
#             tracks.stop()
#             print("Moving to building " + str(settings.current_building)
#                   + ", position: " + str(settings.current_position))
#
#             settings.new = False
#         else:
#             print("Rotating")
#             # acceleration 0.5 seconds for 0.5 seconds, then wait again
#             tracks.turn_left(rotate_speed, rotate_speed, 0.5, 0.5)
#             tracks.stop()
