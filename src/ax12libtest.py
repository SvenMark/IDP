from libs.ax12 import Ax12
import time

boris = Ax12()

ax12id = 13

while True :
  boris.move(ax12id,200)
  time.sleep(5)

  boris.move(ax12id,800)
  time.sleep(5)
