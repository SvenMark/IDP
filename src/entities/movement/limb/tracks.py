from entities.movement.limb.limb import Limb
from entities.movement.limb.joints.dcmotor import DCMotor
import time


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

    def forward(self, duty_cycle, delay, acceleration):

        if acceleration <= 0:
            print("Warning, setting acceleration to 0.01")
            acceleration = 0.01

        diff1 = duty_cycle - self.motor1.currentspeed
        diff2 = duty_cycle - self.motor2.currentspeed

        step = diff1 / acceleration / 100
        step2 = diff2 / acceleration / 100

        speed1 = self.motor1.currentspeed
        speed2 = self.motor2.currentspeed

        for i in range(0, 100 * acceleration):
            self.motor1.forward(speed1, 0)
            self.motor2.forward(speed2, 0)

            speed1 += step
            speed2 += step2
            
            time.sleep(0.01)

        time.sleep(delay)
        
    def backward(self, duty_cycle, delay):
        self.motor1.backward(duty_cycle, 0)
        self.motor2.backward(duty_cycle, delay)

    def turn_right(self, duty_cycle_track_right, duty_cycle_track_left, delay):
        self.motor1.backward(duty_cycle_track_right, 0)
        self.motor2.forward(duty_cycle_track_left, delay)

    def turn_left(self, duty_cycle_track_right, duty_cycle_track_left, delay):
        self.motor1.forward(duty_cycle_track_right, 0)
        self.motor2.backward(duty_cycle_track_left, delay)
