from elements.element7.helpers import Block
from elements.element7.helpers import Building
import os


# saves the current correct contours to positions.py array
def save_contour(blocks):
    try:
        filename = "buildings.py"
        output = open(filename, "a")
        output.seek(-1, os.SEEK_END)
        output.truncate()
        first = True
        for i in range(len(blocks)):
            centre = blocks[i].centre
            color = blocks[i].color
            print("Saving {}, {}..".format(i, color))

            if not first:
                output.write(",\n        Block(\"" + color + "\", (")
            else:
                output.write("        Block(\"" + color + "\", (")  # Position("color",
                first = False

            output.write("{}, {}))".format(centre[0], centre[1]))  # (cx,cy)),

        output.write('\n]')
        output.close()
        print("Successfully saved {}".format(len(blocks)))
    except ValueError:
        print("Failed to save")


buildings = [
        Building(front=[Block("red", (147, 90)),
                        Block("blue", (41, 317)),
                        Block("green", (92, 206)),
                        Block("orange", (31, 89)),
                        Block("yellow", (143, 313))],
                 back=[Block("red", (112, 175)),
                       Block("blue", (44, 304)),
                       Block("green", (36, 68)),
                       Block("orange", (184, 70)),
                       Block("yellow", (180, 307))],
                 left=[Block("red", (112, 175)),
                       Block("blue", (44, 304)),
                       Block("green", (36, 68)),
                       Block("orange", (184, 70)),
                       Block("yellow", (180, 307))],
                 right=[Block("red", (112, 175)),
                        Block("blue", (44, 304)),
                        Block("green", (36, 68)),
                        Block("orange", (184, 70)),
                        Block("yellow", (180, 307))]
                 )
]


positions = [
]