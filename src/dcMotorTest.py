#!/bin/python

import time
from entities.movement.limb.dcmotor import DCMotor

motor = DCMotor()

for cycle in range(0, 20):
    motor.forward(cycle, 0.5)

for cycle in range(20, 0):
    motor.forward(cycle, 0.5)

for cycle in range(0, 20):
    motor.backward(cycle, 0.5)

for cycle in range(20, 0):
    motor.backward(cycle, 0.5)