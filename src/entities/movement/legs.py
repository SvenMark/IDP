from entities.movement.limb.leg import Leg


class Legs(object):

    def __init__(self, leg_0_servos, leg_1_servos, leg_2_servos, leg_3_servos):
        """
        Constructor for the legs
        :param leg_0_servos: Array of servo id`s for leg 0
        :param leg_1_servos: Array of servo id`s for leg 1
        :param leg_2_servos: Array of servo id`s for leg 2
        :param leg_3_servos: Array of servo id`s for leg 3
        """

        # Initialise a leg for each corner of the robot
        self.leg_front_left = Leg(leg_0_servos[0], leg_0_servos[1], leg_0_servos[2], 530, 210, 475)
        # self.leg_front_right = Leg(leg_1_servos[0], leg_1_servos[1], leg_1_servos[2], 600, 450, 850)
        # self.leg_rear_left = Leg(leg_2_servos[0], leg_2_servos[1], leg_2_servos[2], 600, 450, 850)
        # self.leg_rear_right = Leg(leg_3_servos[0], leg_3_servos[1], leg_3_servos[2], 600, 450, 850)
        self.deployed = False

        print("Legs setup, retracting")
        
    def move(self, leg_0_moves, leg_1_moves, leg_2_moves, leg_3_moves, delay, speeds):
        """
        Function to move the legs together
        :param leg_0_moves: Array of positions for leg 0
        :param leg_1_moves: Array of positions for leg 1
        :param leg_2_moves: Array of positions for leg 2
        :param leg_3_moves: Array of positions for leg 3
        :param delay: Time to wait after executing
        :param speeds: The speeds at which the servo moves
        :return: None
        """
        self.leg_front_left.move(leg_0_moves, delay, speeds)
        # self.leg_front_right.move(leg_1_moves[0], leg_1_moves[1], leg_1_moves[2], delay)
        # self.leg_rear_left.move(leg_2_moves[0], leg_2_moves[1], leg_2_moves[2], delay)
        # self.leg_rear_right.move(leg_3_moves[0], leg_3_moves[1], leg_3_moves[2], delay)

    def deploy(self, speed):
        """
        Deploys the legs so they can be used for walking
        :param speed: The speed at which the servo moves
        :return: None
        """
        
        leg_0_deploy = [530, 766, 850]
        leg_1_deploy = [0, 0, 0]
        leg_2_deploy = [0, 0, 0]
        leg_3_deploy = [0, 0, 0]
        delay = 0.1

        self.leg_front_left.move(leg_0_deploy, delay, [speed, speed, speed])
        # self.leg_front_right.move(leg_1_deploy[0], leg_1_deploy[1], leg_1_deploy[2], delay, speed)
        # self.leg_rear_left.move(leg_2_deploy[0], leg_2_deploy[1], leg_2_deploy[2], delay, speed)
        # self.leg_rear_right.move(leg_3_deploy[0], leg_3_deploy[1], leg_3_deploy[2], delay, speed)
        self.deployed = True

    def retract(self, speed):
        """
        Retracts the legs to they are not in the way
        :param speed: The speed at which the servo moves
        :return: None
        """
        
        leg_0_retract = [524, 211, 475]
        leg_1_retract = [0, 0, 0]
        leg_2_retract = [0, 0, 0]
        leg_3_retract = [0, 0, 0]
        delay = 0.1
        
        self.leg_front_left.move(leg_0_retract, delay, [speed, speed, speed])
        # self.leg_front_right.move(leg_1_retract[0], leg_1_retract[1], leg_1_retract[2], delay)
        # self.leg_rear_left.move(leg_2_retract[0], leg_2_retract[1], leg_2_retract[2], delay)
        # self.leg_rear_right.move(leg_3_retract[0], leg_3_retract[1], leg_3_retract[2], delay)
        self.deployed = False

    def handle_controller_input(self, deploy, x_axis, y_axis):
        if deploy == 1 and not self.deployed:
            self.deploy(200)
        elif deploy == 0 and self.deployed:
            self.retract(200)

        if self.deployed:
            self.move([530 + round(x_axis / 10), 680, 760 + round(y_axis / 10)],
                      [650, 400, 400],
                      [400, 400, 400],
                      [600, 400, 400],
                      0,
                      [200, 200, 200])
