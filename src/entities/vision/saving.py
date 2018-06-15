import sys

from imutils.video import VideoStream

sys.path.insert(0, '../../../src')

import time
import datetime
from entities.vision.helpers.vision_helper import *
from tkinter import *
from threading import Thread


class Saving(object):

    def __init__(self, helpers, color_range):
        self.color_range = color_range
        self.helper = helpers.helper
        self.building_handler = helpers.json_handler

        # Saving variables
        self.save_length = 0
        self.save = False
        self.building_to_save = 0
        self.pickup_vertical = 0
        self.side = 0

    def run(self):
        print("[RUN] Starting saving...")

        # Initialize camera
        cap = VideoStream(src=0, usePiCamera=True, resolution=(320, 240)).start()
        time.sleep(0.3)  # startup
        while True:
            # Read frame from the camera
            img = cap.read()

            # Apply gaussian blue to the image
            img = cv2.GaussianBlur(img, (9, 9), 0)

            # Calculate the masks
            mask, _ = self.helper.calculate_mask(img, self.color_range)

            img_cropped, _, _, _ = self.helper.crop_to_contours(mask, img)

            # Calculate new cropped masks
            mask_cropped, valid_contours = self.helper.calculate_mask(img_cropped, self.color_range, set_contour=True)

            if cv2.waitKey(1) & 0xFF == ord('s'):
                self.show_input_fields()

            if self.save and 3 < len(valid_contours) == self.save_length:
                print("--------{}-------".format(datetime.datetime.now().time()))
                for cnt in range(len(valid_contours)):
                    print("[INFO] Valid contour: " + str(valid_contours[cnt]))
                self.save_building(valid_contours)

            # Show the created image
            cv2.imshow('Spider Cum 3000', mask_cropped)
            cv2.imshow('Original', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.stop()
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
            self.building_to_save = e2.get()
            self.pickup_vertical = e3.get()
            self.side = e4.get()
            master.quit()
            master.destroy()

        # Create forum with tkinter
        master = Tk()

        # Add labels
        Label(master, text="Amount of blocks").grid(row=0)
        Label(master, text="Building Number").grid(row=1)
        Label(master, text="Pickup vertical").grid(row=2)
        Label(master, text="Side").grid(row=3)
        e1 = Entry(master)
        e2 = Entry(master)
        e3 = Entry(master)
        e4 = Entry(master)

        # Insert last length and building to save
        e1.insert(0, self.save_length)
        e2.insert(0, self.building_to_save)
        e3.insert(0, self.pickup_vertical)
        e4.insert(0, self.side)

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)
        e3.grid(row=2, column=1)
        e4.grid(row=3, column=1)

        # Create save button
        Button(master, text='Save', command=save_entry_fields).grid(row=4, column=1, sticky=W)
        mainloop()
        self.save = True

    def save_building(self, valid_contours):
        """
        Saves the current building with the given img
        """

        time.sleep(1)

        def confirmed():
            """
            Confirms the building and saves it to a file
            """
            self.save = False
            print("[INFO] saved ", self.building_to_save)
            self.building_handler.set_save_building(valid_contours, self.building_to_save, self.pickup_vertical, self.side)
            master.destroy()

        # Create new forum
        master = Tk()
        Button(master, text='OK', command=confirmed).grid(row=0, column=1, sticky=W)
        Button(master, text='Retry', command=master.destroy).grid(row=0, column=0, sticky=W)
        mainloop()
