from audio import Audio
import sounddevice as sd
from gtts import gTTS
import os


class Speak(Audio):
    @staticmethod
    def play(filename):
        data, fs = Audio.getfile(filename)
        sd.wait()
        sd.play(data, fs, device=sd.default.device)
        sd.wait()

    def tts(self, text):
        # using google text to speech api
        tts = gTTS(text=text, lang='nl')
        tts.save('../../../resources/good.wav')
        # self.play("good.wav")


def main():
    sp = Speak()
    sp.tts("Ik ben een robot. biep bliep")
    #sp.play("test.wav")
    os.system("mpg321 ../../../resources/good.wav")


main()
