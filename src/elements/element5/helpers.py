import numpy as np
import cv2


class Color:
    def __init__(self, color, lower, upper):
        self.color = color
        self.lower = np.array(lower)
        self.upper = np.array(upper)


class ColorRange:
    def __init__(self, color, color_range):
        self.color = color
        self.range = color_range


class Block:
    def __init__(self, color, centre):
        self.color = color
        self.centre = np.array(centre)

    def __str__(self):
        return "Block({}, ({}, {}))".format(self.color, self.centre[0], self.centre[1])


def check_valid_convex(c, sides, area_min):
    """
    Checks if a convex is a valid block
    :return: True if the contour is a block
    """

    # Calculate the perimeter
    peri = cv2.arcLength(c, True)

    # Calculate the sides of the convexhull, 4 is a square/rectangle, 3 is a triangle etc.
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    # Calculate the area of the convexhull
    area = cv2.contourArea(c)

    # If the convexhull counts 4 sides and an area bigger than 4000
    return len(approx) == sides and area_min < area
