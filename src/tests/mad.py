import time
import sys
from threading import Thread

sys.path.insert(0, '../../../src')

from entities.audio.audio import Audio
from entities.visual.emotion import Emotion

audio = Audio()
emotion = Emotion(audio)

emotion.set_emotion("mad")
time.sleep(5)
emotion.set_emotion("happy")
time.sleep(5)
emotion.set_emotion("sad")
time.sleep(11)
emotion.set_emotion("pain")
time.sleep(5)
emotion.set_emotion("confused")
time.sleep(5)
emotion.set_emotion("searching")
time.sleep(5)