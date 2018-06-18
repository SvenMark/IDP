import sys

from imutils.video import VideoStream

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
        self.recognized = False
        self.last_percentage = 50
        self.start_recognize = False

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
            mask, _ = self.helper.calculate_mask(img, self.color_range)

            img_crop, building_center, image_width, building_width = self.helper.crop_to_contours(mask, img)

            # Calculate new cropped masks
            mask_cropped, valid_contours = self.helper.calculate_mask(img_crop, self.color_range, set_contour=True)

            # Recognize building
            if self.saved_buildings:
                self.recognize_building(valid_contours, image_width, building_center, building_width)

            # Show the created image
            cv2.imshow('Spider Cam 3000', mask_cropped)
            cv2.imshow('Spider Cam 2000', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.stop()
        cv2.destroyAllWindows()

    def recognize_building(self, positions, image_width, building_center, building_width):
        """
        Checks if the currents positions of the blocks matches any saved building
        :param building_width: Width of the building
        :param building_center: Center of the building
        :param image_width: Width of the current image
        :param positions: Current reading of POSITIONS
        :return: True if a building is recognized
        """
        result = None
        found = True

        # If there are no blocks in view return false
        if not len(positions) > 0:
            return False

        if self.start_recognize:
            # For each building in the saved building list
            for building in self.saved_buildings:
                # For each block on the front side of the saved building
                found = self.check_building_side(positions, building.side)
                if found:
                    result = building
                    break

        # If recent settings are handled
        self.check_settings(building_center, image_width, building_width, result)

        if found:
            # Use audio to state the recognized building
            print("[INFO] At time: " + str(datetime.datetime.now().time()) + " Found: ", result)
            self.recognized = True

        # Return whether a building has been found
        return found

    def check_building_side(self, positions, side):
        for block in side:
            if not self.helper.is_duplicate(block, positions, 20):
                return False

        return True

    def check_settings(self, building_center, image_width, building_width, building):
        # Calculate and check percentage left
        calculation = building_center / image_width * 100
        percentage_position = calculation if calculation < 100 else self.last_percentage
        self.last_percentage = percentage_position

        # Set min block size according to the distance of the building
        if 250 > building_width > 130:
            # Start recognizing
            self.helper.min_block_size = 300
            self.start_recognize = True
        else:
            self.helper.min_block_size = 0

        # If all requirements are valid, grab
        if self.recognized and 51 > percentage_position > 49 and building_width > 183:
            grab = True
        else:
            grab = False

        if self.recognized and building:
            # Add to settings
            self.settings.pick_up_vertical = building.pick_up_vertical
            self.settings.current_position = percentage_position
            self.settings.grab = grab

            self.settings.new = True

            # Notify settings that the current frame is handled
            self.settings.update = True

    @staticmethod
    def get_real_distance(building_width):
        distance = -0.0006027224509476651 * building_width ** 2 - 0.227689996661844 * building_width + 53.74910055265013
        return distance
