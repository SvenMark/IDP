import sys
sys.path.insert(0, '../../../src')

from entities.vision.recognize import Recognize, Block
from entities.vision.helpers.helpers import Color, Building

# Required to call the Camera function
saved_buildings = saved_buildings = [
        Building(front=[Block("orange", (41, 324)),
                        Block("yellow", (33, 97)),
                        Block("red", (148, 92)),
                        Block("green", (153, 318)),
                        Block("blue", (92, 218))],
                 back=[Block("blue", (31, 316)),
                       Block("green", (86, 209)),
                       Block("orange", (30, 91)),
                       Block("yellow", (144, 317))],
                 left=[Block("red", (112, 175)),
                       Block("blue", (44, 304)),
                       Block("green", (36, 68)),
                       Block("orange", (184, 70)),
                       Block("yellow", (180, 307))],
                 right=[Block("red", (112, 175)),
                        Block("blue", (44, 304)),
                        Block("green", (36, 68)),
                        Block("orange", (184, 70)),
                        Block("yellow", (180, 307))]
                 )
    ]



def run():
    print("run element cup")
    detect_cup()


def detect_cup():

    # Initialize color ranges for detection
    color_range = [Color("beker", [23, 48, 24], [44, 255, 255])]

    cam = Recognize(color_range, saved_buildings=None)
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
