from libs.ax12 import Ax12
import time

boris = Ax12()

servo1 = 13
servo2 = 31

boris.setLedStatus(servo1, 1)
boris.setLedStatus(servo2, 1)

boris.move(servo1, 500)
boris.move(servo2, 500)
