from entities.movement.limb.limb import Limb
from entities.movement.limb.joints.servo import Servo


class Leg(Limb):
    def __init__(self):

        # Define the id`s of the servo`s
        servo_0_id = 13
        servo_1_id = 31
        servo_2_id = 63

        # Create the servo instances with correct id and starting position
        self.servo_0 = Servo(servo_0_id, 500)
        self.servo_1 = Servo(servo_1_id, 500)
        self.servo_2 = Servo(servo_2_id, 500)

        print("Tracks setup")

    def forward(self):
        print('{} forward'.format(self.limb_type))

    def backward(self):
        print('{} backward'.format(self.limb_type))
