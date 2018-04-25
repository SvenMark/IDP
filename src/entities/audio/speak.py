from entities.audio.audio import Audio
import sounddevice as sd
from gtts import gTTS


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
    #sp.tts("ik ben dik en ik hou van kaas")
    sp.play("good.wav")


main()
