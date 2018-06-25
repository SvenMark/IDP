import sys

from entities.threading.utils import SharedObject

sys.path.insert(0, '../../../src')

from entities.vision.helpers.json_handler import JsonHandler
from entities.vision.vision import Vision
from entities.vision.helpers.vision_helper import Color


def run(name):
    print("[RUN] " + str(name))
    shoe = [Color("red", [167, 116, 89], [180, 255, 255])]

    json_handler = JsonHandler(shoe, "shoe_ranges")
    color_range = json_handler.get_color_range()

    vision = Vision(shared_object=SharedObject())

    vision.recognize.run(color_range)


def main():
    run('Follow mode')


if __name__ == '__main__':
    main()
