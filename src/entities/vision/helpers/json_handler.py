import codecs
import sys

import numpy as np

sys.path.insert(0, '../../../src')

import json
from entities.vision.helpers.vision_helper import Color, BuildingSide


class Json_Handler:
    def __init__(self):
        self.file_name_color = "output.txt"
        self.file_name_building = "save.txt"
        self.back_up_color_range = [Color("blue", [84, 44, 52], [153, 255, 255]),
                                    Color("yellow", [21, 110, 89], [30, 255, 255]),
                                    Color("orange", [0, 108, 104], [6, 255, 255]),
                                    Color("green", [28, 39, 0], [94, 255, 255]),
                                    Color("red", [167, 116, 89], [180, 255, 255])]

    def set_color_range(self, color_range):
        """
        Sets the color range into a save file
        :param color_range: The color ranges to save
        """
        # Open the file and dump the array with JSON
        saved_file = open(self.file_name_color, "w")
        json.dump(color_range, saved_file)
        saved_file.close()

    def get_color_range(self):
        """
        Gets the color range from the save file
        :return:
        """
        color_range = []

        try:
            # Open the file and load the data into an array
            saved_file = open(self.file_name_color)
            try:
                data = json.load(saved_file)
                for p in data:
                    color_range.append(Color(p[0], p[1], p[2]))

            except json.decoder.JSONDecodeError:
                color_range = self.back_up_color_range

            saved_file.close()

        except FileNotFoundError:
            color_range = self.back_up_color_range

        return color_range

    def set_save_building(self, positions, building, pick_up_vertical):
        """
        Add the building side to the buildings save file
        :param pick_up_vertical: Pick up vertical of horizontal
        :param positions: Centres of the blocks of the building
        :param building: Building number
        """
        current = self.get_save_buildings()
        exist = False
        for pos in positions:
            print([pos[0], pos[1]])

        # Check if there is a building with the same number saved already
        if len(current) > 0:
            for saved_building in current:
                print(saved_building.number)
                if saved_building.number == building:
                    print("[ERROR] Building already exists!")
                    return

        # If it is a new building, create it and add it to the array
        if not exist:
            current.append(BuildingSide(positions, pick_up_vertical, building))
            print("BuildingSide(", positions, ",", pick_up_vertical, ",", building, ")")
            print(json.dumps(current, default=lambda o: o.__dict__,
                  sort_keys=True))

        saved_file = open(self.file_name_building, "w")
        json.dump(json.dumps(current, default=lambda o: o.__dict__,
                  sort_keys=True), saved_file)
        saved_file.close()

    def get_save_buildings(self):
        """
        Gets the current buildings from the save file
        :return:
        """
        saved_building = []

        try:
            saved_file = open(self.file_name_building)
            try:
                data = json.loads(json.load(saved_file))
                for p in data:
                    saved_building.append(BuildingSide(p.get("side"), p.get("pick_up_vertical"), p.get("number")))

            except json.decoder.JSONDecodeError:
                saved_building = []

            saved_file.close()
        except FileNotFoundError:
            saved_building = []

        return saved_building
