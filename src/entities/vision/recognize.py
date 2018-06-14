import sys
sys.path.insert(0, '../../../src')

import datetime
import time
from entities.vision.helpers.vision_helper import *


class Recognize(object):

    def __init__(self, helpers, color_range, saved_buildings=None, settings=None):
        self.color_range = color_range
        self.positions = []
        self.saved_buildings = saved_buildings
        self.helper = helpers.helper
        self.settings = settings
        self.recognize = True

    def run(self):
        print("[RUN] Starting recognize...")

        # Initialize camera
        cap = VideoStream(src=0, usePiCamera=True, resolution=(320, 240)).start()
        time.sleep(0.3)  # startup

        while True:
            # Read frame from the camera
            img = cap.read()

            # Apply gaussian blue to the image
            img = cv2.GaussianBlur(img, (9, 9), 0)

            # # Calculate the masks
            mask, dead_memes = self.helper.calculate_mask(img, self.color_range)

            image_width, image_height = img.shape[:2]
            img, center = self.helper.crop_to_contours(mask, img)

            # Calculate new cropped masks
            mask_cropped, valid_contours = self.helper.calculate_mask(img, self.color_range, set_contour=True)

            # Append the valid contours to the positions array
            # for cnt in range(len(valid_contours)):
            #     self.positions = self.helper.append_to_positions(self.positions, valid_contours[cnt])

            # Recognize building
            if self.saved_buildings and self.recognize:
                self.recognize_building(valid_contours, image_width, center)

            # Show the created image
            cv2.imshow('Spider Cam 3000', mask_cropped)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.stop()
        cv2.destroyAllWindows()

    def recognize_building(self, positions, image_width, center):
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
        for building in range(len(self.saved_buildings)):
            b = self.saved_buildings[building]

            # For each block on the front side of the saved building
            found = self.check_building_side(positions, b.front)
            result = [building, "front"]

            # For each block on the back side of the saved building
            if not found:
                found = self.check_building_side(positions, b.back)
                result = [building, "back"]
            
            # For each block on the left side of the saved building
            if not found:
                found = self.check_building_side(positions, b.left)
                result = [building, "left"]

            # For each block on the right side of the saved building
            if not found:
                found = self.check_building_side(positions, b.right)
                result = [building, "right"]

        # If recent settings are handled
        self.check_settings(center, image_width, result)

        if found:
            # Use audio to state the recognized building
            print("[INFO] At time: " + str(datetime.datetime.now().time()) + " Found: ", result[0], result[1])
            self.recognize = False

        # Return whether a building has been found
        return found

    @staticmethod
    def get_center(b):
        total = 0

        for block in range(len(b)):
            total += b[block][0]

        return total / len(b)

    def check_building_side(self, positions, side):
        print("--------{}-------".format(datetime.datetime.now().time()))
        for bl in positions:
            print(str(bl))
        print("----- vs -----", len(side))
        for block in side:
            print(str(block))
            if not self.helper.is_duplicate(block, positions, 20):
                return False

        return True

    def check_settings(self, center, image_width, result):
        if not self.settings.new:
            cx = center

            percentage_position = cx / image_width * 100

            # Add to settings
            self.settings.current_building = result[0]
            self.settings.current_side = result[1]
            self.settings.current_position = percentage_position

            self.settings.new = True

        # Notify settings that the current frame is handled
        self.settings.update = True

    def nothing(self, x):
        pass
