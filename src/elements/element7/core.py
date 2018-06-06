import sys
sys.path.insert(0, '../../../src')  # Needed for pi

from entities.vision.vision import Vision
from entities.vision.helpers.helpers import Color

# Initialize color ranges for detection
color_range = [Color("orange", [0, 69, 124], [13, 255, 255]),
               Color("yellow", [15, 103, 124], [31, 255, 255]),
               Color("red", [159, 116, 152], [180, 255, 255]),
               Color("green", [56, 90, 17], [86, 197, 255]),
               Color("blue", [96, 148, 92], [159, 255, 255])]

color_range_cup = [Color("green", [28, 7, 87], [48, 255, 142]),
                   Color("white", [0, 0, 136], [180, 28, 219])]

saved_buildings = [[
        (28, 91),
        (136, 83),
        (137, 312),
        (82, 200),
        (29, 316),
        ]
]


vision = Vision(color_range, saved_buildings)
vision.saving.run()