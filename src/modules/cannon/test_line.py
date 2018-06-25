import sys

sys.path.insert(0, '../../../src')

from entities.threading.utils import SharedObject
from modules.cannon import core, line_detection

shared_object = SharedObject()
line_detection(shared_object)
