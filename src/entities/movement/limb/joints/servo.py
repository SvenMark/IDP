#!/bin/python

import time

from libs.ax12 import Ax12


class Servo(object):
    """
    Base class for servo
    """

    # Constructor for servo class.
    # It expects the id of the servo and the initial position.
    def __init__(self, servo_id, initial_position):

        # Create an instance of the Ax12 servo class from the Ax12 library.
        self.ax12 = Ax12()

        # Set the servo variables and move servo to initial position.
        self.servo_id = servo_id
        self.last_position = initial_position
        self.ax12.move(servo_id, initial_position)
        self.sensitivity = 2
        time.sleep(0.1)

    # Function that checks if the servo already completed it`s last move or not.
    def is_ready(self):
        return abs(self.ax12.read_position(self.servo_id) - self.last_position) <= self.sensitivity

    # Function that moves the servo.
    # It expects the position it needs to move to and a delay.
    def move(self, degrees, delay):

        # If degrees are out of range print an error
        if degrees < 0 or degrees > 998:
            print("In servo " + str(self.servo_id) + ", degrees: " + str(degrees) + ", must be between 0 and 998")

        # While the servo has not completed it last command wait a bit and check again.
        while not self.is_ready():
            time.sleep(0.1)

        # Move the servo using the ax12 library with the servo id and degrees.
        self.ax12.move(self.servo_id, degrees)

        # Set the last position to the degrees.
        self.last_position = degrees

        time.sleep(delay)

    # Read the current position of the servo.
    def read_position(self):
        return self.ax12.read_position(self.servo_id)


def main():
    servo = Servo(13, 0)
    servo.move(500, 0)


if __name__ == "__main__":
    main()
