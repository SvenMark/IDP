#!/bin/python
import time
import math

from entities.movement.legs import Legs
from entities.movement.sequences.walking_sequences import *

import bluetooth
import time

legs = Legs(leg_0_servos=[
    14,
    61,
    63
],
    leg_1_servos=[
        21,
        31,
        53
    ],
    leg_2_servos=[
        61,
        63,
        111
    ],
    leg_3_servos=[
        111,
        111,
        111
    ])


def receive_messages():
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


def receive_data():
    bd_addr = "98:D3:31:FD:15:C1"  # The address from Boris
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    sock.connect((bd_addr, port))

    data = ""

    count = 0
    while 1:
        try:
            data += str(sock.recv(1024))[2:][:-1]
            data_end = data.find('\\n')
            if data_end != -1:
                rec = data[:data_end]
                #print(rec)
                handle_data(rec)
                data = ""
                count += 1

        except KeyboardInterrupt:
            break
    sock.close()


# f 515 b 523
def handle_data(data):
    print(data)
    f_index = data.find('f')
    b_index = data.find('b')
    d_index = data.find('d')

    if d_index != -1:
        d = int(str(data[d_index+2:f_index].replace(" ", "")))
        if d == 1 and not legs.deployed:
            legs.deploy(200)
        elif d == 0 and legs.deployed:
            legs.retract(200)

    if f_index != -1 and b_index != -1:
        f = int(str(data[f_index+2:b_index].replace(" ", "")))
        b = int(str(data[b_index+2:].replace(" ", "")))
        print(str(f))
        print(str(b))
        if legs.deployed:
            legs.move([530 + round(f / 10), 680, 760 + round(f / 10)], [650, 400, 400], [400, 400, 400], [600, 400, 400], 0, [200, 200, 200])


def send_message_to(target):
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((target, port))
    sock.send("Dit is ontvangen met bluetooth")
    sock.close()


def look_nearby():
    nearby_devices = bluetooth.discover_devices()
    for bdaddr in nearby_devices:
        print(str(bluetooth.lookup_name(bdaddr)) + " [" + str(bdaddr) + "]")


receive_data()
