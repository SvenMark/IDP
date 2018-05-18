#!/bin/python

import time  # Import the Time library

import RPi.GPIO as GPIO  # Import the GPIO Library


class DCMotor(object):
    """
    Base class for dc motor
    """

    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.pin_motor_forward = 10
        self.pin_motor_backward = 9
        self.pin_pwm = pin
        self.frequency = 1000
        self.stop = 0
        self.current_speed = 0

        GPIO.setup(self.pin_pwm, GPIO.OUT)
        GPIO.setup(self.pin_motor_forward, GPIO.OUT)
        GPIO.setup(self.pin_motor_backward, GPIO.OUT)

        self.pwm_motor = GPIO.PWM(self.pin_pwm, self.frequency)
        self.pwm_motor.start(self.stop)

        print("Setup")

    # Turn all motors off
    def stop_motor(self):
        self.pwm_motor.ChangeDutyCycle(self.stop)
        self.current_speed = 0

    # Turn both motors forwards
    def forward(self, duty_cycle, delay):
        print("Forwards " + str(duty_cycle))
        GPIO.output(self.pin_motor_forward, GPIO.HIGH)
        GPIO.output(self.pin_motor_backward, GPIO.LOW)
        self.pwm_motor.ChangeDutyCycle(duty_cycle)
        self.current_speed = duty_cycle
        time.sleep(delay)

    def backward(self, duty_cycle, delay):
        print("Backwards " + str(duty_cycle))
        GPIO.output(self.pin_motor_forward, GPIO.LOW)
        GPIO.output(self.pin_motor_backward, GPIO.HIGH)
        self.pwm_motor.ChangeDutyCycle(duty_cycle)
        self.current_speed = duty_cycle
        time.sleep(delay)

    def clean_up(self):
        self.stop_motor()
        self.current_speed = 0
        GPIO.cleanup()


def main():
    dvigatel = DCMotor(16)
    dvigatel.clean_up()


if __name__ == "__main__":
    main()
