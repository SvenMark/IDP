from entities.movement.legs import Legs


def walk_forward(legs, repeat):
    for i in range(repeat):
        legs.move(leg_0_moves=[430, 766, 850],
                  leg_1_moves=[650, 400, 400],
                  leg_2_moves=[400, 400, 400],
                  leg_3_moves=[600, 400, 400],
                  delay=0,
                  speeds=[200,200,200])
        legs.move(leg_0_moves=[430, 766, 850],
                  leg_1_moves=[650, 400, 400],
                  leg_2_moves=[400, 400, 400],
                  leg_3_moves=[600, 400, 400],
                  delay=0,
                  speeds=[200,200,200])
        legs.move(leg_0_moves=[530, 766, 850],
                  leg_1_moves=[650, 400, 400],
                  leg_2_moves=[400, 400, 400],
                  leg_3_moves=[600, 400, 400],
                  delay=0,
                  speeds=[200,200,200])
        legs.move(leg_0_moves=[530, 700, 850],
                  leg_1_moves=[650, 400, 400],
                  leg_2_moves=[400, 400, 400],
                  leg_3_moves=[600, 400, 400],
                  delay=0,
                  speeds=[200,200,200])


def walk_backward(legs, speeds):
    while True:
        legs.move(leg_0_moves=[430, 766, 850],
                  leg_1_moves=[650, 400, 400],
                  leg_2_moves=[400, 400, 400],
                  leg_3_moves=[600, 400, 400],
                  delay=0.1,
                  speeds=speeds)
        legs.move(leg_0_moves=[430, 666, 850],
                  leg_1_moves=[650, 400, 400],
                  leg_2_moves=[400, 400, 400],
                  leg_3_moves=[600, 400, 400],
                  delay=0.1,
                  speeds=speeds)
        legs.move(leg_0_moves=[530, 766, 850],
                  leg_1_moves=[650, 400, 400],
                  leg_2_moves=[400, 400, 400],
                  leg_3_moves=[600, 400, 400],
                  delay=0.1,
                  speeds=speeds)
        legs.move(leg_0_moves=[530, 666, 850],
                  leg_1_moves=[650, 400, 400],
                  leg_2_moves=[400, 400, 400],
                  leg_3_moves=[600, 400, 400],
                  delay=0.1,
                  speeds=speeds)


def enge_dab(legs, speeds):
    print("ENGE DAB")
    legs.move(leg_0_moves=[315, 678, 1023],
              leg_1_moves=[650, 400, 400],
              leg_2_moves=[400, 400, 400],
              leg_3_moves=[600, 400, 400],
              delay=0.1,
              speeds=speeds)


def wave(legs, speeds, repeat):
    for i in range(repeat):
        legs.move(leg_0_moves=[527, 680, 998],
                  leg_1_moves=[650, 400, 400],
                  leg_2_moves=[400, 400, 400],
                  leg_3_moves=[600, 400, 400],
                  delay=0.1,
                  speeds=speeds)
        legs.move(leg_0_moves=[527, 750, 900],
                  leg_1_moves=[650, 400, 400],
                  leg_2_moves=[400, 400, 400],
                  leg_3_moves=[600, 400, 400],
                  delay=0.1,
                  speeds=speeds)
