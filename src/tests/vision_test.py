import sys
import threading


sys.path.insert(0, '../../src')

from entities.vision.helpers.json_handler import JsonHandler
from entities.vision.helpers.vision_helper import Color
from entities.audio.audio import Audio

from entities.threading.utils import SharedObject
from entities.vision.vision import Vision

audio = Audio()

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

for gange in color_range:
    print(gange.lower)

vision = Vision(SharedObject())

try:
    if len(sys.argv) > 1:
        if sys.argv[1] == "hsv" and sys.argv[2] == "picker":
            threading.Thread(target=vision.helpers.hsv_picker.run, args=(color_range, json_handler)).start()
        elif sys.argv[1] == "saving":
            threading.Thread(target=vision.saving.run, args=(color_range, json_handler)).start()
        elif sys.argv[1] == "recognize":
            threading.Thread(target=vision.recognize.run, args=(color_range, saved_buildings, audio)).start()
        else:
            print("[ERROR] Wrong argument given..")

    # Default no argument
    else:
        threading.Thread(target=vision.recognize.run, args=(color_range, saved_buildings, audio)).start()
except AttributeError:
    print("[ERROR] Something went wrong..")

