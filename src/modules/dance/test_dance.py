import time
import threading
from entities.threading.utils import *
from threading import Timer

print("[RUN] " + str("test dance"))

update = False

# beat detectie
pin = 20

#
pin2 = 16

beatPin = 21


def readBeatPin():
    while True:
        # if readpin(beatPin) == high
        time.sleep(0.2)

readBeatPin()
