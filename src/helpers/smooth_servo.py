from __future__ import division
import math

start = 100



def servo_move(degrees, speed):
    print(str(degrees) + " " + str(speed))


def move(degrees, max_speed, total_steps):
    diff = degrees - start
    step = diff / total_steps

    current = start

    for i in range(total_steps):
        current += step
        speed = math.sin((i + 0.5) / total_steps * math.pi) * max_speed
        servo_move(current, round(speed, 2))

move(350, 200, 20)
