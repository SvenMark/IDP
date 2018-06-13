import sys
import time

sys.path.insert(0, '../../src')

from libs.ax12 import Ax12

ax12 = Ax12()

ax12.move(1, 850)
time.sleep(2)
ax12.move(13, 425)
time.sleep(2)
ax12.move(53, 595)
