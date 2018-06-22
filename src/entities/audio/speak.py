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
        file = self.audio.get_file_path('russiananthem.mp3')
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        pygame.event.wait()

    def play(self, file_name):
        """
        Play audio from file
        :param file_name: Audio file
        :return: None
        """



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

