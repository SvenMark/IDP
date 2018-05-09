#!/bin/python

class Servo(object):
    """
    Base class for servo
    """

    @property
    def turn(self):
        raise NotImplementedError('Should be overridden in the child class')
