import datetime
import sys

sys.path.insert(0, '../../../src')

from entities.movement.limb.leg import Leg
from entities.movement.sequences.walking_sequences import *

from threading import Thread
import time

class Legs(object):

    def __init__(self, leg_0_servos,
                 # leg_1_servos,
                 # leg_2_servos,
                 # leg_3_servos
                 ):
        """
        Constructor for the legs
        :param leg_0_servos: Array of servo id`s for leg 0
        :param leg_1_servos: Array of servo id`s for leg 1
        :param leg_2_servos: Array of servo id`s for leg 2
        :param leg_3_servos: Array of servo id`s for leg 3
        """

        self.previous = datetime.datetime.now()


        # Initialise a leg for each corner of the robot
        self.leg_front_left = Leg(leg_0_servos, [530, 210, 475])
        # self.leg_front_right = Leg(leg_1_servos, [530, 210, 475])
        # self.leg_rear_left = Leg(leg_2_servos, [530, 210, 475])
        # self.leg_rear_right = Leg(leg_3_servos, [530, 210, 475])

        self.legs = [self.leg_front_left,
                     #self.leg_front_right, self.leg_rear_left, self.leg_rear_right
                     ]

        self.sequence = 0
        self.type = 'legs'
        self.deployed = False
        self.retract(120)

        self.updater = False
        self.update_thread = Thread()
        self.x_axis = 0
        self.y_axis = 0

        # deploy, x-axis, y-axis
        self.recent_package = [0, 0, 0]

        print("Legs setup, retracting")
        
    def move(self, leg_0_moves, leg_1_moves, leg_2_moves, leg_3_moves, delay, speeds, self_update=True):
        """
        Function to move the legs_not_ready together
        :param leg_0_moves: Array of positions for leg 0
        :param leg_1_moves: Array of positions for leg 1
        :param leg_2_moves: Array of positions for leg 2
        :param leg_3_moves: Array of positions for leg 3
        :param delay: Time to wait after executing
        :param speeds: Array of speeds for each servo
        :param self_update: If True, it locks the thread while legs are not ready,
            else updates must be handled for movement
        :return: None
        """

        self.leg_front_left.move(leg_0_moves, delay, speeds)
        # self.leg_front_right.move(leg_1_moves[0], leg_1_moves[1], leg_1_moves[2], delay)
        # self.leg_rear_left.move(leg_2_moves[0], leg_2_moves[1], leg_2_moves[2], delay)
        # self.leg_rear_right.move(leg_3_moves[0], leg_3_moves[1], leg_3_moves[2], delay)

        # setting previous time, because the delta time would be too big
        self.previous = datetime.datetime.now()

        if self_update:
            self.update_legs()

    def update_legs(self):
        # while legs_not_ready are not ready, update
        legs_not_ready = [elem for elem in self.legs if not elem.ready()]
        self.get_delta()
        while len(legs_not_ready) != 0:
            delta = self.get_delta()
            for i in range(len(legs_not_ready)):
                legs_not_ready[i].update(delta)
            legs_not_ready = [elem for elem in self.legs if not elem.ready()]

    def get_delta(self):
        next_time = datetime.datetime.now()
        elapsed_time = next_time - self.previous
        self.previous = next_time
        return elapsed_time.total_seconds()

    def deploy(self, speed):
        """
        Deploys the legs so they can be used for walking
        :param speed: The speed at which the servo moves
        :return: None
        """
        
        leg_0_deploy = [530, 766, 850]
        leg_1_deploy = [0, 0, 0]
        leg_2_deploy = [0, 0, 0]
        leg_3_deploy = [0, 0, 0]
        delay = 0.1

        self.leg_front_left.move(leg_0_deploy, delay, [speed, speed, speed])
        # self.leg_front_right.move(leg_1_deploy, delay, [speed, speed, speed])
        # self.leg_rear_left.move(leg_2_deploy, delay, [speed, speed, speed])
        # self.leg_rear_right.move(leg_3_deploy, delay, [speed, speed, speed])

        self.update_legs()

        self.deployed = True

    def retract(self, speed):
        """
        Retracts the legs to they are not in the way
        :param speed: The speed at which the servo moves
        :return: None
        """
        
        leg_0_retract = [530, 200, 470]
        leg_1_retract = [0, 0, 0]
        leg_2_retract = [0, 0, 0]
        leg_3_retract = [0, 0, 0]
        delay = 0.1
        
        self.leg_front_left.move(leg_0_retract, delay, [speed, speed, speed])
        # self.leg_front_right.move(leg_1_retract, delay, [speed, speed, speed])
        # self.leg_rear_left.move(leg_2_retract, delay, [speed, speed, speed])
        # self.leg_rear_right.move(leg_3_retract, delay, [speed, speed, speed])

        self.update_legs()

        self.deployed = False

    def update_sequence(self):
        if self.sequence < 3:
            self.sequence = self.sequence + 1
        else:
            self.sequence = 0

    def handle_controller_input(self, deploy, x_axis, y_axis):
        self.recent_package = [deploy, x_axis, y_axis]

        if self.deployed and not self.updater:
            self.update_thread = Thread(target=leg_updater, args=(self, ))
            self.update_thread.start()

            # Move according to joystick direction
            # self.move([530 + round(x_axis / 10), 680, 760 + round(y_axis / 10)],
            #           [650, 400, 400],
            #           [400, 400, 400],
            #           [600, 400, 400],
            #           0,
            #           [200, 200, 200])
        elif self.deployed:
            self.update_thread.join()


def leg_updater(self):
    self.updater = True

    while True:
        deploy = self.recent_package[0]
        x_axis = self.recent_package[1]
        y_axis = self.recent_package[2]

        if deploy == 1 and not self.deployed:
            self.deploy(200)
        elif deploy == 0 and self.deployed:
            self.retract(200)
        speed = 0
        if y_axis > 530:
            speed = (y_axis - 512) * 0.4
        if y_axis < 500:
            speed = (512 - y_axis) * 0.4

        delta = self.get_delta()

        legs_not_ready = [elem for elem in self.legs if not elem.ready()]

        if self.deployed and len(legs_not_ready) == 0:
            if 500 < y_axis < 530:
                self.deploy(200)
            if y_axis > 530:
                walk_forward(self, [100, 100, 100],
                             self_update=False,
                             sequences=[self.sequence])
                self.update_sequence()
            if y_axis < 500:
                walk_backward(self, [100, 100, 100],
                              self_update=False,
                              sequences=[self.sequence])
                self.update_sequence()
            self.get_delta()

        if len(legs_not_ready) > 0:
            for i in range(len(legs_not_ready)):
                for y in range(len(legs_not_ready[i].servos)):
                    legs_not_ready[i].servos[y].set_speed(speed)
                legs_not_ready[i].update(delta)
