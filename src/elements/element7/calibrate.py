from elements.element7.helpers import Color
from elements.element7.helpers import Block
from elements.element7.helpers import ColorRange
from elements.element7.helpers import SavedBuildings as db
from elements.element7.core import calculate_mask

import numpy as np
import cv2

# print("uncomment run before starting..")

POSITIONS = []
CALIBRATED = False
STOP_POSITIONS = False


def run():
    print("run element7")
    cap = cv2.VideoCapture(0)

    # initialize color ranges for detection
    color_range = [Color("orange", [0, 100, 126], [10, 255, 204]),
                   Color("yellow", [100, 100, 100], [30, 255, 255]),
                   Color("red", [170, 100, 100], [190, 255, 255]),
                   Color("green", [60, 100, 50], [90, 255, 255]),
                   Color("blue", [33, 213, 42], [110, 255, 255])]

    while True:
        ret, img = cap.read()
        img = cv2.GaussianBlur(img, (9, 9), 0)

        if not CALIBRATED and len(POSITIONS) > 0:
            color_range[0] = calibrate(POSITIONS, 30)

        # calculate the masks
        mask = calculate_mask(img, color_range)

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
            global CALIBRATED
            CALIBRATED = True
            return Color(color, lower, upper)

    return Color(Color, [50, 100, 126], [10, 255, 204])


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


if __name__ == '__main__':
    run()  # disabled for travis
