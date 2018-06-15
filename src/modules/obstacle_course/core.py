import sys

sys.path.insert(0, '../../../src')

import time
import cv2
import numpy as np
from imutils.video import VideoStream
from entities.vision.recognize import Recognize
from entities.vision.helpers.vision_helper import Color


def run(name, movement, shared_object):
    print("[RUN] " + str(name))
    detect_cup()

    while not shared_object.has_to_stop():
        print("[INFO] Doing calculations and stuff")
        time.sleep(0.1)

    # Notify shared object that this thread has been stopped
    print("[STOPPED]" + str(name))
    shared_object.has_been_stopped()


def detect_cup():
    """
    Detects the cup and calculates distance to cup with
    :return: none
    """
    # Set minimal points which he needs to detect the cup
    MIN_MATCH_COUNT = 20

    # Set the detector and create matcher
    detector = cv2.xfeatures2d.SIFT_create()

    FLANN_INDEX_KDITREE = 0
    flannParam = dict(algorithm=FLANN_INDEX_KDITREE, tree=5)
    flann = cv2.FlannBasedMatcher(flannParam, {})

    # Get training image of cup
    trainImg = cv2.imread("ding.jpg", 0)
    trainKP, trainDesc = detector.detectAndCompute(trainImg, None)

    # Get video of picamera
    cam = VideoStream(src=0, usePiCamera=False, resolution=(320, 240)).start()
    time.sleep(0.3)  # startup

    while True:
        # Get frame and turn it into black and white
        frame = cam.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Set mask
        green = Color('green', [28, 39, 0], [94, 255, 255])
        mask = cv2.inRange(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), green.lower, green.upper)

        # Get contours and draw them when area of them is 1000 or higher
        ret, thresh = cv2.threshold(mask, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1000:
                cv2.drawContours(mask, [cnt], -1, (255, 255, 255), 50)

        cv2.imshow('Masked cup', mask)

        # Detect points and compare with cup image and returns matches
        queryKP, queryDesc = detector.detectAndCompute(frame_gray, mask=mask)
        matches = flann.knnMatch(queryDesc, trainDesc, k=2)

        goodMatch = []

        # Counts matches
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                goodMatch.append(m)

        # If there are more matches then the minimal count, detect the cup and draw border
        if len(goodMatch) > MIN_MATCH_COUNT:
            tp = []
            qp = []
            for m in goodMatch:
                tp.append(trainKP[m.trainIdx].pt)
                qp.append(queryKP[m.queryIdx].pt)
            tp, qp = np.float32((tp, qp))
            H, status = cv2.findHomography(tp, qp, cv2.RANSAC, 3.0)
            h, w = trainImg.shape
            trainBorder = np.float32([[[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]])
            queryBorder = cv2.perspectiveTransform(trainBorder, H)

            moment = cv2.moments(queryBorder)

            # Calculate distance in a really ugly way
            x, y, w, h = cv2.boundingRect(queryBorder)
            distance = 0.00008650519031141868 * h ** 2 - 0.10294117647058823 * h + 35

            # Calculate the centre of mass
            cx = int(moment['m10'] / moment['m00'])
            cy = int(moment['m01'] / moment['m00'])

            # Adds text to center with 'cup'
            cv2.putText(frame, "Cup", (cx - 30, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.polylines(frame, [np.int32(queryBorder)], True, (255, 255, 255), 4)
            print("[INFO] Cup detected at distance: " + str(distance) + "cm")
        else:
            print("[INFO] Not Enough match found- %d/%d" % (len(goodMatch), MIN_MATCH_COUNT))
        cv2.imshow('Detected cup', frame)
        if cv2.waitKey(10) == ord('q'):
            break
    cam.stop()
    cv2.destroyAllWindows()


def detect_bridge():
    """
    Detects the bridge in the parcour
    :return: none
    """
    # Initialize color ranges for detection
    color_range = [Color("Brug", [0, 0, 0], [0, 255, 107]),
                   Color("Gat", [0, 0, 0], [0, 0, 255]),
                   Color("Rand", [0, 0, 185], [0, 0, 255]),
                   Color("White-ish", [0, 0, 68], [180, 98, 255])]

    cam = Recognize(color_range)
    cam.run()


if __name__ == '__main__':
    run(shared_object=None)  # disabled for travis
