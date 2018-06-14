import os

from gtts import gTTS

from entities.audio.audio import Audio


class Speak(Audio):
    """
    Speak class, implements play and text to speech
    """

    def __init__(self):
        super(Speak, self).__init__()

    def play(self, file_name):
        """
        Play audio from file
        :param file_name: Audio file
        :return: None
        """
        path = Audio.get_file_path(self, file_name)
        print(path)
        if self.windows:  # windows
            os.system("\"C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe\" -I null -q --no-qt-system-tray --qt-start-minimized --play-and-exit " + path)
        else:  # linux
            os.system("mpg321 " + path)

    def tts(self, text, lan):
        """
        Speak using text to speech
        :param text: Input text
        :return: None
        """
        # using google text to speech api
        tts = gTTS(text=text, lang=lan)
        filename = "tts.wav"
        tts.save(filename)
        self.play(filename)


def main():
    sp = Speak()
    sp.play("gay.mp3")


if __name__ == '__main__':
    main()

