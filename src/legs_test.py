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


legs.retract(190)

time.sleep(4)

legs.deploy(190)

time.sleep(3)


legs.retract(200)

time.sleep(2)

legs.deploy(150)

legs.move([715, 684, 998], [0,0,0], [0,0,0], [0,0,0], 0.1, 110 )

time.sleep(2)

legs.deploy(150)


while True:
    print("hi")

while True:
    legs.move([430, 766, 850], [650, 400, 400], [400, 400, 400], [600, 400, 400], delay=0.1, speed=140)
    legs.move([430, 600, 850], [500, 500, 500], [500, 500, 500], [500, 500, 500], delay=0.1, speed=140)
    legs.move([630, 766, 850], [600, 600, 600], [600, 600, 600], [600, 600, 600], delay=0.1, speed=140)
    legs.move([630, 600, 850], [500, 500, 500], [500, 500, 500], [500, 500, 500], delay=0.1, speed=140)
