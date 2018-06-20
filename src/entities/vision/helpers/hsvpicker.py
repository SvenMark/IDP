import time
import numpy as np
import cv2
from imutils.video import VideoStream


class Hsv_picker:
    def __init__(self, helpers, color_range):
        self.color_to_save = ""
        self.helper = helpers.helper
        self.color_range = color_range
        self.range_handler = helpers.json_handler
        self.helper.min_block_size = 300

    def run(self, img):
        print("[RUN] HSV picker")

        # Create a trackbar for each color range
        for color in range(len(self.color_range)):
            c = self.color_range[color]
            self.createtrackbars(c)

        # Create the camera stream
        cap = VideoStream(src=0, usePiCamera=True, resolution=(320, 240)).start()
        time.sleep(0.3)  # startup

        while True:
            # Check if there is a given image, else use the camera
            img = cap.read()
            img = cv2.flip(img, 0)

            # Apply gaussian blur
            img = cv2.GaussianBlur(img, (9, 9), 0)
                        
            # Hsv Mask
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, np.array([180, 255, 255]), np.array([180, 255, 255]))

            # Get the color from te trackbars
            for color in range(len(self.color_range)):
                c = self.color_range[color]
                on_off = cv2.getTrackbarPos('off_on', c.color)
                if on_off > 0:
                    lowh = cv2.getTrackbarPos('Low H', c.color)
                    lows = cv2.getTrackbarPos('Low S', c.color)
                    lowv = cv2.getTrackbarPos('Low V', c.color)

                    highh = cv2.getTrackbarPos('High H', c.color)
                    highs = cv2.getTrackbarPos('High S', c.color)
                    highv = cv2.getTrackbarPos('High V', c.color)

                    lower = np.array([lowh, lows, lowv])
                    higher = np.array([highh, highs, highv])
                    mask += cv2.inRange(hsv, lower, higher)

            # Apply the color ranges
            output = cv2.bitwise_and(img, img, mask=mask)

            # Get the contours
            ret, thresh = cv2.threshold(mask, 127, 255, 0)
            im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # Draw the valid contours and data
            for cnt in range(len(contours)):
                c = contours[cnt]
                moment = cv2.moments(c)
                area = cv2.contourArea(c)
                if area > self.helper.min_block_size:
                    cx = int(moment['m10'] / moment['m00'])
                    cy = int(moment['m01'] / moment['m00'])

                    # Draw a circle in the centre of the block
                    cv2.circle(output, (cx, cy), 2, (255, 255, 255), 5)

                    cv2.putText(output, str((cx, cy)), (cx - 30, cy + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                                (255, 255, 255), 1)
                    cv2.putText(output, str(area), (cx - 30, cy + 45), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255),
                                1)
                    cv2.drawContours(output, [c], -1, (255, 255, 255), 2)

            # Show the contours and the original image
            cv2.imshow('hsv-picker', output)
            cv2.imshow('original', img)

            if cv2.waitKey(1) & 0xFF == ord('s'):
                # Save the building when you press KEY s
                self.savehigherlower(self.color_range)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.stop()
        cv2.destroyAllWindows()

    @staticmethod
    def calculate_mask(name, mask, img):
        """
        Calculates mask with given ranges
        :param name: Form name to get the values from
        :param mask: Mask to apply to
        :param img: Image to apply mask to
        """
        # Get all trackbar values
        lowh = cv2.getTrackbarPos('Low H', name)
        lows = cv2.getTrackbarPos('Low S', name)
        lowv = cv2.getTrackbarPos('Low V', name)

        highh = cv2.getTrackbarPos('High H', name)
        highs = cv2.getTrackbarPos('High S', name)
        highv = cv2.getTrackbarPos('High V', name)

        # Hsv Mask
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([lowh, lows, lowv])
        higher = np.array([highh, highs, highv])
        mask += cv2.inRange(hsv, lower, higher)
        return mask

    def createtrackbars(self, c):
        """
        Create trackbar form
        :param c: Color to create trackbar for
        """
        name = c.color

        cv2.namedWindow(name)
        cv2.resizeWindow(name, 300, 300)

        nothing = self.helper.nothing

        # Create trackbars for lower
        cv2.createTrackbar('Low H', name, c.lower[0], 180, nothing)
        cv2.createTrackbar('Low S', name, c.lower[1], 255, nothing)
        cv2.createTrackbar('Low V', name, c.lower[2], 255, nothing)

        # Create trackbars for higher
        cv2.createTrackbar('High H', name, c.upper[0], 180, nothing)
        cv2.createTrackbar('High S', name, c.upper[1], 255, nothing)
        cv2.createTrackbar('High V', name, c.upper[2], 255, nothing)
        cv2.createTrackbar('off_on', name, 0, 1, nothing)

    def savehigherlower(self, color_range):
        """
        Starts form for getting the color of the saving color
        """
        correct_ranges = []

        for color in range(len(color_range)):
            c = self.color_range[color]
            lowh = cv2.getTrackbarPos('Low H', c.color)
            lows = cv2.getTrackbarPos('Low S', c.color)
            lowv = cv2.getTrackbarPos('Low V', c.color)

            highh = cv2.getTrackbarPos('High H', c.color)
            highs = cv2.getTrackbarPos('High S', c.color)
            highv = cv2.getTrackbarPos('High V', c.color)

            correct_ranges.append((c.color, [lowh, lows, lowv], [highh, highs, highv]))

        # Save the ranges to JSON file
        self.range_handler.set_color_range(correct_ranges)
        print("[INFO] Saved settings")

    def nothing(self, x):
        pass
