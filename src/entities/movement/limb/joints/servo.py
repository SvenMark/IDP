from __future__ import division

import sys
import math
import time
import numpy as np

sys.path.insert(0, '../../../../../src')

from libs.ax12 import Ax12


class Servo(object):
    """
    Base class for servo
    """

    def __init__(self, servo_id, initial_position):
        """
        Constructor for servo class
        :param servo_id: ID of the servo
        :param initial_position: The position you want to set the servo at on initialising
        """

        # Create an instance of the Ax12 servo class from the Ax12 library.
        self.ax12 = Ax12()

        print("Setting servo " + str(servo_id) + " to " + str(initial_position))
        # Set the servo variables and move servo to initial position.
        self.servo_id = servo_id
        self.last_position = self.ax12.read_position(self.servo_id)
        self.goal = initial_position
        self.current_speed = 200
        self.current_speed_multiplier = 0.02

        self.start_position = self.last_position

        # self.move(servo_id, initial_position, 300)

        self.sensitivity = 3
        print("rw : " + str(self.ax12.read_rw_status(self.servo_id)))

        time.sleep(0.1)

    def set_speed(self, speed):
        self.current_speed = speed * self.current_speed_multiplier

    def update(self, delta):
        # move towards new position
        step = (self.goal - self.start_position) * delta * self.current_speed

        if step > 0 and self.last_position > self.goal:
            self.start_position = self.last_position
            step = (self.goal - self.start_position) * delta * self.current_speed

        if step < 0 and self.last_position < self.goal:
            self.start_position = self.last_position
            step = (self.goal - self.start_position) * delta * self.current_speed

        # print("Delta: " + str(delta) + " Step: " + str(step) + " Goal: " + str(self.goal) + " Last_pos: " + str(self.last_position) + " Start_pos: " + str(self.start_position))
        if self.last_position + step > 1024 or self.last_position + step < 0:
            print(str(self.last_position + step) + " not in range " + str(self.servo_id) + "speed "
                  + str(self.current_speed) + "delta " + str(delta))
            return
        self.last_position = self.last_position + step
        self.ax12.move(self.servo_id, round(self.last_position))

    def move(self, degrees, delay, speed):
        self.last_position = self.ax12.read_position(self.servo_id)
        self.start_position = self.last_position
        self.goal = degrees
        self.current_speed = speed * self.current_speed_multiplier
        print("servo " + str(self.servo_id) + ", start: " + str(self.last_position) + ", goal: " + str(self.goal))

    def move_speed(self, degrees, delay, max_speed):
        """
        Function that moves the servo using the ax12 library move function
        :param degrees: Position to move to
        :param delay: Time to wait after executing
        :param max_speed: The speed at which the servo moves
        :return: None
        """

        # If degrees are out of range print an error
        if degrees < 0 or degrees > 1024:
            print("In servo " + str(self.servo_id) + ", degrees: " + str(degrees) + ", must be between 0 and 998")

        # While the servo has not completed it last command wait a bit and check again.
        while not self.is_ready():
            time.sleep(0.01)

        max_speed = round(max_speed * 1)
        # Could be changed or set as parameter
        total_steps = 1

        # Calculating de difference that has to be moved
        start_position = self.last_position
        difference = degrees - start_position
        step = difference / total_steps

        current_position = start_position

        for i in range(total_steps):
            current_position += step
            speed = math.sin((i + 0.5) / total_steps * math.pi) * max_speed
            print("Servo " + str(self.servo_id) + ", step: " + str(i) + ", speed: " + str(round(speed)) + ", degrees: " + str(round(current_position)))
            # Move the servo using the ax12 library with the servo id and degrees.
            try:
                self.ax12.move_speed(self.servo_id, round(current_position), round(speed))
            except Ax12.timeout_error:
                print("Timeout")
            self.last_position = current_position
            while not self.is_ready:
                time.sleep(0.1)
        # Set the last position to the degrees.
        self.last_position = degrees

        time.sleep(delay)

    def move_backup(self, degrees, delay, speed):

        # Move the servo using the ax12 library with the servo id and degrees.
        self.ax12.move_speed(self.servo_id, degrees, speed)

        # Set the last position to the degrees.
        self.last_position = degrees

        time.sleep(delay)

    def is_ready(self):
        """
        Function that checks if a servo completed it`s last move
        :return: Whether or not the servo has completed it`s last move
        """
        return abs(round(self.last_position) - round(self.goal)) <= self.sensitivity

    def read_position(self):
        """
        Read the position of the servo
        :return: Current position of this servo
        """
        return self.ax12.read_position(self.servo_id)

    def read_speed(self):
        """
        Read the speed of the servo
        :return: The servo speed
        """
        return self.ax12.read_speed(self.servo_id)


def main():
    servo = Servo(13, 0)
    servo.move(500, 0, 80)


if __name__ == "__main__":
    main()
