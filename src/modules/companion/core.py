import sys

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

    print("[RUN] " + str(name))

    shoe = [Color("red", [167, 116, 89], [180, 255, 255])]

    json_handler = JsonHandler(shoe, "shoe_ranges")
    color_range = json_handler.get_color_range()

    vision.recognize.run(color_range)

    while not shared_object.has_to_stop():
        if vision_settings.update:
            movement.move_towards(vision_settings.current_position)

    # Notify shared object that this thread has been stopped
    print("[STOPPED] {}".format(name))
    shared_object.has_been_stopped()
