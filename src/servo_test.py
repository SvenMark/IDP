#!/bin/python
from entities.movement.limb.joints.servo import Servo

servo0 = Servo(14, 530)
servo1 = Servo(61, 450)
servo2 = Servo(63, 850)


speed = 140

while True:
	servo0.move_speed(500, 0, speed)
	servo1.move_speed(300, 0, speed)
	servo1.move_speed(450, 0.5, speed)
	servo0.move_speed(700, 0, speed)
	servo1.move_speed(300, 0, speed)
	servo1.move_speed(450, 0.5, speed)
