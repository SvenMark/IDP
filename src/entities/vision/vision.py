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

    def __init__(self):
        """
        Constructor for vision class
        """
        self.calibrate = Calibrate([2, 2, 2])
        self.hsv_picker = Hsv_picker()
        self.recognize = Recognize([2, 2, 2])
        self.saving = Saving([2, 2, 2])
