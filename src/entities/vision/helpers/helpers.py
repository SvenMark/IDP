import sys

sys.path.insert(0, '../../../src')

from entities.vision.helpers.calibrate import Calibrate
from entities.vision.helpers.hsvpicker import Hsv_picker
from entities.vision.helpers.vision_helper import Helper


class Helpers(object):
    """
    Base class for vision
    """

    def __init__(self, color_range, img, min_block_size):
        """
        Constructor for vision class
        """
        self.hsv_picker = Hsv_picker(self, img, min_block_size)
        self.calibrate = Calibrate(color_range, min_block_size)
        self.helper = Helper()
