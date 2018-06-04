import numpy as np
import cv2


class Color:
    def __init__(self, color, lower, upper):
        self.color = color
        self.lower = np.array(lower)
        self.upper = np.array(upper)


class Block:
    def __init__(self, color, centre):
        self.color = color
        self.centre = np.array(centre)


class ColorRange:
    def __init__(self, color, color_range):
        self.color = color
        self.range = color_range


class Helpers:

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
            distance = np.linalg.norm(a-b)

            # Check the distance between the blocks
            if distance <= sensitivity:
                return True

        return False

    @staticmethod
    def check_valid_convex(c, sides, area_min, area_max):
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
        return len(approx) == sides and area_max > area > area_min

    def crop_to_contours(self, mask, img):
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
            if self.check_valid_convex(c, 4, 1000, 10000):
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
        img = self.image_resize(img, height=400)

        # Return the resized image
        return img

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

    def append_to_positions(self, positions, block):
        """
        Appends a unique block to the array
        :param positions: Positions array of the current view
        :param block: Centre point
        """

        # If the POSITIONS length is getting too long clear it
        if len(positions) >= 6:
            del positions[:]
        # If the POSITIONS array is empty append the block
        if len(positions) == 0:
            positions.append(block)
        else:
            # Check if the given block is not a duplicate
            if not self.is_duplicate(block, positions, 5):
                # Append the block to positions
                positions.append(block)

        return positions


