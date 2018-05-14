from libs.ax12 import Ax12
import time

boris = Ax12()

ax12id = 13

boris.move(ax12id, 0)

#while True :
#	boris.move(ax12id, 500)
#	time.sleep(1)
#	boris.move(ax12id, 0)
#	time.sleep(1)
#	boris.move(ax12id, 1000)
#	time.sleep(1)
