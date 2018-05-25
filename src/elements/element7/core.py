from entities.vision.camera import Camera
from entities.vision.calibrate import Calibrate
from entities.vision.helpers import Color

# Initialize color ranges for detection
color_range = [Color("orange", [0, 100, 100], [12, 255, 255]),
               Color("yellow", [24, 100, 100], [35, 255, 255]),
               Color("red", [26, 0, 17], [69, 131, 190]),
               Color("green", [71, 89, 11], [83, 202, 120]),
               Color("blue", [99, 152, 128], [119, 228, 174])]


cali = Calibrate(color_range)
color_range = cali.run()
cam = Camera(color_range)
cam.run()
