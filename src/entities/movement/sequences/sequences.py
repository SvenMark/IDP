import sys

sys.path.insert(0, '../../../../src')

current_speed = 90

forward = [
    # omhoog
    [
        [530, 200, 850],
        [530, 266, 850],
        [530, 200, 850],
        [530, 266, 850],
    ],
    # vooruit hoog
    [
        [530 - current_speed, 200, 850],
        [530, 266, 850],
        [530 - current_speed, 200, 850],
        [530, 266, 850],
    ],
    # vooruit laag
    [
        [530 - current_speed, 266, 850],
        [530 - current_speed, 200, 850],
        [530 - current_speed, 266, 850],
        [530 - current_speed, 200, 850],
    ],
    # deployed position
    [

    ],
    [

    ],
    [
        [530, 266, 850],
        [530, 266, 850],
        [530, 266, 850],
        [530, 266, 850]
    ]
]

backward = [
    [
        [630, 266, 850],
        [630, 266, 850],
        [630, 266, 850],
        [630, 266, 850]
    ],
    [
        [630, 200, 850],
        [630, 200, 850],
        [630, 200, 850],
        [630, 200, 850]
    ],
    [
        [530, 200, 850],
        [530, 200, 850],
        [530, 200, 850],
        [530, 200, 850]
    ],
    [
        [530, 266, 850],
        [530, 266, 850],
        [530, 266, 850],
        [530, 266, 850]
    ]
]

dab = [
    [
        [315, 178, 1023],
        [315, 178, 1023],
        [315, 178, 1023],
        [315, 178, 1023]
    ]
]

wave = [
    [
        [527, 180, 998],
        [527, 180, 998],
        [527, 180, 998],
        [527, 180, 998]
    ],
    [
        [527, 250, 900],
        [527, 250, 900],
        [527, 250, 900],
        [527, 250, 900]
    ]
]

pull = [
    [
        [530, 230, 640],
        [530, 230, 640],
        [530, 230, 640],
        [530, 230, 640]
    ],
    [
        [530, 150, 640],
        [530, 150, 640],
        [530, 150, 640],
        [530, 150, 640]
    ],
    [
        [530, 150, 750],
        [530, 150, 750],
        [530, 150, 750],
        [530, 150, 750]
    ],
    [
        [530, 340, 970],
        [530, 340, 970],
        [530, 340, 970],
        [530, 340, 970]
    ]
]

push = [
    [
        [530, 150, 750],
        [530, 150, 750],
        [530, 150, 750],
        [530, 150, 750]
    ],
    [
        [530, 150, 640],
        [530, 150, 640],
        [530, 150, 640],
        [530, 150, 640]

    ],
    [
        [530, 230, 640],
        [530, 230, 640],
        [530, 230, 640],
        [530, 230, 640]
    ],
    [
        [530, 340, 970],
        [530, 340, 970],
        [530, 340, 970],
        [530, 340, 970]
    ]
]

march = [
    [
        [530, 100, 570],
        [530, 100, 570],
        [530, 100, 570],
        [530, 100, 570]
    ],
    [
        [530, 230, 690],
        [530, 230, 690],
        [530, 230, 690],
        [530, 230, 690]
    ]
]

hood_handshake = [
    [
        [530, 180, 950],
        [530, 180, 950],
        [530, 180, 950],
        [530, 180, 950]
    ],
    [
        [420, 180, 950],
        [420, 180, 950],
        [420, 180, 950],
        [420, 180, 950]
    ],
    [
        [640, 180, 950],
        [640, 180, 950],
        [640, 180, 950],
        [640, 180, 950]
    ],
    [
        [530, 180, 950],
        [530, 180, 950],
        [530, 180, 950],
        [530, 180, 950]
    ],
    [
        [530, 830, 855],
        [530, 830, 855],
        [530, 830, 855],
        [530, 830, 855]
    ],
    [
        [530, 940, 790],
        [530, 940, 790],
        [530, 940, 790],
        [530, 940, 790]
    ],
    [
        [530, 830, 855],
        [530, 830, 855],
        [530, 830, 855],
        [530, 830, 855]
    ],
    [
        [530, 800, 580],
        [530, 800, 580],
        [530, 800, 580],
        [530, 800, 580]
    ],
    [
        [530, 1020, 800],
        [530, 1020, 800],
        [530, 1020, 800],
        [530, 1020, 800]
    ],
    [
        [530, 700, 470],
        [530, 700, 470],
        [530, 700, 470],
        [530, 700, 470]
    ]
]
