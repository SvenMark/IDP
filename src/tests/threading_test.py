import sys

sys.path.insert(0, '../../src')

from threading import Thread
import time

speed = 200


def thread2(legs, threadname):
    global speed
    while True:
        speed += 1
        time.sleep(1)

def thread1(threadname):
    #global a       # Optional if you treat a as read-only
    while speed < 500:
        print(str(speed))

thread1 = Thread( target=thread1, args=("Thread-1", ) )
thread2 = Thread( target=thread2, args=(["gasd", "adsf"], "Thread-2", ) )

thread1.start()
thread2.start()


thread1.join()
thread2.join()
