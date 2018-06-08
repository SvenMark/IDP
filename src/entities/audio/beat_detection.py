import pyaudio
import numpy as np


class BeatDetection(object):
    def __init__(self):
        self.CHUNK = 10000  # speed of data point reading, smaller == less datapoints == faster updates
        self.RATE = 44100  # time resolution of the recording device (Hz) Higher == Better accuracy

        self.lowlows = 0
        self.highlows = 200  # low value borders

        self.lowmeds = 200
        self.highmeds = 2000  # med value borders

        self.lowhighs = 2000
        self.highhighs = 2500  # high value borders
        self.running = False

    def detect(self, stream):

        count = 0
        data = np.fromstring(stream.read(self.CHUNK), dtype=np.int16)
        left = data[0::2]
        lf = np.fft.rfft(left)

        lows = 0
        for i in range(self.lowlows, self.highlows):
            lows = lows + abs(lf)[i]
        meds = 0
        for i in range(self.lowmeds, self.highmeds):
            meds = meds + abs(lf)[i]
        high = 0
        for i in range(self.lowhighs, self.highhighs):
            high = high + abs(lf)[i]

        # Print de values
        value = [int(lows), int(meds), int(high)]
        print("Low: " + str(value[0]) + ", Med: " + str(value[1]) + ", High: " + str(value[2]))

        if lows > 9000000:
            count += 1
            print("Bass #" + str(count))


