import numpy as np


class Color:
    def __init__(self, lower, upper):
        self.lower = np.array(lower)
        self.upper = np.array(upper)


class Block:
    def __init__(self, color, centre):
        self.color = color
        self.centre = centre


class ColorRange:
    def __init__(self, color, color_range):
        self.color = color
        self.range = color_range


class Building:
    def __init__(self, front, back, left, right):
        self.front = front
        self.back = back
        self.left = left
        self.right = right

