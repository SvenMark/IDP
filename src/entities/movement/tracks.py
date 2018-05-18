import time
import math

from entities.movement.limb.limb import Limb
from entities.movement.limb.joints.dcmotor import DCMotor


class Tracks(object):
    """
    Base class for tracks that implements DC motors
    """

    def __init__(self, track_0_pin, track_1_pin):

        # Initialise both motors as tracks. Each track has 1 motor.
        self.track_left = DCMotor(track_0_pin)
        self.track_right = DCMotor(track_1_pin)

        print("Tracks setup")

    def move_helper(self, duty_cycle_track_left, duty_cycle_track_right, delay, acceleration,
                    track_left_direction,
                    track_right_direction):
        """
        Function that makes sure the tracks don`t suddenly go to full power,
        instead they accelerate with an acceleration
        which is passed by the forward/backward/right/left functions.
        :param duty_cycle_track_left: percentage of power for left track
        :param duty_cycle_track_right: percentage of power for right track
        :param delay: time to wait after executing
        :param acceleration: time in which the tracks accelerate to their given duty cycle in a linear manner.
        :param track_left_direction: Direction of left track, 1 is forward 0 is backward
        :param track_right_direction: Direction of right track, 1 is forward 0 is backward
        :return: None
        """

        # If acceleration is smaller or equal to 0 set it to 0.01 to prevent sudden shocks in the power train.
        if acceleration <= 0:
            print("Warning, setting acceleration to 0.01")
            acceleration = 0.01

        # Calculate the difference between the required duty cycle and current duty cycle.
        diff_1 = duty_cycle_track_left - self.track_left.current_speed
        diff_2 = duty_cycle_track_right - self.track_right.current_speed

        # Calculate the step size of the acceleration.
        step_1 = diff_1 / acceleration / 100
        step_2 = diff_2 / acceleration / 100

        # Get the current speed.
        speed_1 = self.track_left.current_speed
        speed_2 = self.track_right.current_speed

        # Loop which accelerates the tracks.
        for i in range(0, 100 * acceleration):

            # Add the step size to the speed each cycle.
            speed_1 += step_1
            speed_2 += step_2

            # Round the speed to contain 3 decimals.
            speed_1 = round(speed_1, 3)
            speed_2 = round(speed_2, 3)

            # Prevent speed from going below 0 and above 100.
            if speed_1 < 0:
                speed_1 = 0
            if speed_2 < 0:
                speed_2 = 0
            if speed_1 > 100:
                speed_1 = 100
            if speed_2 > 100:
                speed_2 = 100

            # Pass the new speed to each motor.
            # Track direction 1 is forwards, direction 0 is backwards.
            if track_left_direction == 1 and track_right_direction == 1:
                self.track_left.forward(speed_1, 0)
                self.track_right.forward(speed_2, 0)

            if track_left_direction == 0 and track_right_direction == 0:
                self.track_left.backward(speed_1, 0)
                self.track_right.backward(speed_2, 0)

            if track_left_direction == 1 and track_right_direction == 0:
                self.track_left.forward(speed_1, 0)
                self.track_right.backward(speed_2, 0)

            if track_left_direction == 0 and track_right_direction == 1:
                self.track_left.backward(speed_1, 0)
                self.track_right.forward(speed_2, 0)

            # Add a little delay so the motor accelerates smoothly
            time.sleep(0.01)

        time.sleep(delay)

    def forward(self, duty_cycle, delay, acceleration):
        """
        Function for moving tracks in a forward direction.
        :param duty_cycle: percentage of power for both tracks
        :param delay: time to wait after executing
        :param acceleration: time in which the tracks accelerate to their given duty cycle in a linear manner.
        :return: None
        """
        self.move_helper(duty_cycle, duty_cycle, delay, acceleration, 1, 1)

    def backward(self, duty_cycle, delay, acceleration):
        """
        Function for moving tracks in a backward direction
        :param duty_cycle: percentage of power for both tracks
        :param delay: time to wait after executing
        :param acceleration: time in which the tracks accelerate to their given duty cycle in a linear manner.
        :return: None
        """
        self.move_helper(duty_cycle, duty_cycle, delay, acceleration, 0, 0)

    def turn_right(self, duty_cycle_track_left, duty_cycle_track_right, delay, acceleration):
        """
        Function for moving tracks in a right direction by turning left track forward and right track backward.
        :param duty_cycle_track_left: percentage of power for right track
        :param duty_cycle_track_right: percentage of power for left track
        :param delay: time to wait after executing
        :param acceleration: time in which the tracks accelerate to their given duty cycle in a linear manner.
        :return: None
        """
        self.move_helper(duty_cycle_track_left, duty_cycle_track_right, delay, acceleration, 1, 0)

    def turn_left(self, duty_cycle_track_right, duty_cycle_track_left, delay, acceleration):
        """
        Function for moving tracks in a right direction by turning left track backward and right track forward.
        :param duty_cycle_track_right: percentage of power for right track
        :param duty_cycle_track_left: percentage of power for left track
        :param delay: time to wait after executing
        :param acceleration: time in which the tracks accelerate to their given duty cycle in a linear manner.
        :return: None
        """
        self.move_helper(duty_cycle_track_left, duty_cycle_track_right, delay, acceleration, 0, 1)

    def stop(self):
        """
        Function that stops the tracks moving
        :return: None
        """
        self.track_left.stop_motor()
        self.track_right.stop_motor()

    def clean_up(self):
        """
        Function to clean up the GPIO for both motors
        :return: None
        """
        self.track_left.clean_up()
        self.track_right.clean_up()
