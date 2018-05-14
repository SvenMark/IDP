from libs.ax12 import Ax12
import time

boris = Ax12()

ax12id = 13

while True :
  boris.readPosition(ax12id)
