# from imutils.video import WebcamVideoStream
# import time
# import numpy as np
# import cv2
#
#
# def run():
#     print("run hsvpicker")
#     cap = WebcamVideoStream(src=0).start()
#     time.sleep(1)  # startup
#
#     sample = cap.read()
#     height = sample.shape[0]  # get height
#     width = sample.shape[1]  # get width
#     print("w: " + str(width) + " " + "h: " + str(height))
#
#     createtrackbars()
#
#     while True:
#         img = cap.read()
#         blur = cv2.GaussianBlur(img, (9, 9), 0)
#
#         lowh = cv2.getTrackbarPos('Low H', 'picker')
#         lows = cv2.getTrackbarPos('Low S', 'picker')
#         lowv = cv2.getTrackbarPos('Low V', 'picker')
#
#         highh = cv2.getTrackbarPos('High H', 'picker')
#         highs = cv2.getTrackbarPos('High S', 'picker')
#         highv = cv2.getTrackbarPos('High V', 'picker')
#
#         # Hsv Mask
#         hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
#         lower = np.array([lowh, lows, lowv])
#         higher = np.array([highh, highs, highv])
#         mask = cv2.inRange(hsv, lower, higher)
#
#         output = cv2.bitwise_and(img, img, mask=mask)
#
#         ret, thresh = cv2.threshold(mask, 127, 255, 0)
#         im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
#         for cnt in contours:
#             area = cv2.contourArea(cnt)
#             if area > 100:
#                 cv2.drawContours(output, [cnt], -1, (255, 255, 255), 5)
#
#         cv2.imshow('hsv-picker', output)
#
#         if cv2.waitKey(1) & 0xFF == ord('s'):
#             print("Saved settings")
#             savehigherlower(lowh, lows, lowv, highh, highs, highv)
#
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     cap.stop()
#     cv2.destroyAllWindows()
#
#
# def createtrackbars():
#     cv2.namedWindow('picker')
#
#     # create trackbars for lower
#     cv2.createTrackbar('Low H', 'picker', 90, 180, nothing)
#     cv2.createTrackbar('Low S', 'picker', 100, 255, nothing)
#     cv2.createTrackbar('Low V', 'picker', 100, 255, nothing)
#
#     # create trackbars for higher
#     cv2.createTrackbar('High H', 'picker', 120, 180, nothing)
#     cv2.createTrackbar('High S', 'picker', 255, 255, nothing)
#     cv2.createTrackbar('High V', 'picker', 255, 255, nothing)
#
#
# def savehigherlower(lowh, lows, lowv, highh, highs, highv):
#     text_file = open("Output.txt", "w")
#     text_file.write("([" + str(lowh) + ", " + str(lows) + ", " + str(lowv) + "],"
#                     "[" + str(highh) + ", " + str(highs) + ", " + str(highv) + "])")
#     text_file.close()
#
#
# def nothing(x):
#     pass
#
#
# run()
