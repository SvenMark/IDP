#! /usr/bin/python

import time
import serial

bluetoothSerial = serial.Serial("/dev/rfcomm1", baudrate=9600)

count = None
while count is None:
    try:
        count = int(input("Please enter the number of times to blink the L$"))
    except:
        pass  # Ignore any errors that may occur and try again

bluetoothSerial.write(str(count))
print(bluetoothSerial.readline())
