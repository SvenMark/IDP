import sys
import time
from imutils.video import VideoStream
from threading import Timer
import RPi.GPIO as GPIO

sys.path.insert(0, '../../../src')

from entities.vision.helpers.vision_helper import *
from entities.vision.helpers.fucking_other_helper import *
from entities.movement.sequences.dance_sequence import *

seconds = -4


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

    forwards = True
    prev = 0

    routine()

    print("[RUN] " + str(name))

    while not shared_object.has_to_stop():
        print(str(seconds))
        if seconds < 0:
            # COUNTDOWN
            print(str(abs(seconds)))
        elif seconds < 5:
            print("Dums")
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=None, sequence=drum)
        elif seconds < 13:
            print("Clap")
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=None, sequence=clap)
        elif seconds < 21:
            print("Clap and move")
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=None, sequence=clap)
            if forwards and prev < seconds:
                movement.tracks.forward(50, 55, 0, 0)
                forwards = False
                prev = seconds
            elif not forwards and prev < seconds:
                movement.tracks.backward(60, 65, 0, 0)
                forwards = True
                prev = seconds
        elif seconds < 36:
            print("Ballerina pirouette")
            movement.tracks.turn_left(70, 70, 0, 0)
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=None, sequence=ballerina)
        elif seconds < 48:
            print("Pirouette wave")
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=None, sequence=wave)
            movement.tracks.turn_right(70, 70, 0, 0)
        elif seconds < 54:
            print("Running man")
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=[0], sequence=running_man)
            movement.tracks.forward(60, 65, 0.1, 0)
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=[1], sequence=wave)
            movement.tracks.backward(70, 75, 0.1, 0)
            movement.tracks.stop()
        elif seconds < 61:
            print("Whats goin on?")
            emotion.set_emotion("confused")
            movement.tracks.turn_right(70, 70, 0.2, 0)
            movement.tracks.turn_left(70, 70, 0.2, 0)
        elif seconds < 93:
            emotion.set_emotion("neutral")
            movement.tracks.stop()
            movement.legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=None, sequence=shake_ass)
        elif seconds < 98:
            print("Fast ballerina pirouette")
            emotion.set_emotion("happy")
            movement.tracks.turn_left(95, 95, 0, 0)
            movement.legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=None, sequence=ballerina)
        elif seconds < 102:
            print("Fast pirouette wave")
            movement.tracks.turn_left(95, 95, 0, 0)
            movement.legs.run_sequence(speeds=[150, 150, 150], self_update=True, sequences=None, sequence=wave)
        elif seconds < 105:
            movement.tracks.stop()
            emotion.set_emotion("shutdown")
        elif seconds < 120:
            emotion.set_emotion("neutral")
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=None, sequence=left_dab)
            movement.legs.run_sequence(speeds=[100, 100, 100], self_update=True, sequences=None, sequence=right_dab)
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
