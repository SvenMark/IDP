import io
import time
import picamera
import numpy as np
from PIL import Image
import cv2

def outputs():
    stream = io.BytesIO()
    for i in range(100):
        # This returns the stream for the camera to capture to
        yield stream
        img = Image.open(stream)
        b, g, r = img.split()
        img = Image.merge("RGB", (r, g, b))
        frame = np.asarray(img)

        stream.seek(0)
        stream.truncate()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()
    

with picamera.PiCamera() as camera:
    count = 100
    camera.resolution = (320, 240)
    camera.framerate = 60
    time.sleep(0.1)
    start = time.time()
    camera.capture_sequence(outputs(), 'jpeg', use_video_port=True)
    finish = time.time()
    print('Captured ' + str(count) + ' images at %.2ffps' % (count / (finish - start)))



