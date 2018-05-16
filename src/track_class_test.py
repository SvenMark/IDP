#!/bin/python
from entities.movement.limb.track import Track
from entities.movement.tracks import Tracks

track1 = Track()
track2 = Track()
tracks = Tracks([track1, track2])

tracks.forward(50, 0, 1)
tracks.forward(20, 5, 1)

