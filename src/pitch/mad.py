import time
import sys
from threading import Thread

sys.path.insert(0, '../../../src')

from entities.audio.audio import Audio
from entities.visual.emotion import Emotion

audio = Audio()
emotion = Emotion(audio)

emotion.set_emotion("mad")
