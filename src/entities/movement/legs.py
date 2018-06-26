import datetime
import time
import sys
from threading import Thread

sys.path.insert(0, '../../../src')

from helpers.servo_scanner import scan
from entities.movement.limb.leg import Leg
from entities.movement.sequences.sequences import *


class Legs(object):
    """
    Base class for legs which implements 4 instances of leg
    """

    def __init__(self, leg_0_servos, leg_1_servos, leg_2_servos, leg_3_servos):
        """
        Constructor for the legs
        :param leg_0_servos: Array of servo id`s for leg 0
        :param leg_1_servos: Array of servo id`s for leg 1
        :param leg_2_servos: Array of servo id`s for leg 2
        :param leg_3_servos: Array of servo id`s for leg 3
        """
        self.previous = datetime.datetime.now()  # The time used for delta timing
        self.all_Legs = True

        # Check if only 2 legs are connected for stair module
        servos = scan()
        if 61 in servos and 6 in servos and 21 not in servos:
            print("Initialise legs with only rear legs")
            self.all_Legs = False

        # Initialise a leg for each corner of the robot
        if self.all_Legs:
            self.leg_front_left = Leg(leg_0_servos, [530, 790, 520])
            self.leg_front_right = Leg(leg_1_servos, [530, 790, 520])
        self.leg_rear_left = Leg(leg_2_servos, [530, 790, 520])
        self.leg_rear_right = Leg(leg_3_servos, [530, 790, 520])

        if self.all_Legs:
            self.legs = [
                self.leg_front_left,
                self.leg_front_right,
                self.leg_rear_left,
                self.leg_rear_right
            ]
        else:
            self.legs = [
                self.leg_rear_left,
                self.leg_rear_right
            ]

        self.sequence = 0  # The current move sequence
        self.type = 'legs'
        self.deployed = False
        self.retract(120)  # Retract on constructing
        self.updating = False
        self.recent_package = [0, 0, 0]  # The bluetooth packages used for legs
        self.update_thread = Thread(target=self.leg_updater, args=(self,))  # The thread which runs the leg updater

        print("Legs setup, retracting")

    def move(self, leg_0_moves, leg_1_moves, leg_2_moves, leg_3_moves, speeds, self_update):
        """
        Function to move the legs_not_ready together
        :param leg_0_moves: Array of positions for leg 0
        :param leg_1_moves: Array of positions for leg 1
        :param leg_2_moves: Array of positions for leg 2
        :param leg_3_moves: Array of positions for leg 3
        :param speeds: Array of speeds for each servo
        :param self_update: If True, it locks the thread while legs are not ready,
            else updates must be handled for movement
        :return: None
        """

        if self.all_Legs:
            self.leg_front_left.move(leg_0_moves, speeds)
            self.leg_front_right.move(leg_1_moves, speeds)
        self.leg_rear_left.move(leg_2_moves, speeds)
        self.leg_rear_right.move(leg_3_moves, speeds)

        self.previous = datetime.datetime.now()  # setting previous time, because the delta time would be too big

        # Run this for autonomous movement
        if self_update:
            self.update_legs()

    def deploy(self, speed=100):
        """
        Deploys the legs so they can be used for walking
        :param speed: The speed at which the servo moves
        :return: None
        """
        deploy_state = [530, 250, 850]
        speeds = [speed, speed, speed]

        for leg in self.legs:
            leg.move(deploy_state, speeds)

        self.deployed = True
        self.update_legs()

    def retract(self, speed=100):
        """
        Retracts the legs to they are not in the way
        :param speed: The speed at which the servo moves
        :return: None
        """
        retract_state = [530, 790, 520]
        speeds = [speed, speed, speed]

        for leg in self.legs:
            leg.move(retract_state, speeds)

        self.deployed = False
        self.update_legs()

    def update_legs(self):
        """
        Function that keeps updating the leg positions as long as they are not ready
        :return: None
        """
        legs_not_ready = [elem for elem in self.legs if not elem.ready()]
        self.get_delta()
        print("Undready legs: " + str(len(legs_not_ready)))
        while len(legs_not_ready) != 0:
            delta = self.get_delta()
            for i in range(len(legs_not_ready)):
                legs_not_ready[i].update(delta)
            legs_not_ready = [elem for elem in self.legs if not elem.ready()]

    def get_delta(self):
        """
        Calculate the delta time, which can be used so movement always happens at same speed
        :return: Delta time
        """
        next_time = datetime.datetime.now()
        elapsed_time = next_time - self.previous
        self.previous = next_time
        return elapsed_time.total_seconds()

    def handle_controller_input(self, deploy, x_axis, y_axis):
        """
        Update the deploy, x_axis and y_axis status according to the bluetooth controller
        :param deploy: Int that determines if legs need to be deployed or not. 1 is deployed, 0 is retracted
        :param x_axis: The value of the x_axis
        :param y_axis: The value of the y_axis
        :return: None
        """
        self.recent_package = [deploy, x_axis, y_axis]

    def leg_updater(self, args):
        """
        Function that runs on a thread and constantly updates where the legs
        need to move according to the controller input
        :param args: Possible arguments from thread
        :return: None
        """
        # Keep rerunning so movement is always exactly same as controller input
        while True:

            # Set the variables received from controller
            deploy = self.recent_package[0]
            x_axis = self.recent_package[1]
            y_axis = self.recent_package[2]

            # If all inputs are 0 do nothing
            if deploy == 0 and x_axis == 0 and y_axis == 0:
                continue

            # If deploy command is true and legs are not deployed, deploy
            if deploy == 1 and not self.deployed:
                self.deploy(200)
            # If deploy command is false and legs are deployed, retract
            elif deploy == 0 and self.deployed:
                self.retract(200)

            # Set the speed according to the y_axis (vertical position of controller)
            speed = 0
            if y_axis > 530:
                speed = (y_axis - 512) * 0.4
            if y_axis < 500:
                speed = (512 - y_axis) * 0.4

            delta = self.get_delta()  # Get the delta time

            legs_not_ready = [elem for elem in self.legs if not elem.ready()]  # Retrieve unready legs

            # If the controller is in the neutral position,
            # put the leg in the deploy position
            if 500 < y_axis < 530 and self.deployed:
                self.deploy(200)

            # Run this if legs are deployed and ready
            if self.deployed and len(legs_not_ready) == 0:
                # If the controller is pushed forward, run the forward walking sequence
                if y_axis > 530:
                    self.run_sequence(speeds=[100, 100, 100],
                                      self_update=False,
                                      sequences=[self.sequence],
                                      sequence=None)
                    # Update which part of the current movement sequence is being ran
                    self.update_sequence()
                if y_axis < 500:
                    self.run_sequence(speeds=[100, 100, 100],
                                      self_update=False,
                                      sequences=[self.sequence],
                                      sequence=None)
                    self.update_sequence()
                self.get_delta()  # Update the delta time

            # Run this if not all legs are ready
            if len(legs_not_ready) > 0:
                for i in range(len(legs_not_ready)):
                    for y in range(len(legs_not_ready[i].servos)):
                        legs_not_ready[i].servos[y].set_speed(speed)  # Update servo speeds
                    legs_not_ready[i].update(delta)  # Update the leg
                time.sleep(0.02)  # Add a little delay so the legs move smoothly

            global current_speed
            current_speed = speed

    def update_sequence(self):
        """
        Function that updates on which part of the movement sequence the legs are in
        when controller by the controller.
        :return: None
        """
        if self.sequence < 3:
            self.sequence = self.sequence + 1
        else:
            self.sequence = 0

    def run_sequence(self, speeds, self_update=True, sequences=None, sequence=None):
        """
        Function that runs one of the leg movement sequences
        :param speeds: Array of speeds, one for each leg
        :param self_update: Variable that is false if controlled by controller and true if autonomous
        :param sequences: The moves of the sequence you want to run
        :param sequence: The movement sequence you want to run
        :return: None
        """
        if sequence is None:
            sequence = None
        if sequences is None:
            sequences = []
            seq_len = len(sequence)
            for i in range(seq_len):
                sequences.append(i)

        for moves in sequences:
            self.move(leg_0_moves=sequence[moves][0],
                      leg_1_moves=sequence[moves][1],
                      leg_2_moves=sequence[moves][2],
                      leg_3_moves=sequence[moves][3],
                      speeds=speeds,
                      self_update=self_update)
