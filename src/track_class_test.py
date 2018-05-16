#!/bin/python

from entities.movement.limb.joints.dcmotor import DCMotor
from entities.movement.tracks import Tracks

track1 = DCMotor()
track2 = DCMotor()
tracks = Tracks([track1, track2])

tracks.forward(50, 0, 1)
tracks.forward(20, 5, 1)

