import pyaudio
import numpy as np



def run():
    print("run element4")
    CHUNK = 10000  # speed of data point reading, smaller == less datapoints == faster updates
    RATE = 44100  # time resolution of the recording device (Hz) Higher == Better accuracy
    OUTPUTS = 500  # number of outputs

    LOWLOWS = 0
    HIGHLOWS = 200  # low value borders

    LOWMEDS = 200
    HIGHMEDS = 2000  # med value borders

    LOWHIGHS = 2000
    HIGHHIGHS = 2500  # high value borders

    p = pyaudio.PyAudio()  # start the PyAudio class
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                    frames_per_buffer=CHUNK)  # uses default input device

    count = 0
    for i in range(OUTPUTS):  # Number of outputs
        data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
        left = data[0::2]
        lf = np.fft.rfft(left)

        lows = 0
        for i in range(LOWLOWS, HIGHLOWS):
            lows = lows + abs(lf)[i]
        meds = 0
        for i in range(LOWMEDS, HIGHMEDS):
            meds = meds + abs(lf)[i]
        high = 0
        for i in range(LOWHIGHS, HIGHHIGHS):
            high = high + abs(lf)[i]

        # Print de values
        # value = [int(lows), int(meds), int(high)]
        # print("Low: " + str(value[0]) + ", Med: " + str(value[1]) + ", High: " + str(value[2]))

        if lows > 9000000:
            count += 1
            print("Bass #" + str(count))

        # Mooi grafiekje van de frequenties (Libraries nodig)

        # pylab.clf()
        # pylab.figure(1)
        # b = pylab.subplot(212)
        # b.set_xscale('log')
        # b.set_xlabel('frequency [Hz]')
        # b.set_ylabel('|amplitude|')
        # b.set_ylim([0, 200000])
        # pylab.plot(abs(lf))
        # pylab.savefig('frequency.png')
        # pylab.show()

        # Mooie barchart van de frequenties (Libraries nodig)

        # pylab.ylim(0, 20000000)
        # pylab.bar(np.arange(3), value)
        # pylab.xticks(np.arange(3), ('Low', 'Med', 'High'))
        # pylab.show()

    stream.stop_stream()
    stream.close()
    p.terminate()


# End of def run
if __name__ == '__main__':
    run()
