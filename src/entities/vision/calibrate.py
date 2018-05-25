from collections import OrderedDict
from random import randint

from entities.vision.helpers import *


# print("uncomment run before starting..")


class Calibrate(object):

    def __init__(self, color_range):
        self.positions = []
        self.CALIBRATED = False
        self.calibrated_colors = []

        self.calibrating_building = [Block("orange", (267, 356)),
                                     Block("yellow", (252, 140)),
                                     Block("red", (362, 133)),
                                     Block("green", (369, 350)),
                                     Block("blue", (311, 251))]

        # Initialize color ranges for detection
        self.color_range = color_range

        self.colors = OrderedDict({"red": (0, 0, 255),
                                   "blue": (255, 0, 0),
                                   "green": (0, 255, 0),
                                   "orange": (0, 165, 255),
                                   "yellow": (0, 255, 255)})

        self.helper = Helpers()

    def run(self):
        print("run element7")
        cap = cv2.VideoCapture(0)

        while True:
            ret, img = cap.read()
            img = cv2.GaussianBlur(img, (9, 9), 0)

            if self.calibrate():
                break

            # calculate the masks
            mask = self.helper.calculate_mask(img, self.color_range, set_contour=True)

            self.draw_helper(img)
            self.draw_helper(mask)

            cv2.imshow('aa', mask)
            cv2.imshow('camservice', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def draw_helper(self, img):
        cv2.rectangle(img, (230, 65), (400, 420), (255, 255, 255), 3)
        for i in range(len(self.calibrating_building)):
            cx = self.calibrating_building[i].centre[0]
            cy = self.calibrating_building[i].centre[1]
            cv2.circle(img, (cx, cy), 2, self.colors.get(self.calibrating_building[i].color), 10)

    def calibrate(self):
        for i in range(len(self.color_range)):
            c = self.color_range[i]
            if c.color not in self.calibrated_colors:
                if not self.calibrated_color(self.positions, 50, c.color):
                    if c.upper[0] < 255:
                        c.lower[0] += 10
                        c.upper[0] += 10
                        # print("calibrating {}, [{}, {}, {}], [{}, {}, {}]".format(c.color, c.lower[0], c.lower[1], c.lower[2], c.upper[0], c.upper[1], c.upper[2]))
                    else:
                        c.lower[0] = randint(0, 30)
                        c.upper[0] = randint(0, 30)
                else:

                    self.calibrated_colors.append(c.color)
                    if len(self.calibrated_colors) >= 5:
                        print("Color(\"{}\", [{}, {}, {}], [{}, {}, {}])".format(c.color, c.lower[0], c.lower[1], c.lower[2],
                              c.upper[0], c.upper[1], c.upper[2]))
                        print("Calibrated all colors!")
                        return True
                    else:
                        print("Color(\"{}\", [{}, {}, {}], [{}, {}, {}]),".format(c.color, c.lower[0], c.lower[1], c.lower[2],
                              c.upper[0], c.upper[1], c.upper[2]))

        return False

    def calibrated_color(self, positions, sensitivity, color):
        for j in range(len(positions)):  # for each current position
            pos = positions[j]
            if pos.color == color:
                for k in range(len(self.calibrating_building)):  # and saved position
                    saved_block = self.calibrating_building[k]
                    if saved_block.color == pos.color:  # if the colors match
                        b = pos.centre
                        a = saved_block.centre

                        distance = np.linalg.norm(a - b)

                        if distance <= sensitivity:  # and the positions match
                            return True  # the color is calibrated

        return False

    def set_contours(self, mask, color, img):
        """
        Sets contours for selected masks
        :param mask: The mask to apply on the image
        :param color: Color of the mask to give contours
        :param img: Current image
        :return: New image with the contours
        """

        # Calculates the per-element bit-wise conjunction of two arrays or an array and a scalar
        img_mask = cv2.bitwise_and(img, img, mask=mask)

        # Calculate the threshhold with the mask
        ret, thresh = cv2.threshold(mask, 127, 255, 0)

        # Find the contours with the threshold
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in range(len(contours)):
            # Create a convexhull of the contour
            c = cv2.convexHull(contours[contour])

            # Check if the contour is a vlid block
            if self.helper.check_valid_convex(c, 4, 8000, 9500):
                # Image moments help you to calculate some features like center of mass of the object
                moment = cv2.moments(c)

                # Calculate the centre of mass
                cx = int(moment['m10'] / moment['m00'])
                cy = int(moment['m01'] / moment['m00'])

                # Draw the convexhull for the block
                cv2.drawContours(img_mask, [c], 0, (255, 255, 255), 3)

                # Draw a circle in the centre of the block
                cv2.circle(img_mask, (cx, cy), 2, (255, 255, 255), 5)

                # Write the color and position of the block
                cv2.putText(img_mask, color, (cx - 15, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                cv2.putText(img_mask, str((cx, cy)), (cx - 30, cy + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

                # Append the new block to the global POSITIONS array
                self.positions = self.helper.append_to_positions(self.positions, Block(color, (cx, cy)))

        # Return the new mask
        return img_mask


def main():
    color_range = [Color("orange", [0, 100, 100], [12, 255, 255]),
                   Color("yellow", [24, 100, 100], [35, 255, 255]),
                   Color("red", [26, 0, 17], [69, 131, 190]),
                   Color("green", [71, 89, 11], [83, 202, 120]),
                   Color("blue", [99, 152, 128], [119, 228, 174])]

    cal = Calibrate(color_range)
    cal.run()


if __name__ == '__main__':
    main()  # disabled for travis

