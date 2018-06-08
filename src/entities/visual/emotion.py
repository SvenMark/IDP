from entities.audio.speak import Speak

class BeatDetection(object):
    def __init__(self):
        self.audio = Speak()
    def success(self):
        self.audio.play("success.mp3")

    def happy(self):

    def sad(self):