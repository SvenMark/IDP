import datetime
import time
import sys
from threading import Thread

sys.path.insert(0, '../../../src')

from entities.movement.limb.joints.servo import Servo
from entities.movement.sequences.sequences import *


class Grabber(object):
    """
    Base class for grabber which directly implements servo
    """

    def __init__(self, servos, initial_positions):
        """
        Constructor for grabber class
        :param servos: Array of grabber servo id`s
        :param initial_positions: Array of servo positions
        """
        self.previous = datetime.datetime.now()  # The time used for delta timing

        self.servo_0 = Servo(servos[0], initial_positions[0], 5)
        self.servo_1 = Servo(servos[1], initial_positions[1], 5)
        self.servo_2 = Servo(servos[2], initial_positions[2], 5)

        self.servos = [self.servo_0, self.servo_1, self.servo_2]

        self.reposition = False
        self.grabbed = False
        self.grabbing = False

        self.loosen(100)

        self.type = 'grabber'
        print("Grabber setup")

    def grab(self, speed, pick_up_vertical):
        """
        Function that contains commands to close grabber
        :param speed: Speed to move with
        :param pick_up_vertical: To pick up vertical or not
        :return: None
        """
        positions = [210, 430, 83]  # The servo positions for grabbing

        self.grabbing = True

        # TODO: Implement vertical and horizontal
        if pick_up_vertical:
            for i in range(len(self.servos)):
                self.servos[i].move(positions[i], speed)
        else:
            for i in range(len(self.servos)):
                self.servos[i].move(positions[i], speed)
        self.update()  # Update the servos

        self.grabbed = True
        self.grabbing = False

    def loosen(self, speed):
        """
        Function that contains commands top open grabber
        :param speed: Speed to move with
        :return: None
        """
        positions = [455, 185, 83]  # The servo positions for loosening
        for i in range(len(self.servos)):
            self.servos[i].move(positions[i], speed)
        self.update()
        self.grabbed = False

    def get_delta(self):
        """
        Calculate the delta time, which can be used so movement always happens at same speed
        :return: Delta time
        """
        next_time = datetime.datetime.now()
        elapsed_time = next_time - self.previous
        self.previous = next_time
        return elapsed_time.total_seconds()

    def update(self):
        """
        Update all the unready servos
        :return: None
        """
        self.get_delta()
        while len([elem for elem in self.servos if not elem.is_ready()]) != 0:
            print("Unready servos: " + str(len([elem for elem in self.servos if not elem.is_ready()])))
            delta = self.get_delta()
            for i in range(len(self.servos)):
                if not self.servos[i].is_ready():
                    print("Servo " + str(self.servos[i].servo_id) + " Load: " + str(self.servos[i].read_load()))
                    print("Total load: " + str(self.servos[0].read_load() + self.servos[1].read_load()))
                    if self.servos[0].read_load() + self.servos[1].read_load() > 2000 and self.grabbing:
                        print("Load to high, loosening: " + str(self.servos[i].read_load()))
                        self.loosen(100)
                        self.reposition = True
                        break
                    self.servos[i].update(delta)


