import sys
sys.path.insert(0, '../../../src')

from entities.threading.utils import SharedObject
from modules.obstacle_course import core

core.run(name="Cuptest", shared_object=SharedObject(), movement=None)
