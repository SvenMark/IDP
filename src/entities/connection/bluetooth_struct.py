from __future__ import print_function
import glob
import struct
import numpy as np
import bluetooth
import os
import time


class BluetoothController(object):
    """
    Base class for the bluetooth smart controller
    """

    def __init__(self, limbs, bluetooth_address):
        """
        Constructor for the bluetooth controller class
        :param limbs: Array of robot limbs
        """
        self.bluetooth_address = bluetooth_address
        self.legs = limbs[0]
        self.tracks = limbs[1]

    def look_for_available_ports(self):
        """
        find available serial ports to Arduino
        """
        available_ports = glob.glob('/dev/rfcomm*')
        print("Available ports: ")
        print(available_ports)

        return available_ports[0]

    def receive_data(self):
        """
        Retrieve data from bluetooth connection with bluetooth address from the constructor
        :return: None
        """
        port = open("dev/rfcomm0", "rb")

        while 1:
            try:
                byte = port.read(1)
                print(str(byte))
            except KeyboardInterrupt:
                break

    def handle_data(self, data):
        """
        Handle the data that is retrieved from receive data
        :param data: A data string
        :return: None
        """

        print("Data " + str(data))

        new_values = struct.unpack('<fffffffff', data)

        latest_values = np.array(new_values)

        print("Converted data " + str(latest_values))

        # Index for button to stop motors
        s_index = data.find('s')
        # Index for vertical movement of motors
        v_index = data.find('v')
        # Index for horizontal movement of motors
        h_index = data.find('h')
        # Index for legs deploy button
        d_index = data.find('d')
        # Index of x axis for legs
        x_index = data.find('x')
        # Index of y axis for legs
        y_index = data.find('y')

        # Tracks
        # Check if indexes are not -1
        if s_index != -1 and v_index != -1 and h_index != -1:
            # Convert the indexes to usable integers
            s = int(str(data[s_index + 2:v_index].replace(" ", "")))
            v = int(str(data[v_index + 2:h_index].replace(" ", "")))
            h = int(str(data[h_index + 2:d_index].replace(" ", "")))

            # Convert v and h to percentage to be used by dc motors
            v = ((v * (1000 / 1024)) - 500) / 5
            h = ((h * (1000 / 1024)) - 500) / 5

            # Send data to tracks class
            self.tracks.handle_controller_input(stop_motors=s, vertical_speed=v, horizontal_speed=h, dead_zone=5)

        # Legs
        if x_index != -1 and y_index != -1 and d_index != -1:
            # Convert the indexes to usable integers
            d = int(str(data[d_index + 2:x_index].replace(" ", "")))
            x = int(str(data[x_index + 2:y_index].replace(" ", "")))
            y = int(str(data[y_index + 2:].replace(" ", "")))

            # Send the data to legs class
            self.legs.handle_controller_input(deploy=d, x_axis=x, y_axis=y)

    def send_message(self, target):
        """
        Send a message over bluetooth
        :param target: Bluetooth address to send to
        :return: None
        """
        port = 1
        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        socket.connect((target, port))
        socket.send("Dit is ontvangen met bluetooth")
        socket.close()

    def scan(self):
        """
        Scan for nearby bluetooth devices
        :return: None
        """
        nearby_devices = bluetooth.discover_devices()
        for device in nearby_devices:
            print(str(bluetooth.lookup_name(device)) + " [" + str(device) + "]")


def main():
    limbs = [0, 1]
    bluetooth = BluetoothController(limbs=limbs, bluetooth_address="98:D3:31:FD:15:C1")


if __name__ == '__main__':
    main()