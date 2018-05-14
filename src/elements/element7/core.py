import random
from collections import OrderedDict
import time
import positions
from helpers import Color
import numpy as np
import cv2
import os

print ("uncomment run before starting..")


def run():
    print("run element7")
    url = "http://169.254.104.108:8090"
    cap = cv2.VideoCapture(0)
    time.sleep(1)

    orange = Color([0, 100, 100], [10, 255, 255])
    yellow = Color([20, 100, 100], [30, 255, 255])
    red = Color([170, 100, 100], [190, 255, 255])
    green = Color([60, 100, 50], [90, 255, 255])
    blue = Color([90, 100, 100], [120, 255, 255])

    while True:
        ret, img = cap.read()
        img = cv2.GaussianBlur(img, (9, 9), 0)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        masks = OrderedDict({
            "red": cv2.inRange(hsv, red.lower, red.upper),
            "blue": cv2.inRange(hsv, blue.lower, blue.upper),
            "green": cv2.inRange(hsv, green.lower, green.upper),
            "orange": cv2.inRange(hsv, orange.lower, orange.upper),
            "yellow": cv2.inRange(hsv, yellow.lower, yellow.upper)})

        colors = OrderedDict({
            "red": (0, 0, 255),
            "blue": (255, 0, 0),
            "green": (0, 255, 0),
            "orange": (0, 165, 255),
            "yellow": (0, 255, 255)})

        imgmask = setcontours(masks.get("red"), "red", img)
        for col, mask in masks.items():
            if col == "red":
                continue
            imgmask += setcontours(mask, col, img)

        for i in range(len(positions.positions)):
            cnt = np.array(positions.positions[i].array)
            color = positions.positions[i].color
            c = cv2.convexHull(cnt)
            M = cv2.moments(c)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            text = "{} {}".format("Color", color)
            cv2.drawContours(imgmask, [c], 0, colors.get(color), 3, -1)
            cv2.putText(imgmask, text, (cx - 25, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        cv2.imshow('camservice', imgmask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def setcontours(mask, color, img):

    imgmask = cv2.bitwise_and(img, img, mask=mask)

    ret, thresh = cv2.threshold(mask, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contours)):
        c = cv2.convexHull(contours[i])
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)
        area = cv2.contourArea(c)
        if len(approx) == 4 and area > 4000:
            M = cv2.moments(c)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.drawContours(imgmask, [c], 0, (255, 255, 255), 3)
            text = "{} {}".format("Color:", color)
            cv2.putText(imgmask, text, (cx - 25, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

            for j in range(len(positions.positions)):
                if comparenumpy(c, positions.positions[j].array):
                    print "detected position"

            if len(c) > 0 and cv2.waitKey(1) & 0xFF == ord('s'):
                savecontour(c, color)
                time.sleep(0.1)

    return imgmask


def savecontour(c, color):
    try:
        filename = "positions.py"
        filelen = file_len(filename)
        output = open(filename, "a")
        output.seek(-1, os.SEEK_END)
        output.truncate()
        output.write(", Position(\"" + color + "\", [")
        for i in range(len(c)):
            if i == 0:
                output.write("[[{}{}{}]]".format(str(c[i][0][0]).strip(), ", ", str(c[i][0][1]).strip()))
            else:
                output.write(", [[{}{}{}]]".format(str(c[i][0][0]).strip(), ", ", str(c[i][0][1]).strip()))
        output.seek(-1, os.SEEK_END)
        output.truncate()
        output.write("]])\n]")
        output.close()
        print("succesfully saved")
        # reload(positions)
    except ValueError:
        print("failed to save")


def file_len(filename):
    return sum(1 for line in open(filename))


def comparenumpy(x, y):
    sensitivity = 100
    result = True

    for i in range(len(x)):
        if i == len(x) or i == len(y):
            return False
        else:
            # 500 = 400 - 600.. 400: 500 - 100 >= 400 or 500 + 100 <= 600
            if x[i][0][0] - sensitivity >= y[i][0][0] \
                    or x[i][0][0] + sensitivity <= y[i][0][0] \
                    or x[i][0][1] - sensitivity >= y[i][0][1] \
                    or x[i][0][1] + sensitivity <= y[i][0][1]:
                return False

    return True


run()  # disabled for travis
