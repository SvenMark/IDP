from entities.audio.audio import Audio
import sounddevice as sd
import win32com.client as wincl

class Speak(Audio):
    @staticmethod
    def play(filename):
        data, fs = Audio.getfile(filename)
        sd.wait()
        sd.play(data, fs, device=sd.default.device)
        sd.wait()

    @staticmethod
    def tts(text):
        speak = wincl.Dispatch("SAPI.SpVoice")
        speak.Speak(text)


def main():
    sp = Speak()
    sp.tts("Hello my name is")
    # sp.play("good")


main()
