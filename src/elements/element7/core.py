from elements.element7.helpers import Color
from elements.element7.helpers import Block
from elements.element7.helpers import SavedBuildings as db
from entities.audio.speak import Speak

import numpy as np
import cv2

POSITIONS = []


def run():
    print("run element7")
    # Initialize camera
    cap = cv2.VideoCapture(0)

    # Initialize color ranges for detection
    color_range = [Color("orange", [0, 98, 105], [12, 255, 255]),
                   Color("yellow", [25, 100, 100], [36, 255, 255]),
                   Color("red", [0, 93, 98], [4, 250, 255]),
                   Color("green", [60, 58, 26], [95, 210, 101]),
                   Color("blue", [90, 100, 100], [120, 255, 255])]

    while True:
        # Read frame from the camera
        ret, img = cap.read()

        # Apply gaussian blue to the image
        img = cv2.GaussianBlur(img, (9, 9), 0)

        # calculate the masks
        mask = calculate_mask(img, color_range)

        img = crop_to_contours(mask, img)

        # calculate new cropped masks
        mask_cropped = calculate_mask(img, color_range, set_contour=True)

        # Show the created image
        cv2.imshow('camservice', mask_cropped)

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


def crop_to_contours(mask, img):
    """
    Crops to the contours of the given mask
    :param mask: The mask to crop to
    :param img: The image to crop
    :return: The cropped image
    """

    # Create the threshold for the mask
    ret, thresh = cv2.threshold(mask, 127, 255, 0)

    # Find the contours for the threshold
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Define the extreme points
    extremes = [999999, -99999, 99999, -9999]  # min x, max x, min y, max y

    for contour in range(len(contours)):
        cnt = contours[contour]

        # Get convexhull of the contour
        c = cv2.convexHull(cnt)

        # Check if the convex is a valid block
        if check_valid_convex(c):
            # Calculate extremes of the hull
            min_x = tuple(cnt[cnt[:, :, 0].argmin()][0])
            max_x = tuple(cnt[cnt[:, :, 0].argmax()][0])
            min_y = tuple(cnt[cnt[:, :, 1].argmin()][0])
            max_y = tuple(cnt[cnt[:, :, 1].argmax()][0])

            # Compare with last extremes
            if min_x[0] < extremes[0]:
                extremes[0] = min_x[0]
            if max_x[0] > extremes[1]:
                extremes[1] = max_x[0]
            if min_y[1] < extremes[2]:
                extremes[2] = min_y[1]
            if max_y[1] > extremes[3]:
                extremes[3] = max_y[1]

    # Calculate width and height
    y = extremes[2]
    h = extremes[3] - y
    x = extremes[0]
    w = extremes[1] - x

    # Set new size
    if y + h > 0 and x + w > 0:
        img = img[y:y + h, x:x + w]

    # Resize to new size
    img = image_resize(img, height=400)

    # Return the resized image
    return img


def check_valid_convex(c):
    """
    Checks if a convex is a valid block
    :return: True if the contour is a block
    """

    # Calculate the perimeter
    peri = cv2.arcLength(c, True)

    # Calculate the sides of the convexhull, 4 is a square/rectangle, 3 is a triangle etc.
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    # Calculate the area of the convexhull
    area = cv2.contourArea(c)

    # If the convexhull counts 4 sides and an area bigger than 4000
    return len(approx) == 4 and area > 4000


def image_resize(img, width=None, height=None, inter=cv2.INTER_AREA):
    """
    Resize the image to given size
    :param img: Current image
    :param width: The width to resize to
    :param height: The height to resize to
    :param inter: Resampling method using pixel area relation
    :return: The resized image
    """
    # Initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = img.shape[:2]

    # If both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return img

    # Check to see if the width is None
    if width is None:
        # Calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # Otherwise, the height is None
    else:
        # Calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # Resize the image
    resized = cv2.resize(img, dim, interpolation=inter)

    # Return the resized image
    return resized


def set_contours(mask, color, img):
    """
    Sets contours for selected masks
    :param mask: The mask to apply on the img
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
            if len(POSITIONS) > 5:
                # If there are 5 blocks in POSITIONS (in camera view) try to recognize a building
                recognize_building(POSITIONS)


def recognize_building(positions):
    """
    Checks if the currents positions of the blocks matches any saved building
    :param positions: Current reading of POSITIONS
    :return: True if a building is recognized
    """
    result = []
    found = True

    # If there are no blocks in view return false
    if not len(positions) > 0:
        return False

    # For each building in the saved building list
    for building in range(len(db.buildings)):
        b = db.buildings[building]
        # For each block on the front side of the saved building
        for block_front in range(len(b.front)):
            bl = b.front[block_front]
            result = [building, "front"]
            # If the current block color and position does not match a saved position,
            # break and check the next side.
            if not is_duplicate(bl.centre, positions, 20, bl.color):
                found = False
                break

        # Back side
        if not found:
            for block_back in range(len(b.back)):
                bl = b.front[block_back]
                result = [building, "back"]
                if not is_duplicate(bl.centre, positions, 10, bl.color):
                    found = False
                    break

        # Left side
        if not found:
            for block_back in range(len(b.left)):
                bl = b.front[block_back]
                result = [building, "back"]
                if not is_duplicate(bl.centre, positions, 10, bl.color):
                    found = False
                    break

        # Right side
        if not found:
            for block_back in range(len(b.right)):
                bl = b.front[block_back]
                result = [building, "back"]
                if not is_duplicate(bl.centre, positions, 10, bl.color):
                    found = False
                    break

    # Use audio to state the recognized building
    if found:
        # tts = "Recognized building {}, {} side".format(result[0], result[1])
        # Speak.tts(Speak(), tts)
        print("fakka ik heb je gevonden homo ", result[0], result[1])

    # Return whether a building has been found
    return found


def is_duplicate(centre, positions, sensitivity=10, color=None):
    """
    Compares a centre points to an array with currently visible center points
    :param centre: Centre point to check
    :param positions: Array with blocks
    :param sensitivity: Sensitivity to check with, higher sensitivity allows more distance
    :param color: The color to compare, leave empty for no color
    :return: True if array 'y' contains the centre point
    """

    for block in range(len(positions)):
        # Calculate distance between the centre points
        distance = np.linalg.norm(centre - positions[block].centre)  # x[i] = [520,137] y[t] = [430,180]

        # If there is a given color, check those and
        # the distance between the blocks
        if color and color == positions[block].color and distance <= sensitivity:
            return True
        elif not color and distance <= sensitivity:
            return True

    return False


if __name__ == '__main__':
    run()  # disabled for travis
