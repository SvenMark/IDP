#!/bin/python


import time


from ax12 import Ax12


class Servo(object):
    """
    Base class for servo
    """

    def __init__(self, servo_id):
        self.ax12 = Ax12()
        self.servo_id = servo_id

    def move(self, degrees, delay):
        self.ax12.move(self.servo_id, degrees)
        time.sleep(delay)

    @property
    def turn(self):
        raise NotImplementedError('Should be overridden in the child class')

def test():
	servo = Servo(13)
	servo.move(500, 0.5)
	servo.move(1000, 0.5)

#test()

