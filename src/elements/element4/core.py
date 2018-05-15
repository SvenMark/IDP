import pyaudio
import numpy as np


def run():
    print("run element4")

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
        #print("Peak frequency: %d Hz" % freqPeak)
        bars = "#" * int(500 * freqPeak / 2 ** 16)
        print("Peak: %05d hz %s" % (freqPeak, bars))

    # close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
