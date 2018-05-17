from entities.movement.limb.leg import Leg


class Legs(object):

    def __init__(self):

        # Initialise an array with servo id`s for each leg
        leg_0_servos = [
            13,
            31,
            64
        ]
        leg_1_servos = [
            13,
            31,
            64
        ]
        leg_2_servos = [
            13,
            31,
            64
        ]
        leg_3_servos = [
            13,
            31,
            64
        ]

        # Initialise a leg for each corner of the robot
        self.leg_front_left = Leg(leg_0_servos[0], leg_0_servos[1], leg_0_servos[2], 500, 500, 500)
        self.leg_front_right = Leg(leg_1_servos[0], leg_1_servos[1], leg_1_servos[2], 500, 500, 500)
        self.leg_rear_left = Leg(leg_2_servos[0], leg_2_servos[1], leg_2_servos[2], 500, 500, 500)
        self.leg_rear_right = Leg(leg_3_servos[0], leg_3_servos[1], leg_3_servos[2], 500, 500, 500)

        print("Legs setup")

    def move(self, servo_0_position, servo_1_position, servo_2_position, delay):
        self.leg_front_left.move(servo_0_position, servo_1_position, servo_2_position, delay)
        self.leg_front_right.move(servo_0_position, servo_1_position, servo_2_position, delay)
        self.leg_rear_left.move(servo_0_position, servo_1_position, servo_2_position, delay)
        self.leg_rear_right.move(servo_0_position, servo_1_position, servo_2_position, delay)