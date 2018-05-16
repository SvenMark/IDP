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

    sample = cap.read()
    height = sample.shape[0]  # get height
    width = sample.shape[1]  # get width
    vertices = [
        (0, height),
        (width / 2, height / 2),
        (width, height),
    ]

    while True:
        img = cap.read()
        imgCropped = setregion(img, np.array([vertices], np.int32))
        blur = cv2.GaussianBlur(imgCropped, (9, 9), 0)

        # Hsv Mask
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        low_black = np.array([0, 0, 0])
        high_black = np.array([180, 255, 30])
        mask = cv2.inRange(hsv, low_black, high_black)

        theta = np.pi / 180
        threshold = 150
        min_line_length = 40
        max_line_gap = 25
    
        lines = cv2.HoughLinesP(mask, 6, theta, threshold, np.array([]),
                                min_line_length, max_line_gap)

        imgClone = img.copy()
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(imgClone, (x1, y1), (x2, y2), (255, 0, 0), 5)
        
        cv2.imshow('camservice-lijn', imgClone)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.stop()
    cv2.destroyAllWindows()


def setregion(img, vertices):
    mask = np.zeros_like(img)
    channel_count = img.shape[2]   
    match_mask_color = (255,) * channel_count
    cv2.fillPoly(mask, vertices, match_mask_color)
    
    masked_img = cv2.bitwise_and(img, mask)

    new_mask = np.zeros(masked_img.shape[:2], np.uint8)

    bg = np.ones_like(masked_img, np.uint8)*255
    cv2.bitwise_not(bg, bg, mask=new_mask)
    
    return masked_img + bg


print ("uncomment run before starting..")
run()  # disabled for travis
