import sys

from entities.movement.limb.joints.servo import Servo

sys.path.insert(0, '../../../../src')


class Tire(object):
    def __init__(self, servo_id, position):
        """
        Constructor for tire class
        :param servo_id: Id of the tire servo
        :param position: Position to initialise the servo in
        """
        self.servo = Servo(servo_id, position)
        self.type = 'tire'

    def forward(self, position, delay, speed):
        """
        Function that moves the tire in a forward direction
        :param position: Position to move to
        :param delay: Time to wait after executing
        :param speed: The speed at which the servo moves
        :return: None
        """
        self.servo.move(position, delay, speed)

    def backward(self, position, delay, speed):
        """
        Function that moves the tire in a backward direction
        :param position: Position to move to
        :param delay: Time to wait after executing
        :param speed: The speed at which the servo moves
        :return: None
        """
        self.servo.move(position, delay, speed)
