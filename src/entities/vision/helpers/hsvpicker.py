from tkinter import *
import numpy as np
import cv2
import sys

sys.path.insert(0, '../../../src')


class Hsv_picker:

    def __init__(self, helpers, img):
        self.color_to_save = ""
        self.img = cv2.imread(img)
        self.helper = helpers.helper

    def run(self):
        self.createtrackbars("1")
        print("run hsvpicker")
        cap = cv2.VideoCapture(0)

        while True:
            if self.img is not None:
                img = self.img
            else:
                ret, img = cap.read()
            img = cv2.GaussianBlur(img, (9, 9), 0)

            img = self.helper.image_resize(img, 500)

            lowh = cv2.getTrackbarPos('Low H', '1')
            lows = cv2.getTrackbarPos('Low S', '1')
            lowv = cv2.getTrackbarPos('Low V', '1')

            highh = cv2.getTrackbarPos('High H', '1')
            highs = cv2.getTrackbarPos('High S', '1')
            highv = cv2.getTrackbarPos('High V', '1')

            # Hsv Mask
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower = np.array([lowh, lows, lowv])
            higher = np.array([highh, highs, highv])
            mask = cv2.inRange(hsv, lower, higher)

            output = cv2.bitwise_and(img, img, mask=mask)

            ret, thresh = cv2.threshold(mask, 127, 255, 0)
            im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > self.helper.min_block_size:
                    cv2.drawContours(output, [cnt], -1, (255, 255, 255), 5)

            cv2.imshow('hsv-picker', output)
            cv2.imshow('original', img)

            if cv2.waitKey(1) & 0xFF == ord('s'):
                self.savehigherlower(lowh, lows, lowv, highh, highs, highv)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    def calculate_mask(name, mask, img):
        """
        Calculates mask with given ranges
        :param name: Form name to get the values from
        :param mask: Mask to apply to
        :param img: Image to apply mask to
        """
        lowh = cv2.getTrackbarPos('Low H', name)
        lows = cv2.getTrackbarPos('Low S', name)
        lowv = cv2.getTrackbarPos('Low V', name)

        highh = cv2.getTrackbarPos('High H', name)
        highs = cv2.getTrackbarPos('High S', name)
        highv = cv2.getTrackbarPos('High V', name)

        # Hsv Mask
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([lowh, lows, lowv])
        higher = np.array([highh, highs, highv])
        mask += cv2.inRange(hsv, lower, higher)
        return mask

    def createtrackbars(self, name):
        """
        Create trackbar form
        :param name: Name of form
        """
        cv2.namedWindow(name)

        # create trackbars for lower
        cv2.createTrackbar('Low H', name, 0, 180, self.nothing)
        cv2.createTrackbar('Low S', name, 0, 255, self.nothing)
        cv2.createTrackbar('Low V', name, 0, 255, self.nothing)

        # create trackbars for higher
        cv2.createTrackbar('High H', name, 180, 180, self.nothing)
        cv2.createTrackbar('High S', name, 255, 255, self.nothing)
        cv2.createTrackbar('High V', name, 255, 255, self.nothing)

    def savehigherlower(self, lowh, lows, lowv, highh, highs, highv):
        """
        Starts form for getting the color of the saving color
        """
        def get_color():
            self.color_to_save = e1.get()
            master.destroy()

        master = Tk()
        Label(master, text="Color").grid(row=0)
        e1 = Entry(master)

        e1.grid(row=0, column=1)

        Button(master, text='Save', command=get_color).grid(row=3, column=1, sticky=W)
        mainloop()

        try:
            result = "Color(\"{}\", [{}, {}, {}], [{}, {}, {}]),\n".format(self.color_to_save, lowh, lows, lowv, highh,
                                                                           highs, highv)
            text_file = open("Output.txt", "a")  # Color("orange", [0, 69, 124], [13, 255, 255])
            text_file.write(result)
            text_file.close()
            print("Saved settings", result)
        except ValueError:
            print(ValueError)

    def nothing(self, x):
        pass


def main():
    hsv = Hsv_picker()
    hsv.run()


if __name__ == '__main__':
    main()  # disabled for travis
