# import numpy as np
# import os
#
#
# class Color:
#     def __init__(self, lower, upper):
#         self.lower = np.array(lower)
#         self.upper = np.array(upper)
#
#
# class Block:
#     def __init__(self, color, centre):
#         self.color = color
#         self.centre = centre
#
#
# class ColorRange:
#     def __init__(self, color, color_range):
#         self.color = color
#         self.range = color_range
#
#
# class Building:
#     def __init__(self, front, back, left, right):
#         self.front = front
#         self.back = back
#         self.left = left
#         self.right = right
#
#
# class SavedBuildings:
#     buildings = [
#         Building(front=[Block("red", (33, 317)),
#                         Block("blue", (146, 311)),
#                         Block("orange", (34, 91)),
#                         Block("yellow", (86, 207)),
#                         Block("blue", (141, 90))],
#                  back=[Block("blue", (31, 316)),
#                        Block("green", (86, 209)),
#                        Block("orange", (30, 91)),
#                        Block("yellow", (144, 317))],
#                  left=[Block("red", (112, 175)),
#                        Block("blue", (44, 304)),
#                        Block("green", (36, 68)),
#                        Block("orange", (184, 70)),
#                        Block("yellow", (180, 307))],
#                  right=[Block("red", (112, 175)),
#                         Block("blue", (44, 304)),
#                         Block("green", (36, 68)),
#                         Block("orange", (184, 70)),
#                         Block("yellow", (180, 307))]
#                  )
#     ]
#
#     # saves the current correct contours to positions.py array
#     @staticmethod
#     def save_contour(blocks):
#         try:
#             filename = "buildings.py"
#             output = open(filename, "a")
#             output.seek(-1, os.SEEK_END)
#             output.truncate()
#             first = True
#             for i in range(len(blocks)):
#                 centre = blocks[i].centre
#                 color = blocks[i].color
#                 print("Saving {}, {}..".format(i, color))
#
#                 if not first:
#                     output.write(",\n        Block(\"" + color + "\", (")
#                 else:
#                     output.write("        Block(\"" + color + "\", (")  # Position("color",
#                     first = False
#
#                 output.write("{}, {}))".format(centre[0], centre[1]))  # (cx,cy)),
#
#             output.write('\n]')
#             output.close()
#             print("Successfully saved {}".format(len(blocks)))
#         except ValueError:
#             print("Failed to save")
#
