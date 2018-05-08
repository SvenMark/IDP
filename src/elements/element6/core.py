from collections import OrderedDict
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
        lower_green = np.array([60, 100, 50])
        upper_green = np.array([90, 255, 255])

        # blue 110,120
        lower_blue = np.array([90, 100, 100])
        upper_blue = np.array([120, 255, 255])

        maskBlue = cv2.inRange(hsv, lower_blue, upper_blue)
        maskRed = cv2.inRange(hsv, lower_red, upper_red)
        maskGreen = cv2.inRange(hsv, lower_green, upper_green)
        maskOrange = cv2.inRange(hsv, lower_orange, upper_orange)
        maskYellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

        mask = maskBlue + maskGreen + maskOrange + maskRed + maskYellow

        imgmask = cv2.bitwise_and(img, img, mask=mask)

        ret, thresh = cv2.threshold(mask, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for i in range(len(contours)):
            c = cv2.convexHull(contours[i])
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            area = cv2.contourArea(c)
            if len(approx) == 4 and area > 4000:
                M = cv2.moments(c)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                cv2.drawContours(imgmask, [c], 0, (255, 255, 255), 3)
                text = "{} {}".format("Color:", "")
                cv2.putText(imgmask, text, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        cv2.imshow('camservice', imgmask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def colordetector(img, col, c):
    low_colors = OrderedDict({
        "red": np.array([170, 100, 100]),
        "blue": np.array([90, 100, 100])})
    high_colors = OrderedDict({
        "red": np.array([190, 255, 255]),
        "blue": np.array([120, 255, 255])})

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    for col, low in low_colors.items():
        mask = cv2.inRange(hsv, low, high_colors.get(col))


run()  # disabled for travis
