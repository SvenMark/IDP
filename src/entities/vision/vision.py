import sys
sys.path.insert(0, '../../../src')

from entities.vision.helpers.helpers import Helpers
from entities.vision.recognize import Recognize
from entities.vision.saving import Saving


class Vision(object):
    """
    Base class for vision
    """

    def __init__(self, color_range, saved_buildings=None, img=None,
                 settings=None, shared_object=None,):
        """
        Constructor for vision class
        """
        self.helpers = Helpers(color_range, img)
        self.recognize = Recognize(self.helpers, color_range, shared_object, saved_buildings, settings)
        self.saving = Saving(self.helpers)
