import numpy as np
import cv2


def run():
    print("run element6")
    inp = (2,2,2,2,2,2)
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # orange g00d 0,10
        lower_orange = np.array([0, 100, 100])
        upper_orange = np.array([10, 255, 255])

        # yellow g00d 20,30
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])

        # red 170,180
        lower_red = np.array([170, 100, 100])
        upper_red = np.array([190, 255, 255])

        # green 70,90
        lower_green = np.array([70, 0, 0])
        upper_green = np.array([90, 255, 255])

        # blue 110,120
        lower_blue = np.array([110, 100, 100])
        upper_blue = np.array([120, 255, 255])

        maskBlue = cv2.inRange(hsv, lower_blue, upper_blue)
        maskRed = cv2.inRange(hsv, lower_red, upper_red)
        maskGreen = cv2.inRange(hsv, lower_green, upper_green)
        maskOrange = cv2.inRange(hsv, lower_orange, upper_orange)
        maskYellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # mask = maskBlue + maskGreen + maskOrange + maskRed + maskYellow

        ret, thresh = cv2.threshold(maskRed, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for i in range(len(contours)):
            c = cv2.convexHull(contours[i])
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            area = cv2.contourArea(c)
            if len(approx) == 4 and area > 1000:
                cv2.drawContours(img, [c], -1, (0, 255, 255), 3)

        img = cv2.bitwise_and(img, img, mask=maskRed)

        cv2.imshow('red', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# run()  # disabled for travis
