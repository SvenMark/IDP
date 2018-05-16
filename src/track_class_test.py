#!/bin/python
from entities.movement.limb.track import Track
from entities.movement.tracks import Tracks

track1 = Track()
track2 = Track()
tracks = Tracks([track1, track2])

for cycle in range(0, 20):
    tracks.turn_right(cycle, cycle, 0.5)

for cycle in range(0, 20):
    tracks.turn_right(20 - cycle, 20 - cycle, 0.5)

for cycle in range(0, 20):
    tracks.turn_left(cycle, cycle, 0.5)

for cycle in range(0, 20):
    tracks.turn_left(20 - cycle, 20 - cycle, 0.5)
