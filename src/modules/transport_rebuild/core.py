import sys
import threading
import time

sys.path.insert(0, '../../../src')

from entities.vision.helpers.json_handler import JsonHandler
from entities.vision.helpers.vision_helper import Color, BuildingSide


def transport_to_finish(movement, settings):
    while not settings.black_detected:
        movement.tracks.backward(20, 20, 0, 0.1)

        # wait for update
        while not settings.update:
            time.sleep(0.1)
        settings.update = False


def move_towards(movement, percentage):
    torque = 0.8
    left_speed = 60
    right_speed = 60
    if percentage < 50:
        left_speed = left_speed - percentage * torque
    else:
        right_speed = right_speed - (percentage - 50) * torque

    movement.tracks.forward(left_speed, right_speed, 0.3, 0.3)


def run(name, control):
    movement = control.movement
    shared_object = control.shared_object
    speed_factor = control.speed_factor
    dead_zone = control.dead_zone
    vision = control.vision

    print("[RUN] " + str(name))

    color_ranges = [Color("blue", [84, 44, 52], [153, 255, 255]),
                    Color("yellow", [21, 110, 89], [30, 255, 255]),
                    Color("orange", [0, 108, 104], [6, 255, 255]),
                    Color("green", [28, 39, 0], [94, 255, 255]),
                    Color("red", [167, 116, 89], [180, 255, 255])]
    json_handler = JsonHandler(color_ranges, "color_ranges.txt", "buildings.txt")
    color_range = json_handler.get_color_range()
    saved_buildings = json_handler.get_save_buildings()

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
            threading.Thread(target=vision.recognize.run).start()
    except AttributeError:
        print("[ERROR] Something went wrong..")
        run(name, control)

    while not shared_object.has_to_stop():
        grab = shared_object.bluetooth_settings.d

        movement.tracks.handle_controller_input(stop_motors=shared_object.bluetooth_settings.s,
                                                vertical_speed=shared_object.bluetooth_settings.h * speed_factor,
                                                horizontal_speed=shared_object.bluetooth_settings.v * speed_factor,
                                                dead_zone=dead_zone)

        if movement.grabber.grabbed and grab is 0:
            movement.grabber.loosen([150, 150, 150])
        if not movement.grabber.grabbed and grab is 1:
            movement.grabber.grab([100, 100, 100], vision.settings.pick_up_vertical)

        if vision.settings.update:
            vision.settings.update = False
            if vision.settings.grab:

                movement.grabber.grab([80, 80, 80], vision.settings.pick_up_vertical)

                while movement.grabber.reposition is True:
                    if vision.settings.distance < 50:
                        movement.tracks.backward(20, 20, 0.5, 0.5)
                        movement.grabber.grab([80, 80, 80], vision.settings.pick_up_vertical)

                # TODO: implement this
                transport_to_finish(movement, vision.settings)

                movement.grabber.reposition = False
            # new building found
            elif vision.settings.new:
                vision.settings.new = False
                while not vision.settings.grab:
                    # TODO: implement this
                    move_towards(movement, vision.settings.current_position)
            else:
                # TODO: implement this
                movement.tracks.forward(20, 20, 0.5, 0.5)

    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
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
