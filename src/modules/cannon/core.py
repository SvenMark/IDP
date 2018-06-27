import sys
import time
import numpy as np
import cv2

sys.path.insert(0, '../../../src')

from imutils.video import VideoStream
from entities.vision.helpers.vision_helper import *
from entities.vision.helpers.fucking_other_helper import *
from entities.threading.utils import SharedObject
from threading import Thread

# Last known position of the line with left percentage
last_position = -1000

# From 0 to 1
TORQUE = 1

red_detected = False
line_detected = False
red = False


def run(name, control):
    movement = control.movement
    emotion = control.emotion
    shared_object = control.shared_object
    speed_factor = control.speed_factor
    dead_zone = control.dead_zone

    print("[RUN] " + str(name))
    cannon_thread = SharedObject()
    Thread(target=line_detection, args=(cannon_thread,)).start()

    while not shared_object.has_to_stop():

        movement.tracks.handle_controller_input(stop_motors=shared_object.bluetooth_settings.s,
                                                vertical_speed=shared_object.bluetooth_settings.h * speed_factor,
                                                horizontal_speed=shared_object.bluetooth_settings.v * speed_factor,
                                                dead_zone=dead_zone)

        global last_position, red, TORQUE, line_detected
        offset = 50 - last_position
        offset = offset * TORQUE

        if last_position == -1000:
            emotion.set_emotion("searching")
            print("[INFO] Waiting")
            while last_position == -1000:
                time.sleep(0.1)
        print("[INFO] Driving etc. with offset: {}".format(offset))
        if red_detected:
            movement.tracks.forward(duty_cycle_track_left=50, duty_cycle_track_right=55,
                                    delay=0, acceleration=0)
        if red:
            emotion.set_emotion("confirmed")
            print("[INFO] Red detected!")
            movement.tracks.stop()
            time.sleep(30)
            red = False
        else:
            if not emotion.blinking:
                emotion.set_emotion("searching")
            if line_detected:
                movement.move_towards(offset=offset, torque=1.2)

        time.sleep(0.1)

    # Notify shared object that this thread has been stopped
    print("[STOPPED] {}".format(name))
    cannon_thread.stop = True
    shared_object.has_been_stopped()


def line_detection(shared_object):
    """
    Detects the line in a special set region, calculates the average center of the line in the screen and detects red
    :param shared_object: Thread notifier
    :return: None
    """
    # Get view of picamera and do a small warmup of 0.3s
    cap = VideoStream(src=0, usePiCamera=True, resolution=(320, 240)).start()
    time.sleep(0.3)

    # Get width and height of the frame and make vertices for a traingle shaped region
    sample = cap.read()
    height, width, channel = sample.shape

    vertices = [
        (20, height),
        (width / 2, height / 2 + 20),
        (width - 20, height - 20),
    ]

    while not shared_object.has_to_stop():
        # Get current frame from picamera and make a cropped image with the vertices above with set_region
        img = cap.read()
        img = cv2.flip(img, -1)
        img_cropped = set_region(img, np.array([vertices], np.int32))

        # Add blur to the cropped image
        blur = cv2.GaussianBlur(img_cropped, (9, 9), 0)

        # Generate and set a mask for a range of black (color of the line) to the cropped image
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        black = Color("Black", [0, 0, 0], [180, 40, 110])
        mask = cv2.inRange(hsv, black.lower, black.upper)

        # Checks if the color red is detected and calls function detect_red with the img
        global red_detected, red
        if detect_red(img, hsv):
            red_detected = True
        else:
            if red_detected:
                red = True
            red_detected = False

        # Set variables and get lines with Houghlines function on the mask of black
        theta = np.pi / 180
        threshold = 30
        min_line_length = 10
        max_line_gap = 40

        lines = cv2.HoughLinesP(mask, 1, theta, threshold, np.array([]),
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

        cv2.imshow('camservice-lijn', img_clone)

        # If q is pressed, break while loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.stop()
    cv2.destroyAllWindows()


# Detect red in image function
def detect_red(img, hsv):
    """
    Detects red in the frame
    :param img: The current frame
    :param hsv: The current frame converted to hsv
    :return: Returns true if there is a red area larger then 100. Else it returns false
    """
    # Create red mask to hsv
    redc = Color("Red", [170, 100, 100], [190, 255, 255])
    mask = cv2.inRange(hsv, redc.lower, redc.upper)

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

