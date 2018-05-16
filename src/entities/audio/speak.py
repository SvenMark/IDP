from audio import Audio
from gtts import gTTS
import os
import platform
import sys

class Speak(Audio):
    resources = "../../../resources/"

    def play(self, filename):
        path = self.resources + filename
        print(path)
        if platform.system() == "Windows":  # windows
            os.system("\"C:\Program Files\VideoLAN\VLC\VLC.exe\" -q --no-qt-system-tray --qt-start-minimized --play-and-exit " + path)
        else:  # linux
            os.system("mpg321 " + path)

    def tts(self, text):
        # using google text to speech api
        tts = gTTS(text=text, lang='en')
        filename = "tts.wav"
        tts.save(self.resources + filename)
        self.play(filename)


