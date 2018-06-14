import numpy as np
import cv2
from imutils.video import VideoStream
from enum import Enum


class Color:
    def __init__(self, color, lower, upper):
        self.color = color
        self.lower = np.array(lower)
        self.upper = np.array(upper)


class Side(Enum):
    front = 0
    left = 1
    right = 2
    back = 3


class Building:
    def __init__(self, front=(0, 0), back=(0, 0), left=(0, 0), right=(0, 0), pick_up_vertical=False, number=0):
        self.front = front
        self.back = back
        self.left = left
        self.right = right
        self.pick_up_vertical = pick_up_vertical
        self.number = number


class Block:
    def __init__(self, color, centre):
        self.color = color
        self.centre = np.array(centre)


class ColorRange:
    def __init__(self, color, color_range):
        self.color = color
        self.range = color_range


class Helper:

    def __init__(self, min_block_size, max_block_size):
        self.min_block_size = min_block_size
        self.max_block_size = max_block_size

    def nothing(self, x):
        pass

    @staticmethod
    def is_duplicate(centre, positions, sensitivity=10):
        """
        Compares a centre points to an array with currently visible center points
        :param centre: Centre point to check
        :param positions: Array with blocks
        :param sensitivity: Sensitivity to check with, higher sensitivity allows more distance
        :return: True if array 'y' contains the centre point
        """

        for block in range(len(positions)):
            # Calculate distance between the centre points
            a = np.array(centre)
            b = np.array(positions[block])
            distance = np.linalg.norm(a - b)

            # Check the distance between the blocks
            if distance <= sensitivity:
                return True

        return False

    def check_valid_convex(self, c, sides):
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
        return area > self.min_block_size

    def crop_to_contours(self, mask, img):
        """
        Crops to the contours of the given mask
        :param mask: The mask to crop to
        :param img: The image to crop
        :return: The cropped image
        """

        height, image_width, channels = img.shape

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
            if self.check_valid_convex(c, 4):
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

        center = (x + extremes[1]) / 2

        print("[INFO] Percentage left: " + str(center / image_width * 100))

        # Resize to new size
        img = self.image_resize(img, height=400)

        # Return the resized image
        return img, center

    @staticmethod
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

    def calculate_mask(self, img, color_range, conversion=cv2.COLOR_BGR2HSV, set_contour=False):
        """
        Calculates the mask with the given image
        :param img: The image to calculate the mask on
        :param color_range: Color range for the masks
        :param conversion: Conversion for the mask
        :param set_contour: Boolean to set the contours
        :return: The new mask
        """

        valid_contour = []

        # Convert the image
        hsv = cv2.cvtColor(img, conversion)

        if set_contour:
            img_mask, valid_cntr = self.set_contours(cv2.inRange(hsv, color_range[0].lower, color_range[0].upper),
                                                     color_range[0].color, img)
            valid_contour += valid_cntr
            for i in range(1, len(color_range)):
                mask, valid_cntr = self.set_contours(cv2.inRange(hsv, color_range[i].lower, color_range[i].upper),
                                                     color_range[i].color, img)
                valid_contour += valid_cntr
                img_mask += mask
        else:
            img_mask = cv2.inRange(hsv, color_range[0].lower, color_range[0].upper)
            # Calculate the mask for all color ranges
            for i in range(1, len(color_range)):
                img_mask += cv2.inRange(hsv, color_range[i].lower, color_range[i].upper)

        # Return the new mask
        return img_mask, valid_contour

    def set_contours(self, mask, color, img):
        """
        Sets contours for selected masks
        :param mask: The mask to apply on the image
        :param color: Color of the mask to give contours
        :param img: Current image
        :return: New image with the contours
        """

        # Initialize valid contours for adding to the positions array
        valid_contours = []

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
            if self.check_valid_convex(c, 4):
                # Image moments help you to calculate some features like center of mass of the object
                moment = cv2.moments(c)
                area = cv2.contourArea(c)

                x, y, w, h = cv2.boundingRect(c)
                # Calculate the centre of mass
                cx = int(moment['m10'] / moment['m00'])
                cy = int(moment['m01'] / moment['m00'])

                # Draw the convexhull for the block
                cv2.drawContours(img_mask, [c], 0, (255, 255, 255), 3)

                # Draw a circle in the centre of the block
                cv2.circle(img_mask, (cx, cy), 2, (255, 255, 255), 5)

                block_position = "bottom/top"
                if w > 100:
                    block_position = "laying"
                elif h > 100:
                    block_position = "standing"

                # Write the color and position of the block
                cv2.putText(img_mask, color, (cx - 15, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                cv2.putText(img_mask, str((cx, cy)), (cx - 30, cy + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255),
                            1)
                cv2.putText(img_mask, block_position, (cx - 30, cy + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                            (255, 255, 255), 1)
                cv2.putText(img_mask, str(area), (cx - 30, cy + 45), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

                # Append the new block to the global POSITIONS array
                valid_contours.append((cx, cy))

        # Return the new mask
        return img_mask, valid_contours
