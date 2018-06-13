import sys
import time

sys.path.insert(0, '../../src')

from entities.movement.grabber import Grabber

grabber = Grabber(id_servo=[
            1,
            53,
            13
        ])

grabber.grab([0, 0, 0], 0, [50, 50, 50])
time.sleep(2)
grabber.loosen([0, 0, 0], 0, [50, 50, 50])
