import cv2
import numpy as np


def run():
    print("run element7")

    # define the list of boundaries: red, blue, yellow
    boundaries = [
        ([17, 15, 100], [50, 56, 200]),
        ([86, 31, 4], [220, 88, 50]),
        ([25, 146, 190], [62, 174, 250])
    ]

    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()

        output = None
        cnts = []

        for (lower, upper) in boundaries:
            # create NumPy arrays from the boundaries
            lower = np.array(lower, "uint8")
            upper = np.array(upper, "uint8")

            # find the colors within the specified boundaries and apply
            # the mask
            mask = cv2.inRange(img, lower, upper)
            output = cv2.bitwise_and(img, img, mask)
            cnts += cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)[-2]

        # draw dots
        if len(cnts) > 0:
            for c in cnts:
                moments = cv2.moments(c)
                if moments['m00'] > 1000:
                    hull = cv2.convexHull(c)
                    cx = int(moments['m10'] / moments['m00'])
                    cy = int(moments['m01'] / moments['m00'])
                    cv2.drawContours(img, [hull], -1, (0, 255, 255), 3)
                    cv2.circle(img, (cx, cy), 3, (0, 255, 255), 3)

        cv2.imshow('frame',  np.hstack([img, output]))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
