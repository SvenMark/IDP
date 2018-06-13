import sys
import time

sys.path.insert(0, '../../src')

from entities.movement.grabber import Grabber

grabber = Grabber(id_servo=[
            1,
            53,
            13
        ],
        initial_positions=[1020, 270, 815])

for i in range(10):
    grabber.grab([0, 0, 0], 0, [80, 80, 80])
    time.sleep(2)
    grabber.loosen([0, 0, 0], 0, [80, 80, 80])
