#!/bin/python

from entities.movement.limb.servo import Servo
import time

servoprivod = Servo(31, 500)

while True:
    servoprivod.move(500, 0)
    servoprivod.move(300, 0)

