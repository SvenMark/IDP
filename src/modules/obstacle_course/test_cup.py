import sys
sys.path.insert(0, '../../../src')

from entities.threading.utils import SharedObject
from modules.obstacle_course import core

core.run(name="Cuptest", s=0, v=0, h=0, speed_factor=0, shared_object=SharedObject(), movement=None)
