import sys

sys.path.insert(0, '../../../src')


class BluetoothSettings(object):
    def __init__(self):
        self.s = 0
        self.v = 0
        self.h = 0
        self.d = 0
        self.x = 0
        self.y = 0
        self.m = 0

    def handle_values(self, s, v, h, d, x, y, m):
        self.s = s
        self.v = v
        self.h = h
        self.d = d
        self.x = x
        self.y = y
        self.m = m