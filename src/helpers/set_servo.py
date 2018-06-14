import sys

sys.path.insert(0, '../../src')

from libs.ax12 import Ax12

tester = Ax12()

tester.move(63, 800)
