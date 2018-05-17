#!/bin/python

import time

from entities.movement.limb.joints.servo import Servo

servo0 = Servo(1, 500)
time.sleep(0.1)
servo1 = Servo(13, 500)
time.sleep(0.1)
servo2 = Servo(14, 500)
time.sleep(0.1)
servo3 = Servo(21, 500)
time.sleep(0.1)
servo4 = Servo(31, 500)
time.sleep(0.1)
servo5 = Servo(53, 500)
time.sleep(0.1)
servo6 = Servo(61, 500)
time.sleep(0.1)
servo7 = Servo(63, 500)
time.sleep(0.1)

# should both move at the same time
while True:
    servo0.move(100, 1)
    servo1.move(100, 1)
    servo2.move(100, 1)
    servo3.move(100, 1)
    servo4.move(100, 1)
    servo5.move(100, 1)
    servo6.move(100, 1)
    servo7.move(100, 1)

    servo0.move(900, 1)
    servo1.move(900, 1)
    servo2.move(900, 1)
    servo3.move(900, 1)
    servo4.move(900, 1)
    servo5.move(900, 1)
    servo6.move(900, 1)
    servo7.move(900, 1)

    servo0.move(500, 1)
    servo1.move(500, 1)
    servo2.move(500, 1)
    servo3.move(500, 1)
    servo4.move(500, 1)
    servo5.move(500, 1)
    servo6.move(500, 1)
    servo7.move(500, 1)

