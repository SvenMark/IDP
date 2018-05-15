import unittest

from entities.audio.audio import Audio
from entities.audio.listen import Listen
from entities.audio.speak import Speak
from main import RESOURCES


class CommonTestClass(unittest.TestCase):

    def setUp(self):
        self.audio = Audio()
        self.speak = Speak()
        self.listen = Listen(channels=2, duration=2)

    def test_directory(self):
        self.assertIn(self.audio.resources, RESOURCES)

    def test_instances(self):
        self.assertIsInstance(self.audio, Audio)
        self.assertIsInstance(self.speak, Speak)
        self.assertIsInstance(self.listen, Listen)
