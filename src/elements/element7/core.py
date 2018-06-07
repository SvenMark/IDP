import sys
import threading

sys.path.insert(0, '../../../src')

from entities.vision.vision import Vision
from entities.vision.helpers.vision_helper import Color, Building, Side
from entities.vision.recognize_settings import Recognize_settings
from entities.vision.helpers.range_handler import Range_Handler
# from entities.movement.tracks import Tracks


class Core:
    def __init__(self):
        self.color_range = Range_Handler().get_color_range()
        self.tape = [Color("zwarte_tape", [0, 0, 0], [15, 35, 90])]

        self.saved_buildings = [
            Building(front=[
                (271, 213),
                (294, 209),
                (187, 109),
                (59, 321),
                (87, 160)
                ],
                     back=[

                     ],
                     left=[

                     ],
                     right=[

                     ],
                     pick_up_vertical=Side.left_right
            )
        ]

        self.img = "C:/Users/lars-/Downloads/test.jpeg"

        self.settings = Recognize_settings()
        self.vision = Vision(color_range=self.color_range,
                             saved_buildings=self.saved_buildings,
                             settings=self.settings, max_block_size=35000, min_block_size=1000)

        self.rotate_speed = 50

    def run(self):
        if len(sys.argv) > 1:
            if sys.argv[1] == "hsv_picker":
                threading.Thread(target=self.vision.helpers.hsv_picker.run).start()
            elif sys.argv[1] == "save":
                threading.Thread(target=self.vision.saving.run).start()
            else:
                threading.Thread(target=self.vision.recognize.run).start()
        else:
            threading.Thread(target=self.vision.recognize.run).start()


def main():
    core = Core()
    core.run()


if __name__ == '__main__':
    main()



#
# # TESTING
# tracks = Tracks(track_0_pin=18,
#                 track_1_pin=13,
#                 track_0_forward=22,
#                 track_0_backward=27,
#                 track_1_forward=10,
#                 track_1_backward=9)
#
# while True:
#     if settings.update:
#         settings.update = False
#         if settings.new:
#             tracks.stop()
#             print("Moving to building " + str(settings.current_building)
#                   + ", position: " + str(settings.current_position))
#
#             settings.new = False
#         else:
#             print("Rotating")
#             # acceleration 0.5 seconds for 0.5 seconds, then wait again
#             tracks.turn_left(rotate_speed, rotate_speed, 0.5, 0.5)
#             tracks.stop()
