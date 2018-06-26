import sys

sys.path.insert(0, '../../src')

from entities.threading.utils import SharedObject
from entities.vision.vision import Vision

vision = Vision(SharedObject())

vision.helpers.hsv_picker.run()
