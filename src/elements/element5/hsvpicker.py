from imutils.video import WebcamVideoStream
import time
import numpy as np
import cv2


def run():
    print("run hsvpicker")
    cap = WebcamVideoStream(src=0).start()
    time.sleep(1)  # startup

    sample = cap.read()
    height = sample.shape[0]  # get height
    width = sample.shape[1]  # get width
    print("w: " + str(width) + " " + "h: " + str(height))

    createtrackbars("1")
    createtrackbars("2")

    while True:
        img = cap.read()
        img = cv2.GaussianBlur(img, (9, 9), 0)

        lowh = cv2.getTrackbarPos('Low H', '1')
        lows = cv2.getTrackbarPos('Low S', '1')
        lowv = cv2.getTrackbarPos('Low V', '1')

        highh = cv2.getTrackbarPos('High H', '1')
        highs = cv2.getTrackbarPos('High S', '1')
        highv = cv2.getTrackbarPos('High V', '1')

        # Hsv Mask
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([lowh, lows, lowv])
        higher = np.array([highh, highs, highv])
        mask = cv2.inRange(hsv, lower, higher)

        if cv2.getTrackbarPos('keta', '2') > 50:
            mask += calculate_mask("2", mask, img)
            print("homo")

        output = cv2.bitwise_and(img, img, mask=mask)

        ret, thresh = cv2.threshold(mask, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100:
                cv2.drawContours(output, [cnt], -1, (255, 255, 255), 5)

        cv2.imshow('hsv-picker', output)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            print("Saved settings")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.stop()
    cv2.destroyAllWindows()


def calculate_mask(name, mask, img):
    lowh = cv2.getTrackbarPos('Low H', name)
    lows = cv2.getTrackbarPos('Low S', name)
    lowv = cv2.getTrackbarPos('Low V', name)

    highh = cv2.getTrackbarPos('High H', name)
    highs = cv2.getTrackbarPos('High S', name)
    highv = cv2.getTrackbarPos('High V', name)

    # Hsv Mask
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([lowh, lows, lowv])
    higher = np.array([highh, highs, highv])
    mask += cv2.inRange(hsv, lower, higher)
    return mask


def createtrackbars(name):
    cv2.namedWindow(name)

    # create trackbars for lower
    cv2.createTrackbar('Low H', name, 90, 180, nothing)
    cv2.createTrackbar('Low S', name, 100, 255, nothing)
    cv2.createTrackbar('Low V', name, 100, 255, nothing)

    # create trackbars for higher
    cv2.createTrackbar('High H', name, 120, 180, nothing)
    cv2.createTrackbar('High S', name, 255, 255, nothing)
    cv2.createTrackbar('High V', name, 255, 255, nothing)
    cv2.createTrackbar('keta', name, 255, 255, nothing)


def savehigherlower(lowh, lows, lowv, highh, highs, highv):
    text_file = open("Output.txt", "a")
    text_file.write("([" + str(lowh) + ", " + str(lows) + ", " + str(lowv) + "], "
                    "[" + str(highh) + ", " + str(highs) + ", " + str(highv) + "])")
    text_file.close()


def nothing(x):
    pass


run()
