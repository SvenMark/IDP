import time

from entities.movement.legs import Legs

legs = Legs()

time.sleep(5)

while True:
    legs.move(100, 200, 300, 0)
    legs.move(900, 800, 700, 0)
    legs.move(500, 500, 500, 0)
