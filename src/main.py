import os
import sys

sys.path.insert(0, '../src')
# from elements import element1, element2, element3, element4, element5, element6, element7, element8, element9, \
#    element10
from entities.movement.legs import Legs
from entities.movement.tracks import Tracks
from entities.robot.robot import Robot
from entities.movement.limb.tire import Tire
from entities.movement.sequences.sequences import *

RESOURCES = os.path.dirname(os.path.abspath(__file__)) + '\\resources\\'

#FUNC_MAP = {
#    "1": element1.core,
#    "2": element2.core,
#    "3": element3.core,
#    "4": element4.core,
#    "5": element5.core,
#    "6": element6.core,
#    "7": element7.core,
#    "8": element8.core,
#    "9": element9.core,
#    "10": element10.core
#}


def main():
    #print(RESOURCES)
    # print command line arguments
    #if len(sys.argv) < 2:
        #print("Please pass commandline args")
        #return sys.exit(2)

    limbs = [
            # Legs(leg_0_servos=[
            #         14,
            #         61,
            #         63
            #     ]
            #     # leg_1_servos=[
            #     #     13,
            #     #     21,
            #     #     31
            #     # ]
            #     # leg_2_servos=[
            #     #     14,
            #     #     61,
            #     #     63
            #     # ],
            #     # leg_3_servos=[
            #     #     14,
            #     #     61,
            #     #     63
            #     # ]
            # ),
            Tracks(track_0_pin=18,
                   track_1_pin=13,
                   track_0_forward=22,
                   track_0_backward=27,
                   track_1_forward=10,
                   track_1_backward=9),
            Tire(servo_id=21, position=500)
        ]

    lights = []

    name = 'Boris'
    boris = Robot(name, limbs, lights, bluetooth_address="98:D3:31:FD:15:C1")

    while True:
        boris.controller.receive_data()

    # part = sys.argv[1]

    # part_function = FUNC_MAP[part]

    # run element
    # part_function.run()


if __name__ == "__main__":
    main()
