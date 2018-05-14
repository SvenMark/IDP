import os
import time
from collections import OrderedDict

import cv2
import numpy as np

from elements.element7 import positions
from elements.element7.helpers import Color

print("uncomment run before starting..")


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

        imgmask = set_contours(masks.get("red"), "red", img)
        for col, mask in masks.items():
            if col == "red":
                continue
            imgmask += set_contours(mask, col, img)

        for i in range(len(positions.positions)):
            cv2.drawContours(imgmask, np.array(positions.positions[i]), 0, (0, 0, 255), 3)

        cv2.imshow('camservice', imgmask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def set_contours(mask, color, img):
    img_mask = cv2.bitwise_and(img, img, mask=mask)

    ret, thresh = cv2.threshold(mask, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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

            saved_contour = np.array([[[419, 264]],
                                      [[417, 286]],
                                      [[415, 307]],
                                      [[413, 311]],
                                      [[395, 311]],
                                      [[355, 308]],
                                      [[232, 298]],
                                      [[228, 297]],
                                      [[226, 295]],
                                      [[226, 274]],
                                      [[230, 237]],
                                      [[231, 236]],
                                      [[243, 235]],
                                      [[339, 243]],
                                      [[409, 250]],
                                      [[417, 251]],
                                      [[419, 252]]])

            # img_mask += cv2.drawContours(img_mask, [saved_contour], 0, (30, 255, 255), -1)
            # contour,

            if len(c) > 0 and len(c) == len(saved_contour) and compare_numpy(saved_contour, c):
                print("{}".format("detected position"))

            if len(c) > 0 and cv2.waitKey(1) & 0xFF == ord('s'):
                save_contour(c)
                time.sleep(1)

    return img_mask


def save_contour(c):
    try:
        filename = "positions.py"
        output = open(filename, "a")
        output.seek(-1, os.SEEK_END)
        output.truncate()
        output.write(",[")
        for i in range(len(c)):
            output.write("[[{} {} {}]],".format(str(c[i][0][0]).strip(), ",", str(c[i][0][1]).strip()))
        output.seek(-1, os.SEEK_END)
        output.truncate()
        output.write("]\n]")
        output.close()
        print("successfully saved")
    except ValueError:
        print("failed to save")


def file_len(filename):
    return sum(1 for line in open(filename))


def compare_numpy(x, y):
    for j in range(len(y)):
        for i in range(len(x)):
            # 500 = 400 - 600.. 400: 500 - 100 >= 400 or 500 + 100 <= 600
            sensitivity = 100
            if x[i][0][0] - sensitivity >= y[j][i][0][0] \
                    or x[i][0][0] + sensitivity <= y[j][i][0][0] \
                    or x[i][0][1] - sensitivity >= y[j][i][0][1] \
                    or x[i][0][1] + sensitivity <= y[j][i][0][1]:
                return False

    return True

# run()  # disabled for travis
