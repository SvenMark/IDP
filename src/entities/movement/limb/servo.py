#!/bin/python

import time

from libs.ax12 import Ax12


class Servo(object):
    """
    Base class for servo
    """

    def __init__(self, servo_id):
        self.ax12 = Ax12()
        self.servo_id = servo_id

    #Degrees are 0 - 1000
    def move(self, degrees, delay):
        self.ax12.move(self.servo_id, degrees)
        time.sleep(delay)

    def readPosition(self):
        self.ax12.readPosition(self.servo_id)

def main():
    servoprivod = Servo(13)
    servoprivod.move(500, 0)

#main()
