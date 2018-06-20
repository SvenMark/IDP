import sys
sys.path.insert(0, '../../../src')


class Recognize_settings(object):
    def __init__(self, grab_distance=183,
                 recognize_distance_max=250,
                 recognize_distance_min=130):

        self.current_position = 50
        self.pick_up_vertical = False
        self.grab = False
        self.new = False
        self.update = False
        self.distance = -1
        self.grab_distance = grab_distance
        self.recognize_distance_max = recognize_distance_max
        self.recognize_distance_min = recognize_distance_min

