import numpy as np
import cv2


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

    return masked_img
