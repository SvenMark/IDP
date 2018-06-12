import sys
import time

sys.path.insert(0, '../../src')

from entities.movement.limb.joints.servo import Servo

servo_0 = Servo(1, 820)
servo_1 = Servo(13, 385)
servo_2 = Servo(53, 565)
servo_3 = Servo(254, 0)

servo_0.move(840, 0, 80)
time.sleep(2)
servo_1.move(400, 0, 80)
time.sleep(2)
servo_2.move(520, 0, 80)
time.sleep(2)
servo_3.move(30, 0, 80)
time.sleep(2)