import sys

from elements import element1, element2, element3, element4, element5, element6, element7, element8, element9, element10


def main():
    # print command line arguments
    if len(sys.argv) < 2:
        print("Please pass commandline args")
        return sys.exit(2)

    part = sys.argv[1]

    if part == "1":
        element1.run()
    elif part == "2":
        element2.run()
    elif part == "3":
        element3.run()
    elif part == "4":
        element4.run()
    elif part == "5":
        element5.run()
    elif part == "6":
        element6.run()
    elif part == "7":
        element7.run()
    elif part == "8":
        element8.run()
    elif part == "9":
        element9.run()
    elif part == "10":
        element10.run()
    else:
        print("Not a valid element")
        sys.exit(1)


if __name__ == "__main__":
    main()
