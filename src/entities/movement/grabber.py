import datetime
import time
import sys
from threading import Thread

sys.path.insert(0, '../../../src')

from entities.movement.limb.joints.servo import Servo
from entities.movement.sequences.sequences import *


# Maximum grab state:
#     (1)Grabberarm 0 max pos: 740
#     (53)Grabberarm 1 max pos: 607
#     (13)Grabber pusher max pos: 850

# Retracted state:
# 	(1)Grabberarm 0 min pos: 1020
# 	(53)Grabberarm 1 min pos: 270
# 	(13)Grabber pusher min pos: 815

# Grab tower state:
# 	(1)Grabberarm 0  1020
# 	(53)Grabberarm 1: 270
# 	(13)Grabber pusher: 815


class Grabber(object):

    def __init__(self, id_servo):
        self.servo_0 = Servo(id_servo[0], 850)
        self.servo_1 = Servo(id_servo[1], 450)
        self.servo_2 = Servo(id_servo[2], 550)

        self.servos = [self.servo_0, self.servo_1, self.servo_2]

        self.type = 'grabber'

        print("Grabber setup")

    def ready(self):
        """
        Checks if all servos of this leg are ready
        :return: If all the servos are ready or not
        """
        return len([elem for elem in self.servos if elem.is_ready()]) == 3

    def grab(self, positions, delay, speeds):
        self.servo_0.move(positions[0], delay, speeds[0])
        self.servo_1.move(positions[1], delay, speeds[1])
        self.servo_2.move(positions[2], delay, speeds[2])

    def loosen(self, positions, delay, speeds):
        self.servo_0.move(positions[0], delay, speeds[0])
        self.servo_1.move(positions[1], delay, speeds[1])
        self.servo_2.move(positions[2], delay, speeds[2])
