import sys

sys.path.insert(0, '../../../../src')

stair_3 = [
    [
        [360, 170, 890],  # L voor
        [700, 170, 890],  # R voor
        [360, 170, 890],  # L achter
        [700, 170, 890]  # R achter
    ],
    [
        [350, 390, 685],
        [675, 390, 685],
        [350, 390, 685],
        [675, 390, 685]
    ]
]

stair_2 = [
    [
        [654, 287, 767],
        [368, 296, 759],
        [654, 287, 767],
        [368, 296, 759]
    ],
    [
        [654, 579, 674],
        [367, 557, 674],
        [654, 579, 674],
        [367, 557, 674]
    ]

]

stair = [
    # Laag begin
    [
        [310, 170, 890],  # L voor
        [700, 170, 890],  # R voor
        [310, 170, 890],  # L achter
        [700, 170, 890]  # R achter
    ],
    # Laag eind
    [
        [360, 170, 890],  # L voor
        [700, 350, 890],  # R voor
        [360, 170, 890],  # L achter
        [700, 350, 890]  # R achter
    ],
    # Hoog begin
    [
        [360, 350, 890],  # L voor
        [750, 350, 890],  # R voor
        [360, 350, 890],  # L achter
        [750, 350, 890]  # R achter
    ],
    # Hoog eind
    [
        [310, 350, 890],  # L voor
        [750, 170, 890],  # R voor
        [310, 350, 890],  # L achter
        [750, 170, 890]  # R achter
    ]
]

forward = [
    [
        [630, 266, 850],
        [430, 266, 850],
        [530, 266, 850],
        [530, 266, 850]
    ],
    [
        [530, 266, 850],
        [530, 266, 850],
        [530, 266, 850],
        [530, 266, 850]
    ],
    [
        [530, 266, 850],
        [530, 266, 850],
        [630, 266, 850],
        [430, 266, 850]
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

clap = [
    [
        [287, 459, 840],
        [736, 469, 840],
        [736, 469, 840],
        [287, 459, 840]
    ],
    [
        [608, 433, 863],
        [410, 460, 845],
        [608, 433, 863],
        [410, 460, 845]
    ]
]

dablinks = [
    [
        [530, 358, 990],
        [805, 210, 990],
        [805, 210, 990],
        [530, 358, 990]
    ]
]

dabrechts = [
    [
        [530, 358, 990],
        [255, 210, 990],
        [255, 210, 990],
        [530, 358, 990]
    ]
]

shakeass = [
    [
        [530, 250, 850],
        [530, 250, 850],
        [600, 250, 850],
        [600, 250, 850]
    ],
    [
        [390, 250, 850],
        [390, 250, 850],
        [600, 250, 850],
        [600, 250, 850]
    ]
]

ballerina = [
    [
        [255, 587, 841],
        [759, 603, 812],
        [759, 603, 812],
        [255, 587, 841]
    ]
]

extendarms = [
    [
        [492, 334, 1011],
        [492, 334, 1011],
        [492, 334, 1011],
        [492, 334, 1011]
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

vagedraai = [
    [
        [511, 511, 600],
        [511, 815, 501],
        [511, 815, 501],
        [511, 815, 501]
    ],
    [
        [511, 815, 501],
        [511, 511, 600],
        [511, 815, 501],
        [511, 815, 501]
    ],
    [
        [511, 815, 501],
        [511, 815, 501],
        [511, 815, 501],
        [511, 511, 600]
    ],
    [
        [511, 815, 501],
        [511, 815, 501],
        [511, 511, 600],
        [511, 815, 501]
    ]
]

runningman = [
    [
        [370, 334, 1011],
        [665, 334, 1011],
        [665, 819, 507],
        [370, 819, 507]
    ],
    [
        [370, 812, 507],
        [665, 812, 507],
        [665, 819, 507],
        [370, 819, 507]
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
