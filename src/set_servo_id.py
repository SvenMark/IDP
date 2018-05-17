#!/bin/python

import time

from libs.ax12 import Ax12

servo = Ax12()

servo.factory_reset(13, True)

