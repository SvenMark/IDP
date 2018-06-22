import sys
import time
import cv2
import numpy as np

sys.path.insert(0, '../../../src')

from imutils.video import VideoStream
from entities.vision.recognize import Recognize
from entities.vision.helpers.vision_helper import *


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


def stairdetector(shared_object):
    frame = VideoStream(src=0, usePiCamera=False, resolution=(320, 240)).start()
    time.sleep(0.3)  # startup

    sample = frame.read()
    height, width, channel = sample.shape
    width = 320
    height = 240
    print("[INFO] w:" + str(width) + ", h: " + str(height))

    vertices = [
        (0, (height / 2) + 28),
        (width, (height / 2 + 28)),
        (width, (height / 2 + 48)),
        (0, (height / 2) + 48),
    ]

    while not shared_object.has_to_stop():
        # Get current frame from picamera and make a cropped image with the vertices above with set_region
        img = cv2.imread("../../resources/trap-recht-320px.jpg")
        img_cropped = set_region(img, np.array([vertices], np.int32))

        # Add blur to the cropped image
        blur = cv2.GaussianBlur(img_cropped, (9, 9), 0)

        # Generate and set a mask for a range of black (color of the line) to the cropped image
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        white = Color("White", [95, 0, 140], [180, 35, 255])
        mask = cv2.inRange(hsv, white.lower, white.upper)

        # Set line color to blue and clone the image to draw the lines on
        line_color = (255, 0, 0)
        img_clone = img.copy()

        # Set variables and get lines with Houghlines function on the mask of black
        theta = np.pi / 180
        threshold = 150
        min_line_length = 319
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

        # If q is pressed, break while loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    frame.stop()
    cv2.destroyAllWindows()


def detect_cup(shared_object):
    cam = VideoStream(src=0, usePiCamera=False, resolution=(320, 240)).start()
    time.sleep(0.3)  # startup

    sample = cam.read()
    height, width, channel = sample.shape
    print("[INFO] w:" + str(width) + ", h: " + str(height))

    createtrackbars("canny low high")

    while not shared_object.has_to_stop():
        lowc = cv2.getTrackbarPos('Low Canny', 'canny low high')
        highc = cv2.getTrackbarPos('High Canny', 'canny low high')

        frame = cam.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_canny = cv2.Canny(frame_gray, lowc, highc)
        cv2.imshow("Canny", frame_canny)

        if cv2.waitKey(10) == ord('q'):
            break

    cam.stop()
    cv2.destroyAllWindows()


def createtrackbars(name):
    cv2.namedWindow(name)

    # create trackbars for lower
    cv2.createTrackbar('Low Canny', name, 100, 1000, nothing)
    cv2.createTrackbar('High Canny', name, 200, 1000, nothing)


def nothing(x):
    pass


def detect_cup_old():
    """
    Detects the cup and calculates distance to cup
    :return: None
    """
    # Set minimal points which he needs to detect the cup
    MIN_MATCH_COUNT = 20

    # Set the detector and create matcher
    detector = cv2.xfeatures2d.SIFT_create()

    FLANN_INDEX_KDITREE = 0
    flannParam = dict(algorithm=FLANN_INDEX_KDITREE, tree=5)
    flann = cv2.FlannBasedMatcher(flannParam, {})

    # Get training image of cup
    trainImg = cv2.imread("cup.jpg", 0)
    trainKP, trainDesc = detector.detectAndCompute(trainImg, None)

    # Get video of picamera
    cam = VideoStream(src=0, usePiCamera=False, resolution=(320, 240)).start()
    time.sleep(0.3)  # startup

    while True:
        # Get frame and turn it into black and white
        frame = cam.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Set mask
        green = Color('green', [28, 39, 0], [94, 255, 255])
        mask = cv2.inRange(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), green.lower, green.upper)

        # Get contours and draw them when area of them is 1000 or higher
        ret, thresh = cv2.threshold(mask, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1000:
                cv2.drawContours(mask, [cnt], -1, (255, 255, 255), 50)

        cv2.imshow('Masked cup', mask)

        # Detect points and compare with cup image and returns matches
        queryKP, queryDesc = detector.detectAndCompute(frame_gray, mask=mask)
        matches = flann.knnMatch(queryDesc, trainDesc, k=2)

        goodMatch = []

        # Counts matches
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                goodMatch.append(m)

        # If there are more matches then the minimal count, detect the cup and draw border
        if len(goodMatch) > MIN_MATCH_COUNT:
            tp = []
            qp = []
            for m in goodMatch:
                tp.append(trainKP[m.trainIdx].pt)
                qp.append(queryKP[m.queryIdx].pt)
            tp, qp = np.float32((tp, qp))
            H, status = cv2.findHomography(tp, qp, cv2.RANSAC, 3.0)
            h, w = trainImg.shape
            trainBorder = np.float32([[[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]])
            queryBorder = cv2.perspectiveTransform(trainBorder, H)

            moment = cv2.moments(queryBorder)

            # Calculate distance in a really ugly way
            x, y, w, h = cv2.boundingRect(queryBorder)
            distance = 0.00008650519031141868 * h ** 2 - 0.10294117647058823 * h + 35

            # Calculate the centre of mass
            cx = int(moment['m10'] / moment['m00'])
            cy = int(moment['m01'] / moment['m00'])

            # Adds text to center with 'cup'
            cv2.putText(frame, "Cup", (cx - 30, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.polylines(frame, [np.int32(queryBorder)], True, (255, 255, 255), 4)
            print("[INFO] Cup detected at distance: " + str(distance) + "cm")
        else:
            print("[INFO] Not Enough match found- %d/%d" % (len(goodMatch), MIN_MATCH_COUNT))
        cv2.imshow('Detected cup', frame)
        if cv2.waitKey(10) == ord('q'):
            break
    cam.stop()
    cv2.destroyAllWindows()


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


if __name__ == '__main__':
    run(shared_object=None)  # disabled for travis
