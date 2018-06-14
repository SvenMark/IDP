import sys
import time

sys.path.insert(0, '../../../src')

from entities.vision.recognize import Recognize, Block
from entities.vision.helpers.vision_helper import Color


def run(name, movement, shared_object):
    print("run " + str(name))
    # detect_cup()

    while not shared_object.has_to_stop():
        print("Doing calculations and stuff")
        time.sleep(0.5)

    # Notify shared object that this thread has been stopped
    print("Stopped" + str(name))
    shared_object.has_been_stopped()


def detect_cup():
    import cv2
    import numpy as np

    MIN_MATCH_COUNT = 20

    detector = cv2.xfeatures2d.SIFT_create()

    FLANN_INDEX_KDITREE = 0
    flannParam = dict(algorithm=FLANN_INDEX_KDITREE, tree=5)
    flann = cv2.FlannBasedMatcher(flannParam, {})

    trainImg = cv2.imread("ding.jpg", 0)
    trainKP, trainDesc = detector.detectAndCompute(trainImg, None)

    cam = cv2.VideoCapture(0)
    while True:
        ret, QueryImgBGR = cam.read()
        QueryImg = cv2.cvtColor(QueryImgBGR, cv2.COLOR_BGR2GRAY)
        queryKP, queryDesc = detector.detectAndCompute(QueryImg, None)
        matches = flann.knnMatch(queryDesc, trainDesc, k=2)
        cv2.imshow("Points", cv2.drawKeypoints(QueryImgBGR, queryKP, None))

        goodMatch = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                goodMatch.append(m)
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

            x, y, w, h = cv2.boundingRect(queryBorder)
            distance = 0.00008650519031141868 * h**2 - 0.10294117647058823 * h + 35
            # Calculate the centre of mass
            cx = int(moment['m10'] / moment['m00'])
            cy = int(moment['m01'] / moment['m00'])

            cv2.putText(QueryImgBGR, "Cup", (cx - 30, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.polylines(QueryImgBGR, [np.int32(queryBorder)], True, (255, 255, 255), 4)
            print("Cup detected at distance: " + str(distance) + "cm")
        else:
            print("Not Enough match found- %d/%d" % (len(goodMatch), MIN_MATCH_COUNT))
        cv2.imshow('result', QueryImgBGR)
        if cv2.waitKey(10) == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()


def detect_bridge():

    # Initialize color ranges for detection
    color_range = [Color("Brug", [0, 0, 0], [0, 255, 107]),
                   Color("Gat", [0, 0, 0], [0, 0, 255]),
                   Color("Rand", [0, 0, 185], [0, 0, 255]),
                   Color("White-ish", [0, 0, 68], [180, 98, 255])]

    cam = Recognize(color_range)
    cam.run()


if __name__ == '__main__':
    run()  # disabled for travis
