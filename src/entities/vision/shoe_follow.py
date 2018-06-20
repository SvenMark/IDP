import sys

from entities.vision.helpers.json_handler import Json_Handler

sys.path.insert(0, '../../../src')

from entities.vision.vision import Vision
from entities.vision.helpers.vision_helper import Color
from entities.vision.recognize_settings import Recognize_settings


def run(name):
    print("[RUN] " + str(name))
    shoe = [Color("red", [167, 116, 89], [180, 255, 255])]

    json_handler = Json_Handler(shoe, "shoe_ranges")
    color_range = json_handler.get_color_range()

    settings = Recognize_settings()

    vision = Vision(color_range=color_range, settings=settings, min_block_size=0)

    vision.helpers.hsv_picker.run()
    vision.recognize.run()


run("shoe_detect")
