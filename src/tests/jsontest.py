import os
import sys
import threading
import time

sys.path.insert(0, '../../src')

from entities.vision.helpers.json_handler import JsonHandler
from entities.vision.helpers.vision_helper import Color, BuildingSide

color_ranges = [Color("blue", [84, 44, 52], [153, 255, 255]),
                Color("yellow", [21, 110, 89], [30, 255, 255]),
                Color("orange", [0, 108, 104], [6, 255, 255]),
                Color("green", [28, 39, 0], [94, 255, 255]),
                Color("red", [167, 116, 89], [180, 255, 255])]

json_handler = JsonHandler(color_ranges,
                           "color_ranges.txt",
                           "buildings.txt")

print(json_handler.get_save_buildings()[0].side)
