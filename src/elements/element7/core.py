from collections import OrderedDict
from threading import Timer

from imutils.video import WebcamVideoStream
from elements.element7.helpers import Color
from elements.element7.helpers import Position
from elements.element7.helpers import ColorRange

import time
import positions as db
import numpy as np
import cv2
import os

# print("uncomment run before starting..")

POSITIONS = []
LAST_POS_LEN = 100
STOP_POSITIONS = False

# initialize color ranges for detection
orange = Color([0, 100, 100], [10, 255, 255])
yellow = Color([20, 100, 100], [30, 255, 255])
red = Color([170, 100, 100], [190, 255, 255])
green = Color([60, 100, 50], [90, 255, 255])
blue = Color([90, 100, 100], [120, 255, 255])


def run():
    print("run element7")
    cap = WebcamVideoStream(src=0).start()
    time.sleep(1)

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

        # calculate the masks
        mask = calculate_mask(img)

        # crop to the contours
        img = crop_to_contours(mask, img)

        # calculate new cropped masks
        mask_cropped = calculate_mask(img, set_contour=True)

        # draw_saved_positions(imgmask, colors)

        cv2.imshow('camservice', mask_cropped)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.stop()
    cv2.destroyAllWindows()


def calculate_mask(img, conversion=cv2.COLOR_BGR2HSV, set_contour=False):
    hsv = cv2.cvtColor(img, conversion)

    masks = [ColorRange("red", cv2.inRange(hsv, red.lower, red.upper)),
             ColorRange("blue", cv2.inRange(hsv, blue.lower, blue.upper)),
             ColorRange("green", cv2.inRange(hsv, green.lower, green.upper)),
             ColorRange("orange", cv2.inRange(hsv, orange.lower, orange.upper)),
             ColorRange("yellow", cv2.inRange(hsv, yellow.lower, yellow.upper))]

    if set_contour:
        img_mask = set_contours(masks[0].range, masks[0].color, img)
        for i in range(1, len(masks)):
            img_mask += set_contours(masks[i].range, masks[i].color, img)
    else:
        img_mask = masks[0].range
        for i in range(1, len(masks)):
            img_mask += masks[i].range
    return img_mask


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


def crop_to_contours(mask, img):
    ret, thresh = cv2.threshold(mask, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    extremes = [999999, -99999, 99999, -9999]  # min x, max x, min y, max y

    # draw all correct contours
    for i in range(len(contours)):
        c = cv2.convexHull(contours[i])
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        area = cv2.contourArea(c)

        if len(approx) == 4 and area > 4000:
            a = tuple(contours[i][contours[i][:, :, 0].argmin()][0])
            b = tuple(contours[i][contours[i][:, :, 0].argmax()][0])
            c = tuple(contours[i][contours[i][:, :, 1].argmin()][0])
            d = tuple(contours[i][contours[i][:, :, 1].argmax()][0])
            if a[0] < extremes[0]:
                extremes[0] = a[0]
            if b[0] > extremes[1]:
                extremes[1] = b[0]
            if c[1] < extremes[2]:
                extremes[2] = c[1]
            if d[1] > extremes[3]:
                extremes[3] = d[1]

    y = extremes[2]
    h = extremes[3] - y
    x = extremes[0]
    w = extremes[1] - x

    if y + h > 0 and x + w > 0:
        img = img[y:y + h, x:x + w]

    img = image_resize(img, height=400)
    return img


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


# sets contours for selected masks
def set_contours(mask, color, img):
    img_mask = cv2.bitwise_and(img, img, mask=mask)

    ret, thresh = cv2.threshold(mask, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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

            print STOP_POSITIONS
            if not STOP_POSITIONS:
                if not len(POSITIONS) > 0:
                    POSITIONS.append(Position(color, contours[i]))
                else:
                    for j in range(len(POSITIONS)):
                        if not compare_numpy(contours[i], POSITIONS[j].array):
                            POSITIONS.append(Position(color, contours[i]))
                            print("Found {}, color {}".format(len(POSITIONS), color))

    return img_mask


def routine():
    t = Timer(20, routine)
    t.start()

    global STOP_POSITIONS, LAST_POS_LEN
    if LAST_POS_LEN == len(POSITIONS):
        STOP_POSITIONS = True

        db.positions = []

        # save current positions to file
        for i in range(len(POSITIONS)):
            if not len(db.positions) > 0:
                save_contour(POSITIONS[i])
            elif not compare_numpy(POSITIONS[i], db.positions):
                save_contour(POSITIONS[i])

        # start recognizing building
        print("Looped timer..")
        recognize_building(POSITIONS)

    LAST_POS_LEN = len(POSITIONS)


def recognize_building(positions):
    # for i in range(len(positions)):
    #     print("POSITION: {}, {}, {}".format(i, positions[i].color, positions[i].array[0]))
    # print('\n')

    # check if you recognize position
    for building in range(len(db.buildings)):
        current_building = True
        for contour in range(len(db.buildings[building])):
            # print("BUILDING: {}, {}, {}".format(contour, db.buildings[building][contour].color,
            #                                     db.buildings[building][contour].array[0]))

            found_saved = False
            for saved_position in range(len(positions)):
                if db.buildings[building][contour].color == positions[saved_position].color \
                        and compare_numpy(positions[saved_position].array, db.buildings[building][contour].array):
                    found_saved = True

            current_building = found_saved
            if not current_building:
                break

        if current_building:
            print("{} detected position of building {}".format(time.ctime(), building))


# checks if contour is duplicate
def is_duplicate(x, y, sensitivity=50):
    if len(y) == 0:
        return False
    for i in range(len(y)):
        if abs(x[0][0][0] - y[i].array[0][0][0]) < sensitivity \
                and abs(x[0][0][1] - y[i].array[0][0][1]) < sensitivity:
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
        for i in range(len(db.positions)):
            print db.positions[i].array
        print("successfully saved")
    except ValueError:
        print("failed to save")


# compares two contours for detection
def compare_numpy(x, y, sensitivity=100):
    """
    Compares two numpy arrays.
    :param sensitivity: sensitivy of distance
    :param x: contours array
    :param y: contours array
    :return: true if duplicate array
    """

    for i in range(len(x)):
        point_close = False
        for t in range(len(y)):
            distance = np.linalg.norm(x[i] - y[t])  # x[i] = [520,137] y[430,180]
            if distance <= sensitivity:
                point_close = True

        if not point_close:
            return False
    return True


run()  # disabled for travis
