import sys
sys.path.insert(0, '../../../src')
import threading
import time

from entities.vision.vision import Vision
from entities.vision.helpers.vision_helper import Color
from entities.vision.recognize_settings import Recognize_settings
# from entities.movement.tracks import Tracks

# Initialize color ranges for detection
color_range = [Color("orange", [0, 69, 124], [13, 255, 255]),
               Color("yellow", [15, 103, 124], [31, 255, 255]),
               Color("red", [159, 116, 152], [180, 255, 255]),
               Color("green", [56, 90, 17], [86, 197, 255]),
               Color("blue", [96, 148, 92], [159, 255, 255])]

color_range_test_room = [Color("blue", [84, 44, 52], [153, 255, 255]),
Color("yellow", [21, 110, 89], [30, 255, 255]),
Color("orange", [0, 108, 104], [6, 255, 255]),
Color("green", [28, 39, 0], [94, 255, 255]),
Color("red", [167, 116, 89], [180, 255, 255])]

tape = [Color("zwarte_tape", [0, 0, 0], [15, 35, 90])]

saved_buildings = [[
        (28, 91),
        (136, 83),
        (137, 312),
        (82, 200),
        (29, 316),
        ]
]

img = "C:/Users/lars-/Downloads/test.jpeg"

settings = Recognize_settings()

vision = Vision(color_range=color_range_test_room,
                saved_buildings=saved_buildings,
                settings=settings, max_block_size=12000, min_block_size=2000)
if len(sys.argv) > 1:
    if sys.argv[1] == "hsv_picker":
        threading.Thread(target=vision.helpers.hsv_picker.run).start()
        print("Starting: ", sys.argv[1])
    elif sys.argv[1] == "save":
        threading.Thread(target=vision.saving.run).start()
        print("Starting: ", sys.argv[1])
    else:
        threading.Thread(target=vision.helpers.hsv_picker.run).start()
        print("Starting: recognize")
else:
    threading.Thread(target=vision.helpers.hsv_picker.run).start()
    print("Starting: recognize")

rotate_speed = 50

#
# # TESTING
# tracks = Tracks(track_0_pin=18,
#                 track_1_pin=13,
#                 track_0_forward=22,
#                 track_0_backward=27,
#                 track_1_forward=10,
#                 track_1_backward=9)
#
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
