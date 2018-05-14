from audio import Audio
from gtts import gTTS
import os
import platform


class Speak(Audio):
    resources = "../../../resources/"

    def play(self, filename):
        path = self.resources + filename
        if platform.system() == "Windows":  # windows
            os.system("vlc -q --no-qt-system-tray --qt-start-minimized --play-and-exit " + path)
        else:  # linux
            os.system("mpg321 " + path)

    def tts(self, text):
        # using google text to speech api
        tts = gTTS(text=text, lang='nl')
        filename = "tts.wav"
        tts.save(self.resources + filename)
        self.play(filename)


def main():
    sp = Speak()
    sp.tts("Ik ben een robot. biep bliep")


main()
