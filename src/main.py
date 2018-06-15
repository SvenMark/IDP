import os
import sys

sys.path.insert(0, '../src')

from entities.movement.legs import Legs
from entities.movement.tracks import Tracks
from entities.movement.grabber import Grabber
from entities.connection.bluetooth_controller import BluetoothController
from helpers.servo_scanner import servo_scanner

RESOURCES = os.path.dirname(os.path.abspath(__file__)) + '\\resources\\'


def main():
    """
    Function that initialises an instance of bluetooth controller which controls
    the entire robot.
    :return: None
    """

    bluetooth_address = "98:D3:31:FD:15:C1"  # Set the bt address of the controller
    name = 'Boris'  # Set the name of the robot
    limbs = []

    # Check which servo`s are connected
    servos = servo_scanner()

    # If all servos are connected
    if 6 in servos and 1 in servos:
        print("Initialise limbs with Legs, Tracks and grabber")
        limbs = [
            Legs(
                leg_0_servos=[6, 14, 15],
                leg_1_servos=[16, 17, 18],
                leg_2_servos=[21, 41, 52],
                leg_3_servos=[61, 62, 63]
            ),
            Tracks(track_0_pin=13,
                   track_1_pin=18,
                   track_0_forward=22,
                   track_0_backward=27,
                   track_1_forward=19,
                   track_1_backward=26),
            Grabber(servos=[1, 53, 43],
                    initial_positions=[465, 198, 200])
        ]
    # If only leg servos are connected
    elif 6 in servos:
        print("Initialise limbs with Legs and Tracks")
        limbs = [
            Legs(
                leg_0_servos=[6, 14, 15],
                leg_1_servos=[16, 17, 18],
                leg_2_servos=[21, 41, 52],
                leg_3_servos=[61, 62, 63]
            ),
            Tracks(track_0_pin=13,
                   track_1_pin=18,
                   track_0_forward=22,
                   track_0_backward=27,
                   track_1_forward=19,
                   track_1_backward=26)
        ]
    elif 1 in servos:
        print("Initialise limbs with Grabber and Tracks")
        limbs = [
            Legs(
                leg_0_servos=[6, 14, 15],
                leg_1_servos=[16, 17, 18],
                leg_2_servos=[21, 41, 52],
                leg_3_servos=[61, 62, 63]
            ),
            Grabber(servos=[1, 53, 43],
                    initial_positions=[465, 198, 200])
        ]
    # If no servos are connected
    else:
        print("Initialise limbs with Tracks")
        limbs = [
            Tracks(track_0_pin=13,
                   track_1_pin=18,
                   track_0_forward=22,
                   track_0_backward=27,
                   track_1_forward=19,
                   track_1_backward=26)
        ]

    lights = []

    bluetooth_controller = BluetoothController(name, limbs, lights, bluetooth_address)  # Create bt controller

    bluetooth_controller.receive_data()  # Start the data receive loop


if __name__ == "__main__":
    main()
