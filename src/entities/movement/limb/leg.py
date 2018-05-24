from entities.movement.limb.joints.servo import Servo


class Leg(object):

    def __init__(self, id_servo, positions):
        """
        Constructor for leg class
        :param id_servo: Array of servo id`s
        :param positions: Array of servo positions
        """
        # Create the servo instances with correct id and starting position.
        self.servo_0 = Servo(id_servo[0], positions[0])
        self.servo_1 = Servo(id_servo[1], positions[1])
        self.servo_2 = Servo(id_servo[2], positions[2])
        self.type = 'leg'

        print("Leg setup")

    def move(self, positions, delay, speeds):
        """
        Function that moves the legs in the specified directions
        :param positions: Array of positions for each servo
        :param delay: Time to wait after executing
        :param speeds: Array of speeds for each servo
        :return: None
        """
        self.servo_0.move(positions[0], delay, speeds[0])
        self.servo_1.move(positions[1], delay, speeds[1])
        self.servo_2.move(positions[2], delay, speeds[2])
