from libs.ax12 import Ax12
import time

boris = Ax12()

servo1 = 13
servo2 = 31

while True :
  boris.move(servo1,180)
  boris.move(servo2,-180)
  time.sleep(2)

  boris.move(servo1,-180)
  boris.move(servo2,180)
  time.sleep(2)
