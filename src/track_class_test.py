#!/bin/python

from entities.movement.limb.joints.dcmotor import DCMotor
from entities.movement.tracks import Tracks

tracks = Tracks(track1pin=18, track2pin=13)

tracks.forward(100, 2, 1)
tracks.forward(20, 4, 4)
tracks.forward(0, 1, 1)
tracks.turn_right(70, 20, 8, 12)
tracks.turn_right(10, 15, 8, 7)

