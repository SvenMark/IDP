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
        self.pin_motor_forward = 10
        self.pin_motor_backward = 9
        self.pin_pwm = 18
        self.frequency = 20
        self.stop = 0

        GPIO.setup(self.pin_pwm, GPIO.OUT)
        GPIO.setup(self.pin_motor_forward, GPIO.OUT)
        GPIO.setup(self.pin_motor_backward, GPIO.OUT)

        self.pwmMotor = GPIO.PWM(self.pin_pwm, self.frequency)
        self.pwmMotor.start(self.stop)

        print("Setup")

    # Turn all motors off
    def stop_motor(self):
        self.pwmMotor.ChangeDutyCycle(self.stop)

    # Turn both motors forwards
    def forward(self, dutycycle, delay):
        print("Forwards " + str(dutycycle))
        GPIO.output(self.pin_motor_forward, GPIO.HIGH)
        GPIO.output(self.pin_motor_backward, GPIO.LOW)
        self.pwmMotor.ChangeDutyCycle(dutycycle)
        time.sleep(delay)

    def backward(self, dutycycle, delay):
        print("Backwards " + str(dutycycle))
        GPIO.output(self.pin_motor_forward, GPIO.LOW)
        GPIO.output(self.pin_motor_backward, GPIO.HIGH)
        self.pwmMotor.ChangeDutyCycle(dutycycle)
        time.sleep(delay)

    def clean_up(self):
        self.stopMotor()
        GPIO.cleanup()


def main():
    dvigatel = DCMotor()
    dvigatel.clean_up()


main()
