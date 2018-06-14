import codecs
import sys

import numpy as np

sys.path.insert(0, '../../../src')

import json
from entities.vision.helpers.vision_helper import Color, Building
from entities.vision.helpers.vision_helper import Side


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
        saved_file = open(self.file_name_color, "w")
        json.dump(color_range, saved_file)
        saved_file.close()

    def get_color_range(self):
        color_range = []

        try:
            saved_file = open(self.file_name_color)
            data = json.load(saved_file)
            for p in data:
                color_range.append(Color(p[0], p[1], p[2]))
            saved_file.close()
        except FileNotFoundError:
            color_range = self.back_up_color_range

        return color_range

    def set_save_building(self, positions, building, side):
        current = self.get_save_buildings()
        exist = False
        if len(current) > 0:
            for saved_building in current:
                print(saved_building.number)
                if saved_building.number == building:
                    exist = True
                    if side == 0:
                        saved_building.front = positions
                    elif side == 1:
                        saved_building.back = positions
                    elif side == 2:
                        saved_building.left = positions
                    elif side == 3:
                        saved_building.right = positions

        if not exist:
            new_building = Building(front=[[]], back=[[]], left=[[]], right=[[]], pick_up_vertical=False, number=building)
            if side == Side.front:
                new_building.front = positions
            elif side == Side.back:
                new_building.back = positions
            elif side == Side.left:
                new_building.left = positions
            elif side == Side.right:
                new_building.right = positions
            current.append(new_building)

        saved_file = open(self.file_name_building, "w")
        for bl in current:
            print(bl.front)
        json.dump(current[0].front, saved_file)  # Building([[0,0]] , [[1,3]], .. , .. , .. , False, 0)
        saved_file.close()

    def get_save_buildings(self):
        saved_building = []

        try:
            saved_file = open(self.file_name_building)
            try:
                data = json.load(saved_file)
                for p in data:
                    saved_building.append(Building(p[0], p[1], p[2], p[3], p[4], p[5]))

                saved_file.close()
            except json.decoder.JSONDecodeError:
                saved_building = []
        except FileNotFoundError:
            saved_building = []

        return saved_building
