from entities.movement.legs import Legs
from entities.movement.tracks import Tracks

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

tracks = Tracks(track1pin=18, track2pin=13)

tracks.forward(50, 2, 1)

while True:
    tracks.forward(100, 0, 1)
    tracks.forward(20, 0, 4)
    legs.move([400, 400, 400], [400, 400, 400], [400, 400, 400], [400, 400, 400], 0.1)
    tracks.forward(0, 0, 1)
    legs.move([600, 600, 600], [600, 600, 600], [600, 600, 600], [600, 600, 600], 0.1)
    tracks.turn_right(70, 20, 0, 12)
    tracks.turn_right(10, 15, 0, 7)
    legs.move([500, 500, 500], [500, 500, 500], [500, 500, 500], [500, 500, 500], 0.1)
    tracks.stop()
