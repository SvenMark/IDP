import datetime
import time
import sys
from threading import Thread

sys.path.insert(0, '../../../src')

from entities.movement.limb.joints.servo import Servo
from entities.movement.sequences.sequences import *


class Grabber(object):

    def __init__(self, id_servo, initial_positions):
        self.previous = datetime.datetime.now()

        self.servo_0 = Servo(id_servo[0], initial_positions[0])
        self.servo_1 = Servo(id_servo[1], initial_positions[1])
        self.servo_2 = Servo(id_servo[2], initial_positions[2])

        self.servos = [self.servo_0, self.servo_1, self.servo_2]
        self.reposition = False

        self.servo_0.move_speed(initial_positions[0], 50)
        self.servo_1.move_speed(initial_positions[1], 50)
        self.servo_2.move_speed(initial_positions[2], 50)

        self.type = 'grabber'

        print("Grabber setup")

    def ready(self):
        """
        Checks if all servos of this leg are ready
        :return: If all the servos are ready or not
        """
        return len([elem for elem in self.servos if elem.is_ready()]) == 3

    def grab(self, speeds):
        positions = [186, 528, 111]
        self.servo_0.move_speed(positions[0], speeds[0])
        self.servo_1.move_speed(positions[1], speeds[1])

        # counter = 0
        #
        # while self.ready() is not 3:
        #     if counter > 5:
        #         self.reposition = True
        #         self.loosen([100, 100, 100])
        #     time.sleep(0.01)
        #     counter += 1

        self.servo_2.move_speed(positions[2], speeds[2])

        self.update()

    def loosen(self, speeds):
        positions = [465, 198, 15]
        self.servo_0.move_speed(positions[0], speeds[0])
        self.servo_1.move_speed(positions[1], speeds[1])
        self.servo_2.move_speed(positions[2], speeds[2])

        self.update()

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


