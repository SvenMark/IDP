from entities.audio.audio import Audio
import sounddevice as sd


class Listen(Audio):

    SAMPLE_RATE = 44100
    DURATION = 5  # seconds
    CHANNELS = 2  # stereo

    def record(self):
        recording = sd.rec(int(self.DURATION * self.SAMPLE_RATE), samplerate=self.SAMPLE_RATE, channels=self.CHANNELS)
        sd.wait()
        sd.play(recording)
        sd.wait()
