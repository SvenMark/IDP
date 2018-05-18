from entities.movement.limb.limb import Limb
from entities.movement.limb.joints.servo import Servo


class Leg(object):

    def __init__(self, servo_0_id, servo_1_id, servo_2_id, servo_0_position, servo_1_position, servo_2_position):
        """
        Constructor of the leg class
        :param servo_0_id: ID of the servo closest to the robot(shoulder or hip)
        :param servo_1_id: ID of the middle leg servo(knee or elbow)
        :param servo_2_id: ID of the last leg servo(toe or finger)
        :param servo_0_position: The initial position for servo 0
        :param servo_1_position: The initial position for servo 1
        :param servo_2_position: The initial position for servo 2
        """

        # Create the servo instances with correct id and starting position.
        self.servo_0 = Servo(servo_0_id, servo_0_position)
        self.servo_1 = Servo(servo_1_id, servo_1_position)
        self.servo_2 = Servo(servo_2_id, servo_2_position)

        print("Leg setup")

    def move(self, servo_0_position, servo_1_position, servo_2_position, delay):
        """
        Function that moves the legs in the specified directions
        :param servo_0_position: Position to move servo 0 to
        :param servo_1_position: Position to move servo 1 to
        :param servo_2_position: Position to move servo 2 to
        :param delay: Time to wait after executing
        :return: None
        """
        self.servo_0.move(servo_0_position, delay)
        self.servo_1.move(servo_1_position, delay)
        self.servo_2.move(servo_2_position, delay)
