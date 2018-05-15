#!/bin/python

from entities.movement.limb.servo import Servo

servoprivod = Servo(13)
servoprivod.move(1000, 0)

while True:
    if servoprivod.readPosition() == 1000:
        print(servoprivod.readPosition())
        servoprivod.move(500, 1)
    if servoprivod.readPosition() == 500:
        print(servoprivod.readPosition())
        servoprivod.move(0, 1)
    if servoprivod.readPosition() == 0:
        print(servoprivod.readPosition())
        servoprivod.move(1000, 1)
