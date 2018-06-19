from libs.ax12 import Ax12

ax12 = Ax12()

ax12.move(1, 300)

while True:
    ax12.read_load(1)
