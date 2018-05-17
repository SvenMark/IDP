import time

from entities.movement.legs import Legs

legs = Legs(leg_0_servos=[
                1,
                13,
                14
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
    legs.move([400, 400, 400], [400, 400, 400], [400, 400, 400], [400, 400, 400], 0.1)
    legs.move([600, 600, 600], [600, 600, 600], [600, 600, 600], [600, 600, 600], 0.1)
    legs.move([500, 500, 500], [500, 500, 500], [500, 500, 500], [500, 500, 500], 0.1)
