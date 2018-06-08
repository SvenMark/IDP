import sys
sys.path.insert(0, '../../../src')  # Needed for pi

from imutils.video import WebcamVideoStream
from elements.element6.helpers import Point, Color
from decimal import Decimal
import time
import numpy as np
import cv2


class Element6(object):
    @staticmethod
    def linedetection(shared_object):
        print("run element6")
        cap = WebcamVideoStream(src=0).start()
        time.sleep(1)  # startup

        sample = cap.read()
        height = sample.shape[0]  # get height
        width = sample.shape[1]  # get width
        print("w: " + str(width) + " " + "h: " + str(height))

        vertices = [
            (0, height),
            (width / 2, height / 2),
            (width, height),
        ]

        while True:
            img = cap.read()
            imgCropped = Element6.setregion(img, np.array([vertices], np.int32))
            blur = cv2.GaussianBlur(imgCropped, (9, 9), 0)

            # Hsv Mask
            hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
            low_black = np.array([0, 0, 40])
            high_black = np.array([157, 118, 120])
            mask = cv2.inRange(hsv, low_black, high_black)

            # Red detection
            if Element6.detectred(img, hsv):
                print("red detected (possible sleep)")
                # time.sleep(10)

            # Get lines
            theta = np.pi / 180
            threshold = 150
            min_line_length = 40
            max_line_gap = 25

            lines = cv2.HoughLinesP(mask, 2, theta, threshold, np.array([]),
                                    min_line_length, max_line_gap)

            # Draw lines
            linecolor = (255, 0, 0)
            imgClone = img.copy()

            if lines is not None:
                for line in lines:
                    for x1, y1, x2, y2 in line:
                        p1 = Point(x1, y1)
                        p2 = Point(x2, y2)
                        cv2.line(imgClone, (p1.x, p1.y), (p2.x, p2.y), linecolor, 5)
                left, right = Element6.averagedistance(lines, width)
                print("Percentage left: " + str(round(left)) + "%")
                print("Percentage right: " + str(round(right)) + "%")

            cv2.imshow('camservice-lijn', imgClone)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.stop()
        cv2.destroyAllWindows()

    @staticmethod
    def setregion(img, vertices):       # Region for search
        mask = np.zeros_like(img)
        channel_count = img.shape[2]
        match_mask_color = (255,) * channel_count
        cv2.fillPoly(mask, vertices, match_mask_color)

        masked_img = cv2.bitwise_and(img, mask)

        new_mask = np.zeros(masked_img.shape[:2], np.uint8)

        bg = np.ones_like(masked_img, np.uint8) * 255
        cv2.bitwise_not(bg, bg, mask=new_mask)

        return masked_img + bg

    @staticmethod
    def midpoint(p1, p2):
        midp = Point(0, 0)
        midp.x = (p1.x + p2.x) / 2
        midp.y = (p1.y + p2.y) / 2
        return midp

    @staticmethod
    def averagedistance(lines, width):
        count = 0
        totaldr = 0  # Total distance to right
        totaldl = 0  # Total distance to left
        for line in lines:
            for x1, y1, x2, y2 in line:
                p1 = Point(x1, y1)
                p2 = Point(x2, y2)
                midp = Element6.midpoint(p1, p2)
                totaldr += (width - midp.x)  # Distance to right
                totaldl += (0 + midp.x)  # Distance to right
                count += 1

        # Average to sides (x-as)
        percentageleft = Decimal((Decimal(Decimal(totaldl) / Decimal(count)) / Decimal(width)) * Decimal(100))
        percentageright = Decimal((Decimal(Decimal(totaldr) / Decimal(count)) / Decimal(width)) * Decimal(100))

        return percentageleft, percentageright

    @staticmethod
    def detectred(img, hsv):
        red = Color([170, 100, 100], [190, 255, 255])
        mask = cv2.inRange(hsv, red.lower, red.upper)
        red = cv2.bitwise_and(img, img, mask=mask)

        ret, thresh = cv2.threshold(mask, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            cv2.drawContours(img, [cnt], -1, (0, 0, 255), 10)
            cv2.imshow("red", red)
        if len(contours) < 2:
            return False
        else:
            return True


def main():
    bld = Element6()
    bld.linedetection()


print("uncomment main before starting..")
main()  # disabled for travis
