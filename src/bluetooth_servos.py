#!/bin/python
import time
import math

from entities.movement.legs import Legs
from entities.movement.tracks import Tracks
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
tracks = Tracks(track_0_pin=18, track_1_pin=13)


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
        s = int(str(data[s_index+2:v_index].replace(" ", "")))
        v = int(str(data[v_index+2:h_index].replace(" ", "")))
        h = int(str(data[h_index+2:d_index].replace(" ", "")))

        v = (v - 500) / 5
        h = (h - 500) / 5

        if v < 2:
            if -2 < h < 2:
                tracks.backward(duty_cycle_track_left=v,
                                duty_cycle_track_right=v,
                                delay=0,
                                acceleration=0)
            if h > 2:
                h = h / 5
                tracks.backward(duty_cycle_track_left=v,
                                duty_cycle_track_right=v - h,
                                delay=0,
                                acceleration=0)
            if h < -2:
                h = abs(h / 5)
                tracks.backward(duty_cycle_track_left=v,
                                duty_cycle_track_right=v - h,
                                delay=0,
                                acceleration=0)

        if v > 2:
            if -2 < h < 2:
                tracks.forward(duty_cycle_track_left=v,
                               duty_cycle_track_right=v,
                               delay=0,
                               acceleration=0)
                if h > 2:
                    h = h / 5
                    tracks.backward(duty_cycle_track_left=v,
                                    duty_cycle_track_right=v - h,
                                    delay=0,
                                    acceleration=0)
                if h < -2:
                    h = abs(h / 5)
                    tracks.backward(duty_cycle_track_left=v,
                                    duty_cycle_track_right=v - h,
                                    delay=0,
                                    acceleration=0)

        if -2 < v < 2:
            if h > 2:
                tracks.turn_right(duty_cycle_track_left=h,
                                  duty_cycle_track_right=h,
                                  delay=0,
                                  acceleration=0)

            if h < -2:
                tracks.track_left(duty_cycle_track_left=abs(h),
                                  duty_cycle_track_right=abs(h),
                                  delay=0,
                                  acceleration=0)


    # Legs
    if x_index != -1 and y_index != -1 and d_index != -1:
        d = int(str(data[d_index+2:x_index].replace(" ", "")))
        x = int(str(data[x_index+2:y_index].replace(" ", "")))
        y = int(str(data[y_index+2:].replace(" ", "")))
        print(str(x))
        print(str(y))

        if d == 1 and not legs.deployed:
            legs.deploy(200)
        elif d == 0 and legs.deployed:
            legs.retract(200)

        if legs.deployed:
            legs.move([530 + round(x / 10), 680, 760 + round(y / 10)], [650, 400, 400], [400, 400, 400], [600, 400, 400], 0, [200, 200, 200])


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
