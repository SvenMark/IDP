import sys
sys.path.insert(0, '../../../src')


class Recognize_settings(object):
    def __init__(self):
        self.current_position = 50
        self.current_building = None
        self.current_side = None
        self.new = False

