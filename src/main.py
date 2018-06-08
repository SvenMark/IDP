import os
import sys

sys.path.insert(0, '../src')

from entities.movement.legs import Legs
from entities.movement.tracks import Tracks
from entities.robot.robot import Robot
from entities.connection.bluetooth_controller import BluetoothController

RESOURCES = os.path.dirname(os.path.abspath(__file__)) + '\\resources\\'


def main():
    bluetooth_address = "98:D3:31:FD:15:C1"
    name = 'Boris'

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
                ],
                leg_2_servos=[
                    14,
                    61,
                    63
                ],
                leg_3_servos=[
                    14,
                    61,
                    63
                ]
            ),
            Tracks(track_0_pin=18,
                   track_1_pin=13,
                   track_0_forward=22,
                   track_0_backward=27,
                   track_1_forward=10,  # 19
                   track_1_backward=9),  # 26
        ]

    lights = []

    bluetooth_controller = BluetoothController(name, limbs, lights, bluetooth_address)

    while True:
        bluetooth_controller.receive_data()


if __name__ == "__main__":
    main()
