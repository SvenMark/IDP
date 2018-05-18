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

    # Function that makes sure the tracks don`t suddenly go to full power,
    # instead they accelerate with an acceleration
    # which is passed by the forward/backward/right/left functions.
    def move_helper(self, duty_cycle_track_left, duty_cycle_track_right, delay, acceleration,
                    track_1_direction,
                    track_2_direction):

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
            if track_1_direction == 1 and track_2_direction == 1:
                self.track_left.forward(speed_1, 0)
                self.track_right.forward(speed_2, 0)

            if track_1_direction == 0 and track_2_direction == 0:
                self.track_left.backward(speed_1, 0)
                self.track_right.backward(speed_2, 0)

            if track_1_direction == 1 and track_2_direction == 0:
                self.track_left.forward(speed_1, 0)
                self.track_right.backward(speed_2, 0)

            if track_1_direction == 0 and track_2_direction == 1:
                self.track_left.backward(speed_1, 0)
                self.track_right.forward(speed_2, 0)

            # Add a little delay so the motor accelerates smoothly
            time.sleep(0.01)

        time.sleep(delay)

    # Function for moving tracks in a forward direction.
    # Duty cycle is the percentage of engine power used.
    # Delay is how much time the function will wait after executing.
    # Acceleration is the time it will take to go to the preferred duty cycle.
    def forward(self, duty_cycle, delay, acceleration):
        self.move_helper(duty_cycle, duty_cycle, delay, acceleration, 1, 1)

    # Function for moving tracks in a backward direction
    def backward(self, duty_cycle, delay, acceleration):
        self.move_helper(duty_cycle, duty_cycle, delay, acceleration, 0, 0)

    # Function for moving tracks in a right direction by turning left track forward and right track backward.
    def turn_right(self, duty_cycle_track_left, duty_cycle_track_right, delay, acceleration):
        self.move_helper(duty_cycle_track_left, duty_cycle_track_right, delay, acceleration, 1, 0)

    # Function for moving tracks in a right direction by turning left track backward and right track forward.
    def turn_left(self, duty_cycle_track_right, duty_cycle_track_left, delay, acceleration):
        self.move_helper(duty_cycle_track_left, duty_cycle_track_right, delay, acceleration, 0, 1)

    # Function that stops the tracks moving
    def stop(self):
        self.track_left.stop_motor()
        self.track_right.stop_motor()

    # Function to clean up the GPIO for both motors
    def clean_up(self):
        self.track_left.clean_up()
        self.track_right.clean_up()
