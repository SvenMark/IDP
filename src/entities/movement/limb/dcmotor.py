#!/bin/python

import RPi.GPIO as GPIO # Import the GPIO Library
import time # Import the Time library

class DCMotor(object):
    """
    Base class for dc motor
    """

    def __init__(self, frequency):
        self.pinMotorForward = 10
        self.pinMotorBackward = 9
        self.pinPwm = 18
        self.stop = 0
        self.frequency = frequency
        self.pwmMotor = GPIO.PWM(self.pinPwm, self.frequency)
        GPIO.setup(self.pinPwm, GPIO.OUT)
        GPIO.setup(self.pinMotorForward, GPIO.OUT)
        GPIO.setup(self.pinMotorBackward, GPIO.OUT)
        self.pwmMotor.start(self.stop)

    # Turn all motors off
    def stopMotor(self):
        self.pwmMotor.ChangeDutyCycle(self.stop)

    # Turn both motors forwards
    def forward(self, dutyCycle):
        print("Forwards " + str(dutyCycle))
        GPIO.output(self.pinMotorForward, GPIO.HIGH)
        GPIO.output(self.pinMotorBackward, GPIO.LOW)
        self.pwmMotor.ChangeDutyCycle(dutyCycle)

    def backward(self, dutyCycle):
        print("Backwards " + str(dutyCycle))
        GPIO.output(self.pinMotorForward, GPIO.LOW)
        GPIO.output(self.pinMotorBackward, GPIO.HIGH)
        self.pwmMotor.ChangeDutyCycle(dutyCycle)


def main():
    dvigatel = DCMotor(20)
    dvigatel.forward(20)

main()