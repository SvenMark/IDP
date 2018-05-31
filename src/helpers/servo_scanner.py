import sys

sys.path.insert(0, '../../src')

from libs.ax12 import Ax12

tester = Ax12()

for i in range(0, 255):
    try:
        tester.ping(i)
        print("Servo found with id: " + str(i))
    except tester.timeout_error:
        not_found = True
