import sys

sys.path.insert(0, '../../../src')

from entities.vision.helpers.hsvpicker import Hsv_picker
from entities.vision.helpers.vision_helper import Helper
from entities.vision.helpers.json_handler import Json_Handler


class Helpers(object):
    """
    Base class for vision
    """

    def __init__(self, color_range, img, min_block_size):
        """
        Constructor for vision class
        """
        self.json_handler = Json_Handler()
        self.helper = Helper(min_block_size)
        self.hsv_picker = Hsv_picker(self, color_range, img)
