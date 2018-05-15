import random
from collections import OrderedDict
from imutils.video import WebcamVideoStream
import time
import numpy as np
import cv2

print ("uncomment run before starting..")
def run():
    print("run element6")
    cap = WebcamVideoStream(src=0).start()
    time.sleep(1) #startup

    while True:
        img = cap.read()
        blur = cv2.GaussianBlur(img, (5, 5), 0)
        blurgray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

        low_threshold = 100
        high_threshold = 200
        edges = cv2.Canny(blurgray, low_threshold, high_threshold)

        rho = 1  # distance resolution in pixels of the Hough grid
        theta = np.pi / 180  # angular resolution in radians of the Hough grid
        threshold = 15  # minimum number of votes (intersections in Hough grid cell)
        min_line_length = 50  # minimum number of pixels making up a line
        max_line_gap = 20  # maximum gap in pixels between connectable line segments

        # Run Hough on edge detected image
        # Output "lines" is an array containing endpoints of detected line segments
        lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                    min_line_length, max_line_gap)

        imgClone = img.copy()
        if lines is not None:
            for line in lines:
                for x1,y1,x2,y2 in line:
                    cv2.line(imgClone,(x1,y1),(x2,y2),(255,0,0),5)

            lines_edges = cv2.addWeighted(img, 0.8, imgClone, 1, 0)
        
        cv2.imshow('camservice-lijn', imgClone)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.stop()
    cv2.destroyAllWindows()


run()  # disabled for travis
