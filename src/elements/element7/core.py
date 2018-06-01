import sys
sys.path.insert(0, '../../../src')  # Needed for pi

from entities.vision.calibrate import Calibrate
from entities.vision.camera import Camera
from entities.vision.saving import Saving
from entities.vision.helpers import Color

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

save = Saving(color_range_cup)
save.run()
# cali = Calibrate(color_range)
# color_range = cali.run()
# cam = Camera(color_range, saved_buildings)
# cam.run()
