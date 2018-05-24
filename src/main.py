import os
import sys

# from elements import element1, element2, element3, element4, element5, element6, element7, element8, element9, \
#     element10
from entities.movement.legs import Legs
from entities.movement.tracks import Tracks
from entities.robot.robot import Robot
from entities.movement.limb.tire import Tire

RESOURCES = os.path.dirname(os.path.abspath(__file__)) + '\\resources\\'

# FUNC_MAP = {
#     "1": element1.core,
#     "2": element2.core,
#     "3": element3.core,
#     "4": element4.core,
#     "5": element5.core,
#     "6": element6.core,
#     "7": element7.core,
#     "8": element8.core,
#     "9": element9.core,
#     "10": element10.core
# }


def main():
    # print(RESOURCES)
    # print command line arguments
    # if len(sys.argv) < 2:
        # print("Please pass commandline args")
        # return sys.exit(2)

    limbs = [
            Legs(leg_0_servos=[
                    14,
                    61,
                    63
                ],
                leg_1_servos=[
                    13,
                    21,
                    31
                ]
                # leg_2_servos=[
                #     14,
                #     61,
                #     63
                # ],
                # leg_3_servos=[
                #     14,
                #     61,
                #     63
                # ]
            ),
            Tracks(track_0_pin=18, track_1_pin=13),
            Tire(servo_id=53, position=500)
        ]

    lights = []

    name = 'Boris'
    boris = Robot(name, limbs, lights)

    boris.movement.legs.deploy(80)
    boris.movement.tracks.forward(duty_cycle=80, delay=0, acceleration=10)

    # part = sys.argv[1]

    # part_function = FUNC_MAP[part]

    # run element
    # part_function.run()


if __name__ == "__main__":
    main()
