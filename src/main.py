import sys

from elements.elements10 import element10
from elements.elements9 import element9
from elements.elements8 import element8
from elements.elements7 import element7
from elements.elements6 import element6
from elements.elements5 import element5
from elements.elements4 import element4
from elements.elements3 import element3
from elements.elements2 import element2
from elements.elements1 import element1

FUNC_MAP = {
    "1": element1,
    "2": element2,
    "3": element3,
    "4": element4,
    "5": element5,
    "6": element6,
    "7": element7,
    "8": element8,
    "9": element9,
    "10": element10
}


def main():
    # print command line arguments
    if len(sys.argv) < 2:
        print("Please pass commandline args")
        return sys.exit(2)

    part = sys.argv[1]

    part_function = FUNC_MAP[part]

    part_function.run()


if __name__ == "__main__":
    main()
