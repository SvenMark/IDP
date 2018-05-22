#!/bin/python
import time

from entities.movement.legs import Legs

legs = Legs(leg_0_servos=[
                14,
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

while True:
    legs.move([430, 300, 850], [650, 400, 400], [400, 400, 400], [600, 400, 400], delay=0.1, speed=140)
    legs.move([430, 450, 850], [500, 500, 500], [500, 500, 500], [500, 500, 500], delay=0.1, speed=140)
    legs.move([630, 300, 850], [600, 600, 600], [600, 600, 600], [600, 600, 600], delay=0.1, speed=140)
    legs.move([630, 450, 850], [500, 500, 500], [500, 500, 500], [500, 500, 500], delay=0.1, speed=140)
