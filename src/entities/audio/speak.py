import os
from gtts import gTTS
import sys
import pygame

sys.path.insert(0, '../../../src')


class Speak(object):
    """
    Speak class, implements play and text to speech
    """

    def __init__(self, audio):
        self.audio = audio
        pygame.init()
        self.anthem = pygame.mixer.Sound(self.audio.get_file_path('russiananthem.mp3'))

    def play(self, file_name):
        """
        Play audio from file
        :param file_name: Audio file
        :return: None
        """

        if file_name == 'russiananthem.mp3':
            self.anthem.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            return

        path = self.audio.get_file_path(file_name)
        print(path)
        if self.audio.windows:  # windows
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

