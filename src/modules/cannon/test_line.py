from entities.threading.utils import SharedObject
from modules.cannon import core

core.run(name="test", shared_object=SharedObject(), movement=None)