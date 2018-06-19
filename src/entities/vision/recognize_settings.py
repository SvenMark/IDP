import sys
sys.path.insert(0, '../../../src')


class Recognize_settings(object):
    def __init__(self):
        self.current_position = 50
        self.pick_up_vertical = False
        self.grab = False
        self.new = False
        self.update = False
        self.distance = -1
        self.black_detected = False

