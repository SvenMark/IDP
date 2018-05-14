import numpy as np


class Color:
    def __init__(self, lower, upper):
        self.lower = np.array(lower)
        self.upper = np.array(upper)
