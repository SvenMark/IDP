from entities.movement.legs import Legs


def walk_forward(legs, speed):
    while True:
        legs.move(leg_0_moves=[430, 766, 850],
                  leg_1_moves=[650, 400, 400],
                  leg_2_moves=[400, 400, 400],
                  leg_3_moves=[600, 400, 400],
                  delay=0.1,
                  speed=speed)
        legs.move(leg_0_moves=[430, 666, 850],
                  leg_1_moves=[650, 400, 400],
                  leg_2_moves=[400, 400, 400],
                  leg_3_moves=[600, 400, 400],
                  delay=0.1,
                  speed=speed)
        legs.move(leg_0_moves=[530, 766, 850],
                  leg_1_moves=[650, 400, 400],
                  leg_2_moves=[400, 400, 400],
                  leg_3_moves=[600, 400, 400],
                  delay=0.1,
                  speed=speed)
        legs.move(leg_0_moves=[530, 666, 850],
                  leg_1_moves=[650, 400, 400],
                  leg_2_moves=[400, 400, 400],
                  leg_3_moves=[600, 400, 400],
                  delay=0.1,
                  speed=speed)


def walk_backward(legs, speed):
    while True:
        legs.move(leg_0_moves=[430, 766, 850],
                  leg_1_moves=[650, 400, 400],
                  leg_2_moves=[400, 400, 400],
                  leg_3_moves=[600, 400, 400],
                  delay=0.1,
                  speed=speed)
        legs.move(leg_0_moves=[430, 666, 850],
                  leg_1_moves=[650, 400, 400],
                  leg_2_moves=[400, 400, 400],
                  leg_3_moves=[600, 400, 400],
                  delay=0.1,
                  speed=speed)
        legs.move(leg_0_moves=[530, 766, 850],
                  leg_1_moves=[650, 400, 400],
                  leg_2_moves=[400, 400, 400],
                  leg_3_moves=[600, 400, 400],
                  delay=0.1,
                  speed=speed)
        legs.move(leg_0_moves=[530, 666, 850],
                  leg_1_moves=[650, 400, 400],
                  leg_2_moves=[400, 400, 400],
                  leg_3_moves=[600, 400, 400],
                  delay=0.1,
                  speed=speed)


def enge_dab(legs, speed):
    print("ENGE DAB")
    legs.move(leg_0_moves=[315, 678, 1023],
              leg_1_moves=[650, 400, 400],
              leg_2_moves=[400, 400, 400],
              leg_3_moves=[600, 400, 400],
              delay=0.1,
              speed=speed)
