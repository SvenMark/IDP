import bluetooth
import subprocess
import time
import sys
from threading import Thread

sys.path.insert(0, '../../../src')

from entities.audio.audio import Audio
from entities.threading.utils import SharedObject
from entities.movement.movement import Movement
from entities.vision.vision import Vision
from entities.visual.emotion import Emotion


class BluetoothController(object):
    """
    Base class for the bluetooth smart controller
    """

    def __init__(self, name, limbs, bluetooth_address, names, modules):
        """
        Constructor for the bluetooth controller class
        :param name: Name of the robot
        :param limbs: Array of robot limbs
        :param bluetooth_address: Address of the bluetooth controller
        """
        self.bluetooth_address = bluetooth_address
        self.name = name
        self.limbs = limbs
        self.movement = Movement(limbs)
        self.names = names
        self.modules = modules

        self.vision = None
        self.audio = Audio()
        self.emotion = Emotion(self.audio)
        self.shared_object = SharedObject()  # Create instance of thread sharer

        self.current_module = -1  # Save the current module that is running
        self.speed_factor = 0.75  # Set the amount of speed that can be used, 1 is max or 100%
        self.dead_zone = 10
        self.manual_control = True
        self.data = ""  # Initialise data string
        self.emotion.set_emotion('neutral')  # Set led lights

        if hasattr(self.movement, 'legs'):
            self.movement.legs.update_thread.start()  # Start the leg update class

    def receive_data(self):
        """
        Retrieve data from bluetooth connection with bluetooth address from the constructor
        :return: None
        """

        # Initialise and start bluetooth socket with smart controller
        port = 1
        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        socket.connect((self.bluetooth_address, port))

        # Run this as long as the robot is running
        while True:
            try:
                self.data += str(socket.recv(1024))[2:][:-1]  # Receive data from socket and convert to string

                # if data is "":
                #     print("Closing socket")
                #     sock.close()
                #     while data is "":
                #         try:
                #             sock.connect((self.bluetooth_address, port))
                #             data += str(sock.recv(1024))[2:][:-1]
                #         except bluetooth.btcommon.BluetoothError:
                #             print("Cannot connect, attempting to reconnect")

                data_end = self.data.find('\\n')  # Find the end of one data line
                if data_end != -1:
                    data_line = self.data[:data_end]  # Cut the data to one data line
                    self.handle_data(data_line)  # Handle the data line
                    self.data = ""  # Empty data string
            except KeyboardInterrupt:
                break

        self.movement.tracks.clean_up()  # Clean up gpio
        socket.close()

    def handle_data(self, data):
        """
        Handle the data that is retrieved from receive data
        :param data: A data string
        :return: None
        """
        # print(data)
        s_index = data.find('s')  # Index for button to stop motors
        v_index = data.find('v')  # Index for vertical movement of motors
        h_index = data.find('h')  # Index for horizontal movement of motors
        d_index = data.find('d')  # Index for legs deploy button
        x_index = data.find('x')  # Index of x axis for legs
        y_index = data.find('y')  # Index of y axis for legs
        m_index = data.find('e')  # Index for the module(element) that needs to be ran

        try:
            # Try converting string values to ints
            s = int(str(data[s_index + 2:v_index].replace(" ", "")))
            v = int(str(data[v_index + 2:h_index].replace(" ", "")))
            h = int(str(data[h_index + 2:d_index].replace(" ", "")))
            d = int(str(data[d_index + 2:x_index].replace(" ", "")))
            x = int(str(data[x_index + 2:y_index].replace(" ", "")))
            y = int(str(data[y_index + 2:m_index].replace(" ", "")))
            m = int(str(data[m_index + 2:].replace(" ", "")))

            # Convert v and h to percentage to be used by dc motors
            v = ((v * (1000 / 1024)) - 500) / 5
            h = ((h * (1000 / 1024)) - 500) / 5

            # Set values in bluetooth settings
            self.shared_object.bluetooth_settings.handle_values(s, v, h, d, x, y, m)

            # Turn up speed for race mode and ctf
            if m is 2 or m is 8:
                self.speed_factor = 1
            else:
                self.speed_factor = 0.75

            args = [m, self]

            # If the selected module is different than the last selected and not 0 and 2
            if m is not self.current_module:
                if m is 0 or m is 2:
                    if not self.manual_control:
                        self.shared_object.stop = True  # Notify last module thread to stop
                        while not self.shared_object.has_stopped:
                            time.sleep(0.01)
                        self.manual_control = True

                    self.current_module = m  # Set the current module according to controller input
                    self.run_module(args)
                else:
                    self.shared_object.stop = True  # Notify last module thread to stop
                    while not self.shared_object.has_stopped:
                        time.sleep(0.01)
                    self.shared_object.has_stopped = False  # Set to false because current module is now running
                    self.shared_object.stop = False  # Set to false because current module does not have to stop
                    self.manual_control = False  # Set manual control to false

                    # Run and set selected module
                    self.current_module = m
                    self.run_module(args)

        except ValueError or IndexError:
            temp = 123
            # print("Invalid value in package")

    def run_module(self, args):
        """
        Function that creates and runs a thread of pre-programmed modules,
        based on controller input
        :param args: Array of arguments for each module
        :return: None
        """
        selected_module = args[0]
        current_module = self.modules[args[0]]
        current_module.run(self.names[selected_module], args[1])


def main():
    limbs = [0, 1]
    name = 'Boris'
    bt = BluetoothController(name=name, limbs=limbs, bluetooth_address="98:D3:31:FD:15:C1", names=[], modules=[])
    bt.receive_data()


if __name__ == '__main__':
    main()
