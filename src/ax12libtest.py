from ax12 import Ax12
import time

roby = Ax12()
roby.port = Serial("/dev/ttyS0", baudrate=1000000, timeout=0.001)

while True :
  roby.move(19,200)
  time.sleep(5)

  roby.move(19,800)
  time.sleep(5)
