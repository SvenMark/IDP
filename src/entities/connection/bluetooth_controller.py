import bluetooth
import subprocess
import time
import sys

sys.path.insert(0, '../../../src')

from elements import element1, element2, element3, element4, element5, element6, element7, element8, element9, element10
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
        # self.legs = limbs[0]
        self.tracks = limbs[0]

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
        data_new = ""
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
                        except bluetooth.BluetoothError:
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
        # e_index = data.find('e')

        try:
            s = int(str(data[s_index + 2:v_index].replace(" ", "")))
            v = int(str(data[v_index + 2:h_index].replace(" ", "")))
            h = int(str(data[h_index + 2:d_index].replace(" ", "")))
            d = int(str(data[d_index + 2:x_index].replace(" ", "")))
            x = int(str(data[x_index + 2:y_index].replace(" ", "")))
            y = int(str(data[y_index + 2:].replace(" ", "")))
            # y = int(str(data[y_index + 2:e_index].replace(" ", "")))
            # e = int(str(data[e_index + 2:].replace(" ", "")))

            # Run selected element
            # self.run_element(e)

            # Convert v and h to percentage to be used by dc motors
            v = ((v * (1000 / 1024)) - 500) / 5
            h = ((h * (1000 / 1024)) - 500) / 5

            # Send data to tracks class
            self.tracks.handle_controller_input(stop_motors=s, vertical_speed=h, horizontal_speed=v, dead_zone=5)

            # Send the data to legs class
            # self.legs.handle_controller_input(deploy=d, x_axis=x, y_axis=y)

        except ValueError or IndexError:
            print("Invalid value in package")

    # def run_element(self, element):
    #     if element is 1:
    #         name = 'Entree'
    #         boris = Robot(name, self.limbs, self.lights)
    #         element1.run(boris)
    #     if element is 2:
    #         name = 'Race'
    #         boris = Robot(name, self.limbs, self.lights)
    #         element2.run(boris)
    #     if element is 3:
    #         name = 'Dance'
    #         boris = Robot(name, self.limbs, self.lights)
    #         element3.run(boris)
    #     if element is 4:
    #         name = 'Line Dance'
    #         boris = Robot(name, self.limbs, self.lights)
    #         element4.run(boris)
    #     if element is 5:
    #         name = 'Obstacle Course'
    #         boris = Robot(name, self.limbs, self.lights)
    #         element5.run(boris)
    #     if element is 6:
    #         name = 'Cannon'
    #         boris = Robot(name, self.limbs, self.lights)
    #         element6.main(boris)
    #     if element is 7:
    #         name = 'Transport'
    #         boris = Robot(name, self.limbs, self.lights)
    #         element7.vision(boris)
    #     if element is 8:
    #         name = 'CTF'
    #         boris = Robot(name, self.limbs, self.lights)
    #         element8.run(boris)
    #     if element is 9:
    #         name = 'Qualification'
    #         boris = Robot(name, self.limbs, self.lights)
    #         element9.run(boris)


def main():
    limbs = [0, 1]
    bluetooth = BluetoothController(limbs=limbs, bluetooth_address="98:D3:31:FD:15:C1")


if __name__ == '__main__':
    main()
