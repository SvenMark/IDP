import time

#from elements.element6.core import detect_red

def knaben_wunderhorn(tracks):

    detect_red = False

    while True:
        tracks.forward(100, 0, 2)

        if detect_red:
            while detect_red:
                tracks.forward(100, 0, 0)
            tracks.forward(100, 30, 3)

            break

        break

    tracks.forward(100, 0, 2)
