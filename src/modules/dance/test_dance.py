import time
import threading
from entities.threading.utils import *
from threading import Timer
from entities.audio.audio import Audio

from datetime import datetime

print("[RUN] " + str("test dance"))

# 0 0:00.21       intro
# 1 0:20.66       next part intro
# 2 0:36.04       next part intro
# 3 0:51.35       pitch speedup
# 4 0:58.17       swing start
# 5 1:29.24       swing drop
# 6 1:42.91       brake (tape stop)
# 7 1:43.21       rasputin original
# 8 1:59.43       last hit

m = 60
begin_time = datetime.now()

parts = [0.21, 20.66, 36.04, 51.35, 58.17, m + 29.24, m + 42.91, m + 43.21, m + 59.43]
current_part = -1


def routine():
    global current_part
    delta = datetime.now() - begin_time
    for i in range(len(parts)):
        if delta.seconds > parts[i]:
            current_part = i
        else:
            break
    t = Timer(0.05, routine)
    t.start()


audio = Audio()

time.sleep(0.5)

while audio.playing:
    pass

audio.play('Rasputin.mp3')

while not audio.playing:
    pass

routine()

while True:
    print(str(current_part))
    time.sleep(0.1)
