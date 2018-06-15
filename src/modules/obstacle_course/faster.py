import cv2
import picamera
import picamera.array
import time

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        while True:
            camera.capture(stream, format='bgr')
            image = stream.array
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame', gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # reset the stream before the next capture
            stream.seek(0)
            stream.truncate()
        cv2.destroyAllWindows()
