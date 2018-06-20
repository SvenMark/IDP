import sys

sys.path.insert(0, '../../../src')

from entities.vision.vision import Vision
from entities.vision.helpers.vision_helper import Color
from entities.vision.recognize_settings import Recognize_settings


def run(name):
    print("[RUN] " + str(name))
    shoe = [Color("zwarte_tape", [0, 0, 0], [15, 35, 90])]

    settings = Recognize_settings()
    vision = Vision(color_range=shoe,
                    settings=settings, min_block_size=0)

    vision.recognize.run()


run("shoe_detect")
