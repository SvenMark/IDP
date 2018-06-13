import datetime
import time
import sys
from threading import Thread

sys.path.insert(0, '../../../src')

from entities.movement.limb.joints.servo import Servo
from entities.movement.sequences.sequences import *


class Grabber(object):

    def __init__(self, id_servo, initial_positions):
        """

        :param id_servo:
        :param initial_positions:
        """
        self.previous = datetime.datetime.now()

        self.servo_0 = Servo(id_servo[0], initial_positions[0])
        self.servo_1 = Servo(id_servo[1], initial_positions[1])
        self.servo_2 = Servo(id_servo[2], initial_positions[2])

        self.servos = [self.servo_0, self.servo_1, self.servo_2]
        self.reposition = False

        self.move_grabber(initial_positions, [50, 50, 50])

        self.type = 'grabber'

        print("Grabber setup")

    def ready(self):
        """
        Checks if all servos of this leg are ready
        :return: If all the servos are ready or not
        """
        result = []
        for elem in self.servos:
            if not elem.is_ready():
                result.append(elem)
                # elem.last_position = elem.read_position()
        return len(result) == 3

    def grab(self, speeds):
        positions = [186, 528, 260]
        self.move_grabber(positions, speeds)

    def loosen(self, speeds):
        positions = [465, 198, 200]
        self.move_grabber(positions, speeds)

    def get_delta(self):
        """
        Calculate the delta time, which can be used so movement always happens at same speed
        :return: Delta time
        """
        next_time = datetime.datetime.now()
        elapsed_time = next_time - self.previous
        self.previous = next_time
        return elapsed_time.total_seconds()

    def move_grabber(self, positions, speeds):
        for i in range(len(self.servos)):
            self.servos[i].move(positions[i], 0, speeds[i])
        self.update()

    def update(self):
        """
        Update all the unready servos
        :param delta: The delta time
        :return: None
        """
        servos_not_ready = [elem for elem in self.servos if not elem.is_ready()]
        self.get_delta()
        while len(servos_not_ready) != 0:
            delta = self.get_delta()
            for i in range(len(servos_not_ready)):
                self.servos[i].update(delta)
            servos_not_ready = [elem for elem in self.servos if not elem.is_ready()]


