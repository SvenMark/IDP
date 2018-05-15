import pyaudio
import numpy as np


def run():
    print("run element4")

    np.set_printoptions(suppress=True)  # don't use scientific notation

    CHUNK = 1000  # speed of data point reading, smaller == less datapoints == faster updates
    RATE = 44100  # time resolution of the recording device (Hz)
    OUTPUTS = 12000  # number of outputs

    #Frequency borders
    LOWBORDER = 300
    MEDBORDER = 600
    HIGHBORDER = 1200

    #Set counters
    COUNT = 1
    LOWS = 1
    MEDS = 1
    HIGHS = 1

    p = pyaudio.PyAudio()  # start the PyAudio class
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                    frames_per_buffer=CHUNK)  # uses default input device

    for i in range(OUTPUTS):  # Number of outputs
        COUNT = COUNT+1
        data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
        data = data * np.hanning(len(data))  # smooth the FFT by windowing data
        fft = abs(np.fft.fft(data).real)
        fft = fft[:int(len(fft) / 2)]  # keep only first half
        freq = np.fft.fftfreq(CHUNK, 1.0 / RATE)
        freq = freq[:int(len(freq) / 2)]  # keep only first half
        freqPeak = freq[np.where(fft == np.max(fft))[0][0]] + 1
        #print("Peak frequency: %d Hz" % freqPeak)
        bars = "#" * int(500 * freqPeak / 2 ** 16)

        if LOWBORDER <= freqPeak <= MEDBORDER:
            #print("LOW PEAK: %05d hz %s" % (freqPeak, bars))
            LOWS = LOWS+1
        elif MEDBORDER <= freqPeak <= HIGHBORDER:
            #print("MED PEAK: %05d hz %s" % (freqPeak, bars))
            MEDS = MEDS + 1
        elif HIGHBORDER <= freqPeak <= 99999:
            #print("BIG PEAK: %05d hz %s" % (freqPeak, bars))
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
            #Reset counters
            COUNT = 1
            LOWS = 1
            HIGHS = 1
            MEDS = 1
        #Go back to top of loop


    # close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
