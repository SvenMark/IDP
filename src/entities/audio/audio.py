import platform
import sys

from entities.audio.beat_detection import BeatDetection
from entities.audio.speak import Speak

sys.path.insert(0, '../../../src')


# from main import RESOURCES


class Audio(object):
    """
    Base class for all audio implementations
    """

    def __init__(self):
        self.windows = True if "Windows" == platform.system() else False
        self.resources = "../../resources/"
        self.speak = Speak(self)
        # self.microphone_recognition = MicrophoneRecognition(self)
        self.beat_detection = BeatDetection()

    def get_file_path(self, file_name):
        """
        Gets resource path
        :param file_name: The requested file
        :return: String
        """
        return self.resources + file_name
