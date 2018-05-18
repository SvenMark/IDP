#!/bin/python
import time

from entities.movement.limb.joints.dcmotor import DCMotor

motor = DCMotor(18)
othermotor = DCMotor(13)


#motor.forward(20, 0)
othermotor.forward(20, 0)

time.sleep(10)


for cycle in range(0, 100):
    motor.forward(cycle, 0.1)
    othermotor.forward(cycle, 0.1)

for cycle in range(0, 100):
    motor.forward(100 - cycle, 0.1)
    othermotor.forward(100 - cycle, 0.1)

for cycle in range(0, 20):
    motor.backward(cycle, 0.5)
    othermotor.backward(cycle, 0.5)

for cycle in range(0, 20):
    motor.backward(20 - cycle, 0.5)
    othermotor.backward(20 - cycle, 0.5)
