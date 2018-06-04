import sys

sys.path.insert(0, '../../src')

from threading import Thread
import time


class Shit(object):

    def __init__(self):
        self.speed = 200
                
    def thread1(self, threadname, shit):
        while self.speed < 500:
            print(str(self.speed))

    def main(self):
        thread1 = Thread( target=self.thread1, args=(self, "Thread-1",) )

        thread1.start()
        
        while True:
            self.speed  = self.speed  + 1
            time.sleep(1)

        thread1.join()

    
shit = Shit()
shit.main()
