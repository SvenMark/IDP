import time

from entities.movement.limb.limb import Limb
from entities.movement.limb.joints.dcmotor import DCMotor


class Tracks(object):
    """
    Base class for tracks that implements DC motors
    """

    def __init__(self):
        motor1pin = 18
        motor2pin = 13

        self.motor1 = DCMotor(motor1pin)
        self.motor2 = DCMotor(motor2pin)

        print("Tracks setup")

    def forward(self, duty_cycle, delay, steps):
        for step in range(0, steps, (duty_cycle // steps)):
            print(step)
            self.motor1.forward(step, 0)
            self.motor2.forward(step, delay)

    def backward(self, duty_cycle, delay, steps):
        self.motor1.backward(duty_cycle, 0)
        self.motor2.backward(duty_cycle, delay)

    def turn_right(self, duty_cycle_track_right, duty_cycle_track_left, delay, steps):
        self.motor1.backward(duty_cycle_track_right, 0)
        self.motor2.forward(duty_cycle_track_left, delay)

    def turn_left(self, duty_cycle_track_right, duty_cycle_track_left, delay, steps):
        self.motor1.forward(duty_cycle_track_right, 0)
        self.motor2.backward(duty_cycle_track_left, delay)
