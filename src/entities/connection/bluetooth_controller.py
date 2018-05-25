import bluetooth
import time


class BluetoothController(object):
    """
    Base class for the bluetooth smart controller
    """

    def __init__(self, limbs):
        """

        :param limbs:
        """
        self.bluetooth_addres = "98:D3:31:FD:15:C1"
        self.tracks = limbs[0]
        self.legs = limbs[1]

    def receive_messages(self, legs):
        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        port = 1
        server_sock.bind(("", port))
        server_sock.listen(1)
        print("Waiting for connection...")

        client_sock, address = server_sock.accept()
        print("Accepted connection from " + str(address))
        legs.retract(100)
        time.sleep(3)

        while True:
            data = client_sock.recv(4096)
            print("Received: %s" % data)
            if data == "q":
                break

        client_sock.close()
        server_sock.close()

    def receive_data(self):
        port = 1
        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        socket.connect((self.bluetooth_addres, port))

        data = ""

        count = 0
        while 1:
            try:
                data += str(socket.recv(1024))[2:][:-1]
                data_end = data.find('\\n')
                if data_end != -1:
                    rec = data[:data_end]
                    # print(rec)
                    self.handle_data(rec)
                    data = ""
                    count += 1

            except KeyboardInterrupt:
                break
            socket.close()

    def handle_data(self, data):
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

        # Tracks
        if s_index != -1 and v_index != -1 and h_index != -1:
            s = int(str(data[s_index + 2:v_index].replace(" ", "")))
            v = int(str(data[v_index + 2:h_index].replace(" ", "")))
            h = int(str(data[h_index + 2:d_index].replace(" ", "")))

            # Convert v and h to percentage to be used by dc motors
            v = ((v * (1000 / 1024)) - 500) / 5
            h = ((h * (1000 / 1024)) - 500) / 5

            self.tracks.handle_controller_input(stop_motors=s, vertical_speed=v, horizontal_speed=h, dead_zone=5)

        # Legs
        if x_index != -1 and y_index != -1 and d_index != -1:
            d = int(str(data[d_index + 2:x_index].replace(" ", "")))
            x = int(str(data[x_index + 2:y_index].replace(" ", "")))
            y = int(str(data[y_index + 2:].replace(" ", "")))

            self.legs.handle_controller_input(deploy=d, x_axis=x, y_axis=y)

    def send_message(self, target):
        port = 1
        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        socket.connect((target, port))
        socket.send("Dit is ontvangen met bluetooth")
        socket.close()

    def scan(self):
        nearby_devices = bluetooth.discover_devices()
        for device in nearby_devices:
            print(str(bluetooth.lookup_name(device)) + " [" + str(device) + "]")


def main():
    limbs = [0, 1]
    bluetooth = BluetoothController(limbs=limbs)


if __name__ == '__main__':
    main()
