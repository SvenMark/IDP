from libs.ax12 import Ax12
import time

boris = Ax12()

servo1 = 13
servo2 = 31

boris.setLedStatus(servo1, 1)
boris.setLedStatus(servo2, 1)

while True:
    boris.move(servo1, 0)
    boris.move(servo2, 1000)
    time.sleep(2)

    boris.move(servo1, 1000)
    boris.move(servo2, 0)
    time.sleep(2)

GPIO.cleanup()
