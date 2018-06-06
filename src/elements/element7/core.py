import sys
sys.path.insert(0, '../../../src')
import threading
import time

from entities.vision.vision import Vision
from entities.vision.helpers.vision_helper import Color
from entities.vision.recognize_settings import Recognize_settings
from entities.movement.tracks import Tracks

# Initialize color ranges for detection
color_range = [Color("orange", [0, 69, 124], [13, 255, 255]),
               Color("yellow", [15, 103, 124], [31, 255, 255]),
               Color("red", [159, 116, 152], [180, 255, 255]),
               Color("green", [56, 90, 17], [86, 197, 255]),
               Color("blue", [96, 148, 92], [159, 255, 255])]

color_range_test_room = [Color("blue", [65, 44, 0], [136, 255, 255]),
                    Color("yellow", [21, 110, 89], [30, 255, 255]),
                    Color("orange", [0, 125, 103], [12, 255, 255]),
                    Color("green", [30, 66, 0], [93, 255, 255]),
                    Color("red", [38, 61, 85], [180, 255, 255])]

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
                settings=settings)

threading.Thread(target=vision.saving.run).start()

rotate_speed = 50


# TESTING
tracks = Tracks(track_0_pin=18,
                track_1_pin=13,
                track_0_forward=22,
                track_0_backward=27,
                track_1_forward=10,
                track_1_backward=9)

while True:
    if settings.update:
        settings.update = False
        if settings.new:
            tracks.stop()
            print("Moving to building " + str(settings.current_building)
                  + ", position: " + str(settings.current_position))

            settings.new = False
        else:
            print("Rotating")
            # acceleration 0.5 seconds for 0.5 seconds, then wait again
            tracks.turn_left(rotate_speed, rotate_speed, 0.5, 0.5)
            tracks.stop()
