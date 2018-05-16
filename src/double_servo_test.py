import time

from libs.ax12 import Ax12
from entities.movement.limb.servo import Servo

servo1 = Servo(13, 500)
servo2 = Servo(31, 500)

while True:
    servo1.move(400, 0)
    servo2.move(600, 0)

    servo1.move(600, 0)
    servo2.move(400, 0)
