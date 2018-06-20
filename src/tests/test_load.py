import sys
import time

sys.path.insert(0, '../../src')

from libs.ax12 import Ax12

ax12 = Ax12()

ax12.move(1, 300)

while True:
    print(str(ax12.read_load(1)))
