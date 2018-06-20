import sys
sys.path.insert(0, '../../../src')

from entities.vision.helpers.helpers import Helpers
from entities.vision.recognize import Recognize
from entities.vision.saving import Saving


class Vision(object):
    """
    Base class for vision
    """

    def __init__(self, color_range, json, settings, shared_object, saved_buildings=None,  min_block_size=300):
        """
        Constructor for vision class
        """
        self.helpers = Helpers(color_range, min_block_size, json)
        self.recognize = Recognize(self.helpers, color_range, settings, shared_object, saved_buildings)
        self.saving = Saving(self.helpers, color_range)
