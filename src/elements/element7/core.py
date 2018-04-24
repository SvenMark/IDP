import cv2
import numpy as np


def run():
    print("run element7")

    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()

        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        lower_blue = np.array([110, 100, 100])
        upper_blue = np.array([130, 255, 255])

        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])

        lower_green = np.array([50, 100, 100])
        upper_green = np.array([70, 255, 255])

        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)

        cnts = cv2.findContours(mask_blue.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        cnts += cv2.findContours(mask_red.copy(), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)[-2]
        cnts += cv2.findContours(mask_green.copy(), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(cnts) > 0:
            for c in cnts:
                moments = cv2.moments(c)
                if moments['m00'] > 1000:
                    hull = cv2.convexHull(c)
                    cx = int(moments['m10'] / moments['m00'])
                    cy = int(moments['m01'] / moments['m00'])
                    cv2.drawContours(img, [hull], -1, (0, 255, 255), 3)
                    cv2.circle(img, (cx, cy), 3, (0, 255, 255), 3)

        cv2.imshow('frame', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
