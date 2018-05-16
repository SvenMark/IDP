from entities.movement.limb.limb import Limb
from entities.movement.limb.joints.servo import Servo


class Leg(object):
    def __init__(self, servo_0_id, servo_1_id, servo_2_id):

        # Create the servo instances with correct id and starting position.
        self.servo_0 = Servo(servo_0_id, 500)
        self.servo_1 = Servo(servo_1_id, 500)
        self.servo_2 = Servo(servo_2_id, 500)

        print("Leg setup")

    # Function that moves the legs in the specified directions.
    def move(self, servo_0_position, servo_1_position, servo_2_position, delay):
        self.servo_0.move(servo_0_position, 0)
        self.servo_1.move(servo_1_position, 0)
        self.servo_2.move(servo_2_position, delay)
