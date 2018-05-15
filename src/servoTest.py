#!/bin/python

from entities.movement.limb.servo import Servo

servoprivod = Servo(13)
servoprivod.move(998, 0)

while True:
    if servoprivod.read_position() == 998:
        print(servoprivod.read_position())
        servoprivod.move(500, 1)
    if servoprivod.read_position() == 500:
        print(servoprivod.read_position())
        servoprivod.move(0, 1)
    if servoprivod.read_position() == 0:
        print(servoprivod.read_position())
        servoprivod.move(998, 1)
