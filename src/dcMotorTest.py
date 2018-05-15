#!/bin/python

import time
from entities.movement.limb.dcmotor import DCMotor

motor = DCMotor(18)
othermotor = DCMotor(13)

for cycle in range(0, 20):
    motor.forward(cycle, 0.5)
    othermotor.forward(cycle, 0.5)

for cycle in range(0, 20):
    motor.forward(20 - cycle, 0.5)
    othermotor.forward(20 - cycle, 0.5)

for cycle in range(0, 20):
    motor.backward(cycle, 0.5)
    othermotor.forward(cycle, 0.5)

for cycle in range(0, 20):
    motor.backward(20 - cycle, 0.5)
    othermotor.forward(20 - cycle, 0.5)
