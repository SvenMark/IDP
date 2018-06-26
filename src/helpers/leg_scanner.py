import sys

sys.path.insert(0, '../../src')

from libs.ax12 import Ax12

tester = Ax12()

legs = [
    [21, 41, 52],
    [16, 17, 18],
    [61, 62, 63],
    [6, 14, 15]
]

i = 0
for leg in legs:
    leg_positions = []
    for ax_id in leg:
        positions = []
        try:
            positions.append(tester.read_position(ax_id))
        except:
            print("Servo with id: {}, has not responded".format(ax_id))
        leg_positions.append(positions)
        i = i + 1
    print("Leg " +  str(i) + " servos: " + str(leg_positions))
