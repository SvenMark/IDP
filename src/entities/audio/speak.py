import os
from gtts import gTTS
import sys
import threading
import pygame

sys.path.insert(0, '../../../src')


class Speak(object):
    """
    Speak class, implements play and text to speech
    """

    def __init__(self, audio):
        self.audio = audio
        pygame.init()
        pygame.mixer.init()
        print("Initialised Audio Speak")

    def play(self, file_name):
        """
        Play audio from file
        :param file_name: Audio file
        :return: None
        """

        threading.Thread(target=self.play_threaded, args=(file_name, )).start()

    def play_threaded(self, file_name):
        print("Play")
        pygame.mixer.music.load(self.audio.get_file_path(file_name))
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
