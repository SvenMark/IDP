import os
import platform
import sys

sys.path.insert(0, '../../../src')

from entities.audio.speak import Speak

# from main import RESOURCES

class Audio(object):
    """
    Base class for all audio implementations
    """

    def __init__(self):
        self.windows = True if "Windows" == platform.system() else False
        self.resources = os.path.dirname(os.path.abspath(__file__)) + "/resources/"
        self.speak = Speak(self)
        # self.microphone_recognition = MicrophoneRecognition(self)

    def get_file_path(self, file_name):
        """
        Gets resource path
        :param file_name: The requested file
        :return: String
        """
        return self.resources + file_name


audio = Audio()
audio.speak.play('sad.mp3')
while True:
    pass