import numpy as np
import cv2


def run():
    print("run element7")

    s = 20  # for example sensitivity=5/256 color values in range [0,255]
    # define the list of boundaries: red, blue, yellow
    boundaries = [
        ([86, 31, 4], [220, 88, 50]),
        ([25, 146, 190], [62, 174, 250]),
        ([103, 86, 65], [145, 133, 128])
    ]

    cap = cv2.VideoCapture(0)
    while True:
        # ret, img = cap.read()
        img = cv2.imread('C:/Users/Jildert/Documents/00-gitRepos/Robotica/src/vision/test_img/colorpallet.jpg')
        image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        output = None
        cnts = []

        for i, (lower, upper) in enumerate(boundaries):
            lower = np.array([color - s if color - s > -1 else 0 for color in lower], dtype="uint8")
            upper = np.array([color + s if color + s < 256 else 255 for color in upper], dtype="uint8")

            mask = cv2.inRange(image, lower, upper)
            output = cv2.bitwise_and(image, image, mask=mask)

           # cv2.imwrite(str(i) + 'image.jpg', output)

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

        cv2.imshow('frame',  np.hstack([image, output]))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
