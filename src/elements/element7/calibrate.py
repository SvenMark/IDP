from collections import OrderedDict

from elements.element7.helpers import Color, \
                                      is_duplicate,\
                                      check_valid_convex, \
                                      Block, \
                                      SavedBuildings as db

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
                   Color("green", [21, 26, 0], [180, 136, 93]),
                   Color("blue", [36, 120, 105], [159, 255, 235])]

    colors = OrderedDict({
                "red": (0, 0, 255),
                "blue": (255, 0, 0),
                "green": (0, 255, 0),
                "orange": (0, 165, 255),
                "yellow": (0, 255, 255)})

    calibrated_colors = []

    last_upper = 0
    last_lower = 0

    while True:
        ret, img = cap.read()
        img = cv2.GaussianBlur(img, (9, 9), 0)

        for i in range(len(color_range)):
            c = color_range[i]
            if c.color not in calibrated_colors:
                if not calibrate_color(POSITIONS, 50, c.color):
                    if c.lower[0] < 255:
                        c.upper[0] += 10
                        c.lower[0] += 10
                    else:
                        c.upper[0] = 10
                        c.lower[0] = 0
                else:
                    print(c.upper, c.lower, c.color)
                    calibrated_colors.append(c.color)

        # calculate the masks
        mask = calculate_mask(img, color_range, set_contour=True)
        cv2.rectangle(mask, (230, 65), (400, 420), (255, 255, 255), 3)
        for i in range(len(db.calibrate_building)):
            cx = db.calibrate_building[i].centre[0]
            cy = db.calibrate_building[i].centre[1]
            cv2.circle(mask, (cx, cy), 2, colors.get(db.calibrate_building[i].color), 10)

        cv2.rectangle(img, (230, 65), (400, 420), (255, 255, 255), 3)
        for i in range(len(db.calibrate_building)):
            cx = db.calibrate_building[i].centre[0]
            cy = db.calibrate_building[i].centre[1]
            cv2.circle(img, (cx, cy), 2, colors.get(db.calibrate_building[i].color), 10)

        cv2.imshow('aa', mask)
        cv2.imshow('camservice', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def calculate_mask(img, color_range, conversion=cv2.COLOR_BGR2HSV, set_contour=False):
    """
    Calculates the mask with the given image
    :param img: The image to calculate the mask on
    :param color_range: Color range for the masks
    :param conversion: Conversion for the mask
    :param set_contour: Boolean to set the contours
    :return: The new mask
    """

    # Convert the image
    hsv = cv2.cvtColor(img, conversion)

    if set_contour:
        # Set contours for given image and color ranges
        img_mask = set_contours(cv2.inRange(hsv, color_range[0].lower, color_range[0].upper), color_range[0].color, img)
        for i in range(1, len(color_range)):
            img_mask += set_contours(cv2.inRange(hsv, color_range[i].lower, color_range[i].upper), color_range[i].color, img)
    else:
        # Calculate the mask for all color ranges
        img_mask = cv2.inRange(hsv, color_range[0].lower, color_range[0].upper)
        for i in range(1, len(color_range)):
            img_mask += cv2.inRange(hsv, color_range[i].lower, color_range[i].upper)

    # Return the new mask
    return img_mask


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


def set_contours(mask, color, img):
    """
    Sets contours for selected masks
    :param mask: The mask to apply on the image
    :param color: Color of the mask to give contours
    :param img: Current image
    :return: New image with the contours
    """

    # Calculates the per-element bit-wise conjunction of two arrays or an array and a scalar
    img_mask = cv2.bitwise_and(img, img, mask=mask)

    # Calculate the threshhold with the mask
    ret, thresh = cv2.threshold(mask, 127, 255, 0)

    # Find the contours with the threshold
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in range(len(contours)):
        # Create a convexhull of the contour
        c = cv2.convexHull(contours[contour])

        # Check if the contour is a vlid block
        if check_valid_convex(c):
            # Image moments help you to calculate some features like center of mass of the object
            moment = cv2.moments(c)

            # Calculate the centre of mass
            cx = int(moment['m10'] / moment['m00'])
            cy = int(moment['m01'] / moment['m00'])

            # Draw the convexhull for the block
            cv2.drawContours(img_mask, [c], 0, (255, 255, 255), 3)

            # Draw a circle in the centre of the block
            cv2.circle(img_mask, (cx, cy), 2, (255, 255, 255), 5)

            # Write the color and position of the block
            cv2.putText(img_mask, color, (cx - 15, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            cv2.putText(img_mask, str((cx, cy)), (cx - 30, cy + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

            # Append the new block to the global POSITIONS array
            append_to_positions(Block(color, (cx, cy)))

    # Return the new mask
    return img_mask


def append_to_positions(bl):
    """
    Appends a unique block to the global POSITIONS array
    :param bl: Block class
    """

    # Call to the global variable POSITIONS
    global POSITIONS

    # If the POSITIONS length is getting too long clear it
    if len(POSITIONS) > 10:
        del POSITIONS[:]
    # If the POSITIONS array is empty append the block
    if len(POSITIONS) == 0:
        POSITIONS.append(bl)
    else:
        # Check if the given block is not a duplicate
        if not is_duplicate(bl.centre, POSITIONS, 5):
            # Append the block to positions
            POSITIONS.append(bl)


if __name__ == '__main__':
    run()  # disabled for travis
