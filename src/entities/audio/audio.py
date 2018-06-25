import os
import platform
import sys
import pygame
from gtts import gTTS
import time

sys.path.insert(0, '../../../src')


class Audio(object):
    """
    Base class for all audio implementations
    """

    def __init__(self):
        self.resources = os.path.dirname(os.path.abspath(__file__)) + "/resources/"
        pygame.init()
        pygame.mixer.init()
        print("Initialised Audio Speak")

    def get_file_path(self, file_name):
        """
        Gets resource path
        :param file_name: The requested file
        :return: String
        """
        return self.resources + file_name

    def play(self, file_name):
        """
        Play audio from file
        :param file_name: Audio file
        :return: None
        """
        pygame.mixer.music.load(self.get_file_path(file_name))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

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

