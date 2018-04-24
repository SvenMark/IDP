from entities.audio.audio import Audio
import sounddevice as sd
import soundfile as sf


class Speak(Audio):
    data, fs = sf.read('../../../resources/test.wav', dtype="float32")
    sd.wait()
    sd.play(data, fs, device=sd.default.device)
    sd.wait()


def main():
    data, fs = sf.read('../../../resources/test.wav', dtype="float32")
    sd.wait()
    sd.play(data, fs, device=sd.default.device)
    sd.wait()

