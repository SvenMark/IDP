from entities.vision.camera import Camera
from entities.vision.helpers import Color

# Initialize color ranges for detection
color_range = [Color("orange", [0, 98, 105], [12, 255, 255]),
               Color("yellow", [25, 100, 100], [36, 255, 255]),
               Color("red", [0, 93, 98], [4, 250, 255]),
               Color("green", [60, 58, 26], [95, 210, 101]),
               Color("blue", [90, 100, 100], [120, 255, 255])]

cam = Camera(color_range)
cam.run()
