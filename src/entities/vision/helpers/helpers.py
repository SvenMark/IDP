import sys

sys.path.insert(0, '../../../src')

from entities.vision.helpers.hsvpicker import Hsv_picker
from entities.vision.helpers.vision_helper import Helper
from entities.vision.helpers.json_handler import JsonHandler


class Helpers(object):
    """
    Base class for vision
    """

    def __init__(self):
        """
        Constructor for vision class
        """
        # self.json_handler = json
        self.helper = Helper()
        self.hsv_picker = Hsv_picker(self)
