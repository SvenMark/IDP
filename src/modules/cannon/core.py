import sys
sys.path.insert(0, '../../../src')

from imutils.video import VideoStream
from modules.cannon.helpers import Point, Color
from threading import Thread
import time
import numpy as np
import cv2

# Last known position of the line with left percentage
last_position = -1000

# From 0 to 1
TORQUE = 1

red_detected = False
line_detected = False


def run(name, movement, shared_object):
    print("[RUN] " + str(name))
    Thread(target=line_detection, args=(shared_object,)).start()

    while not shared_object.has_to_stop():
        global last_position, red_detected, TORQUE, line_detected
        offset = 50 - last_position
        offset = offset * TORQUE

        if last_position == -1000:
            print("[INFO] Waiting")
            while last_position == -1000:
                time.sleep(0.1)
        print("[INFO] Driving etc. with offset:" + str(offset))
        if red_detected and not line_detected:
            print("[INFO] Red detected!")
            if movement is not None:
                movement.tracks.stop()
        else:
            if movement is not None:
                left = 20
                right = 20
                if offset < 0:
                    left += offset
                else:
                    right -= offset

                movement.tracks.forward(duty_cycle_track_left=left, duty_cycle_track_right=right,
                                        delay=0, acceleration=0)

        time.sleep(0.1)

    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()


def line_detection(shared_object):
    """
    Detects the line in a special set reagion, calculates the avarge center of the line in the screen and detects red
    :param shared_object: Thread notifier
    :return: None
    """
    # Get view of picamera and do a small warmup of 0.3s
    cap = VideoStream(src=0, usePiCamera=False, resolution=(320, 240)).start()
    time.sleep(0.3)

    # Get width and height of the frame and make vertices for a traingle shaped region
    sample = cap.read()
    height, width, channel = sample.shape

    vertices = [
        (0, height),
        (width / 2, height / 2),
        (width, height),
    ]

    while not shared_object.has_to_stop():
        # Get current frame from picamera and make a cropped image with the vertices above with set_region
        img = cap.read()
        img_cropped = set_region(img, np.array([vertices], np.int32))

        # Add blur to the cropped image
        blur = cv2.GaussianBlur(img_cropped, (9, 9), 0)

        # Generate and set a mask for a range of black (color of the line) to the cropped image
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        black = Color([0, 0, 40], [157, 118, 120])
        mask = cv2.inRange(hsv, black.lower, black.upper)

        # Checks if the color red is detected and calls function detect_red with the img
        global red_detected
        if detect_red(img, hsv):
            red_detected = True
        else:
            red_detected = False

        # Set variables and get lines with Houghlines function on the mask of black
        theta = np.pi / 180
        threshold = 150
        min_line_length = 40
        max_line_gap = 25

        lines = cv2.HoughLinesP(mask, 2, theta, threshold, np.array([]),
                                min_line_length, max_line_gap)

        # Set line color to blue and clone the image to draw the lines on
        line_color = (255, 0, 0)
        img_clone = img.copy()

        global line_detected

        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    # Make two points with the pixels of the line and draw the line on the cloned image
                    p1 = Point(x1, y1)
                    p2 = Point(x2, y2)
                    cv2.line(img_clone, (p1.x, p1.y), (p2.x, p2.y), line_color, 5)
            # Calculate avarge distance with avarge_distance in percentages to the left and right
            left, right = average_distance(lines, width)
            global last_position
            last_position = round(left)
            line_detected = True
        else:
            line_detected = False

        # cv2.imshow('camservice-lijn', img_clone)

        # If q is pressed, break while loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


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

    return masked_img


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


# Detect red in image function
def detect_red(img, hsv):
    """
    Detects red in the frame
    :param img: The current frame
    :param hsv: The current frame converted to hsv
    :return: Returns true if there is a red area larger then 100. Else it returns false
    """
    # Create red mask to hsv
    red = Color([170, 100, 100], [190, 255, 255])
    mask = cv2.inRange(hsv, red.lower, red.upper)
    red = cv2.bitwise_and(img, img, mask=mask)

    # Find contours on the set mask so it sees only red
    ret, thresh = cv2.threshold(mask, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    total_area = 0
    # For each contour that is found, draw them
    for cnt in contours:
        cv2.drawContours(img, [cnt], -1, (0, 0, 255), 10)
        total_area += cv2.contourArea(cnt)
    # print("[INFO] Known red area: {}".format(total_area))

    # Check if the lenght of contours isn't 0 so it knows there is red in the frame
    if len(contours) == 0 or total_area < 100:
        return False
    else:
        return True


if __name__ == '__main__':
    run(shared_object=None)  # disabled for travis
