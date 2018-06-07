import time

import pyaudio
import numpy as np
from entities.audio.beat_detection import BeatDetection


def run():
    print("run element4")

    p = pyaudio.PyAudio()  # start the PyAudio class
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True,
                    frames_per_buffer=10000)  # uses default input device

    test = BeatDetection()
    while True:
        test.detect(stream)

    stream.stop_stream()
    stream.close()
    p.terminate()


# End of def run
if __name__ == '__main__':
    run()
