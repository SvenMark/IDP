import bluetooth
import time


def receivemessages():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    port = 1
    server_sock.bind(("", port))
    server_sock.listen(1)
    print("Waiting for connection...")

    client_sock, address = server_sock.accept()
    print("Accepted connection from " + str(address))
    time.sleep(3)

    data = client_sock.recv(1024)
    print("Received: %s" % data)

    client_sock.close()
    server_sock.close()


def sendmessageto(target):
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((target, port))
    sock.send("Dit is ontvangen met bluetooth")
    sock.close()


def looknearby():
    nearby_devices = bluetooth.discover_devices()
    for bdaddr in nearby_devices:
        print(str(bluetooth.lookup_name(bdaddr)) + " [" + str(bdaddr) + "]")


# receivemessages()
# sendmessageto("B8:27:EB:F6:A8:B2")
looknearby()
