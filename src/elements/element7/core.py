from entities.vision.camera import Camera, Building, Block
from entities.vision.calibrate import Calibrate
from entities.vision.helpers import Color

# Initialize color ranges for detection
color_range = [Color("orange", [0, 100, 100], [12, 255, 255]),
               Color("yellow", [24, 100, 100], [35, 255, 255]),
               Color("red", [26, 0, 17], [69, 131, 190]),
               Color("green", [71, 89, 11], [83, 202, 120]),
               Color("blue", [99, 152, 128], [119, 228, 174])]

saved_buildings = [
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


cali = Calibrate(color_range)
color_range = cali.run()
cam = Camera(color_range, saved_buildings)
cam.run()
