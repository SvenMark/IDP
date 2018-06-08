import sys
import time

sys.path.insert(0, '../../../src')

from entities.vision.helpers.vision_helper import *
from tkinter import *
from threading import Thread


class Saving(object):

    def __init__(self, helpers, color_range):
        self.color_range = color_range
        self.positions = []
        self.helper = helpers.helper

        # Saving variables
        self.save_length = 0
        self.save = False
        self.building_to_save = 0
        self.last_positions = []

    def run(self):
        print("Starting saving")

        # Initialize camera
        cap = cv2.VideoCapture(0)
        while True:
            # Read frame from the camera
            ret, img = cap.read()

            # Apply gaussian blue to the image
            img = cv2.GaussianBlur(img, (9, 9), 0)

            # Calculate the masks
            mask, dead_memes = self.helper.calculate_mask(img, self.color_range)

            img4, dead_memes = self.helper.crop_to_contours(mask, img)
            # xd

            # Calculate new cropped masks
            mask_cropped, valid_contours = self.helper.calculate_mask(img4, self.color_range, set_contour=True)

            # Append the valid contours to the positions array
            for cnt in range(len(valid_contours)):
                self.positions = self.helper.append_to_positions(self.positions, valid_contours[cnt], 5, self.save_length)

            print(len(self.positions))
            if cv2.waitKey(1) & 0xFF == ord('s'):
                self.show_input_fields()

            print(len(self.positions))
            if self.save and 3 < len(self.positions) == self.save_length:
                cv2.imshow('Spider Cam Result', mask_cropped)
                for pos in range(len(self.positions)):
                    print(self.positions[pos])
                self.save_building(mask_cropped, self.positions)

            # Show the created image
            cv2.imshow('Spider Cam 3000', mask_cropped)
            cv2.imshow('Original', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def show_input_fields(self):
        """
        Shows the input fields for saving the building
        """
        def save_entry_fields():
            """
            Saves the entry fields
            """
            self.save_length = int(e1.get())
            self.save = e2.get()
            master.quit()
            master.destroy()

        # Create forum with tkinter
        master = Tk()

        # Add labels
        Label(master, text="Amount of blocks").grid(row=0)
        Label(master, text="Building Number").grid(row=1)
        e1 = Entry(master)
        e2 = Entry(master)

        # Insert last length and building to save
        e1.insert(0, self.save_length)
        e2.insert(0, self.building_to_save)

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)

        # Create save button
        Button(master, text='Save', command=save_entry_fields).grid(row=3, column=1, sticky=W)
        mainloop()
        self.save = True

    def save_building(self, img, positions):
        """
        Saves the current building with the given img
        :param img: The current frame
        """

        time.sleep(1)

        def confirmed():
            """
            Confirms the building and saves it to a file
            """
            self.save = False
            print("saved ", self.building_to_save)
            master.destroy()

            out = open("save.txt", "w")
            out.write("{} = [\n".format(self.building_to_save))

            for block in range(len(self.positions)):
                b = self.positions[block]
                print(b)
                if block == len(self.positions):
                    out.write("        ({}, {})\n".format(b[0], b[1]))
                else:
                    out.write("        ({}, {}),\n".format(b[0], b[1]))

            out.write("]\n")
            out.close()

        # Create new forum
        master = Tk()
        Button(master, text='OK', command=confirmed).grid(row=0, column=1, sticky=W)
        Button(master, text='Retry', command=master.destroy).grid(row=0, column=0, sticky=W)
        mainloop()

        self.last_positions = self.positions
