#!/bin/python
import time

from entities.movement.legs import Legs

legs = Legs(leg_0_servos=[
                1,
                61,
                63
            ],
            leg_1_servos=[
                21,
                31,
                53
            ],
            leg_2_servos=[
                61,
                63,
                111
            ],
            leg_3_servos=[
                111,
                111,
                111
            ]
            )

time.sleep(5)

while True:
    legs.move([550, 450, 850], [650, 400, 400], [400, 400, 400], [600, 400, 400], 0.1)
    legs.move([600, 450, 850], [500, 500, 500], [500, 500, 500], [500, 500, 500], 0.1)
    legs.move([650, 450, 850], [600, 600, 600], [600, 600, 600], [600, 600, 600], 0.1)
    legs.move([600, 450, 850], [500, 500, 500], [500, 500, 500], [500, 500, 500], 0.1)
