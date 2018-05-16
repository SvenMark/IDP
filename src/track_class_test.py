#!/bin/python

from entities.movement.limb.joints.dcmotor import DCMotor
from entities.movement.tracks import Tracks

tracks = Tracks()

tracks.forward(50, 0, 1)
tracks.forward(20, 5, 1)

