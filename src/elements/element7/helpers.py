import numpy as np
import os


class Color:
    def __init__(self, color, lower, upper, base):
        self.color = color
        self.lower = np.array(lower)
        self.upper = np.array(upper)
        self.base = base


class Block:
    def __init__(self, color, centre):
        self.color = color
        self.centre = np.array(centre)


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


class SavedBuildings:
    calibrate_building = [Block("orange", (267, 356)),
                         Block("yellow", (252, 140)),
                         Block("red", (362, 133)),
                         Block("green", (369, 350)),
                         Block("blue", (311, 251))]

    buildings = [
        Building(front=[Block("orange", (41, 324)),
                        Block("yellow", (33, 97)),
                        Block("red", (148, 92)),
                        Block("green", (153, 318)),
                        Block("blue", (92, 218))],
                 back=[Block("blue", (31, 316)),
                       Block("green", (86, 209)),
                       Block("orange", (30, 91)),
                       Block("yellow", (144, 317))],
                 left=[Block("red", (112, 175)),
                       Block("blue", (44, 304)),
                       Block("green", (36, 68)),
                       Block("orange", (184, 70)),
                       Block("yellow", (180, 307))],
                 right=[Block("red", (112, 175)),
                        Block("blue", (44, 304)),
                        Block("green", (36, 68)),
                        Block("orange", (184, 70)),
                        Block("yellow", (180, 307))]
                 )
    ]

