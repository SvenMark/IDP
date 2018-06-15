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
        result = []
        found = True

        # If there are no blocks in view return false
        if not len(positions) > 0:
            return False

        # For each building in the saved building list
        for building in self.saved_buildings:
            # For each block on the front side of the saved building
            found = self.check_building_side(positions, building.side)
            result = [building.number, building.side_number, building.pick_up_vertical]
            if found:
                break

        # If recent settings are handled
        self.check_settings(building_center, image_width, building_width, result)

        if found:
            # Use audio to state the recognized building
            print("[INFO] At time: " + str(datetime.datetime.now().time()) + " Found: ", result[0], result[1])
            self.recognized = True

        # Return whether a building has been found
        return found

    def check_building_side(self, positions, side):
        for block in side:
            if not self.helper.is_duplicate(block, positions, 20):
                return False

        return True

    def check_settings(self, building_center, image_width, building_width, result):
        # Calculate and check percentage left
        print("---------------")
        calculation = building_center / image_width * 100
        percentage_position = calculation if calculation < 100 else self.last_percentage
        self.last_percentage = percentage_position
        # Set min block size according to the distance of the building
        print("[INFO] building width:", building_width)
        if 250 > building_width > 130:
            self.helper.min_block_size = 300
        else:
            self.helper.min_block_size = 0
        print("[INFO] min blok sies:", self.helper.min_block_size)

        # If all requirements are valid, grab that ho
        if self.recognized and 51 > percentage_position > 49 and building_width > 183:
            print("[WOO] building with:grab that ho by the vertical way:", result[2])
        else:
            print("[INFO] percentage left:", percentage_position)

        # Add to settings
        self.settings.current_building = result[0]
        self.settings.current_side = result[1]
        self.settings.current_position = percentage_position

        self.settings.new = True

        # Notify settings that the current frame is handled
        self.settings.update = True

    def nothing(self, x):
        pass
