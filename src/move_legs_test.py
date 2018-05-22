#!/bin/python
import time

from entities.movement.legs import Legs
from entities.movement.sequences.walking_sequences import *

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

time.sleep(2)


legs.deploy(150)

count = 0

spood = 200

while True:
    if spood >= 10:
        spood -= 10
    legs.move([430, 766, 850], [650, 400, 400], [400, 400, 400], [600, 400, 400], delay=0.1, speed=spood)
    legs.move([430, 666, 850], [500, 500, 500], [500, 500, 500], [500, 500, 500], delay=0.1, speed=spood)
    legs.move([530, 766, 850], [600, 600, 600], [600, 600, 600], [600, 600, 600], delay=0.1, speed=spood)
    legs.move([530, 666, 850], [500, 500, 500], [500, 500, 500], [500, 500, 500], delay=0.1, speed=spood)
    print(str(count))
    count += 1
