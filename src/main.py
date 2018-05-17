import os
import sys

from elements import element1, element2, element3, element4, element5, element6, element7, element8, element9, \
    element10
from entities.movement.legs import Legs
from entities.movement.tracks import Tracks
from entities.robot.robot import Robot
from entities.movement.limb.leg import Leg
from entities.movement.limb.tire import Tire

RESOURCES = os.path.dirname(os.path.abspath(__file__)) + '\\resources\\'

FUNC_MAP = {
    "1": element1.core,
    "2": element2.core,
    "3": element3.core,
    "4": element4.core,
    "5": element5.core,
    "6": element6.core,
    "7": element7.core,
    "8": element8.core,
    "9": element9.core,
    "10": element10.core
}


def main():
    print(RESOURCES)
    # print command line arguments
    if len(sys.argv) < 2:
        print("Please pass commandline args")
        return sys.exit(2)

    lights = []

    limbs = [
        Tracks(track1pin=18, track2pin=13),
        Legs(leg_0_servos=[
                1,
                13,
                14
            ],
            leg_1_servos=[
                21,
                31,
                53
            ],
            leg_2_servos=[
                61,
                63,
                111
            ],
            leg_3_servos=[
                111,
                111,
                111
            ]
        )
    ]

    name = 'Boris'
    boris = Robot(name, limbs, lights)

    boris.movement.tracks.forward(20, 0, 2)

    #print(boris.movement.tracks.turn_left())

    #part = sys.argv[1]

    #part_function = FUNC_MAP[part]

    # run element
    #part_function.run()


if __name__ == "__main__":
    main()
