import datetime
import time
import sys
from threading import Thread

sys.path.insert(0, '../../../src')

from entities.movement.limb.joints.servo import Servo
from entities.movement.sequences.sequences import *


# Maximum grab state:
#     (1)Grabberarm 0 max pos: 740
#     (53)Grabberarm 1 max pos: 610
#     (13)Grabber pusher max pos: 850

# Retracted state:
# 	(1)Grabberarm 0 min pos: 1020
# 	(53)Grabberarm 1 min pos: 270
# 	(13)Grabber pusher min pos: 815

# Grab tower state:
# 	(1)Grabberarm 0  810
# 	(53)Grabberarm 1: 540
# 	(13)Grabber pusher: 755


class Grabber(object):

    def __init__(self, id_servo, initial_positions):
        self.servo_0 = Servo(id_servo[0], initial_positions[0])
        self.servo_1 = Servo(id_servo[1], initial_positions[1])
        self.servo_2 = Servo(id_servo[2], initial_positions[2])

        self.servos = [self.servo_0, self.servo_1, self.servo_2]

        self.servo_0.move_speed(initial_positions[0], 50)
        self.servo_1.move_speed(initial_positions[1], 50)
        self.servo_2.move_speed(initial_positions[2], 50)

        self.type = 'grabber'

        print("Grabber setup")

    def ready(self):
        """
        Checks if all servos of this leg are ready
        :return: If all the servos are ready or not
        """
        return len([elem for elem in self.servos if elem.is_ready()]) == 3

    def grab(self, positions, delay, speeds):
        positions = [765, 555, 710]
        self.servo_0.move_speed(positions[0], speeds[0])
        self.servo_1.move_speed(positions[1], speeds[1])
        self.servo_2.move_speed(positions[2], speeds[2])

    def loosen(self, positions, delay, speeds):
        positions = [1023, 290, 690]
        self.servo_0.move_speed(positions[0], speeds[0])
        self.servo_1.move_speed(positions[1], speeds[1])
        self.servo_2.move_speed(positions[2], speeds[2])
