from entities.movement.limb.leg import Leg

leg = Leg()

while True:
    leg.move(1000, 1000, 1000, 2)
    leg.move(500, 500, 500, 2)
    leg.move(0, 0, 0, 2)
    leg.move(500, 500, 500, 2)
