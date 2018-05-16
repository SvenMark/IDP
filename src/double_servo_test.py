from libs.ax12 import Ax12
import time

boris = Ax12()

servo1 = 13
servo2 = 31

boris.set_led_status(servo1, 1)
boris.set_led_status(servo2, 1)

while True:
    boris.move(servo1, 0)
    boris.move(servo2, 998)
    time.sleep(2)

    boris.move(servo1, 998)
    boris.move(servo2, 0)
    time.sleep(2)
