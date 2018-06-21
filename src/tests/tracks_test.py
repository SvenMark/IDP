import sys

sys.path.insert(0, '../../src')

from entities.movement.tracks import Tracks

tracks = Tracks(track_0_pin=13,
                track_1_pin=18,
                track_0_forward=22,
                track_0_backward=27,
                track_1_forward=19,
                track_1_backward=26)

tracks.forward(100, 100, 2, 1)
tracks.forward(20, 20, 4, 4)
tracks.forward(0, 0, 1, 1)
tracks.turn_right(70, 20, 8, 12)
tracks.turn_right(10, 15, 8, 7)
