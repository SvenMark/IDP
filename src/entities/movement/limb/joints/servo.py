from __future__ import division

import sys
import math
import time
import numpy as np
from threading import Thread
sys.path.insert(0, '../../../../../src')

from libs.ax12 import Ax12


class Servo(object):
    """
    Base class for servo
    """

    def __init__(self, servo_id, initial_position, sensitivity):
        """
        Constructor for servo class
        :param servo_id: ID of the servo
        :param initial_position: The position you want to set the servo at on initialising
        :param sensitivity: The amount of play there is in the servo position
        """
        self.ax12 = Ax12()  # Create an instance of the Ax12 servo class from the Ax12 library.
        self.servo_id = servo_id  # Set the servo variables

        self.last_position = self.read_position()  # Set the last servo position as the current position
        self.goal = initial_position  # Set the initial position as the goal position
        self.current_speed = 200
        self.current_speed_multiplier = 0.02
        self.start_position = self.last_position  # Set the starting position of each move as the last pos
        self.sensitivity = sensitivity

        print("Servo " + str(self.servo_id) + " setup")
        time.sleep(0.1)  # Add a little delay so data line doesnt overflow

    def set_speed(self, speed):
        """
        Update the speed of the servo
        :param speed: The speed
        :return: None
        """
        self.current_speed = speed * self.current_speed_multiplier

    def lock_thread(self):
        """
        Locks the servo while idle
        :return: None
        """
        while self.is_ready():
            self.ax12.move(self.servo_id, round(self.last_position))
            time.sleep(0.1)

    def update(self, delta):
        """
        Update the servo position according to delta time
        :param delta: Delta time
        :return: None
        """

        # No update needed
        # if not self.is_ready():
        #     print("Servo {} is ready, but update has been called".format(self.servo_id))
        #     return

        step = (self.goal - self.start_position) * delta * self.current_speed  # move towards new position

        if step > 0 and self.last_position > self.goal:
            self.start_position = self.last_position
            step = (self.goal - self.start_position) * delta * self.current_speed

        if step < 0 and self.last_position < self.goal:
            self.start_position = self.last_position
            step = (self.goal - self.start_position) * delta * self.current_speed

        if self.last_position + step > 1024 or self.last_position + step < 0:
            print(str(self.last_position + step) + " not in range " + str(self.servo_id) + "speed "
                  + str(self.current_speed) + "delta " + str(delta))
            return

        self.last_position = self.last_position + step
        self.ax12.move(self.servo_id, round(self.last_position))

        if self.is_ready():
            Thread(target=self.lock_thread, args=(self,)).start()  # Lock the servo if the move is finished

    def move(self, degrees, speed):
        """
        Function that moves the servo using the ax12 library move function
        :param degrees: Position to move to
        :param speed: The speed at which the servo moves
        :return: None
        """
        self.last_position = self.read_position()  # Set the last_position as current position
        self.start_position = self.last_position  # Set the start position of the movement
        self.goal = degrees
        self.current_speed = speed * self.current_speed_multiplier
        print("servo " + str(self.servo_id) + ", start: " + str(self.last_position) + ", goal: " + str(self.goal))

    def is_ready(self):
        """
        Function that checks if a servo completed it`s last move
        :return: Whether or not the servo has completed it`s last move
        """
        print("Last pos: " + str(self.last_position) + " Goal: " + str(self.goal))
        return abs(round(self.last_position) - round(self.goal)) <= self.sensitivity

    def read_position(self):
        """
        Read the position of the servo
        :return: Current position of this servo
        """
        result = self.ax12.read_position(self.servo_id)

        # In case servo position is not read the first time, keep trying
        while result is None:
            print("Can't read servo " + str(self.servo_id) + " position, trying again")
            result = self.ax12.read_position(self.servo_id)

        return result

    def read_speed(self):
        """
        Read the speed of the servo
        :return: The servo speed
        """
        return self.ax12.read_speed(self.servo_id)


def main():
    servo = Servo(13, 0, 5)
    servo.move(500, 80)


if __name__ == "__main__":
    main()
