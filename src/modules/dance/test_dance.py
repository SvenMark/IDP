import time
import threading
from entities.threading.utils import *
from threading import Timer

print("[RUN] " + str("test dance"))

update = False

# 1 0:00.21       intro
# 2 0:20.66       next part intro
# 3 0:36.04       next part intro
# 4 0:51.35       pitch speedup
# 5 0:58.17       swing start
# 6 1:29.24       swing drop
# 7 1:42.91       brake (tape stop)
# 8 1:43.21       rasputin original
# 9 1:59.43       last hit


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
