import sys

sys.path.insert(0, '../../src')

from libs.ax12 import Ax12


def servo_scanner():
    axscanner = Ax12()

    servos = []

    for i in range(0, 200):
        try:
            axscanner.ping(i)
            pos = axscanner.read_position(i)
            if str(pos) != "None":
                print("Servo found with id: " + str(i) + " and position: " + str(pos))
                servos.append(i)
        except axscanner.timeout_error:
            pass

    if len(servos) is 0:
        print("No servo`s found")
    return servos
