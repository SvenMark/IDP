import cv2

cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)

    if cv2.waitKey(10) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
