import sys

sys.path.insert(0, '../../../src')

from entities.vision.calibrate import Calibrate
from entities.vision.hsvpicker import Hsv_picker
from entities.vision.recognize import Recognize
from entities.vision.saving import Saving


class Vision(object):
    """
    Base class for vision
    """

    def __init__(self, color_range, saved_buildings=None):
        """
        Constructor for vision class
        """
        self.calibrate = Calibrate(color_range)
        self.hsv_picker = Hsv_picker()
        self.recognize = Recognize(color_range, saved_buildings)
        self.saving = Saving(color_range)
