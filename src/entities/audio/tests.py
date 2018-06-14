import unittest

from entities.audio.audio import Audio
from entities.audio.listen import Listen
from entities.audio.speak import Speak
from main import RESOURCES


class CommonTestClass(unittest.TestCase):

    def setUp(self):
        """
        Setup objects
        :return: None
        """
        self.audio = Audio()
        self.speak = Speak()
        self.listen = Listen(channels=2, duration=2)

    def test_directory(self):
        """
        Test if directory can be found
        :return: None
        """
        self.assertIn(self.audio.resources, RESOURCES)

    def test_instances(self):
        """
        Test if instances have been created
        :return: None
        """
        self.assertIsInstance(self.audio, Audio)
        self.assertIsInstance(self.speak, Speak)
        self.assertIsInstance(self.listen, Listen)
