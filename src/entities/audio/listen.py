import sounddevice as sd
import soundfile as sf

from entities.audio.audio import Audio


class Listen(Audio):
    def __init__(self, duration, channels):
        """
        Recording of audio
        :param duration: Length of recording
        :param channels: Amount of audio channels e.g. 2=stereo
        """
        super(Listen, self).__init__()
        self.sample_rate = 44100
        self.duration = duration  # seconds
        self.channels = channels  # 2=stereo

    def record(self, play_recording=False, save=False, file_name='rec.wav'):
        """
        Record audio
        :param play_recording: Set True for playback
        :param save: Set True to save as file
        :param file_name: Set filename
        :return None
        """
        recording = sd.rec(int(self.duration * self.sample_rate), samplerate=self.sample_rate, channels=self.channels)
        sd.wait()
        if play_recording:
            sd.play(recording)
            sd.wait()
        if save:
            self.save(recording, file_name)
            sd.wait()

    def save(self, recording, file_name):
        """
        Save file
        :param recording: Input of a recording
        :param file_name: File name to write
        :return: None
        """
        file_location = self.resources + file_name
        sf.write(file_location, recording, self.sample_rate)


def main():
    listen = Listen(duration=5, channels=2)
    listen.record(play_recording=False, save=False, file_name='kevin_plz.wav')


if __name__ == '__main__':
    main()
