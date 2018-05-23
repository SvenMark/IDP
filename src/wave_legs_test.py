#!/bin/python
import time
import  math

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


legs.retract(100)

time.sleep(3)

spood = 250

count = 0

while True:
    count += 0.1
    legs.move([527, 680 + math.sin(count), 998], [650, 400, 400], [400, 400, 400], [600, 400, 400], delay=0.1, speed=spood)


while True:
    legs.move([527, 680, 998], [650, 400, 400], [400, 400, 400], [600, 400, 400], delay=0.1, speed=spood)
    legs.move([527, 750, 900], [650, 400, 400], [400, 400, 400], [600, 400, 400], delay=0.1, speed=spood)
    print(str(count))
    count += 1
    if count > 8:
        spood = 120
        legs.move([315, 684, 998], [500, 500, 500], [500, 500, 500], [500, 500, 500], delay=0.1, speed=140)
        break
