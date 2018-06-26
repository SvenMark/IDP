import sys
import time
import numpy as np
import cv2

sys.path.insert(0, '../../../src')

from entities.vision.helpers.vision_helper import *


# Set the triangle region with the vertices on the img
def set_region(img, vertices):
    """
    Sets a region with the points of vertices on the image
    :param img: The current frame of the picamera
    :param vertices: Points on the screen
    :return: A masked image with only the region
    """
    mask = np.zeros_like(img)
    channel_count = img.shape[2]
    match_mask_color = (255,) * channel_count
    cv2.fillPoly(mask, vertices, match_mask_color)

    masked_img = cv2.bitwise_and(img, mask)

    new_mask = np.zeros(masked_img.shape[:2], np.uint8)

    bg = np.ones_like(masked_img, np.uint8) * 255
    cv2.bitwise_not(bg, bg, mask=new_mask)

    return masked_img + bg


# Calculate midpoint of 2 points
def midpoint(p1, p2):
    """
    Calculates a midpoint between two points
    :param p1: Point number one with a x and y coordinate
    :param p2: Point number two with a x and y coordinate
    :return: The midpoint as a point with a x and y coordinate
    """
    midp = Point(0, 0)
    midp.x = (p1.x + p2.x) / 2
    midp.y = (p1.y + p2.y) / 2
    return midp


# Calculate the average distance from left and right to center
def average_distance(lines, width):
    """
    Calculates the average distance of the lines from the left and the right of the screen so it can
    centralize
    :param lines: All the lines it has detected
    :param width: The width of the frame
    :return: The average percentage (decimal) of al the lines from the left and the right of the screen
    """
    # Set count, total distance left and total distance right
    count = 0
    totaldr = 0
    totaldl = 0
    # For each line, calculate midpoint and add to totals
    for line in lines:
        for x1, y1, x2, y2 in line:
            p1 = Point(x1, y1)
            p2 = Point(x2, y2)
            midp = midpoint(p1, p2)
            totaldr += (width - midp.x)  # Distance to right
            totaldl += (0 + midp.x)  # Distance to right
            count += 1

    # Calculate average to sides (x-as)
    percentage_left = (totaldl / count) / width * 100
    percentage_right = (totaldr / count) / width * 100

    return percentage_left, percentage_right