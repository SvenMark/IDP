#!/bin/python

from entities.movement.limb.tracks import Tracks

tracks = Tracks()

tracks.forward(50, 0, 1)
tracks.forward(20, 0, 1)

while True:
	print("Lars houdt van piemels")
