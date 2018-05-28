from entities.vision.camera import Camera
from entities.vision.calibrate import Calibrate
from entities.vision.helpers import Color

POSITIONS = []


import sys
sys.path.insert(0, '../../../src')

from elements.element5.helpers import Color
from elements.element5.helpers import check_valid_convex

import cv2

POSITIONS = []


def run():
    print("run element5")
    detect_bridge()


def detect_cup():

    # Initialize color ranges for detection
    color_range = [Color("beker", [30, 10, 93], [83, 87, 175])]

    cam = Camera(color_range)
    cam.run()


def detect_bridge():

    # Initialize color ranges for detection
    color_range = [Color("Brug", [0, 0, 0], [0, 255, 107]),
                   # Color("Gat", [0, 0, 0], [0, 0, 255]),
                   Color("Rand", [0, 0, 185], [0, 0, 255])]

    cam = Camera(color_range)
    cam.run()


if __name__ == '__main__':
    run()  # disabled for travis
