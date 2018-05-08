#!/bin/python

class Servo(object):
    """
    Base class for servo
    """
    def __init__(self):
        super(Servo, self).__init__('servo ')

    @property
    def turn(self):
        raise NotImplementedError('Should be overridden in the child class')