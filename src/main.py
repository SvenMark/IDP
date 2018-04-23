import sys

from elements import element1, element2, element3, element4, element5, element6, element7, element8, element9, element10

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
