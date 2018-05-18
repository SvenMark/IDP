import os

from gtts import gTTS

from entities.audio.audio import Audio


class Speak(Audio):
    """
    Speak class
    """

    def __init__(self):
        super(Speak, self).__init__()

    def play(self, file_name):
        """
        Play audio from file
        :param file_name: Audio file
        :return: None
        """
        path = self.get_file_path(file_name)
        if self.windows:  # windows
            os.system("vlc -q --no-qt-system-tray --qt-start-minimized --play-and-exit " + path)
        else:  # linux
            os.system("mpg321 " + path)

    def tts(self, text):
        """
        Speak using text to speech
        :param text: Input text
        :return: None
        """
        # using google text to speech api
        tts = gTTS(text=text, lang='en')
        filename = "tts.wav"
        tts.save(self.get_file_path(filename))
        self.play(filename)


spoke = Speak()

spoke.tts("Hello")


def main():
    sp = Speak()
    sp.tts("Ik ben een robot. biep bliep")


if __name__ == '__main__':
    main()

