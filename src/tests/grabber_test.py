import sys
import time

sys.path.insert(0, '../../src')

from entities.movement.tracks import Tracks
from entities.movement.grabber import Grabber
from entities.movement.limb.joints.servo import Servo
from libs.ax12 import Ax12

grabber = Grabber(servos=[
            1,
            53,
            43
        ],
        initial_positions=[455, 185, 83])

grabber.grab(20, True)
grabber.loosen(30)
# grabber.loosen(80)

# tracks = Tracks(track_0_pin=13,
#                 track_1_pin=18,
#                 track_0_forward=22,
#                 track_0_backward=27,
#                 track_1_forward=19,
#                 track_1_backward=26),
#
# while True:
#     grabber.grab([80, 80, 80])
#     if grabber.reposition is True:
#         tracks.forward(30, 30, 2, 3)
#         grabber.reposition = False
