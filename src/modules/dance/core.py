import sys
import time
from imutils.video import VideoStream
from threading import Timer
import RPi.GPIO as GPIO

sys.path.insert(0, '../../../src')

from entities.vision.helpers.vision_helper import *
from entities.vision.helpers.fucking_other_helper import *
from entities.movement.sequences.dance_sequence import *
from entities.movement.sequences.sequences import *

seconds = 0


def routine():
    global seconds
    seconds += 1
    t = Timer(1, routine)
    t.start()


def run(name, control):
    movement = control.movement
    emotion = control.emotion
    shared_object = control.shared_object
    speed_factor = control.speed_factor
    dead_zone = control.dead_zone

    routine()

    print("[RUN] " + str(name))

    while not shared_object.has_to_stop():
        forwards = True
        print("test")
        print(str(seconds))
        if seconds < 5:
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=None, sequence=drum)
        elif seconds < 13:
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=None, sequence=clap)
        elif seconds < 21:
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=None, sequence=clap)
            if forwards:
                movement.tracks.forward(50, 50, 0.1, 5)
                forwards = False
            else:
                movement.tracks.backward(50, 50, 0.1, 5)
                forwards = True
        elif seconds < 36:
            movement.tracks.turn_left(50, 50, 0, 5)
            movement.legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=None, sequence=ballerina)
        elif seconds < 48:
            movement.tracks.turn_right(50, 50, 0, 5)
            movement.legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=None, sequence=wave)
        elif seconds < 54:
            pass
        elif seconds < 61:
            pass
        elif seconds < 93:
            pass
        elif seconds < 102:
            pass
        elif seconds < 105:
            pass
        elif seconds < 120:
            pass
        else:
            print("DONE")
            shared_object.stop = True

    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()


def black_detection(shared_object):
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
        img = cap.read()
        img = cv2.flip(img, -1)
        img_cropped = set_region(img, np.array([vertices], np.int32))

        blur = cv2.GaussianBlur(img_cropped, (9, 9), 0)

        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        black = Color("Black", [0, 0, 0], [180, 40, 110])
        mask = cv2.inRange(hsv, black.lower, black.upper)

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

    cap.stop()
    cv2.destroyAllWindows()
