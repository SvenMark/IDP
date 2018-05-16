from collections import OrderedDict
from threading import Timer

from imutils.video import WebcamVideoStream
from elements.element7.helpers import Color
from elements.element7.helpers import Position

import time
import positions as db
import numpy as np
import cv2
import os

# print("uncomment run before starting..")

POSITIONS = []
LAST_POS_LEN = 100
STOP_POSITIONS = False


def run():
    print("run element7")
    cap = WebcamVideoStream(src=1).start()
    time.sleep(1)

    # initialize color ranges for detection
    orange = Color([0, 100, 100], [10, 255, 255])
    yellow = Color([20, 100, 100], [30, 255, 255])
    red = Color([170, 100, 100], [190, 255, 255])
    green = Color([60, 100, 50], [90, 255, 255])
    blue = Color([90, 100, 100], [120, 255, 255])

    colors = OrderedDict({
        "red": (0, 0, 255),
        "blue": (255, 0, 0),
        "green": (0, 255, 0),
        "orange": (0, 165, 255),
        "yellow": (0, 255, 255)})

    routine()

    while True:
        img = cap.read()
        img = cv2.GaussianBlur(img, (9, 9), 0)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        masks = OrderedDict({
            "red": cv2.inRange(hsv, red.lower, red.upper),
            "blue": cv2.inRange(hsv, blue.lower, blue.upper),
            "green": cv2.inRange(hsv, green.lower, green.upper),
            "orange": cv2.inRange(hsv, orange.lower, orange.upper),
            "yellow": cv2.inRange(hsv, yellow.lower, yellow.upper)})

        # set contours
        imgmask = set_contours(masks.get("red"), "red", img)
        for col, mask in masks.items():
            if col == "red":
                continue
            imgmask += set_contours(mask, col, img)

        draw_saved_positions(imgmask, colors)

        cv2.imshow('camservice', imgmask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.stop()
    cv2.destroyAllWindows()


# draw saved positions
def draw_saved_positions(imgmask, colors):
    for i in range(len(db.buildings[0])):
        cnt = np.array(db.buildings[0][i].array)
        color = db.buildings[0][i].color
        c = cv2.convexHull(cnt)
        M = cv2.moments(c)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        text = "{} {}".format("Color", color)
        cv2.drawContours(imgmask, [c], 0, colors.get(color), 3, -1)
        cv2.putText(imgmask, text, (cx - 25, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)


# sets contours for selected masks
def set_contours(mask, color, img):
    img_mask = cv2.bitwise_and(img, img, mask=mask)

    ret, thresh = cv2.threshold(mask, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # save correct contours when key 's' is pressed
    # if cv2.waitKey(1) & 0xFF == ord('s') or keyboard.is_pressed('s'):
    #     for i in range(len(POSITIONS)):
    #         color = POSITIONS[i].color
    #         cnt = POSITIONS[i].array
    #         save_contour(cnt, color)

    # draw all correct contours
    for i in range(len(contours)):
        c = cv2.convexHull(contours[i])
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        area = cv2.contourArea(c)

        if len(approx) == 4 and area > 4000:
            moment = cv2.moments(c)
            cx = int(moment['m10'] / moment['m00'])
            cy = int(moment['m01'] / moment['m00'])
            cv2.drawContours(img_mask, [c], 0, (255, 255, 255), 3)
            text = "{} {}".format("Color:", color)
            cv2.putText(img_mask, text, (cx - 25, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

            global LAST_POS_LEN, STOP_POSITIONS

            if not STOP_POSITIONS:
                if not is_duplicate(contours[i], POSITIONS):
                    POSITIONS.append(Position(color, contours[i]))
                    print("Found {}, color {}".format(len(POSITIONS), color))

    return img_mask


def routine():
    t = Timer(2, routine)
    t.start()
    global STOP_POSITIONS, LAST_POS_LEN
    if LAST_POS_LEN == len(POSITIONS):
        STOP_POSITIONS = True

        # save current positions to file
        # save_contour(POSITIONS)

        # start recognizing building
        print("napalm")
        recognize_building(POSITIONS)

    LAST_POS_LEN = len(POSITIONS)


def recognize_building(positions):
    # check if you recognize position
    for building in range(len(db.buildings)):
        currentbuilding = False
        for contour in range(len(db.buildings[building])):
            if not len(positions) == len(db.buildings[building]):
                break
            for position in range(len(db.buildings[building][contour].array)):
                if db.buildings[building][contour].color == positions[building].color:
                    print "{}, {}\n".format(db.buildings[building][contour].color, positions[building].color)

                    if compare_numpy(positions[contour].array, db.buildings[building][contour].array):  # found block
                        currentbuilding = True
                    else:  # wrong block
                        currentbuilding = False
                        break
        if currentbuilding:
            print("{} detected position of building {}".format(time.ctime(), building))


# checks if contour is duplicate
def is_duplicate(x, y, sensitivity=50):
    if len(y) == 0:
        return False
    for i in range(len(y)):
        if abs(x[0][0][0] - y[i].array[0][0][0]) < sensitivity:
            return True

    return False


# saves the current correct contours to positions.py array
def save_contour(positions):
    try:
        reload(db)
        filename = "positions.py"
        output = open(filename, "a")
        output.seek(-1, os.SEEK_END)
        output.truncate()
        first = True
        for i in range(len(positions)):
            c = positions[i].array
            color = positions[i].color
            print("{}, {}".format(i, color))

            if not first:
                output.write("        , Position(\"" + color + "\", [")
            else:
                output.write("        Position(\"" + color + "\", [")
                first = False

            for j in range(len(c)):
                if j == 0:
                    output.write("[[{}{}{}]]".format(str(c[j][0][0]).strip(), ", ", str(c[j][0][1]).strip()))
                else:
                    output.write(", [[{}{}{}]]".format(str(c[j][0][0]).strip(), ", ", str(c[j][0][1]).strip()))
            output.seek(-1, os.SEEK_END)
            output.truncate()
            output.write("]])\n")
        output.write(']')
        output.close()
        reload(db)
        print("successfully saved")
    except ValueError:
        print("failed to save")


# compares two contours for detection
def compare_numpy(x, y):
    sensitivity = 100

    for i in range(len(x)):
        point_close = False
        for t in range(len(y)):
            distance = np.linalg.norm(x[i] - y[t]) # x[i] = [520,137] y[430,180]
            if distance <= sensitivity:
                point_close = True

        if not point_close:
            return False
    return True


run()  # disabled for travis
