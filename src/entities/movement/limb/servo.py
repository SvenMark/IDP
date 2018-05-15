#!/bin/python

import time

from libs.ax12 import Ax12

class Servo(object):
    """
    Base class for servo
    """

    def __init__(self, servo_id, initial_position):
        self.ax12 = Ax12()
        self.servo_id = servo_id
        self.lastPosition = initial_position

    #Degrees are 0 - 998
    def move(self, degrees, delay):
        while self.readPosition() != self.lastPosition:
            time.sleep(0.2)

        if degrees < 0 or degrees > 998:
            print("In servo " + str(self.servo_id) + ", degrees: " + str(degrees) + ", must be between 0 and 998")
        self.lastPosition = degrees
        self.ax12.move(self.servo_id, degrees)
        time.sleep(delay)

    def __new__(cls):
        return super(Servo, cls).__new__(cls)

    def readPosition(self):
        return self.ax12.readPosition(self.servo_id)

def main():
    servoprivod = Servo(13)
    servoprivod.move(500, 0)

#main()
