import time
import sys


sys.path.insert(0, '../../src')

from entities.movement.legs import Legs
from entities.movement.tracks import Tracks
from entities.movement.sequences.sequences import *

legs = Legs(
    leg_0_servos=[21, 41, 52],
    leg_1_servos=[16, 17, 18],
    leg_2_servos=[61, 62, 63],
    leg_3_servos=[6, 14, 15]
)

tracks = Tracks(track_0_pin=13,
                track_1_pin=18,
                track_0_forward=22,
                track_0_backward=27,
                track_1_forward=19,
                track_1_backward=26)

tracks.forward(100, 100, 3, 0)

# legs.move(leg_0_moves=[354, 166, 853],
#           leg_1_moves=[682, 166, 853],
#           leg_2_moves=[354, 384, 660],
#           leg_3_moves=[682, 384, 660],
#           speeds=[150, 150, 150],
#           self_update=True)
#
# while True:
#     tracks.forward(100, 100, 0, 0)
#     legs.move(leg_0_moves=[354, 166, 853],
#               leg_1_moves=[682, 166, 853],
#               leg_2_moves=[352, 170, 840],
#               leg_3_moves=[682, 170, 840],
#               speeds=[150, 150, 150],
#               self_update=True)
