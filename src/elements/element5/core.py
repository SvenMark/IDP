from entities.vision.camera import Camera
from entities.vision.helpers import Color


def run():
    print("run element5")
    detect_bridge()


def detect_cup():

    # Initialize color ranges for detection
    color_range = [Color("beker", [30, 10, 93], [83, 87, 175])]

    cam = Camera(color_range)
    cam.run()


def detect_bridge():

    # Initialize color ranges for detection
    color_range = [Color("Brug", [0, 0, 0], [0, 255, 107]),
                   # Color("Gat", [0, 0, 0], [0, 0, 255]),
                   Color("Rand", [0, 0, 185], [0, 0, 255])]

    cam = Camera(color_range)
    cam.run()


if __name__ == '__main__':
    run()  # disabled for travis
