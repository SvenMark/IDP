import time
import threading
from entities.threading.utils import *
from threading import Timer

print("[RUN] " + str("test dance"))

update = False

# 0:00.21       intro
# 0:20.66       next part intro
# 0:36.04       next part intro
# 0:51.35       pitch speedup
# 0:58.17       swing start
# 1:29.24       swing drop
# 1:42.91       brake (tape stop)
# 1:43.21       rasputin original
# 1:59.43       last hit


def routine():
    global update
    update = True
    t = Timer(60 / 153, routine)
    t.start()


routine()


while True:
    if update:
        print("beat")
        update = False
