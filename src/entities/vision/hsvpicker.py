from tkinter import *
import numpy as np
import cv2
import sys

sys.path.insert(0, '../../../src')


class Hsv_picker:

    def __init__(self):
        self.createtrackbars("1")
        self.color_to_save = ""

    def run(self):
        print("run hsvpicker")
        cap = cv2.VideoCapture(0)

        while True:
            ret, img = cap.read()
            img = cv2.GaussianBlur(img, (9, 9), 0)

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
                if area > 100:
                    cv2.drawContours(output, [cnt], -1, (255, 255, 255), 5)

            cv2.imshow('hsv-picker', output)

            if cv2.waitKey(1) & 0xFF == ord('s'):
                self.savehigherlower(lowh, lows, lowv, highh, highs, highv)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    def calculate_mask(name, mask, img):
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
        cv2.namedWindow(name)

        # create trackbars for lower
        cv2.createTrackbar('Low H', name, 90, 180, self.nothing)
        cv2.createTrackbar('Low S', name, 100, 255, self.nothing)
        cv2.createTrackbar('Low V', name, 100, 255, self.nothing)

        # create trackbars for higher
        cv2.createTrackbar('High H', name, 120, 180, self.nothing)
        cv2.createTrackbar('High S', name, 255, 255, self.nothing)
        cv2.createTrackbar('High V', name, 255, 255, self.nothing)

    def savehigherlower(self, lowh, lows, lowv, highh, highs, highv):
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
