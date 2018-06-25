import time
import threading
from entities.threading.utils import *
from threading import Timer

print("[RUN] " + str("test dance"))

update = False


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
