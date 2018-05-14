from libs.ax12 import Ax12
from dcMotorTest import Forwards
import time

boris = Ax12()

ax12id = 13

for cycle in range(0, 20):
    Forwards(cycle)
    boris.move(ax12id, 0)
    time.sleep(1)
    boris.move(ax12id, 1000)
    time.sleep(0.5)