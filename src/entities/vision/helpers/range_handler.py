import json

from entities.vision.helpers.vision_helper import Color


class Range_Handler:
    def __init__(self, file_name):
        self.file_name = file_name

    def set_color_range(self, color_range):
        json.dump(color_range, self.file_name)

    def get_color_range(self):
        color_range = []

        saved_file = open(self.file_name)
        data = json.load(saved_file)
        for p in data:
            print(p[0], p[1], p[2])
            color_range.append(Color(p[0], p[1], p[2]))

        return color_range
