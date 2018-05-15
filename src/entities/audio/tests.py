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

    def test_speak(self):
        self.speak.play('test.wav')
        self.speak.tts('this is a test sentence')

    def test_listen(self):
        self.listen.record()
        self.listen.record(save=True, play_recording=True, file_name='test_rec.wav')
        self.assertEqual(self.listen.get_file_path('test_rec.wav'), RESOURCES + 'test_rec.wav')
