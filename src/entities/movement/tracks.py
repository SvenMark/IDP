import time
import sys

sys.path.insert(0, '../../../src')

from entities.movement.limb.joints.dcmotor import DCMotor
from entities.movement.limb.track import Track


class Tracks(object):
    """
    Base class for tracks that controls the track classes
    """

    def __init__(self, track_0_pin, track_1_pin, track_0_forward, track_0_backward, track_1_forward, track_1_backward):
        """
        Constructor for the tracks class
        :param track_0_pin: The GPIO pin which the first track is connected to
        :param track_1_pin: The GPIO pin which the second track is connected to
        :param track_0_forward: GPIO direction pin for track 0
        :param track_0_backward: GPIO direction pin for track 0
        :param track_1_forward: GPIO direction pin for track 1
        :param track_1_backward: GPIO direction pin for track 1
        """

        # Initialise both motors as tracks. Each track has 1 motor.
        self.track_left = Track(track_0_pin, track_0_forward, track_0_backward)
        self.track_right = Track(track_1_pin, track_1_forward, track_1_backward)
        self.type = 'tracks'

        print("Tracks setup")

    def move_helper(self, duty_cycle_track_left, duty_cycle_track_right, delay, acceleration,
                    track_left_direction,
                    track_right_direction):
        """
        Function that makes sure the tracks don`t suddenly go to full power,
        instead they accelerate with an acceleration
        which is passed by the forward/backward/right/left functions
        :param duty_cycle_track_left: Percentage of power for left track
        :param duty_cycle_track_right: Percentage of power for right track
        :param delay: Time to wait after executing
        :param acceleration: Time in which the tracks accelerate to their given duty cycle in a linear manner
        :param track_left_direction: Direction of left track, 1 is forward 0 is backward
        :param track_right_direction: Direction of right track, 1 is forward 0 is backward
        :return: None
        """

        # If acceleration is smaller or equal to 0 set it to 0.01 to prevent sudden shocks in the power train.
        if acceleration <= 0:
            # print("Warning, setting acceleration to 0.01")
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
        for i in range(0, int(100 * acceleration)):

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
            time.sleep(0.01)  # Add a little delay so the motor accelerates smoothly

        time.sleep(delay)

    def forward(self, duty_cycle_track_left, duty_cycle_track_right, delay, acceleration):
        """
        Function for moving tracks in a forward direction.
        :param duty_cycle_track_left: Percentage of power for left track
        :param duty_cycle_track_right: Percentage of power for right track
        :param delay: Time to wait after executing
        :param acceleration: Time in which the tracks accelerate to their given duty cycle in a linear manner.
        :return: None
        """
        self.move_helper(duty_cycle_track_left, duty_cycle_track_right, delay, acceleration, 1, 1)

    def backward(self, duty_cycle_track_left, duty_cycle_track_right, delay, acceleration):
        """
        Function for moving tracks in a backward direction
        :param duty_cycle_track_left: Percentage of power for left track
        :param duty_cycle_track_right: Percentage of power for right track
        :param delay: Time to wait after executing
        :param acceleration: Time in which the tracks accelerate to their given duty cycle in a linear manner.
        :return: None
        """
        self.move_helper(duty_cycle_track_left, duty_cycle_track_right, delay, acceleration, 0, 0)

    def turn_right(self, duty_cycle_track_left, duty_cycle_track_right, delay, acceleration):
        """
        Function for moving tracks in a right direction by turning left track forward and right track backward.
        :param duty_cycle_track_left: Percentage of power for left track
        :param duty_cycle_track_right: Percentage of power for right track
        :param delay: Time to wait after executing
        :param acceleration: Time in which the tracks accelerate to their given duty cycle in a linear manner.
        :return: None
        """
        self.move_helper(duty_cycle_track_left, duty_cycle_track_right, delay, acceleration, 1, 0)

    def turn_left(self, duty_cycle_track_right, duty_cycle_track_left, delay, acceleration):
        """
        Function for moving tracks in a right direction by turning left track backward and right track forward.
        :param duty_cycle_track_left: Percentage of power for left track
        :param duty_cycle_track_right: Percentage of power for right track
        :param delay: Time to wait after executing
        :param acceleration: Time in which the tracks accelerate to their given duty cycle in a linear manner.
        :return: None
        """
        self.move_helper(duty_cycle_track_left, duty_cycle_track_right, delay, acceleration, 0, 1)

    def handle_controller_input(self, stop_motors, vertical_speed, horizontal_speed, dead_zone):
        """
        Function that handles the bluetooth controller input
        :param stop_motors: Value that stops or starts motors, 1 is off, 0 is on
        :param vertical_speed: The vertical speed of the controller joystick
        :param horizontal_speed: The horizontal speed of the controller joystick
        :param dead_zone: Variable that determines the size of the dead zone
        :return: None
        """
        if stop_motors == 1:
            self.stop()
        elif stop_motors == 0:
            if -dead_zone < vertical_speed < dead_zone and -dead_zone < horizontal_speed < dead_zone:
                self.stop()

            # Move backwards
            if vertical_speed < -dead_zone:
                if -dead_zone < horizontal_speed < dead_zone:
                    self.backward(duty_cycle_track_left=abs(vertical_speed),
                                  duty_cycle_track_right=abs(vertical_speed) * 0.95,
                                  delay=0,
                                  acceleration=0)
                # Backward left
                if horizontal_speed < -dead_zone:
                    horizontal_speed = horizontal_speed / 2
                    self.backward(duty_cycle_track_left=abs(vertical_speed),
                                  duty_cycle_track_right=abs(vertical_speed) - horizontal_speed,
                                  delay=0,
                                  acceleration=0)
                # Backward right
                if horizontal_speed > dead_zone:
                    horizontal_speed = abs(horizontal_speed / 2)
                    self.backward(duty_cycle_track_left=abs(vertical_speed),
                                  duty_cycle_track_right=abs(vertical_speed) - horizontal_speed,
                                  delay=0,
                                  acceleration=0)

            # Move forward
            if vertical_speed > dead_zone:
                if -dead_zone < horizontal_speed < dead_zone:
                    self.forward(duty_cycle_track_left=vertical_speed,
                                 duty_cycle_track_right=vertical_speed * 0.95,
                                 delay=0,
                                 acceleration=0)
                # Forward left
                if horizontal_speed < -dead_zone:
                    horizontal_speed = horizontal_speed / 2
                    self.forward(duty_cycle_track_left=vertical_speed,
                                 duty_cycle_track_right=vertical_speed - horizontal_speed,
                                 delay=0,
                                 acceleration=0)
                # Forward right
                if horizontal_speed > dead_zone:
                    horizontal_speed = abs(horizontal_speed / 2)
                    self.forward(duty_cycle_track_left=vertical_speed,
                                 duty_cycle_track_right=vertical_speed - horizontal_speed,
                                 delay=0,
                                 acceleration=0)

            # Turn around it`s axis
            if -dead_zone < vertical_speed < dead_zone:
                if horizontal_speed > dead_zone:
                    self.turn_right(duty_cycle_track_left=horizontal_speed / 1.5,
                                    duty_cycle_track_right=horizontal_speed / 1.6,
                                    delay=0,
                                    acceleration=0)

                if horizontal_speed < -dead_zone:
                    self.turn_left(duty_cycle_track_left=abs(horizontal_speed) / 1.5,
                                   duty_cycle_track_right=abs(horizontal_speed) / 1.6,
                                   delay=0,
                                   acceleration=0)

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
