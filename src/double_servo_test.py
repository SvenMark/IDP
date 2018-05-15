import time

from libs.ax12 import Ax12
from entities.movement.limb.servo import Servo

servo1 = Servo(13, 500)
servo2 = Servo(31, 500)

while True:
    servo1.move(servo1, 400)
    servo2.move(servo2, 600)

    servo1.move(servo1, 600)
    servo2.move(servo2, 400)
