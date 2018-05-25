import sys
sys.path.insert(0, '../../../src')

from elements.element5.helpers import Color
from elements.element5.helpers import check_valid_convex

import cv2

POSITIONS = []


def run():
    print("run element5")
    # Initialize camera
    cap = cv2.VideoCapture(0)

    # Initialize color ranges for detection
    color_range = [Color("beker", [30, 10, 93], [83, 87, 175])]

    while True:
        # Read frame from the camera
        ret, img = cap.read()

        # Apply gaussian blue to the image
        img = cv2.GaussianBlur(img, (9, 9), 0)

        # calculate the masks
        mask = calculate_mask(img, color_range)

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
            # append_to_positions(Block(color, (cx, cy)))

    # Return the new mask
    return img_mask


if __name__ == '__main__':
    run()  # disabled for travis
