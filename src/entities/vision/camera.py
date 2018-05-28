from entities.vision.helpers import *
from entities.audio.speak import Speak


class Camera(object):

    def __init__(self, color_range):
        self.color_range = color_range
        self.positions = []
        self.saved_buildings = [
            Building(front=[Block("orange", (41, 324)),
                            Block("yellow", (33, 97)),
                            Block("red", (148, 92)),
                            Block("green", (153, 318)),
                            Block("blue", (92, 218))],
                     back=[Block("blue", (31, 316)),
                           Block("green", (86, 209)),
                           Block("orange", (30, 91)),
                           Block("yellow", (144, 317))],
                     left=[Block("red", (112, 175)),
                           Block("blue", (44, 304)),
                           Block("green", (36, 68)),
                           Block("orange", (184, 70)),
                           Block("yellow", (180, 307))],
                     right=[Block("red", (112, 175)),
                            Block("blue", (44, 304)),
                            Block("green", (36, 68)),
                            Block("orange", (184, 70)),
                            Block("yellow", (180, 307))]
                     )
        ]
        self.helper = Helpers()

    def run(self):
        # Initialize camera
        cap = cv2.VideoCapture(0)

        while True:
            # Read frame from the camera
            ret, img = cap.read()

            # Apply gaussian blue to the image
            img = cv2.GaussianBlur(img, (9, 9), 0)

            # Calculate the masks
            mask = self.calculate_mask(img, self.color_range)

            img = self.helper.crop_to_contours(mask, img)

            # Calculate new cropped masks
            mask_cropped = self.calculate_mask(img, self.color_range, set_contour=True)

            # Show the created image
            cv2.imshow('camservice', mask_cropped)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def calculate_mask(self, img, color_range, conversion=cv2.COLOR_BGR2HSV, set_contour=False):
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
            img_mask = self.set_contours(cv2.inRange(hsv, color_range[0].lower, color_range[0].upper), color_range[0].color, img)
            for i in range(1, len(color_range)):
                img_mask += self.set_contours(cv2.inRange(hsv, color_range[i].lower, color_range[i].upper), color_range[i].color, img)
        else:
            # Calculate the mask for all color ranges
            img_mask = cv2.inRange(hsv, color_range[0].lower, color_range[0].upper)
            for i in range(1, len(color_range)):
                img_mask += cv2.inRange(hsv, color_range[i].lower, color_range[i].upper)

        # Return the new mask
        return img_mask

    def set_contours(self, mask, color, img):
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
            if self.helper.check_valid_convex(c, 4, 4000, 10000):
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
                self.positions = self.helper.append_to_positions(self.positions, Block(color, (cx, cy)))

        # Return the new mask
        return img_mask

    def recognize_building(self, positions):
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
            for block_front in range(len(b.front)):
                bl = b.front[block_front]
                result = [building, "front"]
                # If the current block color and position does not match a saved position,
                # break and check the next side.
                if not self.helper.is_duplicate(bl.centre, positions, 20, bl.color):
                    found = False
                    break

            # Back side
            if not found:
                for block_back in range(len(b.back)):
                    bl = b.front[block_back]
                    result = [building, "back"]
                    if not self.helper.is_duplicate(bl.centre, positions, 10, bl.color):
                        found = False
                        break

            # Left side
            if not found:
                for block_back in range(len(b.left)):
                    bl = b.front[block_back]
                    result = [building, "back"]
                    if not self.helper.is_duplicate(bl.centre, positions, 10, bl.color):
                        found = False
                        break

            # Right side
            if not found:
                for block_back in range(len(b.right)):
                    bl = b.front[block_back]
                    result = [building, "back"]
                    if not self.helper.is_duplicate(bl.centre, positions, 10, bl.color):
                        found = False
                        break

        # Use audio to state the recognized building
        if found:
            # tts = "Recognized building {}, {} side".format(result[0], result[1])
            # Speak.tts(Speak(), tts)
            print("Hebbes ", result[0], result[1])

        # Return whether a building has been found
        return found
