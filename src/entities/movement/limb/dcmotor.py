#!/bin/python

import time  # Import the Time library

import RPi.GPIO as GPIO  # Import the GPIO Library


class DCMotor(object):
    """
    Base class for dc motor
    """

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.pinMotorForward = 10
        self.pinMotorBackward = 9
        self.pinPwm = 18
        self.frequency = 20
        self.stop = 0

        GPIO.setup(self.pinPwm, GPIO.OUT)
        GPIO.setup(self.pinMotorForward, GPIO.OUT)
        GPIO.setup(self.pinMotorBackward, GPIO.OUT)

        self.pwmMotor = GPIO.PWM(self.pinPwm, self.frequency)
        self.pwmMotor.start(self.stop)

        print("Setup")

    # Turn all motors off
    def stopMotor(self):
        self.pwmMotor.ChangeDutyCycle(self.stop)

    # Turn both motors forwards
    def forward(self, dutycycle, delay):
        print("Forwards " + str(dutycycle))
        GPIO.output(self.pinMotorForward, GPIO.HIGH)
        GPIO.output(self.pinMotorBackward, GPIO.LOW)
        self.pwmMotor.ChangeDutyCycle(dutycycle)
        time.sleep(delay)

    def backward(self, dutycycle, delay):
        print("Backwards " + str(dutycycle))
        GPIO.output(self.pinMotorForward, GPIO.LOW)
        GPIO.output(self.pinMotorBackward, GPIO.HIGH)
        self.pwmMotor.ChangeDutyCycle(dutycycle)
        time.sleep(delay)

    def cleanUp(self):
        self.stopMotor()
        GPIO.cleanup()


def main():
    dvigatel = DCMotor()
    dvigatel.cleanUp()


main()
