from libs.ax12 import Ax12

servo = Ax12()

servo.factory_reset(1, True)
servo.set_id(1, 2)
