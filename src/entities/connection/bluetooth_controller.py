import bluetooth
import subprocess
import time
import sys
from threading import Thread

sys.path.insert(0, '../../../src')

from elements import element1, element2, element3, element4, element8
# element5, element6, element7,
# element9, element10
from entities.threading_.utils import SharedObject
# from entities.robot.robot import Robot


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
        self.limbs = limbs
        self.legs = limbs[0]
        self.tracks = limbs[1]

        self.current_element = 0
        self.shared_object = SharedObject()

        # self.legs.update_thread.start()

    def receive_data(self):
        """
        Retrieve data from bluetooth connection with bluetooth address from the constructor
        :return: None
        """
        port = 1
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((self.bluetooth_address, port))

        data = ""
        while True:
            try:
                data += str(sock.recv(1024))[2:][:-1]

                if data is "":
                    print("Closing socket")
                    sock.close()
                    while data is "":
                        try:
                            sock.connect((self.bluetooth_address, port))
                            data += str(sock.recv(1024))[2:][:-1]
                        except bluetooth.btcommon.BluetoothError:
                            print("Cannot connect, attempting to reconnect")

                data_end = data.find('\\n')
                if data_end != -1:
                    rec = data[:data_end]
                    # print(rec)
                    self.handle_data(rec)
                    data = ""

            except KeyboardInterrupt:
                break

        self.tracks.clean_up()
        sock.close()

    def handle_data(self, data):
        """
        Handle the data that is retrieved from receive data
        :param data: A data string
        :return: None
        """
        print(data)
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
        # Index for the element that needs to be ran
        e_index = data.find('e')

        try:
            s = int(str(data[s_index + 2:v_index].replace(" ", "")))
            v = int(str(data[v_index + 2:h_index].replace(" ", "")))
            h = int(str(data[h_index + 2:d_index].replace(" ", "")))
            d = int(str(data[d_index + 2:x_index].replace(" ", "")))
            x = int(str(data[x_index + 2:y_index].replace(" ", "")))
            y = int(str(data[y_index + 2:e_index].replace(" ", "")))
            e = int(str(data[e_index + 2:].replace(" ", "")))

            # Convert v and h to percentage to be used by dc motors
            v = ((v * (1000 / 1024)) - 500) / 5
            h = ((h * (1000 / 1024)) - 500) / 5

            # Max speed
            speed_factor = 1

            # Not max speed in controlled mode
            if e is 0:
                speed_factor = 0.75

            if e is 0 or e is 2:
                self.current_element = 0

                # Send data to tracks class
                self.tracks.handle_controller_input(stop_motors=s, vertical_speed=h * speed_factor,
                                                    horizontal_speed=v * speed_factor, dead_zone=5)

                # Send the data to legs class
                self.legs.handle_controller_input(deploy=d, x_axis=x, y_axis=y)

            if e is not self.current_element and e is not 0:
                # Stopping the current element
                self.shared_object.stop = True

                # Wait for it to stop ?
                while not self.shared_object.has_stopped:
                    time.sleep(0.01)
                self.shared_object.has_stopped = False

                # Run selected element
                self.current_element = e
                self.run_element(e)

        except ValueError or IndexError:
            temp = 0
            # print("Invalid value in package")

    def run_element(self, element):
        print("Running element " + str(element))
        if element is 1:
            name = 'Entree'
            print(name)

            # starting thread
            Thread(target=element1.run, args=(self.shared_object,)).start()

        if element is 2:
            name = 'Race'
            print(name)

            # starting thread
            Thread(target=element2.run, args=(self.shared_object,)).start()

        if element is 3:
            name = 'Dance'
            print(name)

            # starting thread
            Thread(target=element3.run, args=(self.shared_object,)).start()

        if element is 4:
            name = 'Line Dance'
            print(name)

            # starting thread
            Thread(target=element4.run, args=(self.shared_object,)).start()

        if element is 5:
            name = 'Obstacle course'
            print(name)

            # starting thread
            # Thread(target=element5.run, args=(self.shared_object,)).start()

        if element is 6:
            name = 'Cannon'
            print(name)

            # starting thread
            # Thread(target=element6.Element6.linedetection, args=(self.shared_object,)).start()

        if element is 7:
            name = 'Transport'
            print(name)

            # starting thread
            # Thread(target=element7.run, args=(self.shared_object,)).start()

        if element is 8:
            name = 'Capture the flag'
            print(name)

            # starting thread
            Thread(target=element8.run, args=(self.shared_object,)).start()


def main():
    limbs = [0, 1]
    bluetooth = BluetoothController(limbs=limbs, bluetooth_address="98:D3:31:FD:15:C1")


if __name__ == '__main__':
    main()
