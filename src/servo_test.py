#!/bin/python
from entities.movement.limb.joints.servo import Servo

servo0 = Servo(14, 600)
servo1 = Servo(61, 450)
servo2 = Servo(63, 850)

servo0.read_speed()
