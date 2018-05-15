from collections import OrderedDict
from threading import Timer

from imutils.video import WebcamVideoStream
from elements.element7.helpers import Color

import time
import positions as db
import numpy as np
import cv2
import os
import keyboard


# print("uncomment run before starting..")

_C, _COLOR = 1, 1

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

    routine()

    colors = OrderedDict({
        "red": (0, 0, 255),
        "blue": (255, 0, 0),
        "green": (0, 255, 0),
        "orange": (0, 165, 255),
        "yellow": (0, 255, 255)})

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

    for i in range(len(db.buildings[1])):
        cnt = np.array(db.buildings[1][i].array)
        color = db.buildings[1][i].color
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
    if cv2.waitKey(1) & 0xFF == ord('s') or keyboard.is_pressed('s'):
        for x in range(len(contours)):
            c = cv2.convexHull(contours[x])
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            area = cv2.contourArea(c)
            if len(approx) == 4 and area > 4000 and not is_duplicate(contours[x], db.positions):
                save_contour(contours[x], color)

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

            global _C, _COLOR
            _C = c
            _COLOR = color

    return img_mask


def routine():
    t = Timer(7200, routine)
    t.start()
    recognizebuilding(_C, _COLOR)


def recognizebuilding(c, color):
    # check if you recognize position
    for j in range(len(db.buildings)):
        currentbuilding = True
        for k in range(len(db.buildings[j])):
            for l in range(len(db.buildings[j][k].array)):
                if db.buildings[j][k].color == color:
                    if compare_numpy(c, db.buildings[j][k].array):  # found block
                        currentbuilding = True
                    else:  # wrong block
                        currentbuilding = False
                        # look for next building
                        break
        if currentbuilding:
            print("{} detected position of building {}".format(time.ctime(), j))


# checks if contour is duplicate
def is_duplicate(x, y):

    reload(db)
    time.sleep(.1)
    if len(y) == 0:
        return False
    sensitivity = 30
    for i in range(len(y)):
        if abs(x[0][0][0] - y[i].array[0][0][0]) < sensitivity:
            return True

    return False


# saves the current correct contours to positions.py array
def save_contour(c, color):
    try:
        filename = "positions.py"
        output = open(filename, "a")
        output.seek(-1, os.SEEK_END)
        output.truncate()
        if len(db.positions) == 0:
            output.write("        Position(\"" + color + "\", [")
        else:
            output.write("        , Position(\"" + color + "\", [")
        for i in range(len(c)):
            if i == 0:
                output.write("[[{}{}{}]]".format(str(c[i][0][0]).strip(), ", ", str(c[i][0][1]).strip()))
            else:
                output.write(", [[{}{}{}]]".format(str(c[i][0][0]).strip(), ", ", str(c[i][0][1]).strip()))
        output.seek(-1, os.SEEK_END)
        output.truncate()
        output.write("]])\n]")
        output.close()
        print("successfully saved")
        reload(db)
    except ValueError:
        print("failed to save")


# compares two contours for detection
def compare_numpy(x, y):

    sensitivity = 30

    for i in range(len(x)):
        point_close = False
        for t in range(len(y)):
            distance = np.linalg.norm(x[i] - y[t])
            if distance <= sensitivity:
                point_close = True

        if not point_close:
            return False
    return True


run()  # disabled for travis
