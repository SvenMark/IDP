import datetime
import time
import sys
from threading import Thread

sys.path.insert(0, '../../../src')

from entities.movement.limb.joints.servo import Servo
from entities.movement.sequences.sequences import *


class Grabber(object):

    def __init__(self, id_servo, positions):
        self.servo_0 = Servo(id_servo[0], positions[0])
        self.servo_1 = Servo(id_servo[1], positions[1])
        self.servo_2 = Servo(id_servo[2], positions[2])

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
