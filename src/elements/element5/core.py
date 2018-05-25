from elements.element7.helpers import Color
from elements.element7.helpers import Block
from elements.element7.helpers import SavedBuildings as db
from elements.element7.helpers import crop_to_contours, \
                                      check_valid_convex, \
                                      is_duplicate

import cv2

POSITIONS = []


def run():
    print("run element5")
    # Initialize camera
    cap = cv2.VideoCapture(0)

    # Initialize color ranges for detection
    color_range = [Color("beker", [26, 0, 17], [69, 131, 190])]

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
        if check_valid_convex(c, 4, 5000):
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


if __name__ == '__main__':
    run()  # disabled for travis
