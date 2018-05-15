#!/bin/python

from libs.ax12 import Ax12
from entities.movement.limb.servo import Servo
import time

servoprivod = Servo(13)
servoprivod.move(1000, 0)

#while True :
#	servoprivod.move(500, 1)
#	servoprivod.move(0, 1)
#	servoprivod.move(1000, 1)
