from __future__ import print_function
import glob
import struct
import time
import numpy as np


available_ports = glob.glob('/dev/rfcomm*')
print("Available porst: ")
print(available_ports)
