import sys

sys.path.insert(0, '../../../../src')

from entities.movement.limb.joints.servo import Servo


class Leg(object):
    """
    Base class for leg which directly implements servo
    """

    def __init__(self, id_servo, positions):
        """
        Constructor for leg class
        :param id_servo: Array of servo id`s
        :param positions: Array of servo positions
        """
        # Create the servo instances with correct id and starting position.
        self.servo_0 = Servo(id_servo[0], positions[0], 3)
        self.servo_1 = Servo(id_servo[1], positions[1], 3)
        self.servo_2 = Servo(id_servo[2], positions[2], 3)

        self.servos = [self.servo_0, self.servo_1, self.servo_2]

        self.sequence = 0

        self.type = 'leg'

        print("Leg setup")

    def ready(self):
        """
        Checks if all servos of this leg are ready
        :return: If all the servos are ready or not
        """
        return len([elem for elem in self.servos if elem.is_ready()]) == 3

    def move(self, positions, speeds):
        """
        Function that moves the legs in the specified directions
        :param positions: Array of positions for each servo
        :param speeds: Array of speeds for each servo
        :return: None
        """
        self.servo_0.move(positions[0], speeds[0])
        self.servo_1.move(positions[1], speeds[1])
        self.servo_2.move(positions[2], speeds[2])

    def update_sequence(self):
        """
        Function that updates on which part of the movement sequence the legs are in
        when controlled by the controller.
        :return: None
        """
        if self.sequence < 3:
            self.sequence = self.sequence + 1
        else:
            self.sequence = 0

    def update(self, delta):
        """
        Update all the unready servos
        :param delta: The delta time
        :return: None
        """
        for i in range(len(self.servos)):
            if not self.servos[i].is_ready():
                self.servos[i].update(delta)
