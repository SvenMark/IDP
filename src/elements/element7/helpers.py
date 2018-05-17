import numpy as np


class Color:
    def __init__(self, lower, upper):
        self.lower = np.array(lower)
        self.upper = np.array(upper)


class Position:
    def __init__(self, color, array):
        self.color = color
        self.array = array


class ColorRange:
    def __init__(self, color, color_range):
        self.color = color
        self.range = color_range
