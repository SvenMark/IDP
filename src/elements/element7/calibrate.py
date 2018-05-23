from elements.element7.helpers import Color
from elements.element7.helpers import Block
from elements.element7.helpers import ColorRange
from elements.element7.helpers import SavedBuildings as db
from elements.element7.core import is_duplicate

import numpy as np
import cv2

# print("uncomment run before starting..")

POSITIONS = []
CALIBRATED = False
STOP_POSITIONS = False


def run():
    print("run element7")
    cap = cv2.VideoCapture(0)

    while True:
        ret, img = cap.read()
        img = cv2.GaussianBlur(img, (9, 9), 0)

        # initialize color ranges for detection
        color_range = [Color("orange", [0, 100, 126], [10, 255, 204]),
                       Color("yellow", [10, 100, 100], [30, 255, 255]),
                       Color("red", [170, 100, 100], [190, 255, 255]),
                       Color("green", [60, 100, 50], [90, 255, 255]),
                       Color("blue", [33, 213, 42], [110, 255, 255])]

        if not CALIBRATED and len(POSITIONS) > 0:
            print("calibrting")
            color_range[0] = calibrate(POSITIONS, 10)

        # calculate the masks
        mask = calculate_mask(img, color_range)
        cv2.rectangle(mask, (230, 65), (400, 420), (255, 255, 255), 3)

        cv2.imshow('camservice', mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def calibrate(positions, sensitivity=50):
    c = ([0, 100, 126], [10, 255, 204])
    color = "orange"
    lower = c[0]
    upper = c[1]

    lower[0] = 0
    upper[0] = 10
    while upper[0] < 255:  # while the color value is not higher than 255
        if not calibrate_color(positions, sensitivity, color):
            # try with other color range
            lower[0] += 10
            upper[0] += 10
        else:
            print(lower, upper, color)
            return Color(color, lower, upper)

    return Color(Color, [50, 100, 126], [10, 255, 204])
    # new_range = list()
    # for i in range(len(color_range)):  # for each color range available
    #     c = color_range[i]
    #     c.lower[0] = 0
    #     c.upper[0] = 20
    #     while c.upper[0] < 255:  # while the color value is not higher than 255
    #         if not calibrate_color(POSITIONS, sensitivity, c.color):
    #             # try with other color range
    #             c.lower[0] += 10
    #             c.upper[0] += 10
    #         else:  # calibrated color
    #             new_range.append(Color(c.color, c.lower, c.upper))
    #         print(c.color, (c.lower, c.upper))
    #
    # return new_range


def calibrate_color(positions, sensitivity, color):
    for j in range(len(positions)):  # for each current position
        pos = positions[j]
        if pos.color == color:
            for k in range(len(db.calibrate_building)):  # and saved position
                saved_block = db.calibrate_building[k]
                if saved_block.color == pos.color:  # if the colors match
                    b = pos.centre
                    a = saved_block.centre

                    distance = np.linalg.norm(a - b)

                    if distance <= sensitivity:  # and the positions match
                        return True  # the color is calibrated

    return False


def calculate_mask(img, color_range, conversion=cv2.COLOR_BGR2HSV):
    hsv = cv2.cvtColor(img, conversion)

    masks = list()
    for i in range(len(color_range)):
        c = color_range[i]
        masks.append(ColorRange(c.color, cv2.inRange(hsv, c.lower, c.upper)))

    img_mask = set_contours(masks[0].range, masks[0].color, img)
    for i in range(1, len(masks)):
        img_mask += set_contours(masks[i].range, masks[i].color, img)

    return img_mask


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


run()  # disabled for travis
