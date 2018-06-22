import sys

sys.path.insert(0, '../../../src')

from entities.threading.utils import SharedObject
from modules.obstacle_course import stairdetector, detect_cup, detect_cup_old

shared_object = SharedObject()

stairdetector(shared_object)
# detect_cup(shared_object)
