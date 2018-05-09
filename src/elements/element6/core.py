from collections import OrderedDict
from helpers import Color
import cv2

print "uncomment run before starting.."


def run():
    print("run element6")
    cap = cv2.VideoCapture(0)

    orange = Color([0, 100, 100], [10, 255, 255])
    yellow = Color([20, 100, 100], [30, 255, 255])
    red = Color([170, 100, 100], [190, 255, 255])
    green = Color([60, 100, 50], [90, 255, 255])
    blue = Color([90, 100, 100], [120, 255, 255])

    while True:
        ret, img = cap.read()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        masks = OrderedDict({
            "red": cv2.inRange(hsv, red.lower, red.upper),
            "blue": cv2.inRange(hsv, blue.lower, blue.upper),
            "green": cv2.inRange(hsv, green.lower, green.upper),
            "orange": cv2.inRange(hsv, orange.lower, orange.upper),
            "yellow": cv2.inRange(hsv, yellow.lower, yellow.upper)})

        imgmask = setcontours(masks.get("red"), "red", img)
        for col, mask in masks.items():
            if col == "red":
                continue
            imgmask += setcontours(mask, col, img)

        cv2.imshow('camservice', imgmask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def setcontours(mask, color, img):

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
            text = "{} {}".format("Color:", color)
            cv2.putText(imgmask, text, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    return imgmask


# run()  # disabled for travis
