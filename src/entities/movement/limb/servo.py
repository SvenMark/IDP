#!/bin/python

class Servo(object):
    """
    Base class for servi
    """
    def __init__(self):
        super(Servo, self).__init__('servi')

    @property
    def turn(self):
        raise NotImplementedError('Should be overridden in the child class')