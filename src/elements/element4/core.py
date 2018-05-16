import pyaudio
import numpy as np
import pylab
import time


def run():
    print("run element4")

    OPTION = 0  # 0 is best

    if OPTION == 0:
        from matplotlib.ticker import FuncFormatter

        np.set_printoptions(suppress=True)  # don't use scientific notation

        CHUNK = 700  # speed of data point reading, smaller == less datapoints == faster updates
        RATE = 11025  # time resolution of the recording device (Hz) Higher == Better accuracy
        OUTPUTS = 1000  # number of outputs

        LOWLOWS = 0
        HIGHLOWS = 50  # low value borders

        LOWMEDS = 50
        HIGHMEDS = 100  # med value borders

        LOWHIGHS = 100
        HIGHHIGHS = 175  # high value borders

        p = pyaudio.PyAudio()  # start the PyAudio class
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                        frames_per_buffer=CHUNK)  # uses default input device

        pylab.interactive(True)
        for i in range(OUTPUTS):  # Number of outputs
            data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
            left = data[0::2]
            lf = np.fft.rfft(left)

            # Plot the graph
            # pylab.clf()
            # pylab.figure(1)
            # b = pylab.subplot(212)
            # b.set_xscale('log')
            # b.set_xlabel('frequency [Hz]')
            # b.set_ylabel('|amplitude|')

            # b.set_ylim([0, 50000])
            # pylab.plot(abs(lf))
            # pylab.savefig('frequency.png')
            # pylab.show()

            lows = 0
            for i in range(LOWLOWS, HIGHLOWS):
                lows = lows + abs(lf)[i]
            meds = 0
            for i in range(LOWMEDS, HIGHMEDS):
                meds = meds + abs(lf)[i]
            high = 0
            for i in range(LOWHIGHS, HIGHHIGHS):
                high = high + abs(lf)[i]

            value = [lows, meds, high]
            pylab.ylim(0, 2000000)
            pylab.bar(np.arange(3), value)
            pylab.xticks(np.arange(3), ('Low', 'Med', 'High'))
            pylab.show()

            print("Low: " + str(lows) + ", Med: " + str(meds) + ", High: " + str(high))

        stream.stop_stream()
        stream.close()
        p.terminate()

    elif OPTION == 1:
        np.set_printoptions(suppress=True)  # don't use scientific notation

        CHUNK = 2000  # speed of data point reading, smaller is less datapoints is faster updates
        RATE = 44100  # time resolution of the recording device (Hz)
        OUTPUTS = 12000  # number of outputs

        p = pyaudio.PyAudio()  # start the PyAudio class
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                        frames_per_buffer=CHUNK)  # uses default input device

        for i in range(OUTPUTS):  # Number of outputs
            data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
            data = data * np.hanning(len(data))  # smooth the FFT by windowing data
            fft = abs(np.fft.fft(data).real)
            fft = fft[:int(len(fft) / 2)]  # keep only first half
            freq = np.fft.fftfreq(CHUNK, 1.0 / RATE)
            freq = freq[:int(len(freq) / 2)]  # keep only first half
            freqPeak = freq[np.where(fft == np.max(fft))[0][0]] + 1
            # print("Peak frequency: %d Hz" % freqPeak)
            bars = "#" * int(500 * freqPeak / 2 ** 16)
            print("Peak: %05d hz %s" % (freqPeak, bars))

        # close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

    elif OPTION == 2:

        class SWHear(object):
            """
            The SWHear class is made to provide access to continuously recorded
            (and mathematically processed) microphone data.
            """

            def __init__(self, device=None, startStreaming=True):
                """fire up the SWHear class."""
                print(" -- initializing SWHear")

                self.chunk = 4096  # number of data points to read at a time
                self.rate = 44100  # time resolution of the recording device (Hz)

                # for tape recording (continuous "tape" of recent audio)
                self.tapeLength = 2  # seconds
                self.tape = np.empty(self.rate * self.tapeLength) * np.nan

                self.p = pyaudio.PyAudio()  # start the PyAudio class
                if startStreaming:
                    self.stream_start()

            ### LOWEST LEVEL AUDIO ACCESS
            # pure access to microphone and stream operations
            # keep math, plotting, FFT, etc out of here.
            def stream_read(self):
                """return values for a single chunk"""
                data = np.fromstring(self.stream.read(self.chunk), dtype=np.int16)
                # print(data)
                return data

            def stream_start(self):
                """connect to the audio device and start a stream"""
                print(" -- stream started")
                self.stream = self.p.open(format=pyaudio.paInt16, channels=1,
                                          rate=self.rate, input=True,
                                          frames_per_buffer=self.chunk)

            def stream_stop(self):
                """close the stream but keep the PyAudio instance alive."""
                if 'stream' in locals():
                    self.stream.stop_stream()
                    self.stream.close()
                print(" -- stream CLOSED")

            def close(self):
                """gently detach from things."""
                self.stream_stop()
                self.p.terminate()

            ### TAPE METHODS
            # tape is like a circular magnetic ribbon of tape that's continously
            # recorded and recorded over in a loop. self.tape contains this data.
            # the newest data is always at the end. Don't modify data on the type,
            # but rather do math on it (like FFT) as you read from it.

            def tape_add(self):
                """add a single chunk to the tape."""
                self.tape[:-self.chunk] = self.tape[self.chunk:]
                self.tape[-self.chunk:] = self.stream_read()

            def tape_flush(self):
                """completely fill tape with new data."""
                readsInTape = int(self.rate * self.tapeLength / self.chunk)
                print(" -- flushing %d s tape with %dx%.2f ms reads" % \
                      (self.tapeLength, readsInTape, self.chunk / self.rate))
                for i in range(readsInTape):
                    self.tape_add()

            def tape_forever(self, plotSec=.25):
                t1 = 0
                try:
                    while True:
                        self.tape_add()
                        if (time.time() - t1) > plotSec:
                            t1 = time.time()
                            self.tape_plot()
                except:
                    print(" ~~ exception (keyboard?)")
                    return

            def tape_plot(self, saveAs="garbage.png"):
                """plot what's in the tape."""
                pylab.plot(np.arange(len(self.tape)) / self.rate, self.tape)
                pylab.axis([0, self.tapeLength, -2 ** 13 / 2, 2 ** 13 / 2])
                if saveAs:
                    t1 = time.time()
                    pylab.savefig(saveAs, dpi=50)
                    pylab.show()
                    print("plotting saving took %.02f ms" % ((time.time() - t1) * 1000))
                else:
                    pylab.show()
                    print()  # good for IPython
                pylab.close('all')

        ear = SWHear()
        ear.tape_forever()
        ear.close()
        print("DONE")

    elif OPTION == 3:
        np.set_printoptions(suppress=True)  # don't use scientific notation
        CHUNK = 1000  # speed of data point reading, smaller == less datapoints == faster updates
        RATE = 44100  # time resolution of the recording device (Hz)
        OUTPUTS = 12000  # number of outputs

        # Frequency borders
        LOWBORDER = 300
        MEDBORDER = 600
        HIGHBORDER = 1200

        # Set counters
        COUNT = 1
        LOWS = 1
        MEDS = 1
        HIGHS = 1

        p = pyaudio.PyAudio()  # start the PyAudio class
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                        frames_per_buffer=CHUNK)  # uses default input device

        for i in range(OUTPUTS):  # Number of outputs
            COUNT = COUNT + 1
            data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
            data = data * np.hanning(len(data))  # smooth the FFT by windowing data
            fft = abs(np.fft.fft(data).real)
            fft = fft[:int(len(fft) / 2)]  # keep only first half
            freq = np.fft.fftfreq(CHUNK, 1.0 / RATE)
            freq = freq[:int(len(freq) / 2)]  # keep only first half
            freqPeak = freq[np.where(fft == np.max(fft))[0][0]] + 1
            # print("Peak frequency: %d Hz" % freqPeak)
            bars = "#" * int(500 * freqPeak / 2 ** 16)

            if LOWBORDER <= freqPeak <= MEDBORDER:
                # print("LOW PEAK: %05d hz %s" % (freqPeak, bars))
                LOWS = LOWS + 1
            elif MEDBORDER <= freqPeak <= HIGHBORDER:
                # print("MED PEAK: %05d hz %s" % (freqPeak, bars))
                MEDS = MEDS + 1
            elif HIGHBORDER <= freqPeak <= 99999:
                # print("BIG PEAK: %05d hz %s" % (freqPeak, bars))
                HIGHS = HIGHS + 1
            if COUNT == 10:
                print()
                print('LOWS ', end='')
                for x in range(0, LOWS):
                    print('#', end='')
                print()
                print('MEDS ', end='')
                for x in range(0, MEDS):
                    print('#', end='')
                print()
                print('HIGH ', end='')
                for x in range(0, HIGHS):
                    print('#', end='')
                print()
                # Reset counters
                COUNT = 1
                LOWS = 1
                HIGHS = 1
                MEDS = 1
            # Go back to top of loop
        # close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()
        # Exit program


# End of def run
if __name__ == '__main__':
    run()
