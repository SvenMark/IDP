import sys

sys.path.insert(0, '../../../src')

from entities.vision.helpers.calibrate import Calibrate
from entities.vision.helpers.hsvpicker import Hsv_picker
from entities.vision.helpers.vision_helper import Helper


class Helpers(object):
    """
    Base class for vision
    """

    def __init__(self, color_range, img=None):
        """
        Constructor for vision class
        """
        self.hsv_picker = Hsv_picker(self, img)
        self.calibrate = Calibrate(color_range)
        self.helper = Helper()
