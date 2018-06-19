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


def transport_to_finish(movement, settings):
    while not settings.black_detected:
        movement.tracks.backward(20, 20, 0, 0.1)

        # wait for update
        while not settings.update:
            time.sleep(0.1)
        settings.update = False


def move_towards(movement, percentage):
    torque = 0.8
    left_speed = 20
    right_speed = 20
    if percentage < 50:
        left_speed = left_speed - percentage * torque
    else:
        right_speed = right_speed - (percentage - 50) * torque

    movement.tracks.forward(left_speed, right_speed, 0.3, 0.3)


def run(name, movement, shared_object):
    json_handler = Json_Handler()
    color_range = json_handler.get_color_range()
    tape = [Color("zwarte_tape", [0, 0, 0], [15, 35, 90])]

    saved_buildings = json_handler.get_save_buildings()

    settings = Recognize_settings()
    vision = Vision(color_range=color_range,
                    saved_buildings=saved_buildings,
                    settings=settings, min_block_size=0,
                    shared_object=shared_object
                    )

    rotate_speed = 50
    print("run " + str(name))
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
        if settings.update:
            settings.update = False
            if settings.grab:
                movement.grabber.grab([80, 80, 80])
                if movement.grabber.reposition is True:

                    # TODO: implement this
                    transport_to_finish(movement, settings)

                    movement.grabber.reposition = False
            # new building found
            elif settings.new:
                settings.new = False
                while not settings.grab:
                    # TODO: implement this
                    move_towards(movement, settings.current_position)
                    pass
            else:
                # TODO: implement this
                movement.tracks.forward(20, 20, 0.5, 0.5)
                pass


    # Handle cleanup
    # Notify shared object that this thread has been stopped
    print("Stopped" + str(name))
    shared_object.has_been_stopped()

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


