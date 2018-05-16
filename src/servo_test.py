#!/bin/python

import time

from entities.movement.limb.joints.servo import Servo

servoprivod = Servo(31, 500)
otherservo = Servo(13, 500)
anotherservo = Servo(63, 500)

# should both move at the same time
while True:
    servoprivod.move(500, 0)
    otherservo.move(500, 0)
    anotherservo.move(500, 0)

    otherservo.move(300, 0)
    servoprivod.move(300, 0)
    anotherservo.move(300, 0)

