import sys
import threading
import time

sys.path.insert(0, '../../../src')

from entities.audio.audio import Audio
from entities.movement.grabber import Grabber
from entities.movement.movement import Movement
from entities.movement.tracks import Tracks
from entities.threading.utils import SharedObject
from entities.vision.vision import Vision
from entities.visual.emotion import Emotion

from entities.vision.helpers.json_handler import JsonHandler
from entities.vision.helpers.vision_helper import Color, BuildingSide


def transport_to_finish(movement, settings):
    # While not in finish part move backwards
    while not settings.black_detected:
        if settings.update:
            movement.tracks.backward(20, 20, 0, 0.1)
            time.sleep(0.1)
            settings.update = False


# def run(name, control):
def run():
    limbs = [
        Tracks(track_0_pin=13,
               track_1_pin=18,
               track_0_forward=22,
               track_0_backward=27,
               track_1_forward=19,
               track_1_backward=26),
        Grabber(servos=[1, 53, 43],
                initial_positions=[465, 198, 200])
    ]

    movement = Movement(limbs)
    shared_object = SharedObject()
    vision = Vision(shared_object)
    audio = Audio()
    emotion = Emotion(audio)
    speed_factor = 0.75
    dead_zone = 5

    print("[RUN] " + str(name))

    color_ranges = [Color("blue", [84, 44, 52], [153, 255, 255]),
                    Color("yellow", [21, 110, 89], [30, 255, 255]),
                    Color("orange", [0, 108, 104], [6, 255, 255]),
                    Color("green", [28, 39, 0], [94, 255, 255]),
                    Color("red", [167, 116, 89], [180, 255, 255])]
    json_handler = JsonHandler(color_ranges,
                               "color_ranges.txt",
                               "buildings.txt")
    color_range = json_handler.get_color_range()
    saved_buildings = json_handler.get_save_buildings()
    for building in saved_buildings:
        print(str(building.number))

    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == "hsv" and sys.argv[2] == "picker":
                threading.Thread(target=vision.helpers.hsv_picker.run, args=(color_range, json_handler)).start()
            elif sys.argv[1] == "saving":
                threading.Thread(target=vision.saving.run, args=(color_range, json_handler)).start()
            elif sys.argv[1] == "recognize":
                threading.Thread(target=vision.recognize.run, args=(color_range, saved_buildings)).start()
            else:
                print("[ERROR] Wrong argument given..")
                run(name, control)

        # Default no argument
        else:
            threading.Thread(target=vision.recognize.run, args=(color_range, saved_buildings)).start()
    except AttributeError:
        print("[ERROR] Something went wrong..")
        run(name, control)

    # Movement based on vision settings
    while not shared_object.has_to_stop():

        # print("Update movement with vision")
        time.sleep(0.2)

        grab = shared_object.bluetooth_settings.d

        # Input backup if automatic movement failed
        movement.tracks.handle_controller_input(stop_motors=shared_object.bluetooth_settings.s,
                                                vertical_speed=shared_object.bluetooth_settings.h * speed_factor,
                                                horizontal_speed=shared_object.bluetooth_settings.v * speed_factor,
                                                dead_zone=dead_zone)

        if hasattr(movement, 'grabber'):
            if movement.grabber.grabbed and grab is 0:
                movement.grabber.loosen([150, 150, 150])
            if not movement.grabber.grabbed and grab is 1:
                movement.grabber.grab([100, 100, 100], vision.settings.pick_up_vertical)

        # If a vision frame has been handled
        if vision.settings.update:
            print("grab {} distance {} percentage {}".format(vision.settings.grab, vision.settings.distance, vision.settings.current_position))
            # Frame is now handled
            vision.settings.update = False

            # If the robot is close enough to grab
            if vision.settings.grab:
                movement.tracks.stop()
                print("GRABBING VISION")
                # Try grab
                if hasattr(movement, 'grabber'):
                    movement.grabber.grab([80, 80, 80], vision.settings.pick_up_vertical)

                # While grabbing failed, try again
                max_attempts = 10
                attempts = 0
                if hasattr(movement, 'grabber'):
                    while movement.grabber.reposition is True \
                            and not shared_object.has_to_stop() and attempts < max_attempts:
                        if vision.settings.distance < 50:
                            movement.tracks.backward(20, 20, 0.5, 0.5)
                            movement.grabber.grab([80, 80, 80], vision.settings.pick_up_vertical)
                        attempts += 1

                # If all attempts failed
                if attempts == max_attempts:
                    print("[FAIL] GRABBING FAILED AFTER {} ATTEMPTS".format(attempts))
                else:
                    # TODO: implement this
                    transport_to_finish(movement, vision.settings)

            # When a new building found
            elif vision.settings.new:
                print("NEW BUILDING IN VISION")
                if not vision.settings.grab:
                    # TODO: implement this
                    movement.move_towards(vision.settings.current_position)
            else:
                # TODO: implement this
                print("Move towards contours")
                movement.move_towards(vision.settings.current_position)

    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()

run()
