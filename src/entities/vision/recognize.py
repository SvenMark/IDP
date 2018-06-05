import time
import sys

sys.path.insert(0, '../../../src')

from entities.vision.helpers.vision_helper import *


class Recognize(object):

    def __init__(self, color_range, min_block_size, saved_buildings=None):
        self.color_range = color_range
        self.positions = []
        self.saved_buildings = saved_buildings
        self.helper = Helper()
        self.min_block_size = min_block_size

    def run(self):
        # Initialize camera
        cap = cv2.VideoCapture(0)

        while True:
            # Read frame from the camera
            ret, img = cap.read()

            # Apply gaussian blue to the image
            img = cv2.GaussianBlur(img, (9, 9), 0)

            # Calculate the masks
            mask, dead_memes = self.helper.calculate_mask(img, self.color_range, self.min_block_size)

            img = self.helper.crop_to_contours(mask, img)

            # Calculate new cropped masks
            mask_cropped, valid_contours = self.helper.calculate_mask(img, self.color_range, self.min_block_size, set_contour=True)

            # Append the valid contours to the positions array
            for cnt in range(len(valid_contours)):
                self.positions = self.helper.append_to_positions(self.positions, valid_contours[cnt])

            # Recognize building
            if self.saved_buildings:
                self.recognize_building(self.positions)

            # Show the created image
            cv2.imshow('Spider Cam 3000', mask_cropped)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def recognize_building(self, positions):
        """
        Checks if the currents positions of the blocks matches any saved building
        :param positions: Current reading of POSITIONS
        :return: True if a building is recognized
        """
        result = []

        # If there are no blocks in view return false
        if not len(positions) > 0:
            return False

        # For each building in the saved building list
        for building in range(len(self.saved_buildings)):
            b = self.saved_buildings[building]
            # For each block on the front side of the saved building
            for block in range(len(b)):
                bl = b[block]
                result = [building, "front"]
                # If the current block color and position does not match a saved position,
                # break and check the next side.
                if not self.helper.is_duplicate(bl, positions, 20):
                    return False

        # Use audio to state the recognized building
        print("At time: " + time.ctime() + " Found: ", result[0], result[1])

        # Return whether a building has been found
        return True
