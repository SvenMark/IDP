import sys
sys.path.insert(0, '../../../src')

from entities.threading.utils import SharedObject
from modules.cannon import core

core.run(name="Linetest", shared_object=SharedObject(), movement=None)
