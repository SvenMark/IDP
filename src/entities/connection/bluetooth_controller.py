import bluetooth
import subprocess
import time
import sys
from threading import Thread

sys.path.insert(0, '../../../src')

from modules import base_module, capture_flag, dance, entering_arena, line_dance, race, \
    transport_rebuild, cannon, obstacle_course
from entities.audio.audio import Audio
from entities.threading.utils import SharedObject
from entities.movement.movement import Movement
from entities.vision.vision import Vision
from entities.visual.emotion import Emotion


class BluetoothController(object):
    """
    Base class for the bluetooth smart controller
    """

    def __init__(self, name, limbs, bluetooth_address):
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

        self.vision = None
        self.audio = Audio()
        self.emotion = Emotion(self.audio)
        self.shared_object = SharedObject()  # Create instance of thread sharer

        self.current_module = 0  # Save the current module that is running, standard is 0
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

            speed_factor = 1  # Set the amount of speed that can be used, 1 is max or 100%

            # Turn down speed in standard mode
            if m is 0:
                speed_factor = 0.75

            # If the selected module is basic or race mode
            # Race and basic mode are both just basic controller modes but with different speeds
            if m is 0 or m is 2:
                # If last ran module was not manual control
                if not self.manual_control:
                    self.shared_object.stop = True  # Notify last module thread to stop

                    # Wait for the thread to stop
                    while not self.shared_object.has_stopped:
                        time.sleep(0.01)

                    self.manual_control = True

                self.current_module = m  # Set the current module according to controller input

                # Send controller tracks input to tracks
                self.movement.tracks.handle_controller_input(stop_motors=s,
                                                             vertical_speed=h * speed_factor,
                                                             horizontal_speed=v * speed_factor,
                                                             dead_zone=5)

                if hasattr(self.movement, 'legs'):
                    # Send controller leg input to legs
                    self.movement.legs.handle_controller_input(deploy=d,
                                                               x_axis=x,
                                                               y_axis=y)

            # If the selected module is different than the last selected and not 0 and 2
            if m is not self.current_module and m is not 0 and m is not 2:
                self.shared_object.stop = True  # Notify last module thread to stop

                # Wait for the thread to stop
                while not self.shared_object.has_stopped:
                    time.sleep(0.01)

                self.shared_object.has_stopped = False  # Set to false because current module is now running
                self.shared_object.stop = False  # Set to false because current module does not have to stop
                self.manual_control = False  # Set manual control to false

                # Run and set selected module
                self.current_module = m
                self.run_module(m, self.movement, s, v, h, speed_factor, d)

        except ValueError or IndexError:
            temp = 123
            # print("Invalid value in package")

    def run_module(self, module, movement, s, v, h, speed_factor, d):
        """
        Function that creates and runs a thread of pre-programmed modules,
        based on controller input
        :param module: Which module to run
        :param movement: An instance of the movement class
        :param s: Boolean value for disabling dc motors
        :param v: Vertical dc motor speed
        :param h: Horizontal dc motor speed
        :param speed_factor: Amount of max speed to be used by dc motors
        :return: None
        """
        # Switch with all modules
        if module is 1:
            name = 'Entree'  # Set name for module
            Thread(target=entering_arena.run, args=(name, movement, s, v, h, speed_factor, self.shared_object,)).start()  # Start module thread

        if module is 3:
            name = 'Dance'
            Thread(target=dance.run, args=(name, movement, self.shared_object,)).start()

        if module is 4:
            name = 'Line Dance'
            Thread(target=line_dance.run, args=(name, movement, self.shared_object,)).start()

        if module is 5:
            name = 'Obstacle course'
            Thread(target=obstacle_course.run, args=(name, movement, s, v, h, speed_factor, self.shared_object,)).start()

        if module is 6:
            name = 'Cannon'
            Thread(target=cannon.run, args=(name, movement, s, v, h, speed_factor, self.shared_object,)).start()

        if module is 7:
            name = 'Transport'
            Thread(target=transport_rebuild.run, args=(name, movement, s, v, h, speed_factor, d, self.shared_object,)).start()

        if module is 8:
            name = 'Capture the flag'
            speed_factor = 1  # Set speed to max for maximum capture ability
            Thread(target=capture_flag.run, args=(name, movement, s, v, h, speed_factor, d, self.shared_object,)).start()


def main():
    limbs = [0, 1]
    name = 'Boris'
    bluetooth = BluetoothController(name=name, limbs=limbs, bluetooth_address="98:D3:31:FD:15:C1")


if __name__ == '__main__':
    main()
