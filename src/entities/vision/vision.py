import sys
sys.path.insert(0, '../../../src')

from entities.vision.helpers.helpers import Helpers
from entities.vision.recognize import Recognize
from entities.vision.recognize_settings import Recognize_settings
from entities.vision.saving import Saving


class Vision(object):
    """
    Base class for vision
    """

    def __init__(self, shared_object):
        """
        Constructor for vision class
        """
        self.helpers = Helpers()
        self.settings = Recognize_settings()
        self.recognize = Recognize(helpers=self.helpers, settings=self.settings, shared_object=shared_object)
        self.saving = Saving(self.helpers)
