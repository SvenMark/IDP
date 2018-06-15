import sys
sys.path.insert(0, '../../../src')

from imutils.video import VideoStream
from modules.cannon.helpers import Point, Color
from decimal import Decimal
from threading import Thread
import time
import numpy as np
import cv2

# last known position of the line with left percentage
last_position = -1000

# from 0 to 1
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
        print("[INFO] Doing shit with offset:" + str(offset))
        if red_detected and not line_detected:
            print("[INFO] Red detected")
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
    # Get view of picamera and do a small warmup of 0.3s
    cap = VideoStream(src=0, usePiCamera=True, resolution=(320, 240)).start()
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
    midp = Point(0, 0)
    midp.x = (p1.x + p2.x) / 2
    midp.y = (p1.y + p2.y) / 2
    return midp


# Calculate the average distance from left and right to center
def average_distance(lines, width):
    count = 0
    totaldr = 0  # Total distance to right
    totaldl = 0  # Total distance to left
    for line in lines:
        for x1, y1, x2, y2 in line:
            p1 = Point(x1, y1)
            p2 = Point(x2, y2)
            midp = midpoint(p1, p2)
            totaldr += (width - midp.x)  # Distance to right
            totaldl += (0 + midp.x)  # Distance to right
            count += 1

    # Average to sides (x-as)
    percentage_left = Decimal((Decimal(Decimal(totaldl) / Decimal(count)) / Decimal(width)) * Decimal(100))
    percentage_right = Decimal((Decimal(Decimal(totaldr) / Decimal(count)) / Decimal(width)) * Decimal(100))

    return percentage_left, percentage_right


def detect_red(img, hsv):
    red = Color([170, 100, 100], [190, 255, 255])
    mask = cv2.inRange(hsv, red.lower, red.upper)
    red = cv2.bitwise_and(img, img, mask=mask)

    ret, thresh = cv2.threshold(mask, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    total_area = 0
    for cnt in contours:
        cv2.drawContours(img, [cnt], -1, (0, 0, 255), 10)
        # cv2.imshow("red", red)
        total_area += cv2.contourArea(cnt)
    # print("[INFO] Known red area: {}".format(total_area))
    if len(contours) == 0 or total_area < 100:
        return False
    else:
        return True


if __name__ == '__main__':
    run(shared_object=None)  # disabled for travis
