import sys

sys.path.insert(0, '../../../src')

from entities.vision.helpers.helpers import Helpers
from entities.vision.recognize import Recognize
from entities.vision.saving import Saving


class Vision(object):
    """
    Base class for vision
    """

    def __init__(self, color_range, saved_buildings=None, img=None, min_block_size=1000):
        """
        Constructor for vision class
        """
        self.helpers = Helpers(color_range, img, min_block_size)
        self.recognize = Recognize(color_range, min_block_size, saved_buildings)
        self.saving = Saving(color_range, min_block_size)
