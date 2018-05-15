#!/bin/python

from libs.ax12 import Ax12
from entities.movement.limb.dc_motor import DCMotor
from entities.movement.limb.servo import Servo
import time

motor = DCMotor()
servo = Servo(13, 500)

for cycle in range(0, 20):
    motor.forward(cycle)
    servo.move(400, 0)
    servo.move(500, 0)
    servo.move(600, 0)
    servo.move(500, 0)