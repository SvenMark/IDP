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
        self.resources = "/home/pi/Desktop/IDP/src/entities/audio" + os.path.dirname(sys.modules['__main__'].__file__) + "/resources/"
        self.speak = Speak(self)
        # self.microphone_recognition = MicrophoneRecognition(self)

    def get_file_path(self, file_name):
        """
        Gets resource path
        :param file_name: The requested file
        :return: String
        """
        print(self.resources)
        return self.resources + file_name


audio = Audio()
audio.speak.play("russiananthem.mp3")