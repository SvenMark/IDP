import os
import sys

sys.path.insert(0, '../src')

from entities.movement.legs import Legs
from entities.movement.tracks import Tracks
from entities.robot.robot import Robot
from entities.movement.grabber import Grabber
from entities.connection.bluetooth_controller import BluetoothController

RESOURCES = os.path.dirname(os.path.abspath(__file__)) + '\\resources\\'


def main():
    bluetooth_address = "98:D3:31:FD:15:C1"
    name = 'Boris'

    limbs = [
        Legs(leg_0_servos=[
                6,
                14,
                15
            ],
            leg_1_servos=[
                16,
                17,
                18
            ],
            leg_2_servos=[
                21,
                41,
                52
            ],
            leg_3_servos=[
                61,
                62,
                63,
            ]
        ),
        Tracks(track_0_pin=13,
               track_1_pin=18,
               track_0_forward=22,
               track_0_backward=27,
               track_1_forward=19,
               track_1_backward=26),
        Grabber(id_servo=[
            1,
            53,
            13
        ],
            initial_positions=[
                160,
                615,
                693])
    ]

    lights = []

    bluetooth_controller = BluetoothController(name, limbs, lights, bluetooth_address)

    while True:
        bluetooth_controller.receive_data()


if __name__ == "__main__":
    main()
