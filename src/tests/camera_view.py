import sys
import time
import cv2

sys.path.insert(0, '../../../src')

from imutils.video import VideoStream

cap = VideoStream(src=0, usePiCamera=True, resolution=(320, 240)).start()
time.sleep(0.3)

while True:
    img = cap.read()
    cv2.imshow('cam', img)
