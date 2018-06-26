import sys

sys.path.insert(0, '../../src')

from libs.ax12 import Ax12

tester = Ax12()


def scan():
    servos = []
    for i in range(0, 255):
        try:
            tester.ping(i)
            pos = tester.read_position(i)
            if str(pos) != "None":
                print("Servo found with id: " + str(i) + " and position: " + str(pos))
                servos.append(i)
        except tester.timeout_error:
            pass

    if len(servos) is not 0:
        return servos
    else:
        print("No servos found")
        return servos