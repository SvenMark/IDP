import random
from collections import OrderedDict
from imutils.video import WebcamVideoStream
import time
import numpy as np
import cv2


def run():
    print("run element6")
    cap = WebcamVideoStream(src=0).start()
    time.sleep(1)  # startup

    while True:
        img = cap.read()
        blur = cv2.GaussianBlur(img, (9, 9), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        # Mask
        low_white = np.array([0, 0, 0])
        high_white = np.array([180, 255, 30])
        mask = cv2.inRange(hsv, low_white, high_white)

        theta = np.pi / 180  # angular resolution in radians of the Hough grid
        threshold = 25  # minimum number of votes (intersections in Hough grid cell)
        min_line_length = 100  # minimaal aantal pixels voor een lijn
        max_line_gap = 50  # mmaximale gap in pixels tussen verbindbare lijn segmenten

        lines = cv2.HoughLinesP(mask, 1, theta, threshold, np.array([]),
                                min_line_length, max_line_gap)

        imgClone = img.copy()
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(imgClone, (x1, y1), (x2, y2), (0, 255, 255), 5)

        cv2.imshow('camservice-lijn', imgClone)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.stop()
    cv2.destroyAllWindows()


print ("uncomment run before starting..")
run()  # disabled for travis
