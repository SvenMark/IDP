import json

from entities.vision.helpers.vision_helper import Color


class Range_Handler:
    def __init__(self):
        self.file_name = "output.txt"
        self.back_up_color_range = [Color("blue", [84, 44, 52], [153, 255, 255]),
                                    Color("yellow", [21, 110, 89], [30, 255, 255]),
                                    Color("orange", [0, 108, 104], [6, 255, 255]),
                                    Color("green", [28, 39, 0], [94, 255, 255]),
                                    Color("red", [167, 116, 89], [180, 255, 255])]

    def set_color_range(self, color_range):
        saved_file = open(self.file_name, "w")
        json.dump(color_range, saved_file)
        saved_file.close()

    def get_color_range(self):
        color_range = []

        try:
            saved_file = open(self.file_name)
            data = json.load(saved_file)
            for p in data:
                print("[INFO] Color range: " + str(p[0], p[1], p[2]))
                color_range.append(Color(p[0], p[1], p[2]))
        except FileNotFoundError:
            color_range = self.back_up_color_range

        return color_range
