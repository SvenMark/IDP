import sys

from elements import element1, element2, element3, element4, element5, element67, element6, element8, element9, \
    element10

FUNC_MAP = {
    "1": element1.core,
    "2": element2.core,
    "3": element3.core,
    "4": element4.core,
    "5": element5.core,
    "6": element67.core,
    "7": element6.core,
    "8": element8.core,
    "9": element9.core,
    "10": element10.core
}


def main():
    # print command line arguments
    if len(sys.argv) < 2:
        print("Please pass commandline args")
        return sys.exit(2)

    part = sys.argv[1]

    part_function = FUNC_MAP[part]

    # run element
    part_function.run()


if __name__ == "__main__":
    main()
