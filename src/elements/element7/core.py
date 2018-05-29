from entities.vision.calibrate import Calibrate
from entities.vision.camera import Camera
from entities.vision.helpers import Color

# Initialize color ranges for detection
color_range = [Color("orange", [0, 100, 100], [12, 255, 255]),
               Color("yellow", [24, 100, 100], [35, 255, 255]),
               Color("red", [0, 122, 112], [37, 255, 154]),
               Color("green", [71, 89, 11], [83, 202, 120]),
               Color("blue", [99, 152, 128], [119, 228, 174])]

saved_buildings = [
                [(41, 324),
                 (33, 97),
                 (148, 92),
                 (153, 318),
                 (92, 218)]
]


# cali = Calibrate(color_range)
# color_range = cali.run()
cam = Camera(color_range, saved_buildings)
cam.run()
