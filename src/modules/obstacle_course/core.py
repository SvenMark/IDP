import sys
import time
import cv2
import numpy as np

sys.path.insert(0, '../../../src')

from imutils.video import VideoStream
from entities.vision.recognize import Recognize
from entities.vision.obstacle_settings import ObstacleSettings
from entities.vision.helpers.vision_helper import *


def obstacle_course(shared_object):
    frame = VideoStream(src=0, usePiCamera=True, resolution=(320, 240)).start()
    time.sleep(0.3)  # startup

    sample = frame.read()
    height, width = sample.shape
    print("[INFO] W: " + str(width) + "px , H: " + str(height) + "px")

    while not shared_object.has_to_stop():

        # If q is pressed, break while loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    frame.stop()
    cv2.destroyAllWindows()


def run(name, control):
    movement = control.movement
    shared_object = control.shared_object
    speed_factor = control.speed_factor
    dead_zone = control.dead_zone

    print("[RUN] " + str(name))
    stairdetector(shared_object)

    while not shared_object.has_to_stop():
        movement.tracks.handle_controller_input(stop_motors=shared_object.bluetooth_settings.s,
                                                vertical_speed=shared_object.bluetooth_settings.h * speed_factor,
                                                horizontal_speed=shared_object.bluetooth_settings.v * speed_factor,
                                                dead_zone=dead_zone)
        time.sleep(0.1)

    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()


def stairdetector(frame, width, height):
    vertices = [
        (0, (height / 2) + 28),
        (width, (height / 2 + 28)),
        (width, (height / 2 + 48)),
        (0, (height / 2) + 48),
    ]

    # Get current frame from picamera and make a cropped image with the vertices above with set_region
    img = frame.read()
    img_cropped = set_region(img, np.array([vertices], np.int32))

    # Add blur to the cropped image
    blur = cv2.GaussianBlur(img_cropped, (9, 9), 0)

    # Generate and set a mask for a range of black (color of the line) to the cropped image
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    white = Color("Staircolor", [95, 0, 140], [180, 35, 255])
    mask = cv2.inRange(hsv, white.lower, white.upper)

    # Set line color to blue and clone the image to draw the lines on
    line_color = (255, 0, 0)
    img_clone = img.copy()

    # Set variables and get lines with Houghlines function on the mask of black
    theta = np.pi / 180
    threshold = 150
    min_line_length = 310
    max_line_gap = 50

    lines = cv2.HoughLinesP(mask, 2, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)

    if lines is not None:
        print("[INFO] Stair Detected!")
        for line in lines:
            for x1, y1, x2, y2 in line:
                # Make two points with the pixels of the line and draw the line on the cloned image
                p1 = Point(x1, y1)
                p2 = Point(x2, y2)
                cv2.line(img_clone, (p1.x, p1.y), (p2.x, p2.y), line_color, 2)

    cv2.imshow('camservice-stair', img_clone)


def detect_cup(frame, width, height):
    print("[RUN] Cup Detection")
    img = frame.read()
    img = cv2.GaussianBlur(img, (9, 9), 0)

    # Generate and set a mask for a range of black (color of the line) to the cropped image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cupc = Color("Cup Color", [30, 10, 60], [80, 135, 160])
    mask = cv2.inRange(hsv, cupc.lower, cupc.upper)
    mask_green = cv2.bitwise_and(img, img, mask=mask)

    # Get contours and draw them when area of them is 1000 or higher
    ret, thresh = cv2.threshold(mask, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        c = max(contours, key=cv2.contourArea)
        m = cv2.moments(c)
        try:
            cx = int(m["m10"] / m["m00"])
            cy = int(m["m01"] / m["m00"])
        except ZeroDivisionError:
            cx = 0
            cy = 0

        distanceleft = cx / width * 100
        distanceright = (width - cx) / width * 100

        cv2.drawContours(mask_green, [c], -1, (255, 255, 255), 5)
        cv2.circle(mask_green, (cx, cy), 7, (255, 255, 255), -1)

    cv2.imshow("Cup center", mask_green)


def detect_bridge():
    """
    Detects the bridge in the obstacle course
    :return: None
    """
    # Initialize color ranges for detection
    color_range = [Color("Brug", [0, 0, 0], [0, 255, 107]),
                   Color("Gat", [0, 0, 0], [0, 0, 255]),
                   Color("Rand", [0, 0, 185], [0, 0, 255]),
                   Color("White-ish", [0, 0, 68], [180, 98, 255])]

    cam = Recognize(color_range)
    cam.run()


# Set the region with the vertices on the img
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


if __name__ == '__main__':
    run(shared_object=None)  # disabled for travis
