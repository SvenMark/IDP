import sys
import time
from imutils.video import VideoStream
from entities.vision.helpers.vision_helper import *
from entities.vision.helpers.fucking_other_helper import *

sys.path.insert(0, '../../../src')


def run(name, control):
    movement = control.movement
    emotion = control.emotion
    shared_object = control.shared_object
    speed_factor = control.speed_factor
    dead_zone = control.dead_zone

    BPM = 150
    delay = 60 / 150

    print("[RUN] " + str(name))

    while not shared_object.has_to_stop():
        print("Doing calculations and stuff")

        movement.tracks.turn_right(30, 30, 0.1, 0)
        time.sleep(delay)

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
