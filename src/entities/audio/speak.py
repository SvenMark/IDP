from entities.audio.audio import Audio
import sounddevice as sd
import soundfile as sf


class Speak(Audio):
    @staticmethod
    def play():
        data, fs = sf.read('../../../resources/test.wav', dtype="float32")
        sd.wait()
        sd.play(data, fs, device=sd.default.device)
        sd.wait()


# Just for testing purposes
def main():
    x = Speak()
    x.play()


main()


