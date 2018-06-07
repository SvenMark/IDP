import json

from entities.vision.helpers.vision_helper import Color


class Range_Handler:
    def __init__(self):
        self.file_name = "output.txt"

    def set_color_range(self, color_range):
        saved_file = open(self.file_name, "w")
        json.dump(color_range, saved_file)
        saved_file.close()

    def get_color_range(self):
        color_range = []

        saved_file = open(self.file_name)
        data = json.load(saved_file)
        for p in data:
            print(p[0], p[1], p[2])
            color_range.append(Color(p[0], p[1], p[2]))

        return color_range
