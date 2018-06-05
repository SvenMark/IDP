import bluetooth
import subprocess
import time
import sys

sys.path.insert(0, '../../../src')


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

        self.legs.update_thread.start()

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
                # data_new += str(sock.recv(1024).decode("utf-8"))

                data += str(sock.recv(1024))[2:][:-1]
                if data is "":
                    print("Reconnecting")
                    sock.close()
                    sock.connect((self.bluetooth_address, port))

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

            # Send data to tracks class
            self.tracks.handle_controller_input(stop_motors=s, vertical_speed=h, horizontal_speed=v, dead_zone=5)

            # Send the data to legs class
            self.legs.handle_controller_input(deploy=d, x_axis=x, y_axis=y)

        except ValueError or IndexError:
            print("Invalid value in package")


def main():
    limbs = [0, 1]
    bluetooth = BluetoothController(limbs=limbs, bluetooth_address="98:D3:31:FD:15:C1")


if __name__ == '__main__':
    main()
