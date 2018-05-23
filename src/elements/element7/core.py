from collections import OrderedDict
from threading import Timer

from elements.element7.helpers import Color
from elements.element7.helpers import Block
from elements.element7.helpers import ColorRange
from elements.element7.helpers import SavedBuildings as db
from entities.audio.speak import Speak

import numpy as np
import cv2

# print("uncomment run before starting..")

POSITIONS = []
LAST_POS_LEN = 100
STOP_POSITIONS = False

# initialize color ranges for detection
color_range = [Color("orange", [0, 100, 126], [10, 255, 204], 0),
               Color("yellow", [10, 100, 100], [30, 255, 255], 10),
               Color("red", [170, 100, 100], [190, 255, 255], 170),
               Color("green", [60, 100, 50], [90, 255, 255], 60),
               Color("blue", [33, 213, 42], [110, 255, 255], 90)]


def run():
    print("run element7")
    cap = cv2.VideoCapture(0)

    colors = OrderedDict({
        "red": (0, 0, 255),
        "blue": (255, 0, 0),
        "green": (0, 255, 0),
        "orange": (0, 165, 255),
        "yellow": (0, 255, 255)})

    while True:
        ret, img = cap.read()
        img = cv2.GaussianBlur(img, (9, 9), 0)

        # calculate the masks
        mask = calculate_mask(img)

        img = crop_to_contours(mask, img)

        # calculate new cropped masks
        mask_cropped = calculate_mask(img, set_contour=True)

        cv2.imshow('camservice', mask_cropped)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def calculate_mask(img, conversion=cv2.COLOR_BGR2HSV, set_contour=False):
    hsv = cv2.cvtColor(img, conversion)

    masks = list()
    for i in range(len(color_range)):
        c = color_range[i]
        masks.append(ColorRange(c.color, cv2.inRange(hsv, c.lower, c.upper)))

    if set_contour:
        img_mask = set_contours(masks[0].range, masks[0].color, img)
        for i in range(1, len(masks)):
            img_mask += set_contours(masks[i].range, masks[i].color, img)
    else:
        img_mask = masks[0].range
        for i in range(1, len(masks)):
            img_mask += masks[i].range
    return img_mask


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
            cv2.circle(img_mask, (cx, cy), 2, (255, 255, 255), 5)

            global LAST_POS_LEN

            if not STOP_POSITIONS:
                if len(POSITIONS) > 10:
                    print("Cleared POSITIONS of length ", len(POSITIONS))
                    del POSITIONS[:]
                if len(POSITIONS) == 0:
                    POSITIONS.append(Block(color, (cx, cy)))
                    print("Block(\"{}\", {}),".format(color, (cx, cy)))
                else:
                    if len(POSITIONS) > 0:
                        for j in range(len(POSITIONS)):
                            if not is_duplicate((cx, cy), POSITIONS, 5):
                                POSITIONS.append(Block(color, (cx, cy)))
                                print("Block(\"{}\", {}),".format(color, (cx, cy)))

    return img_mask


def routine():
    t = Timer(2, routine)
    t.start()

    global STOP_POSITIONS, LAST_POS_LEN
    if LAST_POS_LEN == len(POSITIONS):

        # save current positions to file
        # db.save_contour(POSITIONS)

        # start recognizing building
        print("Looped timer..")

        recognize_building(POSITIONS)
        del POSITIONS[:]

        LAST_POS_LEN = 100

    LAST_POS_LEN = len(POSITIONS)


def recognize_building(positions):
    # check if you recognize position
    result = []
    found = True
    if not len(positions) > 0:
        return False
    for building in range(len(db.buildings)):
        b = db.buildings[building]
        for block_front in range(len(b.front)):
            bl = b.front[block_front]
            result = [building, "front"]
            if not is_duplicate(bl.centre, positions, 20, bl.color):
                return False

        # if not found:
        #     for block_back in range(len(b.back)):
        #         bl = b.front[block_back]
        #         result = [building, "back"]
        #         if not is_duplicate(bl.centre, positions, 10, bl.color):
        #             found = False

        # if not found:
        #             for block_back in range(len(b.back)):
        #                 bl = b.front[block_back]
        #                 result = [building, "back"]
        #                 if not is_duplicate(bl.centre, positions, 10, bl.color):
        #                     found = False
        # if not found:
        #             for block_back in range(len(b.back)):
        #                 bl = b.front[block_back]
        #                 result = [building, "back"]
        #                 if not is_duplicate(bl.centre, positions, 10, bl.color):
        #                     found = False

    tts = "Recognized building {}, {} side".format(result[0], result[1])
    Speak.tts(Speak(), tts)
    return True


# checks if contour is duplicate
def is_duplicate(x, y, sensitivity=10, color=None):
    for i in range(len(y)):
        b = y[i].centre
        a = x

        distance = np.linalg.norm(a - b)  # x[i] = [520,137] y[t] = [430,180]

        if color and color == y[i].color and distance <= sensitivity:
            return True
        elif not color and distance <= sensitivity:
            return True

    return False


routine()
run()  # disabled for travis
