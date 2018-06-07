import os
import sys

sys.path.insert(0, '../../src')

from entities.audio.listen import Listen
from entities.audio.microphone_recognition import Microphone_recognition
from entities.audio.speak import Speak


def run():
    print("run element2")
    speak = Speak()
    speak.tts("Hello", 'en-GB-Standard-D')
    speak.play("\"C:\\Users\\renda\\Desktop\\Git\\IDP\\src\\resources\\Whats going on.mp3\"")


run()
