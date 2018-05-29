def walk_forward(legs, speeds):
    legs.move(leg_0_moves=[530, 700, 850],
              leg_1_moves=[650, 400, 400],
              leg_2_moves=[400, 400, 400],
              leg_3_moves=[600, 400, 400],
              delay=0,
              speeds=speeds)
    legs.move(leg_0_moves=[430, 766, 850],
              leg_1_moves=[650, 400, 400],
              leg_2_moves=[400, 400, 400],
              leg_3_moves=[600, 400, 400],
              delay=0,
              speeds=speeds)
    legs.move(leg_0_moves=[430, 766, 850],
              leg_1_moves=[650, 400, 400],
              leg_2_moves=[400, 400, 400],
              leg_3_moves=[600, 400, 400],
              delay=0,
              speeds=speeds)
    legs.move(leg_0_moves=[530, 766, 850],
              leg_1_moves=[650, 400, 400],
              leg_2_moves=[400, 400, 400],
              leg_3_moves=[600, 400, 400],
              delay=0,
              speeds=speeds)


def walk_forward_repeat(legs, speeds, repeat):
    for i in range(repeat):
        walk_forward(legs, speeds)


def walk_backward(legs, speeds):
    legs.move(leg_0_moves=[530, 766, 850],
              leg_1_moves=[650, 400, 400],
              leg_2_moves=[400, 400, 400],
              leg_3_moves=[600, 400, 400],
              delay=0,
              speeds=speeds)
    legs.move(leg_0_moves=[630, 766, 850],
              leg_1_moves=[650, 400, 400],
              leg_2_moves=[400, 400, 400],
              leg_3_moves=[600, 400, 400],
              delay=0,
              speeds=speeds)
    legs.move(leg_0_moves=[530, 700, 850],
              leg_1_moves=[650, 400, 400],
              leg_2_moves=[400, 400, 400],
              leg_3_moves=[600, 400, 400],
              delay=0,
              speeds=speeds)
    legs.move(leg_0_moves=[530, 766, 850],
              leg_1_moves=[650, 400, 400],
              leg_2_moves=[400, 400, 400],
              leg_3_moves=[600, 400, 400],
              delay=0,
              speeds=speeds)


def walk_backward_repeat(legs, speeds, repeat):
    for i in range(repeat):
        walk_backward(legs, speeds)


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


def lol(legs, speeds, repeat):
    for i in range(repeat):
        legs.move(leg_0_moves=[315, 678, 1023],
                  leg_1_moves=[650, 400, 400],
                  leg_2_moves=[400, 400, 400],
                  leg_3_moves=[600, 400, 400],
                  delay=0.1,
                  speeds=speeds)
        legs.move(leg_0_moves=[729, 821, 966],
                  leg_1_moves=[650, 400, 400],
                  leg_2_moves=[400, 400, 400],
                  leg_3_moves=[600, 400, 400],
                  delay=0.1,
                  speeds=speeds)


def pull(legs, speeds, ):
    legs.move(leg_0_moves=[530, 766, 850],
              leg_1_moves=[650, 400, 400],
              leg_2_moves=[400, 400, 400],
              leg_3_moves=[600, 400, 400],
              delay=0.1,
              speeds=speeds)
    legs.move(leg_0_moves=[530, 700, 800],
              leg_1_moves=[650, 400, 400],
              leg_2_moves=[400, 400, 400],
              leg_3_moves=[600, 400, 400],
              delay=0.1,
              speeds=speeds)