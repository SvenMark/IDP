import sounddevice as sd
import soundfile as sf

# class Audio(object):
#     """
#     Base class for audio
#     """
#     raise NotImplementedError
#
#
# class Speak(Audio):
#     """
#     Should implement methods for music output
#     """
#     raise NotImplementedError
#
#
# class Listen(Audio):
#     """
#     Should implement methods for music input
#     """
#     raise NotImplementedError


def main():
    SAMPLE_RATE = 44100
    DURATION = 5 # secondos
    CHANNELS = 2 # stereo

    data,fs = sf.read("../../resources/test.mp3", dtype="float32")
    #recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS)
    #sd.wait()
    sd.play(data,fs)
    sd.wait()


main()
