import sys
sys.path.insert(0, '../../../src')

from entities.vision.recognize import Recognize, Block
from entities.vision.helpers import Color


def run(shared_object):
    print("run element cup")
    detect_cup()


def detect_cup():

    # Initialize color ranges for detection
    color_range = [Color("beker", [23, 48, 24], [44, 255, 255])]

    cam = Recognize(color_range)
    cam.run()


def detect_bridge():

    # Initialize color ranges for detection
    color_range = [Color("Brug", [0, 0, 0], [0, 255, 107]),
                   Color("Gat", [0, 0, 0], [0, 0, 255]),
                   Color("Rand", [0, 0, 185], [0, 0, 255]),
                   Color("White-ish", [0, 0, 68], [180, 98, 255])]

    cam = Recognize(color_range)
    cam.run()


if __name__ == '__main__':
    run()  # disabled for travis
