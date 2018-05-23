import numpy as np


class Color:
    def __init__(self, lower, upper):
        self.lower = np.array(lower)
        self.upper = np.array(upper)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
