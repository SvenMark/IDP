from entities.movement.limb.leg import Leg


class Legs(object):

    def __init__(self, leg_0_servos, leg_1_servos, leg_2_servos, leg_3_servos):

        # Initialise a leg for each corner of the robot
        self.leg_front_left = Leg(leg_0_servos[0], leg_0_servos[1], leg_0_servos[2], 500, 500, 500)
        self.leg_front_right = Leg(leg_1_servos[0], leg_1_servos[1], leg_1_servos[2], 500, 500, 500)
        # self.leg_rear_left = Leg(leg_2_servos[0], leg_2_servos[1], leg_2_servos[2], 500, 500, 500)
        # self.leg_rear_right = Leg(leg_3_servos[0], leg_3_servos[1], leg_3_servos[2], 500, 500, 500)

        print("Legs setup")

    def move(self, leg_0_moves, leg_1_moves, leg_2_moves, leg_3_moves, delay):
        self.leg_front_left.move(leg_0_moves[0], leg_0_moves[1], leg_0_moves[2], delay)
        self.leg_front_right.move(leg_1_moves[0], leg_1_moves[1], leg_1_moves[2], delay)
        # self.leg_rear_left.move(leg_2_moves[0], leg_2_moves[1], leg_2_moves[2], delay)
        # self.leg_rear_right.move(leg_3_moves[0], leg_3_moves[1], leg_3_moves[2], delay)
